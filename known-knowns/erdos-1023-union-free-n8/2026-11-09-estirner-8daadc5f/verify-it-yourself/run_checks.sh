#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Needs only Python 3 (standard library); takes a few seconds.
P=${PYTHON:-python3}
if "$P" -I verify-it-yourself/check_union_free.py object/union_free_n8_80.txt 8 80; then exit 0; else exit 1; fi
