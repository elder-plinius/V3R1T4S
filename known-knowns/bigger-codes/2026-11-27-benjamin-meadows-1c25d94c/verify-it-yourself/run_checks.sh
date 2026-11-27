#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Last line: PASS or FAIL.
ok=1
echo "== exact check of the code against the table cell"
python3 verify-it-yourself/check_cw.py object/A-29-6-6-1207words.txt 29 6 6 1207 1205 1459 1c25d94ca5861e9762b92ce4dc28d493bf2c2d5827466cb73cdf949c73079642 || ok=0
echo "== planted bugs (each must be rejected)"
python3 verify-it-yourself/planted_bugs.py object/A-29-6-6-1207words.txt 29 6 6 1207 1205 1459 || ok=0
if [ "$ok" = 1 ]; then echo PASS; else echo FAIL; exit 1; fi
