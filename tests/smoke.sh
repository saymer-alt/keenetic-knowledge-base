#!/bin/sh
# Offline BusyBox ash integration smoke. Run from repository root.
set -eu
cd "$(dirname "$0")/.."
sh -n NVR/v2/nvr.sh
busybox sh -n NVR/v2/nvr.sh
sh -n NVR/v2/install-router.sh
sh -n NVR/v2/bootstrap.sh
T=$(mktemp -d)
cleanup() {
  NVR_CONFIG="$T/conf" sh NVR/v2/nvr.sh stop >/dev/null 2>&1 || :
  rm -rf "$T"
}
trap cleanup EXIT
mkdir -p "$T/mount/cctv" "$T/state"
M="$T/mount"
printf '/dev/mock %s ext4 rw,relatime 0 0\n' "$M" > "$T/mounts"
gcc -Wall -Wextra -O2 -o "$T/ffmpeg" tests/ffmpeg-stub.c
cat > "$T/conf" <<EOT
NVR_MOUNT='$M'
NVR_BASE_DIR='$M/cctv'
RTSP_USER='dummy'
RTSP_PASS='test-only-secret'
RTSP_IP='192.0.2.1'
NVR_STATE_DIR='$T/state'
NVR_MOUNTS_FILE='$T/mounts'
NVR_FFMPEG='$T/ffmpeg'
NVR_CAMERAS='101 201 301'
NVR_STALE_SECONDS=120
NVR_GRACE_SECONDS=0
NVR_RETENTION_SECONDS=259200
NVR_DISK_WARN_PERCENT=75
NVR_DISK_CRIT_PERCENT=90
EOT
NVR_CONFIG="$T/conf" busybox sh NVR/v2/nvr.sh status | grep -q 'USB: RW'
NVR_CONFIG="$T/conf" busybox sh NVR/v2/nvr.sh start
sleep 2
for id in 101 201 301; do
  [ "$(cat "$T/state/cam$id.pid")" -gt 1 ]
  [ -n "$(find "$M/cctv/cam$id" -name '*.mkv' -type f -size +0c -print -quit)" ]
done
p0=$(cat "$T/state/cam101.pid")
p201=$(cat "$T/state/cam201.pid")
p301=$(cat "$T/state/cam301.pid")
NVR_CONFIG="$T/conf" busybox sh NVR/v2/nvr.sh check
[ "$(cat "$T/state/cam101.pid")" = "$p0" ]
# One stalled camera must be restarted, others left untouched.
kill -STOP "$p0"
f=$(find "$M/cctv/cam101" -name '*.mkv' | head -n 1)
touch -d '1 hour ago' "$f"
for suffix in started last_try failures; do printf '0\n' > "$T/state/cam101.$suffix"; done
NVR_CONFIG="$T/conf" busybox sh NVR/v2/nvr.sh check
[ "$(cat "$T/state/cam101.pid")" != "$p0" ]
[ "$(cat "$T/state/cam201.pid")" = "$p201" ]
[ "$(cat "$T/state/cam301.pid")" = "$p301" ]
# Expire only old (>72h) segments in each camera folder.
printf 'old\n' > "$M/cctv/cam101/cam101_old.mkv"
touch -d '73 hours ago' "$M/cctv/cam101/cam101_old.mkv"
printf 'keep\n' > "$M/cctv/cam201/cam201_keep.mkv"
touch -d '71 hours ago' "$M/cctv/cam201/cam201_keep.mkv"
NVR_CONFIG="$T/conf" busybox sh NVR/v2/nvr.sh cleanup
[ ! -f "$M/cctv/cam101/cam101_old.mkv" ]
[ -f "$M/cctv/cam201/cam201_keep.mkv" ]
# If a camera is stopped, its completed last old file still expires by age.
NVR_CONFIG="$T/conf" busybox sh NVR/v2/nvr.sh stop
printf 'old final\n' > "$M/cctv/cam301/cam301_final.mkv"
touch -d '5 days ago' "$M/cctv/cam301/cam301_final.mkv"
NVR_CONFIG="$T/conf" busybox sh NVR/v2/nvr.sh cleanup
[ ! -f "$M/cctv/cam301/cam301_final.mkv" ]
# Mount read-only: fail closed, never delete.
printf '/dev/mock %s ext4 ro,relatime 0 0\n' "$M" > "$T/mounts"
if NVR_CONFIG="$T/conf" busybox sh NVR/v2/nvr.sh cleanup; then
  echo 'ERROR cleanup succeeded with read-only mount' >&2; exit 1
fi
if NVR_CONFIG="$T/conf" busybox sh NVR/v2/nvr.sh check; then
  echo 'ERROR health check succeeded with read-only mount' >&2; exit 1
fi
if grep -q 'test-only-secret' "$M/cctv/.nvr-v2/events.log"; then
  echo 'ERROR leaked credential in events.log' >&2; exit 1
fi
echo 'BusyBox ash NVR v2.3 smoke PASS'
