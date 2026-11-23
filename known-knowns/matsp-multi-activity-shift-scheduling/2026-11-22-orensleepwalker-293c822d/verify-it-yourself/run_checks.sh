#!/bin/sh
set -eu
failure() { printf '%s\n' FAIL; exit 1; }
sha256sum --check --quiet SHA256SUMS || failure
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
curl -fsSL --max-time 180 -A 'V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)' -o "$tmp/instances1_225.zip" 'https://www.schedulingbenchmarks.org/matsp/data/instances1_225.zip' || failure
printf '%s  %s\n' '202ddbc48da844a404298f24edecc00f717c21e334e1dfe510e9b20d081cd556' "$tmp/instances1_225.zip" | sha256sum --check --quiet || failure
PYTHONDONTWRITEBYTECODE=1 python3 -I verify-it-yourself/verify.py "$tmp/instances1_225.zip" object/certificates.csv || failure
printf '%s\n' PASS
