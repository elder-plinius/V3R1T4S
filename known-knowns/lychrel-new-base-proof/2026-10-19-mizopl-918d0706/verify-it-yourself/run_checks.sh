#!/bin/sh
# Standalone check for mechanical audit of Kuitche (2023) across bases 3..10 (object/kuitche_2023_audit.json).
# Run from the package folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
PY="/opt/homebrew/bin/python3"
[ -x "$PY" ] || PY="python3"
PYTHONDONTWRITEBYTECODE=1
export PYTHONDONTWRITEBYTECODE

OBJ="$HERE/object"
REC="$HERE/the-record-we-beat"
CHK="$HERE/verify-it-yourself/check_lychrel.py"
P1="$OBJ/kuitche_2023_audit.json"

fail=0
for f in "$P1" "$CHK"; do
  if [ ! -f "$f" ]; then echo "FAIL missing $f"; exit 1; fi
done

echo "== running check_lychrel.py on object/kuitche_2023_audit.json =="
"$PY" -B "$CHK" "$OBJ" "$REC" || fail=1

echo "== negative control: a corrupted copy must FAIL =="
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
cp -R "$OBJ" "$TMP/bad_obj"
sed 's/"base": 3/"base": 4/' "$P1" > "$TMP/bad_obj/kuitche_2023_audit.json"
if "$PY" -B "$CHK" "$TMP/bad_obj" "$REC" >"$TMP/neg.txt" 2>&1; then
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
