#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Needs Python 3 with numpy and onnxruntime (CPU); set PYTHON to that interpreter if python3 lacks them.
# NREF (default 256) sets how many saved configurations step 5 re-evaluates; NREF=2048 takes about 8 minutes on 2 threads.
P=${PYTHON:-python3}
if "$P" -I verify-it-yourself/verify.py; then exit 0; else echo FAIL; exit 1; fi
