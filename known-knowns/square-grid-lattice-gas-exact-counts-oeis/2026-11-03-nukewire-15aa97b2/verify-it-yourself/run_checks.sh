#!/bin/sh
# Standalone verification for the A210662 row-28 package. From the package folder:
#   sh verify-it-yourself/run_checks.sh
PY=""
for c in python3 python py; do
  if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then
  echo "FAIL: no python interpreter found"
  exit 1
fi
"$PY" verify-it-yourself/verify_standalone.py
