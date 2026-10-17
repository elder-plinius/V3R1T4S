#!/bin/sh
# Standalone check for object/2x4x7_m45_cr169_ZT_reduced.json. Run from this folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/2x4x7_m45_cr169_ZT_reduced.json"
CHK="$HERE/verify-it-yourself/check_slp.py"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== check_slp.py on object/2x4x7_m45_cr169_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)"
python3 "$CHK" "$OBJ" | tee "$HERE/verify-it-yourself/.last_check.json"
python3 -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); ok=r.get('VALID') is True and r.get('adds_total')==169 and r.get('tensor_exact') in ('C^T','C=AB'); print('checker verdict:', 'PASS' if ok else 'FAIL', '(VALID=%s, adds_total=%s, tensor=%s)'%(r.get('VALID'),r.get('adds_total'),r.get('tensor_exact'))); sys.exit(0 if ok else 1)" "$HERE/verify-it-yourself/.last_check.json" || fail=1
rm -f "$HERE/verify-it-yourself/.last_check.json"
echo "== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
python3 -c "import json,sys; d=json.load(open(sys.argv[1])); d['u_fresh'][0][0]['value']*=-1; json.dump(d,open(sys.argv[2],'w'))" "$OBJ" "$TMP/neg.json"
python3 "$CHK" "$TMP/neg.json" >"$TMP/neg.txt" 2>&1
if python3 -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); sys.exit(0 if r.get('VALID') is True else 1)" "$TMP/neg.txt"; then echo "negative control NOT rejected"; fail=1; else echo "negative control rejected as expected (VALID false)"; fi
rm -f "$TMP/neg.json" "$TMP/neg.txt"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
