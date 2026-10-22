#!/bin/sh
# Standalone check for object/new_optimal_stabilizer_codes_r11_d4.json, cell [[37,26]]. Run from the package folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/new_optimal_stabilizer_codes_r11_d4.json"
CHK="$HERE/verify-it-yourself/check_stabilizer.py"
TAB="$HERE/the-record-we-beat/cell_37_26_excerpt.txt"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== check_stabilizer.py on [[37,26]]"
python3 "$CHK" "$OBJ" 37 26 "$TAB" || fail=1
echo "== negative control: a copy with one bit of the first X row flipped must FAIL"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
python3 -c "import json,sys; d=json.load(open(sys.argv[1])); c=[c for c in d['new_optimal_codes'] if c['n']==37 and c['k']==26][0]; c['HX'][0][0]^=1; json.dump(d,open(sys.argv[2],'w'))" "$OBJ" "$TMP/neg.json"
if python3 "$CHK" "$TMP/neg.json" 37 26 "$TAB" >"$TMP/neg.txt" 2>&1; then echo "negative control NOT rejected"; fail=1; else echo "negative control rejected as expected: $(tail -n 1 "$TMP/neg.txt")"; fi
rm -f "$TMP/neg.json" "$TMP/neg.txt"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; fi
[ "$fail" -eq 0 ]
