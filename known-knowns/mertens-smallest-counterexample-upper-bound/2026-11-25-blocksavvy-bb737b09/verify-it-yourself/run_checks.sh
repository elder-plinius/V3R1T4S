#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (FLINT=1 adds a python-flint recompute of 4 chunks)
# Needs python3 >= 3.8 (standard library only). Last line: PASS or FAIL.
python3 verify-it-yourself/check_k2.py || { echo FAIL; exit 1; }
