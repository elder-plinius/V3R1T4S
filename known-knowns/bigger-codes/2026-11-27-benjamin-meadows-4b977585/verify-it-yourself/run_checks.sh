#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Last line: PASS or FAIL.
ok=1
echo "== exact check of the code against the table cell"
python3 verify-it-yourself/check_cw.py object/A-27-8-12-3387words.txt 27 8 12 3387 3374 10460 4b977585972408991e43784ce2f81591c529d9f3a9d770ee9fc4262eb056e3ba || ok=0
echo "== planted bugs (each must be rejected)"
python3 verify-it-yourself/planted_bugs.py object/A-27-8-12-3387words.txt 27 8 12 3387 3374 10460 || ok=0
if [ "$ok" = 1 ]; then echo PASS; else echo FAIL; exit 1; fi
