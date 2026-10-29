#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs only python3 (standard library). Last line: PASS or FAIL.
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
PY=$(command -v python3 || command -v python)
[ -n "$PY" ] || { echo "no python3 found"; echo FAIL; exit 1; }
echo "== exact Brent-equation check (check_scheme.py)"
"$PY" -I verify-it-yourself/check_scheme.py object 2>&1; s1=$?
echo "== random exact evaluation against AB (check_random_eval.py)"
"$PY" -I verify-it-yourself/check_random_eval.py object 3 2>&1; s2=$?
if [ "$s1" -eq 0 ] && [ "$s2" -eq 0 ]; then echo PASS; exit 0; fi
echo FAIL; exit 1
