#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
PY=$(command -v python3 || command -v python)
"$PY" verify-it-yourself/check_total_domatic.py object/tdom-Q10-16-partition.txt 10 16 211f9188400687ad9e5fbe69cb47cf465acd1de52e9476992e0c7497efd034ec
