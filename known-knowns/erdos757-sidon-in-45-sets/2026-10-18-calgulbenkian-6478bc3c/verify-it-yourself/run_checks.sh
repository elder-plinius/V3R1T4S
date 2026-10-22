#!/bin/sh
# Standalone check for object/witness_n21_s12.json. Run from the package folder: sh verify-it-yourself/run_checks.sh
# Methods: (1) bitmask branch-and-bound, (2) exhaustive enumeration of all 2^n subsets (both in check_e757.py),
# (3) ILP with pulp and CBC (ilp_sidon.py; needs pulp, installed with: pip install pulp).
# If pulp is missing the ILP is skipped with a clear line and the other methods still run.
# PASS is printed only if every method that ran agreed AND branch-and-bound and exhaustive enumeration both ran.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
PY=${PY:-python3}
OBJ="$HERE/object/witness_n21_s12.json"
CHK="$HERE/verify-it-yourself/check_e757.py"
CAL="$HERE/verify-it-yourself/calibration_ma_tang.json"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== branch-and-bound and exhaustive enumeration: Ma-Tang 14-set calibration (must give s = 8)"
"$PY" "$CHK" "$CAL" --expect-s 8 --expect-n 14 || fail=1
echo "== branch-and-bound and exhaustive enumeration: object, n = 21, s = 12"
"$PY" "$CHK" "$OBJ" --expect-s 12 --expect-n 21 || fail=1
echo "== ILP (needs pulp)"
if "$PY" -c "import pulp" >/dev/null 2>&1; then
  ilp=ran
  "$PY" "$HERE/verify-it-yourself/ilp_sidon.py" "$CAL" --expect-s 8 || fail=1
  "$PY" "$HERE/verify-it-yourself/ilp_sidon.py" "$OBJ" --expect-s 12 || fail=1
else
  ilp=skipped
  echo "ILP SKIPPED: the python package pulp is not installed for $PY (pip install pulp); the other methods ran above"
fi
echo "== negative control: a copy with elements moved to break the (4,5)-property must FAIL"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
"$PY" -c "import json,sys; d=json.load(open(sys.argv[1])); A=d['A']; A[1]=A[0]+1; A[2]=A[0]+2; A[3]=A[0]+3; d['A']=A; json.dump(d,open(sys.argv[2],'w'))" "$OBJ" "$TMP/neg.json"
if "$PY" "$CHK" "$TMP/neg.json" --expect-s 12 --expect-n 21 >"$TMP/neg.txt" 2>&1; then echo "negative control NOT rejected"; fail=1; else echo "negative control rejected as expected: $(head -n 1 "$TMP/neg.txt" | cut -c1-110)"; fi
rm -f "$TMP/neg.json" "$TMP/neg.txt"; rmdir "$TMP" 2>/dev/null
echo "methods that ran: branch-and-bound, exhaustive enumeration, ILP $ilp"
if [ "$fail" -eq 0 ]; then
  if [ "$ilp" = "skipped" ]; then echo "ALL CHECKS THAT RAN PASS (ILP skipped: install pulp to run the criterion's second method)"; echo "PASS"; else echo "ALL CHECKS PASS"; fi
else echo "FAIL"; exit 1; fi
