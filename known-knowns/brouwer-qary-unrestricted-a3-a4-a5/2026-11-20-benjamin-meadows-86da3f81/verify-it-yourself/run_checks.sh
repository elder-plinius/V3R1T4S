#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Last line: PASS or FAIL.
ok=1
echo "== exact check of the code against the table cell"
python3 verify-it-yourself/check_code.py object/A3-15-10-31words.txt 3 15 10 31 27 39 86da3f818e06cbe15a35aabf63c8849ee96e1ccf3dd36c9964113732876d9555 || ok=0
echo "== rebuild from the written description"
python3 verify-it-yourself/rebuild.py object/A3-15-10-31words.txt || ok=0
echo "== planted bugs (each must be rejected)"
python3 verify-it-yourself/planted_bugs.py object/A3-15-10-31words.txt 3 15 10 31 27 39 || ok=0
if [ "$ok" = 1 ]; then echo PASS; else echo FAIL; exit 1; fi
