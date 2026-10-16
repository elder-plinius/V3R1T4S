#!/bin/sh
# run from the package folder: sh verify-it-yourself/run_checks.sh
cd "$(dirname "$0")/.." || exit 1
python3 verify-it-yourself/check_labs.py object/L464.txt
