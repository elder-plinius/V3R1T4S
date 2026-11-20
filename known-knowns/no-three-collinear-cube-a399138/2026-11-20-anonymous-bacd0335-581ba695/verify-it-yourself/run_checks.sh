#!/bin/sh
# Standalone check for a(7) <= 97 (OEIS A399138, the 7x7x7 no-three-in-line
# cube problem). Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs: python3 (3.8+, standard library only), a C compiler (cc).
set -u
python3 "$(dirname "$0")/check_a7_le_97.py"
