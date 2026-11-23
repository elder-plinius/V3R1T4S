#!/bin/sh
# Run the standalone checker from the package folder (stdlib python3 only).
# Usage: sh verify-it-yourself/run_checks.sh
cd "$(dirname "$0")/.." || exit 1
python3 verify-it-yourself/checker.py
rc=$?
exit $rc
