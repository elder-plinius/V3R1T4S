#!/bin/sh
# run from the package folder: sh verify-it-yourself/run_checks.sh
out=$(python3 verify-it-yourself/check_union.py object/A054961_n14_m65.txt 14 2); echo "$out"
m=$(echo "$out" | sed -n 's/.* m=\([0-9]*\) .*/\1/p' | head -1)
if [ "$(echo "$out" | tail -1)" = VALID ] && [ "$m" -gt 63 ]; then echo "m=$m > OEIS bound 63"; echo PASS; else echo FAIL; fi
