#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs a Python 3 interpreter (standard library only). Last output line: PASS or FAIL.
PY=""
for c in python3 python; do
  if "$c" -c "import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then echo "no working python3 found"; echo "FAIL"; exit 1; fi
"$PY" verify-it-yourself/check_cw.py object/A26_6_9_5997.txt 26 6 9 5997
