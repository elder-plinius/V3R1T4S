#!/bin/sh
# Standalone check for the object in this folder. Run from the package folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
VD="$HERE/verify-it-yourself"
OBJ="$HERE/object/qecc_p1_n23_k9_d5.json"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 of object matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
echo "== qecc_check.py (exact stabilizer-code check, d = 5, comparison with live bounds and neighbours)"
python3 -I "$VD/qecc_check.py" "$OBJ" | tee "$TMP/out.txt"
python3 -I "$VD/verdict.py" qecc "$TMP/out.txt" || fail=1
echo "== negative control: one X bit of generator 1 flipped (must fail self-orthogonality or change the distance) (must be rejected)"
python3 -I -c "import json,sys; d=json.load(open(sys.argv[1])); d['X'][0][0]^=1; json.dump(d,open(sys.argv[2],'w'))" "$OBJ" "$TMP/neg.json"
(python3 -I "$VD/qecc_check.py" "$TMP/neg.json" || echo '{"VALID": false}') > "$TMP/neg.txt" 2>&1
python3 -I "$VD/verdict.py" negative "$TMP/neg.txt" || fail=1
rm -f "$TMP"/*.json "$TMP"/*.txt "$TMP"/md 2>/dev/null; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "PASS"; else echo "FAIL"; exit 1; fi
