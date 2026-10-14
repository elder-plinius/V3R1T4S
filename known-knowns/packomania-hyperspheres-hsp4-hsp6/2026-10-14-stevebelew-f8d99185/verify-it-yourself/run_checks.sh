#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (Python 3 standard library only; about 5 s)
cd "$(dirname "$0")/.." || exit 1
python3 verify-it-yourself/check_hsp4.py object/hsp4-35-candidate.txt 0.306285269828 the-record-we-beat/hsp4-35-posted.txt
