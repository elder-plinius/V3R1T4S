#!/bin/sh
# Standalone check for object/cert_A35_14_14.json. Run from this folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
PY="${PYTHON:-python3}"
OBJ="$HERE/object/cert_A35_14_14.json"
CHK="$HERE/verify-it-yourself/check_delsarte.py"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== self-test of the checker on cells with known answers (exact Delsarte LP by vertex enumeration)"
"$PY" -I "$CHK" --selftest || fail=1
echo "== known answer: merged certificate for A(31,12,10) must give 197"
"$PY" -I "$CHK" "$HERE/verify-it-yourself/known-answer/cert_A31_12_10.json" 31 12 10 197 || fail=1
echo "== check_delsarte.py on object/cert_A35_14_14.json (exact dual feasibility, objective, floor)"
out=$("$PY" -I "$CHK" "$OBJ" 35 14 14 837 2>&1); rc=$?
echo "$out"
if [ "$rc" -ne 0 ]; then fail=1; echo "checker verdict: FAIL"; else echo "checker verdict: PASS"; fi
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
echo "== negative control 1: the same certificate checked against a claim one smaller must FAIL"
if "$PY" -I "$CHK" "$OBJ" 35 14 14 $((837 - 1)) >"$TMP/n1.txt" 2>&1; then echo "negative control 1 NOT rejected"; fail=1; else echo "negative control 1 rejected as expected"; fi
echo "== negative control 2: a copy with every dual value multiplied by 99/100 must FAIL (dual infeasible)"
"$PY" -I -c "import json,sys; from fractions import Fraction as F; d=json.load(open(sys.argv[1])); d['y']={k:str(F(v)*F(99,100)) for k,v in d['y'].items()}; json.dump(d,open(sys.argv[2],'w'))" "$OBJ" "$TMP/neg2.json"
if "$PY" -I "$CHK" "$TMP/neg2.json" 35 14 14 837 >"$TMP/n2.txt" 2>&1; then echo "negative control 2 NOT rejected"; fail=1; else echo "negative control 2 rejected as expected"; fi
echo "== negative control 3: a copy with one dual value set negative must FAIL"
"$PY" -I -c "import json,sys; d=json.load(open(sys.argv[1])); k=sorted(d['y'],key=int)[0]; d['y'][k]='-'+d['y'][k]; json.dump(d,open(sys.argv[2],'w'))" "$OBJ" "$TMP/neg3.json"
if "$PY" -I "$CHK" "$TMP/neg3.json" 35 14 14 837 >"$TMP/n3.txt" 2>&1; then echo "negative control 3 NOT rejected"; fail=1; else echo "negative control 3 rejected as expected"; fi
rm -f "$TMP"/*.txt "$TMP"/*.json; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
