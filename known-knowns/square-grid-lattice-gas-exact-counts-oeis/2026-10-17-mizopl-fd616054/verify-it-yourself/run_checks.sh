#!/bin/sh
# Run from the package root: sh verify-it-yourself/run_checks.sh
# Last output line is PASS or FAIL.
cd "$(dirname "$0")/.." || exit 1
python3 verify-it-yourself/check.py
