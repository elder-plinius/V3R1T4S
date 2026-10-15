#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
cd "$(dirname "$0")/.." || exit 1
${PYTHON:-python3} verify-it-yourself/check.py "$@"
