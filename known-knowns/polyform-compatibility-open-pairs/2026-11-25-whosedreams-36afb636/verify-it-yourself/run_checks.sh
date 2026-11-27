#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line PASS or FAIL)
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
out=$(python3 verify-it-yourself/check_mx.py 2>&1); rc=$?
printf '%s\n' "$out" | sed '$d'
if [ $rc -eq 0 ] && [ "$(printf '%s\n' "$out" | tail -n 1)" = "PASS" ]; then echo PASS; exit 0; fi
echo FAIL; exit 1
