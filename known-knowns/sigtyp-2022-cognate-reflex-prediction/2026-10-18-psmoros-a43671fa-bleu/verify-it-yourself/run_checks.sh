#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Fetches the pinned public inputs (or uses an existing folder named by V3R1T4S_Q15_DATA, checked file by file
# against verify-it-yourself/inputs.sha256), then runs the standard-library checker. Last line: PASS or FAIL.
D="${V3R1T4S_Q15_DATA:-verify-it-yourself/inputs}"
python3 verify-it-yourself/fetch_inputs.py "$D" || { echo FAIL; exit 1; }
python3 verify-it-yourself/check_q15.py "$D" object
