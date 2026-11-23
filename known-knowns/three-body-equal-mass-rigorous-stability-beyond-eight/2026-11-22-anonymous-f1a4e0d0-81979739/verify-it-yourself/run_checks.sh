#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs python3 with python-flint 0.9.0 (and sympy for the full check). Set PY to choose the interpreter.
# Quick check (seconds): stability half from the saved enclosure. FULL=1 also reruns the whole certificate
# (existence + stability from scratch, about 20 minutes on one core) and the symbolic lemmas.
PY=${PY:-${V3R1T4S_PYTHON:-python3}}
set -e
if [ "$FULL" = "1" ]; then
  (cd how-we-built-it && $PY lemmas.py && nice $PY certify.py 2 55 0 448 96 384 72 | tail -1 | grep -q "CERT ROW 2: PASS") || { echo FAIL; exit 1; }
fi
out=$($PY verify-it-yourself/check_c3.py) || { echo "$out" | tail -3; echo FAIL; exit 1; }
echo "$out" | tail -1
