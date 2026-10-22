#!/bin/sh
_PKG=$(cd "$(dirname "$0")/.." && pwd)
if command -v shasum >/dev/null 2>&1; then _S="shasum -a 256"; else _S="sha256sum"; fi
( cd "$_PKG" && grep "  object/" SHA256SUMS > "${TMPDIR:-/tmp}/objsums.$$" && $_S -c "${TMPDIR:-/tmp}/objsums.$$" >/dev/null 2>&1 ) || { echo "object file sha256 MISMATCH against SHA256SUMS"; echo "FAIL"; exit 1; }
# Standalone check for object/p3_sn13_drifted_r0_Q13_2946.txt. Run from this folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/p3_sn13_drifted_r0_Q13_2946.txt"
CHK="$HERE/verify-it-yourself/check_snake.py"
PUB="$HERE/the-record-we-beat/published.json"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
echo "== check_snake.py: two independent induced-snake tests, length, calibration on published records, class comparison"
python3 -I "$CHK" "$OBJ" 13 snake "$PUB" | tee "$TMP/out.json"
python3 -I -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); sym=None; ok=r.get('valid') is True and r.get('length')==2946 and r.get('calibration_all_reproduce') is True and (sym is None or r.get('half_period_symmetric_per_table_page_test') is True); print('checker verdict:', 'PASS' if ok else 'FAIL', '(valid=%s, length=%s, calibration reproduces published lengths=%s, half-period symmetric=%s)'%(r.get('valid'),r.get('length'),r.get('calibration_all_reproduce'),r.get('half_period_symmetric_per_table_page_test'))); sys.exit(0 if ok else 1)" "$TMP/out.json" || fail=1
echo "== negative control: one transition changed must NOT be a valid snake"
python3 -I "$CHK" "$OBJ" 13 snake "$PUB" --neg > "$TMP/neg.json"
if python3 -I -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); sys.exit(0 if r.get('valid') is False else 1)" "$TMP/neg.json"; then echo "negative control rejected as expected (valid false)"; else echo "negative control NOT rejected"; fail=1; fi
rm -f "$TMP/out.json" "$TMP/neg.json"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
