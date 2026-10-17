#!/bin/sh
# Run this file from the package folder:
#     sh verify-it-yourself/run_checks.sh
# The last line of the output is PASS or FAIL.
# This file needs python3 and numpy.
cd "$(dirname "$0")/.." || exit 1
python3 -c "import numpy" 2>/dev/null || { echo "numpy is necessary"; echo "FAIL"; exit 1; }
python3 verify-it-yourself/check.py
