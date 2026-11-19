#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Python 3 standard library only. Uses $MBM_TEST_CSV if set, else downloads the 6 MB test CSV once into
# verify-it-yourself/cache/ and checks its sha256.
cd "$(dirname "$0")/.." || exit 1
python3 -I -B verify-it-yourself/check.py || exit 1
