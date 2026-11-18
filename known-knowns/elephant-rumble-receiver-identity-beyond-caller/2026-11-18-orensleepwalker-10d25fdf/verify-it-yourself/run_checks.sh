#!/bin/sh
set -eu
failure() { printf '%s\n' FAIL; exit 1; }
sha256sum --check --quiet SHA256SUMS || failure
PYTHONDONTWRITEBYTECODE=1 python3 -I verify-it-yourself/verify.py . || failure
printf '%s\n' PASS
