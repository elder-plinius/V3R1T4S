#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
PY=$(command -v python3 || command -v python)
"$PY" verify-it-yourself/check_domatic.py object/dom-Q12-21-partition.txt 12 21 e5ea86593b4ec792d5957ca307e6eed42f65b676ab19de42d79c0733211b1b2e
