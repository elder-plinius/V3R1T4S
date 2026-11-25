#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs python3 >= 3.8 (standard library only). Last line: PASS or FAIL.
python3 verify-it-yourself/check_sexy.py || { echo FAIL; exit 1; }
