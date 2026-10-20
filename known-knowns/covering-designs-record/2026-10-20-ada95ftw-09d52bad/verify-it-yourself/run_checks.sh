#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
out=$(python3 verify-it-yourself/verify.py 38 6 3 object/C38_6_3_469blocks.txt 469 2>&1)
rc=$?
printf '%s\n' "$out"
if [ $rc -eq 0 ] && printf '%s\n' "$out" | grep -q "^VERIFIED C(38,6,3) <= 469$"; then
  echo PASS
else
  echo FAIL
  exit 1
fi
