#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs only python3 (standard library). Last line is ALL CHECKS PASS or FAIL.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
PY=${PYTHON:-python3}
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
n=0
tail -n +2 "$HERE/INDEX.csv" | while IFS=, read -r tid cell value table fetched file sum; do
  got=$($SHA "$HERE/$file" | cut -d' ' -f1)
  if [ "$got" = "$sum" ]; then echo "sha256 ok $file"; else echo "sha256 MISMATCH $file"; echo MISMATCH >> "$HERE/verify-it-yourself/.mismatch"; fi
done
if [ -f "$HERE/verify-it-yourself/.mismatch" ]; then rm -f "$HERE/verify-it-yourself/.mismatch"; fail=1; fi
echo "== check_sc.py: 50-digit decimal arithmetic, normalise, all pairs, against the saved live rows"
$PY -I "$HERE/verify-it-yourself/check_sc.py" "$HERE/the-record-we-beat/index_rows.html" "$HERE/the-record-we-beat/plain_rows.csv" "$HERE"/object/*.txt > "$HERE/verify-it-yourself/.out.txt" || fail=1
cat "$HERE/verify-it-yourself/.out.txt"
$PY -I "$HERE/verify-it-yourself/assert_sc.py" full 1 "$HERE/verify-it-yourself/.out.txt" || fail=1
rm -f "$HERE/verify-it-yourself/.out.txt"
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
