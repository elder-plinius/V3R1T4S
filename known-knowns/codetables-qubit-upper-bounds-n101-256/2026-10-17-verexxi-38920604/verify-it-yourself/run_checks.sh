#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (Python 3.8+, standard library only)
ok=1
for f in object/cert_135_1_45_sh.json; do
  python3 -I verify-it-yourself/check_cert.py "$f" || ok=0
  python3 -I verify-it-yourself/check2_recurrence.py "$f" || ok=0
done
if [ $ok = 1 ]; then echo PASS; else echo FAIL; exit 1; fi
