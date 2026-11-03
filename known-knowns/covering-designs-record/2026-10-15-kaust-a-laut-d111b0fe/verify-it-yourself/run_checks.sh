#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
PY=""
for c in python3 python; do
  if "$c" -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then echo "no working Python 3 found"; echo FAIL; exit 1; fi
"$PY" verify-it-yourself/check_covering.py 85 24 3 object/C85_24_3_76blocks.txt 76 d111b0feb0cd74f5af84f8bbf660d65979caca2eb05885191dbd3fb63c14ea53
