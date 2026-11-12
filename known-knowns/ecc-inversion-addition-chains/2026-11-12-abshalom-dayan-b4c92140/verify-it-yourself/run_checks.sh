#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Last output line is PASS or FAIL. Python 3 standard library only, no network.
D=$(cd "$(dirname "$0")" && pwd)
cd "$D/.." || { echo FAIL; exit 1; }
if python3 "$D/check_chain.py" object/chain.txt; then echo PASS; else echo FAIL; exit 1; fi
