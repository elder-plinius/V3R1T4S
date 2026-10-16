#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
set -eu
python3 -I -B verify-it-yourself/check_code.py
