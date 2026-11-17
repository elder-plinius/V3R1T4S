#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
cd "$(dirname "$0")/.." || exit 1
python3 verify-it-yourself/check_term.py object/A389690_23.txt
