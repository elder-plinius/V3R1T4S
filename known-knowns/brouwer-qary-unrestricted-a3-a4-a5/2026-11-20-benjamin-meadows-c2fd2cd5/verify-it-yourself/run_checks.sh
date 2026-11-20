#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Last line: PASS or FAIL.
ok=1
echo "== exact check of the code against the table cell"
python3 verify-it-yourself/check_code.py object/A4-12-8-145words.txt 4 12 8 145 128 240 c2fd2cd5a942d6381693303c92e3f4ad107ad0a2f5565239dc443a55a6e24d6b || ok=0
echo "== rebuild from the written description"
python3 verify-it-yourself/rebuild.py object/A4-12-8-145words.txt || ok=0
echo "== planted bugs (each must be rejected)"
python3 verify-it-yourself/planted_bugs.py object/A4-12-8-145words.txt 4 12 8 145 128 240 || ok=0
if [ "$ok" = 1 ]; then echo PASS; else echo FAIL; exit 1; fi
