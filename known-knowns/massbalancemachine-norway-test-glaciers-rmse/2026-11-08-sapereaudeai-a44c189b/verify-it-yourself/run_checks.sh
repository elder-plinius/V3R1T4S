#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Uses $PYTHON if set, else the first python3/python on PATH that actually runs.
PY="${PYTHON:-}"
if [ -z "$PY" ]; then
  for c in python3 python; do
    if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 6) else 1)' >/dev/null 2>&1; then
      PY="$c"; break
    fi
  done
fi
if [ -z "$PY" ]; then echo "no Python 3 found (set PYTHON=/path/to/python3)"; echo FAIL; exit 1; fi
"$PY" -I -B verify-it-yourself/check.py object/test_record_predictions_primary.csv
