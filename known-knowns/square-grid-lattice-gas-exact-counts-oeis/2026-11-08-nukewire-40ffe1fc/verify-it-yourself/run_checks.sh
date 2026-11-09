#!/bin/sh
# Verify the A210662 row-29 claim from this package folder:
#   sh verify-it-yourself/run_checks.sh
# Requires Python 3.8+ with the standard library only; ~15-30 min (own DP).
cd "$(dirname "$0")/.." || exit 1
PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
"$PY" verify-it-yourself/verify_row29.py 2>&1
rc=$?
if [ $rc -ne 0 ]; then
  exit 1
fi
