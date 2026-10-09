#!/bin/sh
# Offline credential quoting smoke test: never use real RTSP credentials.
set -eu
cd "$(dirname "$0")/.."
busybox ash -n NVR/v2/fresh-install.sh
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT HUP INT TERM
# Extract only pure quote helper; do not invoke hardware/terminal installation.
sed -n '/^quote_sh() {/,/^}/p' NVR/v2/fresh-install.sh > "$T/quote.sh"
. "$T/quote.sh"
sample='safe value with spaces, $dollars, a '"'"'single quote'"'"' and ; semicolon'
encoded=$(quote_sh "$sample")
eval "decoded=$encoded"
[ "$decoded" = "$sample" ] || { echo 'FAIL: quoting did not round-trip' >&2; exit 1; }
# An injected shell fragment must remain inert after source.
marker="$T/unexpected"
sample="'; touch $marker; #"
encoded=$(quote_sh "$sample")
eval "decoded=$encoded"
[ "$decoded" = "$sample" ] && [ ! -e "$marker" ] || { echo 'FAIL: shell injection risk' >&2; exit 1; }
echo 'Fresh credentials escaping: PASS'
