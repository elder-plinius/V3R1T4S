#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh  (Python 3, standard library only)
cd "$(dirname "$0")/.." || exit 1
python3 -I verify-it-yourself/verify_code.py object/code_6_256.txt 6 256 0.704931969352 f1478e6af59430f60997ba2d052fd658e92314fa61deb5439ff49df96d595411
