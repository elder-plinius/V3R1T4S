#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Checks object/pair.json with the standalone standard-library checker; the last output line is PASS or FAIL.
cd "$(dirname "$0")/.." || exit 1
if command -v python3 >/dev/null 2>&1; then PY=python3; else PY=python; fi
"$PY" verify-it-yourself/verify.py object/pair.json
