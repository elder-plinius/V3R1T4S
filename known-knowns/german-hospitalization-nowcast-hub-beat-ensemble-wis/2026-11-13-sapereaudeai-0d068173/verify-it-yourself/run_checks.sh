#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
PY=${PYTHON:-python3}
"$PY" verify-it-yourself/check_p3.py
exit $?
