#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
PY=""
for c in python3 python; do
  if "$c" -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then echo "no working Python 3 found"; echo FAIL; exit 1; fi
"$PY" -I -B verify-it-yourself/check_bound.py object
