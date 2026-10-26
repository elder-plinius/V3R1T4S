#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Prints PASS or FAIL as its last line. Python 3 standard library only, no network, a few seconds.
python3 verify-it-yourself/check.py 2>&1
