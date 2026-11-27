#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Last line: PASS or FAIL.
ok=1
echo "== exact check of the code against the table cell"
python3 verify-it-yourself/check_cw.py object/A-26-10-12-214words.txt 26 10 12 214 213 691 c78abc24b831d29945e88f58953941927761132fa60f8a2cd2696a5dcec81715 || ok=0
echo "== planted bugs (each must be rejected)"
python3 verify-it-yourself/planted_bugs.py object/A-26-10-12-214words.txt 26 10 12 214 213 691 || ok=0
if [ "$ok" = 1 ]; then echo PASS; else echo FAIL; exit 1; fi
