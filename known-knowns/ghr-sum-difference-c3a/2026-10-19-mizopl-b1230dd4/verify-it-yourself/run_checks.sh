#!/bin/sh
# Standalone check for GHR sum-difference constant C_{3a} finite-depth certificate (object/finite_certificate_17086_27995.json).
# Run from the package folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
PY="/opt/homebrew/bin/python3"
[ -x "$PY" ] || PY="python3"
PYTHONDONTWRITEBYTECODE=1
export PYTHONDONTWRITEBYTECODE

OBJ="$HERE/object"
CHK="$HERE/verify-it-yourself/check_c3a.py"
P1="$OBJ/finite_certificate_17086_27995.json"

fail=0
for f in "$P1" "$OBJ/finite_certificate_17032_27995.json" "$OBJ/kleinwaks_finite_certificate_17032_34065.json" "$OBJ/mask_17086.txt" "$OBJ/sum_support_17086.txt" "$OBJ/pruned_differences_17086_27995.tsv" "$CHK"; do
  if [ ! -f "$f" ]; then echo "FAIL missing $f"; exit 1; fi
done

echo "== running check_c3a.py on object/ files =="
"$PY" "$CHK" "$OBJ" || fail=1

echo "== negative control: a corrupted copy must FAIL =="
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
cp -R "$OBJ" "$TMP/bad_obj"
sed 's/17074745018/17074745019/' "$P1" > "$TMP/bad_obj/finite_certificate_17086_27995.json"
if "$PY" "$CHK" "$TMP/bad_obj" >"$TMP/neg.txt" 2>&1; then
  echo "negative control NOT rejected"
  fail=1
else
  echo "negative control rejected as expected ($(tail -n 1 "$TMP/neg.txt"))"
fi
rm -rf "$TMP"

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASS"
else
  echo "FAIL"
  exit 1
fi
