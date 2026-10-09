#!/bin/sh
# First-time Keenetic/Entware installation. Credentials never leave the router.
set -eu
umask 077
PATH=/opt/bin:/opt/sbin:/bin:/sbin:/usr/bin:/usr/sbin
HERE=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
SOURCE="$HERE/nvr.sh"
RECORDER=/opt/etc/nvr-v2.sh
CONFIG=/opt/etc/nvr-v2.conf
CRON=/opt/etc/init.d/S10cron
fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
number() { case ${1:-} in ''|*[!0-9]*) return 1;; esac; }
prerequisites() {
    [ -r "$SOURCE" ] && sh -n "$SOURCE" || fail 'Missing or invalid nvr.sh'
    [ -x /opt/bin/ffmpeg ] || fail 'Missing FFmpeg: opkg update && opkg install ffmpeg'
    [ -x /opt/sbin/cron ] && [ -x "$CRON" ] || fail 'Missing Entware cron: opkg install cron'
    command -v stat >/dev/null 2>&1 || fail 'Missing GNU stat: opkg install coreutils-stat'
    mt=$(stat -c %Y "$SOURCE" 2>/dev/null) || fail 'stat -c %Y failed'
    sz=$(stat -c %s "$SOURCE" 2>/dev/null) || fail 'stat -c %s failed'
    number "$mt" && [ "$mt" -gt 0 ] && number "$sz" && [ "$sz" -gt 0 ] || fail 'Invalid stat output'
    /opt/bin/ffmpeg -hide_banner -h demuxer=rtsp 2>&1 | grep -q -- '-timeout ' || fail 'FFmpeg RTSP -timeout unsupported'
    [ ! -e /opt/etc/init.d/S99cctv ] && [ ! -e /tmp/cctv_is_running ] || fail 'Legacy NVR found: use preflight/switch instead of install-fresh'
    printf 'Fresh preflight PASS: FFmpeg, cron, stat available; no legacy NVR.\n'
    printf 'Writable USB mount candidates:\n'
    awk '$2 ~ /^\/tmp\/mnt\// && $4 ~ /(^|,)rw(,|$)/ {print "  " $2 " (" $3 ")"}' /proc/mounts
}
quote_sh() {
    # Store untrusted single-line credentials as safely quoted POSIX shell literals.
    printf "'"
    printf '%s' "$1" | sed "s/'/'\\\\''/g"
    printf "'"
}
ask() {
    printf '%s' "$1" > /dev/tty
    IFS= read -r answer < /dev/tty || fail 'Input cancelled'
}
ask_password() {
    [ -r /dev/tty ] && [ -w /dev/tty ] || fail 'Interactive SSH terminal required (ssh -t)'
    printf 'RTSP password (input hidden): ' > /dev/tty
    tty_state=$(stty -g < /dev/tty) || fail 'Unable to configure terminal'
    stty -echo < /dev/tty || fail 'Unable to hide password'
    trap 'stty "$tty_state" < /dev/tty 2>/dev/null || :' EXIT
    trap 'exit 130' INT
    trap 'exit 143' HUP TERM
    if IFS= read -r answer < /dev/tty; then password=$answer; else fail 'Password input cancelled'; fi
    stty "$tty_state" < /dev/tty
    trap - EXIT INT HUP TERM
    printf '\n' > /dev/tty
    [ -n "$password" ] || fail 'Empty RTSP password is not allowed'
}
configured_mount() {
    awk -v d="$1" '$2==d && $4 ~ /(^|,)rw(,|$)/ {ok=1} END{exit !ok}' /proc/mounts
}
configure() {
    [ -r /dev/tty ] && [ -w /dev/tty ] || fail 'Run through interactive SSH with TTY'
    if [ -e "$CONFIG" ]; then
        for pidfile in /tmp/nvr-v2/cam*.pid; do
            [ -f "$pidfile" ] || continue
            pid=$(cat "$pidfile" 2>/dev/null || :)
            case "$pid" in ''|*[!0-9]*) continue;; esac
            if kill -0 "$pid" 2>/dev/null; then
                fail 'Stop v2 recorder before changing credentials: sh /opt/etc/nvr-v2.sh stop'
            fi
        done
        ask 'Local config already exists. Replace it? [type YES]: '
        [ "$answer" = YES ] || fail 'No changes to existing config'
    fi
    printf '\nChoose the exact external USB mount path (not /opt).\n' > /dev/tty
    ask 'USB mount (/tmp/mnt/UUID): '
    mount_path=$answer
    case "$mount_path" in /tmp/mnt/*) ;; *) fail 'Only external /tmp/mnt/ paths are supported';; esac
    case "$mount_path" in *' '*|*'..'*) fail 'Mount path contains unsupported characters';; esac
    configured_mount "$mount_path" || fail 'USB disk is not mounted read-write'
    ask 'RTSP IP/hostname (one recorder/source): '
    host=$answer
    case "$host" in ''|*[!a-zA-Z0-9.-]*) fail 'Expected IPv4 address or DNS hostname without URL/port';; esac
    ask 'RTSP username: '
    username=$answer
    [ -n "$username" ] || fail 'Empty username is not allowed'
    ask_password
    ask 'RTSP channel IDs, space-separated [101 201 301]: '
    channels=${answer:-101 201 301}
    seen=' '
    for id in $channels; do
        number "$id" || fail 'Channel IDs must be numeric'
        case "$seen" in *" $id "*) fail "Duplicate channel: $id";; esac
        seen="$seen$id "
    done
    [ "$seen" != ' ' ] || fail 'At least one channel required'
    temp=$(mktemp /opt/etc/.nvr-v2.conf.XXXXXX) || fail 'Cannot create temporary config'
    trap 'rm -f "$temp"' EXIT HUP INT TERM
    {
        printf 'NVR_MOUNT='; quote_sh "$mount_path"; printf '\n'
        printf 'NVR_BASE_DIR='; quote_sh "$mount_path/cctv"; printf '\n'
        printf 'RTSP_IP='; quote_sh "$host"; printf '\n'
        printf 'RTSP_USER='; quote_sh "$username"; printf '\n'
        printf 'RTSP_PASS='; quote_sh "$password"; printf '\n'
        printf 'NVR_CAMERAS='; quote_sh "$channels"; printf '\n'
        printf 'NVR_RETENTION_SECONDS=259200\nNVR_DISK_WARN_PERCENT=75\nNVR_DISK_CRIT_PERCENT=90\n'
    } > "$temp"
    chmod 600 "$temp"
    sh -n "$temp" || fail 'Generated config has invalid syntax'
    mkdir -p "$mount_path/cctv"
    for id in $channels; do mkdir -p "$mount_path/cctv/cam$id"; done
    mv -f "$temp" "$CONFIG"
    trap - EXIT HUP INT TERM
    unset password answer
    printf 'Local configuration saved at %s (mode 600). Password not displayed.\n' "$CONFIG"
}
check_config() {
    [ -r "$CONFIG" ] && [ -f "$RECORDER" ] || fail 'Local config or recorder missing'
    sh -n "$CONFIG" || fail 'Invalid local config'
    . "$CONFIG"
    configured_mount "$NVR_MOUNT" || fail 'Configured disk not mounted read-write'
}
verify_video() {
    count=0
    while [ "$count" -lt 12 ]; do
        good=1
        result=$(sh "$RECORDER" status) || good=0
        for id in $NVR_CAMERAS; do
            line=$(printf '%s\n' "$result" | grep "^CAM $id: running ") || { good=0; continue; }
            age=${line##*latest_write_age_sec=}
            case "$age" in ''|*[!0-9]*) good=0;; *) [ "$age" -lt 60 ] || good=0;; esac
        done
        [ "$good" -eq 1 ] && return 0
        count=$((count+1))
        [ "$count" -ge 12 ] || sleep 5
    done
    printf '%s\n' "$result" >&2
    fail 'Video verification failed; cron not added. Inspect local FFmpeg logs and retry.'
}
schedule() {
    tempfile=$(mktemp /tmp/nvr-fresh-cron.XXXXXX) || fail 'Cannot create cron temp file'
    trap 'rm -f "$tempfile"' EXIT HUP INT TERM
    oldcron=$(mktemp /tmp/nvr-fresh-oldcron.XXXXXX) || fail 'Cannot create cron backup temp file'
    if crontab -l > "$oldcron" 2>"$tempfile.err"; then
        :
    elif grep -qi 'no crontab' "$tempfile.err"; then
        :
    else
        fail 'Cannot read existing root crontab; refusing to overwrite other jobs'
    fi
    sed '/\/opt\/etc\/nvr-v2\.sh check/d; /\/opt\/etc\/nvr-v2\.sh cleanup/d' "$oldcron" > "$tempfile"
    rm -f "$oldcron" "$tempfile.err"
    printf '\n*/5 * * * * /bin/sh /opt/etc/nvr-v2.sh check\n' >> "$tempfile"
    printf '3 * * * * /bin/sh /opt/etc/nvr-v2.sh cleanup\n' >> "$tempfile"
    crontab "$tempfile" || fail 'Unable to install cron'
    "$CRON" restart || fail 'Unable to restart cron'
    rm -f "$tempfile"
    trap - EXIT HUP INT TERM
}
install_fresh() {
    prerequisites
    [ -e "$RECORDER" ] && [ ! -e "$CONFIG" ] && fail 'Recorder exists without config; inspect manually'
    if [ ! -e "$CONFIG" ]; then configure; fi
    cp "$SOURCE" "$RECORDER"
    chmod 700 "$RECORDER"
    check_config
    sh "$RECORDER" start || fail 'NVR start failed; cron unchanged'
    verify_video
    schedule
    printf '\nFresh NVR installation PASS. Cron configured.\n'
    sh "$RECORDER" status
}
case ${1:-} in
    preflight-fresh) prerequisites ;;
    install-fresh) install_fresh ;;
    configure-fresh) prerequisites; configure ;;
    *) echo 'Usage: fresh-install.sh {preflight-fresh|install-fresh|configure-fresh}' >&2; exit 2;;
esac
