#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
out=$(python3 verify-it-yourself/verify.py object/cert_A31_10_7.json 2>&1)
rc=$?
printf '%s\n' "$out"
if [ $rc -eq 0 ] && printf '%s\n' "$out" | grep -q "^VERIFIED bound 106$"; then
  echo PASS
else
  echo FAIL
  exit 1
fi
