#!/bin/sh
# Run from the package root: sh verify-it-yourself/run_checks.sh   (FULL=1 for the full recompute from k = 1)
# Last output line is PASS or FAIL.
cd "$(dirname "$0")/.." || exit 1
python3 verify-it-yourself/check.py
