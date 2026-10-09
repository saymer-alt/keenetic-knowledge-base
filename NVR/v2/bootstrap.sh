#!/bin/sh
# Download NVR v2.3 from the owner's GitHub repository before installation.
set -eu
umask 077
ACTION=${1:-}
case "$ACTION" in preflight|switch) ;; *) echo 'Usage: bootstrap.sh {preflight|switch}' >&2; exit 2;; esac
RAW=${NVR_RAW_BASE:-https://raw.githubusercontent.com/saymer-alt/keenetic-knowledge-base/nvr/watchdog-v2-candidate/NVR/v2}
if ! command -v curl >/dev/null 2>&1; then
    echo 'curl missing. Install: opkg update && opkg install curl' >&2
    exit 1
fi
DIR=$(mktemp -d /tmp/nvr-setup.XXXXXX) || exit 1
trap 'rm -rf "$DIR"' EXIT
for file in nvr.sh install-router.sh; do
    echo "Fetching $file from GitHub..."
    curl -fSsL --retry 2 --connect-timeout 15 "$RAW/$file" -o "$DIR/$file" || { echo "Failed to fetch $file" >&2; exit 1; }
    [ -s "$DIR/$file" ] && sh -n "$DIR/$file" || exit 1
done
sh "$DIR/install-router.sh" "$ACTION"
