#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh PLAIN INDEX
# PLAIN and INDEX are your own fetches of https://spherical-codes.org/plain and https://spherical-codes.org/ .
# Needs only python3 (standard library). Writes no files. Last line is ALL CHECKS PASS or FAIL.
set -u
if [ $# -ne 2 ]; then echo "usage: sh verify-it-yourself/run_checks.sh PLAIN INDEX"; exit 2; fi
HERE=$(cd "$(dirname "$0")/.." && pwd)
PY=${PYTHON:-python3}
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
{
  read -r header
  while IFS=, read -r tid cell value table fetched file sum; do
    got=$($SHA "$HERE/$file" | cut -d' ' -f1)
    if [ "$got" = "$sum" ]; then echo "sha256 ok $file"; else echo "sha256 MISMATCH $file"; fail=1; fi
  done
} < "$HERE/INDEX.csv"
echo "== check_sc.py: 50-digit decimal arithmetic, normalise, all pairs, against the table pages given"
out=$($PY -I "$HERE/verify-it-yourself/check_sc.py" "$2" "$1" "$HERE"/object/*.txt) || fail=1
printf '%s\n' "$out"
printf '%s\n' "$out" | $PY -I "$HERE/verify-it-yourself/assert_sc.py" full 1 /dev/stdin || fail=1
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
