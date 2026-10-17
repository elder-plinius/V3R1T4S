#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
# Downloads the pinned NCBI export (551 MB) and cluster list on first run; Python 3 standard library only.
cd "$(dirname "$0")/.." || exit 1
python3 verify-it-yourself/check.py || exit 1
