#!/bin/sh
set -eu
failure() { printf '%s\n' FAIL; exit 1; }
sha256sum --check --quiet SHA256SUMS || failure
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
curl -fsSL --max-time 180 -o "$tmp/MMLIB_v2_1.zip" 'https://github.com/MarioVanhoucke/MMLIB-Multi-Mode-Resource-Constrained-Project-Library/releases/download/v2.1/MMLIB_v2_1.zip' || failure
printf '%s  %s\n' '4f6f5318fcbc01943ec74dfbf8b16afc25b65759963666f631d6cdd2f242fecd' "$tmp/MMLIB_v2_1.zip" | sha256sum --check --quiet || failure
PYTHONDONTWRITEBYTECODE=1 python3 -I verify-it-yourself/verify.py . "$tmp/MMLIB_v2_1.zip" || failure
printf '%s\n' PASS
