#!/bin/sh
# Standalone check for the object in this folder. Run from the package folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
VD="$HERE/verify-it-yourself"
OBJ="$HERE/object/win_q4_n163_k11_d104.json"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 of object matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
echo "== mindist_gf4.py (exact minimum distance by full enumeration of all 4^11 messages; rank; comparison with the live bounds)"
python3 -I "$VD/mindist_gf4.py" "$OBJ" | tee "$TMP/out.txt"
python3 -I "$VD/verdict.py" linear "$TMP/out.txt" || fail=1
echo "== second implementation in C (only if a C compiler is available)"
if command -v cc >/dev/null 2>&1; then
  cc -O2 -o "$TMP/md" "$VD/mindist4_gf4.c" && python3 -I "$VD/json2txt.py" "$OBJ" > "$TMP/g.txt" && "$TMP/md" "$TMP/g.txt" | tee "$TMP/c.txt"
  python3 -I -c "import sys,re,json; s=open(sys.argv[1]).read(); r=json.loads(open(sys.argv[2]).read().strip().splitlines()[-1]); m=re.search(r'min_distance=(\d+) A_d=(\d+)', s); ok=m and int(m[1])==r['min_distance'] and int(m[2])==r['A_d'] and 'rank_deficient=no' in s; print('C implementation agrees' if ok else 'C implementation DISAGREES'); sys.exit(0 if ok else 1)" "$TMP/c.txt" "$TMP/out.txt" || fail=1
else echo "no C compiler found; C cross-check skipped"; fi
echo "== negative control: generator row 2 replaced by a copy of row 1 (rank deficient) (must be rejected)"
python3 -I -c "import json,sys; d=json.load(open(sys.argv[1])); d['G'][1]=list(d['G'][0]); json.dump(d,open(sys.argv[2],'w'))" "$OBJ" "$TMP/neg.json"
(python3 -I "$VD/mindist_gf4.py" "$TMP/neg.json" || echo '{"VALID": false}') > "$TMP/neg.txt" 2>&1
python3 -I "$VD/verdict.py" negative "$TMP/neg.txt" || fail=1
rm -f "$TMP"/*.json "$TMP"/*.txt "$TMP"/md 2>/dev/null; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "PASS"; else echo "FAIL"; exit 1; fi
