#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Needs Python 3 (standard library) and drat-trim (DRAT_TRIM=path, or drat-trim on PATH). The full check also needs
# CADICAL=path to CaDiCaL 3.0.1 (regenerates the n = 22 proof: about 10 minutes, 1.5 GB of temporary disk).
P=${PYTHON:-python3}
if "$P" -I verify-it-yourself/verify.py; then exit 0; else exit 1; fi
