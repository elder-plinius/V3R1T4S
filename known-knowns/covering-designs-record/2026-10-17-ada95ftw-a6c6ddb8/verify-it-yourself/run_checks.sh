#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
out=$(python3 verify-it-yourself/verify.py 20 6 3 object/C20_6_3_70blocks.txt 70 2>&1)
rc=$?
printf '%s\n' "$out"
if [ $rc -eq 0 ] && printf '%s\n' "$out" | grep -q "^VERIFIED C(20,6,3) <= 70$"; then
  echo PASS
else
  echo FAIL
  exit 1
fi
