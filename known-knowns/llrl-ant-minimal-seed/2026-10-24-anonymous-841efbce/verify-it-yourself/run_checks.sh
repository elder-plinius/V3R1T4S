#!/bin/sh
# run from the package folder: sh verify-it-yourself/run_checks.sh   (last line PASS or FAIL)
cd "$(dirname "$0")/.." || exit 1
sha256sum -c verify-it-yourself/OBJECT_SHA256 >/dev/null 2>&1 || { echo "object sha256 mismatch"; echo FAIL; exit 1; }
python3 verify-it-yourself/verify.py object/minimisers.txt
