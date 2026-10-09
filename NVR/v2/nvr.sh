#!/bin/sh
# Keenetic/Entware NVR v2.3 — supervised ffmpeg stream-copy recorder.
# Each cron tick is independent; no persistent shell watchdog.
set -u
umask 077
PATH=/opt/bin:/opt/sbin:/bin:/sbin:/usr/bin:/usr/sbin

CONFIG=${NVR_CONFIG:-/opt/etc/nvr-v2.conf}
[ -r "$CONFIG" ] || { echo "NVR: missing config: $CONFIG" >&2; exit 2; }
. "$CONFIG"
: "${NVR_MOUNT:?}" "${NVR_BASE_DIR:?}" "${RTSP_USER:?}" "${RTSP_PASS:?}" "${RTSP_IP:?}"
STATE=${NVR_STATE_DIR:-/tmp/nvr-v2}
FFMPEG=${NVR_FFMPEG:-/opt/bin/ffmpeg}
CAMERAS=${NVR_CAMERAS:-'101 201 301'}
STALE=${NVR_STALE_SECONDS:-720}
GRACE=${NVR_GRACE_SECONDS:-600}
RETENTION=${NVR_RETENTION_SECONDS:-259200}
DISK_WARN=${NVR_DISK_WARN_PERCENT:-75}
DISK_CRIT=${NVR_DISK_CRIT_PERCENT:-90}
NOW=$(date +%s)

isnum() { case ${1:-} in ''|*[!0-9]*) return 1;; esac; return 0; }
numfile() { v=$(cat "$1" 2>/dev/null) || v=0; isnum "$v" || v=0; printf '%s\n' "$v"; }
# Reject dangerous free-form camera identifiers or nonsensical settings.
for id in $CAMERAS; do
    isnum "$id" || { echo 'NVR: numeric camera IDs required' >&2; exit 2; }
done
for v in "$STALE" "$GRACE" "$RETENTION" "$DISK_WARN" "$DISK_CRIT"; do
    isnum "$v" || { echo 'NVR: invalid numeric configuration' >&2; exit 2; }
done
[ "$STALE" -ge 120 ] && [ "$RETENTION" -ge 259200 ] && \
[ "$DISK_WARN" -ge 1 ] && [ "$DISK_WARN" -le 100 ] && \
[ "$DISK_CRIT" -ge "$DISK_WARN" ] && [ "$DISK_CRIT" -le 100 ] || exit 2

mounted_rw() {
    awk -v d="$NVR_MOUNT" '$2==d && $4 ~ /(^|,)rw(,|$)/ {ok=1} END {exit !ok}' "${NVR_MOUNTS_FILE:-/proc/mounts}"
}
disk_ok() {
    if ! mounted_rw || [ ! -d "$NVR_BASE_DIR" ]; then
        log 'ERROR volume missing, unmounted or read-only; no writes/deletions'
        return 1
    fi
}
log() {
    line="$(date '+%Y-%m-%d %H:%M:%S') $*"
    printf '%s\n' "$line" >> "$STATE/events.log"
    # Persist event history across reboots, only when actual USB volume is mounted.
    if mounted_rw && [ -d "$NVR_BASE_DIR" ]; then
        mkdir -p "$NVR_BASE_DIR/.nvr-v2" 2>/dev/null || return 0
        printf '%s\n' "$line" >> "$NVR_BASE_DIR/.nvr-v2/events.log"
    fi
}
usage_pct() {
    u=$(df -P "$NVR_MOUNT" 2>/dev/null | awk 'NR==2 {gsub(/%/, "", $5); print $5}')
    isnum "$u" || return 1
    printf '%s\n' "$u"
}
# Verify both ffmpeg executable identity and which RTSP channel it owns.
owned() {
    id=$1; p=$2
    isnum "$p" && [ "$p" -gt 1 ] && [ -r "/proc/$p/cmdline" ] || return 1
    bin=$(readlink "/proc/$p/exe" 2>/dev/null) || return 1
    case "$bin" in */ffmpeg|*/ffmpeg\ \(deleted\)) ;; *) return 1;; esac
    tr '\000' '\n' < "/proc/$p/cmdline" 2>/dev/null | grep -Fq "/Streaming/Channels/$id"
}
# A stray v1/v2 process must not be duplicated accidentally.
find_camera_pid() {
    id=$1
    for p in $(pidof ffmpeg 2>/dev/null); do
        if owned "$id" "$p"; then printf '%s\n' "$p"; return 0; fi
    done
    return 1
}
newest() { ls -t "$NVR_BASE_DIR/cam$1"/cam"$1"_*.mkv 2>/dev/null | head -n 1; }
healthy_file() {
    f=$(newest "$1")
    [ -f "$f" ] || return 1
    mt=$(stat -c %Y "$f" 2>/dev/null) || return 1
    sz=$(stat -c %s "$f" 2>/dev/null) || return 1
    isnum "$mt" && isnum "$sz" && [ "$sz" -gt 0 ] || return 1
    age=$(( $(date +%s) - mt ))
    [ "$age" -ge 0 ] && [ "$age" -le "$STALE" ]
}
rotate_fflog() {
    f=$1
    [ -f "$f" ] || return 0
    sz=$(stat -c %s "$f" 2>/dev/null) || return 0
    isnum "$sz" || return 0
    if [ "$sz" -gt 524288 ]; then
        tail -c 262144 "$f" > "$f.tmp" && cat "$f.tmp" > "$f"
        rm -f "$f.tmp"
    fi
}
# Small bounded exponential backoff on broken cameras.
allow_retry() {
    id=$1
    last=$(numfile "$STATE/cam$id.last_try")
    failures=$(numfile "$STATE/cam$id.failures")
    if [ "$last" -gt 0 ] && [ $((NOW-last)) -ge 3600 ]; then failures=0; fi
    case $failures in 0) delay=0;; 1) delay=300;; 2) delay=600;; 3) delay=1200;; *) delay=1800;; esac
    [ $((NOW-last)) -ge "$delay" ] || return 1
    printf '%s\n' "$NOW" > "$STATE/cam$id.last_try"
    printf '%s\n' $((failures+1)) > "$STATE/cam$id.failures"
}
start_cam() {
    id=$1
    mkdir -p "$NVR_BASE_DIR/cam$id" "$NVR_BASE_DIR/.nvr-v2" || return 1
    fl="$NVR_BASE_DIR/.nvr-v2/ffmpeg-cam$id.log"
    rotate_fflog "$fl"
    url="rtsp://$RTSP_USER:$RTSP_PASS@$RTSP_IP:554/Streaming/Channels/$id"
    "$FFMPEG" -hide_banner -nostdin -loglevel error \
        -timeout 15000000 -rtsp_transport tcp -i "$url" \
        -c copy -f segment -segment_time 900 -strftime 1 -reset_timestamps 1 \
        "$NVR_BASE_DIR/cam$id/cam${id}_%Y-%m-%d_%H-%M-%S.mkv" \
        </dev/null >> "$fl" 2>&1 &
    p=$!
    printf '%s\n' "$p" > "$STATE/cam$id.pid"
    printf '%s\n' "$NOW" > "$STATE/cam$id.started"
    log "INFO camera=$id launch pid=$p"
}
stop_cam() {
    id=$1
    p=$(numfile "$STATE/cam$id.pid")
    if owned "$id" "$p"; then
        kill -TERM "$p" 2>/dev/null || :
        n=0
        while owned "$id" "$p" && [ "$n" -lt 10 ]; do sleep 1; n=$((n+1)); done
        if owned "$id" "$p"; then
            log "WARN camera=$id SIGTERM timeout; SIGKILL pid=$p"
            kill -KILL "$p" 2>/dev/null || :
            sleep 1
        fi
    fi
    if owned "$id" "$p"; then
        log "ERROR camera=$id process will not terminate; refusing duplicate"
        return 1
    fi
    rm -f "$STATE/cam$id.pid" "$STATE/cam$id.started"
}
# Serializes cron checks, cleanups, starts and stops.
lock() {
    L="$STATE/.lock"
    if mkdir "$L" 2>/dev/null; then
        printf '%s\n' "$$" > "$L/pid"
        trap 'rm -f "$L/pid"; rmdir "$L" 2>/dev/null || :' EXIT
        trap 'exit 130' INT
        trap 'exit 143' HUP TERM
        return 0
    fi
    lp=$(numfile "$L/pid")
    # Never remove a lock belonging to a live PID. Stale lock reclamation only.
    if [ "$lp" -gt 1 ] && kill -0 "$lp" 2>/dev/null; then return 1; fi
    age=$(stat -c %Y "$L" 2>/dev/null) || return 1
    [ $((NOW-age)) -gt 90 ] || return 1
    rm -f "$L/pid"
    rmdir "$L" 2>/dev/null || return 1
    mkdir "$L" 2>/dev/null || return 1
    printf '%s\n' "$$" > "$L/pid"
    trap 'rm -f "$L/pid"; rmdir "$L" 2>/dev/null || :' EXIT
    trap 'exit 130' INT
    trap 'exit 143' HUP TERM
}
ensure_no_legacy() {
    if [ -e /tmp/cctv_is_running ]; then
        log 'ERROR legacy marker detected; v2 check refused'
        return 1
    fi
}
check() {
    disk_ok || return 1
    disk_health
    ensure_no_legacy || return 1
    printf '%s\n' "$NOW" > "$STATE/last_check"
    for id in $CAMERAS; do
        pid=$(numfile "$STATE/cam$id.pid")
        if ! owned "$id" "$pid"; then
            other=$(find_camera_pid "$id") || other=''
            if [ -n "$other" ]; then
                log "WARN camera=$id untracked ffmpeg pid=$other; adopting process"
                printf '%s\n' "$other" > "$STATE/cam$id.pid"
                printf '%s\n' "$NOW" > "$STATE/cam$id.started"
                continue
            fi
            if allow_retry "$id"; then
                log "WARN camera=$id ffmpeg missing; start attempt"
                start_cam "$id"
            fi
        elif healthy_file "$id"; then
            printf '0\n' > "$STATE/cam$id.failures"
        else
            started=$(numfile "$STATE/cam$id.started")
            if [ "$started" -gt 0 ] && [ $((NOW-started)) -lt "$GRACE" ]; then continue; fi
            if allow_retry "$id"; then
                log "WARN camera=$id stream stale; restarting camera only"
                if stop_cam "$id"; then start_cam "$id"; fi
            fi
        fi
    done
}
disk_health() {
    pct=$(usage_pct) || return 0
    if [ "$pct" -ge "$DISK_CRIT" ]; then
        level=CRITICAL
    elif [ "$pct" -ge "$DISK_WARN" ]; then
        level=WARN
    else
        return 0
    fi
    prev=$(numfile "$STATE/last_disk_alert")
    if [ $((NOW-prev)) -ge 3600 ]; then
        log "$level disk usage=${pct}% warning=${DISK_WARN}% critical=${DISK_CRIT}%; monitoring only"
        printf '%s\n' "$NOW" > "$STATE/last_disk_alert"
    fi
}
status() {
    echo "NVR v2 | $(date)"
    if mounted_rw; then
        echo 'USB: RW'
        u=$(usage_pct) || u='unknown'
        echo "DISK USE: ${u}% (warning >= ${DISK_WARN}%; critical >= ${DISK_CRIT}%; monitor-only)"
    else
        echo 'USB: NOT MOUNTED/RW'
    fi
    [ -f /tmp/cctv_is_running ] && echo 'LEGACY: marker present' || :
    t=$(numfile "$STATE/last_check")
    echo "LAST CHECK EPOCH: $t"
    for id in $CAMERAS; do
        pid=$(numfile "$STATE/cam$id.pid")
        if owned "$id" "$pid"; then state=running; else state=stopped; fi
        f=$(newest "$id")
        if [ -f "$f" ]; then
            mt=$(stat -c %Y "$f" 2>/dev/null) || mt=0
            if isnum "$mt"; then age=$((NOW-mt)); else age='?'; fi
        else age='no_files'; fi
        echo "CAM $id: $state pid=$pid latest_write_age_sec=$age"
    done
}
cleanup() {
    disk_ok || return 1
    # Strict retention policy: a per-camera, rolling 72-hour *time* horizon.
    # Fullness must NEVER shorten it; do not remove unexpired footage.
    # mtime marks the last bytes actually written, not the filename start time.
    # Cleanup runs hourly, so expiration may occur up to an hour later.
    cutoff=$((NOW-RETENTION))
    removed=0
    for id in $CAMERAS; do
        # Don't unlink a segment potentially still held open by an FFmpeg process.
        pid=$(numfile "$STATE/cam$id.pid")
        open_file=''
        if owned "$id" "$pid"; then
            open_file=$(newest "$id")
        else
            # Also protect against an untracked but active recorder process.
            other=$(find_camera_pid "$id") || other=''
            [ -z "$other" ] || open_file=$(newest "$id")
        fi
        for f in "$NVR_BASE_DIR/cam$id"/cam"$id"_*.mkv; do
            [ -f "$f" ] || continue
            [ "$f" = "$open_file" ] && continue
            mt=$(stat -c %Y "$f" 2>/dev/null) || continue
            isnum "$mt" || continue
            if [ "$mt" -lt "$cutoff" ]; then
                rm -f -- "$f" && removed=$((removed+1))
            fi
        done
    done
    [ "$removed" -eq 0 ] || log "INFO retention_72h cleanup removed=$removed expired MKV"
    # Disk alerts only; NEVER evict video because of free-space pressure.
    disk_health
}

# This is a temporary state directory: replaced at next boot, with cron recovery.
mkdir -p "$STATE" || exit 2
case ${1:-status} in
  status) status ;;
  check|start) lock || exit 0; check ;;
  cleanup) lock || exit 0; cleanup ;;
  stop)
      lock || { echo 'NVR: controller busy' >&2; exit 1; }
      for id in $CAMERAS; do stop_cam "$id" || :; done
      log 'INFO requested stop of v2 processes'
      ;;
  *) echo 'Usage: nvr.sh {start|check|status|stop|cleanup}' >&2; exit 2;;
esac