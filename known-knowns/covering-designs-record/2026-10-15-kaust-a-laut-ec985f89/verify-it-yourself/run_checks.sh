#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line: PASS or FAIL)
PY=""
for c in python3 python; do
  if "$c" -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then echo "no working Python 3 found"; echo FAIL; exit 1; fi
"$PY" verify-it-yourself/check_covering.py 41 12 5 object/C41_12_5_2207blocks.txt 2207 ec985f89dd793006ccf15346b6937419e1ce4e922034d73b18e769fb958778aa
