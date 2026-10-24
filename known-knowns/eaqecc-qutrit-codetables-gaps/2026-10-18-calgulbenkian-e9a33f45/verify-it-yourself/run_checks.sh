#!/bin/sh
# Standalone check for object/eaqecc_34_2_24_24.json. Run from the claim folder: sh verify-it-yourself/run_checks.sh
# Needs python3 with numpy (set PY to another interpreter if needed).
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
PY=${PY:-python3}
OBJ="$HERE/object/eaqecc_34_2_24_24.json"
CHK="$HERE/verify-it-yourself/check_eaqecc.py"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== calibration on hand-derived cases"
"$PY" "$HERE/verify-it-yourself/calibration.py" || fail=1
echo "== check_eaqecc.py on object/eaqecc_34_2_24_24.json (table cell dlower-dupper = 23-32)"
"$PY" "$CHK" "$OBJ" 23 32 || fail=1
echo "== negative control: a copy with one matrix entry changed must FAIL"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
"$PY" -c "import json,sys; d=json.load(open(sys.argv[1])); d['S'][0][0]=(d['S'][0][0]+1)%3; json.dump(d,open(sys.argv[2],'w'))" "$OBJ" "$TMP/neg.json"
if "$PY" "$CHK" "$TMP/neg.json" 23 32 >"$TMP/neg.txt" 2>&1; then echo "negative control NOT rejected"; fail=1; else echo "negative control rejected as expected: $(tail -n 1 "$TMP/neg.txt")"; fi
rm -f "$TMP/neg.json" "$TMP/neg.txt"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
