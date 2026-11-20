#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Last line: PASS or FAIL.
ok=1
echo "== exact check of the code against the table cell"
python3 verify-it-yourself/check_code.py object/A4-11-7-145words.txt 4 11 7 145 128 320 96ddddaebbcc6cf5d43f8869ebf951cf4520634e12d32df060e8b4acc5b6f9f0 || ok=0
echo "== rebuild from the written description"
python3 verify-it-yourself/rebuild.py object/A4-11-7-145words.txt || ok=0
echo "== planted bugs (each must be rejected)"
python3 verify-it-yourself/planted_bugs.py object/A4-11-7-145words.txt 4 11 7 145 128 320 || ok=0
if [ "$ok" = 1 ]; then echo PASS; else echo FAIL; exit 1; fi
