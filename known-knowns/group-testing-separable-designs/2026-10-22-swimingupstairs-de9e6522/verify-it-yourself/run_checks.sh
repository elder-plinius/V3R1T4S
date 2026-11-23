#!/bin/sh
# run from the package folder: sh verify-it-yourself/run_checks.sh
# two checkers written from the OEIS A054961 definition (ORs of any 2 distinct vectors all distinct)
a=$(python3 verify-it-yourself/check_union.py object/A054961_n16_m102.txt 16 2); echo "$a"
b=$(python3 verify-it-yourself/check_indep_stdlib.py object/A054961_n16_m102.txt 16); echo "$b"
m=$(grep -c . object/A054961_n16_m102.txt)
bad=$(grep -c -v '^[01]\{16\}$' object/A054961_n16_m102.txt)
if [ "$(echo "$a" | tail -1)" = VALID ] && [ "$(echo "$b" | tail -1)" = PASS ] && [ "$bad" -eq 0 ] && [ "$m" -gt 91 ]; then echo "m=$m > OEIS bound 91"; echo PASS; else echo FAIL; fi
