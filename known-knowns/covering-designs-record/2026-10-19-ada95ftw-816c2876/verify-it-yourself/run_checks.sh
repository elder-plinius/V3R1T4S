#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
out=$(python3 verify-it-yourself/verify.py 29 5 3 object/C29_5_3_399blocks.txt 399 2>&1)
rc=$?
printf '%s\n' "$out"
if [ $rc -eq 0 ] && printf '%s\n' "$out" | grep -q "^VERIFIED C(29,5,3) <= 399$"; then
  echo PASS
else
  echo FAIL
  exit 1
fi
