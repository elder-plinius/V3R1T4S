#!/bin/sh
# Standalone check for object/C_57_14_3_b108.json. Run from the claim folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
PY=${PY:-python3}
OBJ="$HERE/object/C_57_14_3_b108.json"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== check_covering.py: every 3-subset of the 57-set lies in some block"
"$PY" "$HERE/verify-it-yourself/check_covering.py" "$OBJ" | tee "$HERE/verify-it-yourself/.last_check.txt"
grep -q "PASS" "$HERE/verify-it-yourself/.last_check.txt" || fail=1
grep -q "C(57,14,3) b=108 " "$HERE/verify-it-yourself/.last_check.txt" || fail=1
rm -f "$HERE/verify-it-yourself/.last_check.txt"
echo "== schonheim.py"
"$PY" "$HERE/verify-it-yourself/schonheim.py" "$OBJ" || fail=1
echo "== negative control: a copy with one block removed (and b adjusted) must FAIL the coverage check"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
"$PY" -c "import json,sys; d=json.load(open(sys.argv[1])); d['blocks']=d['blocks'][1:]; d['b']=len(d['blocks']); json.dump(d,open(sys.argv[2],'w'))" "$OBJ" "$TMP/neg.json"
"$PY" "$HERE/verify-it-yourself/check_covering.py" "$TMP/neg.json" >"$TMP/neg.txt" 2>&1
if grep -q "PASS" "$TMP/neg.txt"; then echo "negative control NOT rejected"; fail=1; else echo "negative control rejected as expected: $(cat "$TMP/neg.txt" | cut -c1-120)"; fi
rm -f "$TMP/neg.json" "$TMP/neg.txt"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
