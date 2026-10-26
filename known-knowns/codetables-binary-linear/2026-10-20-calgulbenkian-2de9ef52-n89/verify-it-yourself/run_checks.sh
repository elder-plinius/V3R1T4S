#!/bin/sh
_PKG=$(cd "$(dirname "$0")/.." && pwd)
if command -v shasum >/dev/null 2>&1; then _S="shasum -a 256"; else _S="sha256sum"; fi
( cd "$_PKG" && grep "  object/" SHA256SUMS > "${TMPDIR:-/tmp}/objsums.$$" && $_S -c "${TMPDIR:-/tmp}/objsums.$$" >/dev/null 2>&1 ) || { echo "object file sha256 MISMATCH against SHA256SUMS"; echo "FAIL"; exit 1; }
# Standalone check for object/new_stabilizer_codes_d5.json, cell [[89,71]]. Run from the claim folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/new_stabilizer_codes_d5.json"
CHK="$HERE/verify-it-yourself/check_stabilizer.py"
TAB="$HERE/the-record-we-beat/cell_89_71_excerpt.txt"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== check_stabilizer.py on [[89,71]]"
python3 "$CHK" "$OBJ" 89 71 "$TAB" || fail=1
echo "== negative control: a copy with one bit of the first X row flipped must FAIL"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
python3 -c "import json,sys; d=json.load(open(sys.argv[1])); c=[c for c in d['new_d5_codes'] if c['n']==89 and c['k']==71][0]; c['HX'][0][0]^=1; json.dump(d,open(sys.argv[2],'w'))" "$OBJ" "$TMP/neg.json"
if python3 "$CHK" "$TMP/neg.json" 89 71 "$TAB" >"$TMP/neg.txt" 2>&1; then echo "negative control NOT rejected"; fail=1; else echo "negative control rejected as expected: $(tail -n 1 "$TMP/neg.txt")"; fi
rm -f "$TMP/neg.json" "$TMP/neg.txt"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; fi
[ "$fail" -eq 0 ]
