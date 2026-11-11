#!/bin/sh
# Standalone verification for the A210662 row-29 package, invoked as
# `sh verify-it-yourself/run_checks.sh` in the package folder with any
# Python 3.8+ (standard library only); the run takes roughly 15-30 minutes
# and its final output line is PASS or FAIL.
cd "$(dirname "$0")/.." || exit 1
PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
"$PY" verify-it-yourself/verify_row29.py 2>&1
rc=$?
if [ $rc -ne 0 ]; then
  exit 1
fi
