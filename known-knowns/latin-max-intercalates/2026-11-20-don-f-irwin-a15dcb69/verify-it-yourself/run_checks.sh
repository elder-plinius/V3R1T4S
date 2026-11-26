#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Last line is PASS or FAIL.
set -u
cd "$(dirname "$0")/.." || exit 1
python3 verify-it-yourself/run_checks.py
