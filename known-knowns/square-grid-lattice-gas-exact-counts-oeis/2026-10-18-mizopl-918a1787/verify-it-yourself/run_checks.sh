#!/bin/sh
# Standalone check for OEIS A089980 antidiagonal d = 79 (object/a089980_antidiag79.txt).
# Run from the package folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
PY="/opt/homebrew/bin/python3"
[ -x "$PY" ] || PY="python3"
PYTHONDONTWRITEBYTECODE=1
export PYTHONDONTWRITEBYTECODE

BFILE="$HERE/verify-it-yourself/b089980.txt"
TXT="$HERE/object/a089980_antidiag79.txt"
TSV="$HERE/object/a089980_antidiag79.tsv"
HS_RES="$HERE/object/residues_hs_mod.tsv"
FAR_RES="$HERE/object/residues_far.tsv"
IND="$HERE/object/antidiag79_indep_bigint.tsv"
CHK="$HERE/verify-it-yourself/check_a089980_ad79.py"

fail=0
for f in "$BFILE" "$TXT" "$TSV" "$HS_RES" "$FAR_RES" "$IND" "$CHK"; do
  if [ ! -f "$f" ]; then echo "FAIL missing $f"; exit 1; fi
done

echo "== running check_a089980_ad79.py on object/ files =="
"$PY" "$CHK" "$BFILE" "$TXT" "$TSV" "$HS_RES" "$FAR_RES" "$IND" || fail=1

echo "== negative control: a corrupted copy must FAIL =="
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
sed '1s/3160 1/3160 2/' "$TXT" > "$TMP/bad.txt"
if "$PY" "$CHK" "$BFILE" "$TMP/bad.txt" "$TSV" "$HS_RES" "$FAR_RES" "$IND" >"$TMP/neg.txt" 2>&1; then
  echo "negative control NOT rejected"
  fail=1
else
  echo "negative control rejected as expected ($(tail -n 1 "$TMP/neg.txt"))"
fi
rm -f "$TMP/bad.txt" "$TMP/neg.txt"
rmdir "$TMP" 2>/dev/null

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASS"
else
  echo "FAIL"
  exit 1
fi
