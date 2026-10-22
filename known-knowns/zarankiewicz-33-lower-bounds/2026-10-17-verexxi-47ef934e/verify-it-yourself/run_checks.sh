#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL; exit status 0 only on PASS)
# Python 3 standard library only. Takes about 1 second.
cd "$(dirname "$0")/.." || exit 1
PY=python3
"$PY" -c "import sys" >/dev/null 2>&1 || PY=python
"$PY" verify-it-yourself/verify.py
exit $?
