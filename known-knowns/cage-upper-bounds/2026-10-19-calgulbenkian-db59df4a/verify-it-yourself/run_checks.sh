#!/bin/sh
_PKG=$(cd "$(dirname "$0")/.." && pwd)
if command -v shasum >/dev/null 2>&1; then _S="shasum -a 256"; else _S="sha256sum"; fi
( cd "$_PKG" && grep "  object/" SHA256SUMS > "${TMPDIR:-/tmp}/objsums.$$" && $_S -c "${TMPDIR:-/tmp}/objsums.$$" >/dev/null 2>&1 ) || { echo "object file sha256 MISMATCH against SHA256SUMS"; echo "FAIL"; exit 1; }
# Standalone check for object/mixed_z2_r9_g6_N294.json. Run from this folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/mixed_z2_r9_g6_N294.json"
CHK="$HERE/verify-it-yourself/check_mixed.py"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
echo "== check_mixed.py: regularity, rebuild from generators, girth under both cycle conventions"
python3 -I "$CHK" "$OBJ" | tee "$TMP/out.json"
python3 -I -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); ok=r['VALID_under_forward_arc_convention'] is True and r['N']==294 and r['N']<320; print('checker verdict:', 'PASS' if ok else 'FAIL', '(valid under the forward-arc convention=%s, N=%s, table upper bound 320; direction-blind girth=%s)'%(r['VALID_under_forward_arc_convention'], r['N'], r['girth_direction_blind_convention'])); sys.exit(0 if ok else 1)" "$TMP/out.json" || fail=1
echo "== negative control: one arc head changed must NOT be valid"
python3 -I "$CHK" "$OBJ" --neg > "$TMP/neg.json"
if python3 -I -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); sys.exit(0 if r.get('VALID_under_forward_arc_convention') is False else 1)" "$TMP/neg.json"; then echo "negative control rejected as expected"; else echo "negative control NOT rejected"; fail=1; fi
rm -f "$TMP/out.json" "$TMP/neg.json"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
