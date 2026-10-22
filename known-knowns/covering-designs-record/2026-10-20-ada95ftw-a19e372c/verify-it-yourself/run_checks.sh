#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
out=$(python3 verify-it-yourself/verify.py 35 5 3 object/C35_5_3_713blocks.txt 713 2>&1)
rc=$?
printf '%s\n' "$out"
if [ $rc -eq 0 ] && printf '%s\n' "$out" | grep -q "^VERIFIED C(35,5,3) <= 713$"; then
  echo PASS
else
  echo FAIL
  exit 1
fi
