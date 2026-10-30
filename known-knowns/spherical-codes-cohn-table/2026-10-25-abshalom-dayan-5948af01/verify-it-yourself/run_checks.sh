#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh  (Python 3, standard library only)
cd "$(dirname "$0")/.." || exit 1
python3 verify-it-yourself/verify_code.py object/code_6_575.txt 6 575 0.792780236785 5948af010bf1c2e12ca85af0af8cf84930f34cf3f8db5824147153d7eab95a8c
