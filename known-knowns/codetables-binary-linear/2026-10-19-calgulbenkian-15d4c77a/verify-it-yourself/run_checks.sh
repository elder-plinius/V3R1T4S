#!/bin/sh
# Standalone check for the object in this folder. Run from the package folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
VD="$HERE/verify-it-yourself"
OBJ="$HERE/object/lp_cert_q8_n67_k5_dub56.json"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 of object matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
echo "== lp_delsarte_check.py (exact Fractions, excluded distance D = live upper bound 56) and neighbour propagation"
python3 -I "$VD/lp_delsarte_check.py" "$OBJ" 56 | tee "$TMP/out.txt"
python3 -I "$VD/verdict.py" lp "$TMP/out.txt" || fail=1
echo "== negative control: first multiplier made negative (must be rejected) (must be rejected)"
python3 -I -c "import json,sys; d=json.load(open(sys.argv[1])); d['y_multipliers_rational'][0]='-'+d['y_multipliers_rational'][0]; json.dump(d,open(sys.argv[2],'w'))" "$OBJ" "$TMP/neg.json"
(python3 -I "$VD/lp_delsarte_check.py" "$TMP/neg.json" 56 || echo '{"VALID": false}') > "$TMP/neg.txt" 2>&1
python3 -I "$VD/verdict.py" negative "$TMP/neg.txt" || fail=1
rm -f "$TMP"/*.json "$TMP"/*.txt "$TMP"/md 2>/dev/null; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "PASS"; else echo "FAIL"; exit 1; fi
