#!/bin/sh
# Standalone verification script for 2026-11-02-rainrat-dcc89550 (etp-finite-magma-677-255, p2).
# Run from the package root: sh verify-it-yourself/run_checks.sh
set -eu
python3 verify-it-yourself/check_p2.py object/separation_models.json object/Equation677.lean
