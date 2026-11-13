#!/bin/sh
# Standalone verification for the A210662 row-28 package, invoked as
# `sh verify-it-yourself/run_checks.sh` in the package folder; the final output
# line of the run is PASS or FAIL.
PY=""
for c in python3 python py; do
  if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then
  echo "FAIL: no python interpreter found"
  exit 1
fi
"$PY" verify-it-yourself/verify_standalone.py
