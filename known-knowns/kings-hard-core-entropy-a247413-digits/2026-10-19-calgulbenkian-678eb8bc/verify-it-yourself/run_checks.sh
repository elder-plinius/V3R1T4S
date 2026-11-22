#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs only python3 (standard library). The last output line is PASS or FAIL; exit status 0 only on PASS.
HERE=$(cd "$(dirname "$0")" && pwd)
out=$(python3 -I "$HERE/check_kings.py" 2>&1)
status=$?
printf '%s\n' "$out" | sed '$d'
last=$(printf '%s\n' "$out" | tail -n 1)
if [ "$status" -eq 0 ] && [ "$last" = "PASS" ]; then echo PASS; else echo FAIL; exit 1; fi
