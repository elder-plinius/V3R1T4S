#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
PY=""
for c in python3 python; do
  if "$c" -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then echo "no working Python 3 found"; echo FAIL; exit 1; fi
"$PY" verify-it-yourself/check_covering.py 61 25 3 object/C61_25_3_27blocks.txt 27 097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e
