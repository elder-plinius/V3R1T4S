#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs Python 3 with torch (CUDA) and numpy; set PYTHON to that interpreter if python3 lacks torch.
P=${PYTHON:-python3}
if "$P" -I verify-it-yourself/verify.py; then exit 0; else echo FAIL; exit 1; fi
