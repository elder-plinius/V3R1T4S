#!/bin/sh
# run from the package folder: sh verify-it-yourself/run_checks.sh   (Python 3 standard library only; ~5 s)
SHA=$(tail -1 INDEX.csv | awk -F, '{print $NF}')
REC=$(tail -1 INDEX.csv | awk -F, '{print $4}')
python3 verify-it-yourself/check_layout.py object/layout16.json object/iea37-v3r1t4s-opt16.yaml "$SHA" "$REC" || { echo FAIL; exit 1; }
echo PASS
