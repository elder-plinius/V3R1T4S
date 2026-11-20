#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Last line: PASS or FAIL.
ok=1
echo "== exact check of the code against the table cell"
python3 verify-it-yourself/check_code.py object/A4-12-7-320words.txt 4 12 7 320 256 1167 7a882f805e40e7ef6a9565684cc1c36d616b91f2d3081be69aef2d00dfe69d82 || ok=0
echo "== rebuild from the written description"
python3 verify-it-yourself/rebuild.py object/A4-12-7-320words.txt || ok=0
echo "== planted bugs (each must be rejected)"
python3 verify-it-yourself/planted_bugs.py object/A4-12-7-320words.txt 4 12 7 320 256 1167 || ok=0
if [ "$ok" = 1 ]; then echo PASS; else echo FAIL; exit 1; fi
