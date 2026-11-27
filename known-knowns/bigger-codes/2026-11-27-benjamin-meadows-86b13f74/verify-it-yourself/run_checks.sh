#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Last line: PASS or FAIL.
ok=1
echo "== exact check of the code against the table cell"
python3 verify-it-yourself/check_cw.py object/A-25-10-12-142words.txt 25 10 12 142 141 433 86b13f74de60c58c60f8255a4ced73ad9a126038dc79c543021b55b5159bc658 || ok=0
echo "== planted bugs (each must be rejected)"
python3 verify-it-yourself/planted_bugs.py object/A-25-10-12-142words.txt 25 10 12 142 141 433 || ok=0
if [ "$ok" = 1 ]; then echo PASS; else echo FAIL; exit 1; fi
