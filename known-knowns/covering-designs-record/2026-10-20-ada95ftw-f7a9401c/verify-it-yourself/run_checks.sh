#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
out=$(python3 verify-it-yourself/verify.py 36 5 3 object/C36_5_3_812.txt 812 2>&1)
rc=$?
printf '%s\n' "$out"
if [ $rc -eq 0 ] && printf '%s\n' "$out" | grep -q "^VERIFIED C(36,5,3) <= 812$"; then
  echo PASS
else
  echo FAIL
  exit 1
fi
