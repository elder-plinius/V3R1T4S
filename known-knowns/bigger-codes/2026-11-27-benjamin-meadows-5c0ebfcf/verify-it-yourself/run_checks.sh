#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Last line: PASS or FAIL.
ok=1
echo "== exact check of the code against the table cell"
python3 verify-it-yourself/check_cw.py object/A-29-10-8-98words.txt 29 10 8 98 96 203 5c0ebfcf58bd20ac9e89c62b10560e485e9a416bf027df1dd4c680feaf3354ee || ok=0
echo "== planted bugs (each must be rejected)"
python3 verify-it-yourself/planted_bugs.py object/A-29-10-8-98words.txt 29 10 8 98 96 203 || ok=0
if [ "$ok" = 1 ]; then echo PASS; else echo FAIL; exit 1; fi
