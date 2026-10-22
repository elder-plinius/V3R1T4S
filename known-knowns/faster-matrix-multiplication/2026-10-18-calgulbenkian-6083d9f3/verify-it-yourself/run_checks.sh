#!/bin/sh
# Standalone check for object/4x13x15_m533_Z.json. Run from the claim folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/4x13x15_m533_Z.json"
CHK="$HERE/verify-it-yourself/check_fmm_fast.py"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== check_fmm_fast.py: exact Brent equations over Z, rank 533, coefficient class Z"
python3 -I "$CHK" "$OBJ" --expect-rank 533 --expect-class Z || fail=1
echo "== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t ringcheck)
python3 -I -c "
import json,sys
d=json.load(open(sys.argv[1]))
row=d['u'][0]
k=[i for i,x in enumerate(row) if x][0]
row[k]=-row[k]
json.dump(d,open(sys.argv[2],'w'))" "$OBJ" "$TMP/neg.json"
if python3 -I "$CHK" "$TMP/neg.json" >"$TMP/neg.txt" 2>&1; then echo "negative control NOT rejected"; fail=1; else tail -n 1 "$TMP/neg.txt"; echo "negative control rejected as expected"; fi
rm -f "$TMP/neg.json" "$TMP/neg.txt"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
