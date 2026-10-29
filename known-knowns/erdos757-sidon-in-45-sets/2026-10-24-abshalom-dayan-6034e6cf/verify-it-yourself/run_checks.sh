#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (needs python3, standard library only; no network)
cd "$(dirname "$0")/.." || exit 1
python3 verify-it-yourself/check_p2_stdlib.py object/H.json 56
