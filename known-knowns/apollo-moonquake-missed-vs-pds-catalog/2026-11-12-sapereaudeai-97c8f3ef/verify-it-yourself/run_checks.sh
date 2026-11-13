#!/bin/sh
# run from the package folder: sh verify-it-yourself/run_checks.sh
PY="${PYTHON:-python3}"
command -v "$PY" >/dev/null 2>&1 || PY=python
"$PY" verify-it-yourself/check_p2.py
