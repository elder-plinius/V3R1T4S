#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Last line: PASS or FAIL.
ok=1
echo "== exact check of the code against the table cell"
python3 verify-it-yourself/check_cw.py object/A-30-12-9-45words.txt 30 12 9 45 44 74 806649f74bcb4ec5746f248ef5f087f88d56120661f95e0d7a464d9965f9060d || ok=0
echo "== planted bugs (each must be rejected)"
python3 verify-it-yourself/planted_bugs.py object/A-30-12-9-45words.txt 30 12 9 45 44 74 || ok=0
if [ "$ok" = 1 ]; then echo PASS; else echo FAIL; exit 1; fi
