#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Last line: PASS or FAIL.
ok=1
echo "== exact check of the code against the table cell"
python3 verify-it-yourself/check_cw.py object/A-27-8-8-778words.txt 27 8 8 778 777 1252 68eabec3d2808175e4f0f8db629c0b6137d8ab94b19e8e24e23186b03f6bc26f || ok=0
echo "== planted bugs (each must be rejected)"
python3 verify-it-yourself/planted_bugs.py object/A-27-8-8-778words.txt 27 8 8 778 777 1252 || ok=0
if [ "$ok" = 1 ]; then echo PASS; else echo FAIL; exit 1; fi
