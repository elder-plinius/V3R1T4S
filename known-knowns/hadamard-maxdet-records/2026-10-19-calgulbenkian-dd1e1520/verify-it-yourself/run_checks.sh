#!/bin/sh
_PKG=$(cd "$(dirname "$0")/.." && pwd)
if command -v shasum >/dev/null 2>&1; then _S="shasum -a 256"; else _S="sha256sum"; fi
( cd "$_PKG" && grep "  object/" SHA256SUMS > "${TMPDIR:-/tmp}/objsums.$$" && $_S -c "${TMPDIR:-/tmp}/objsums.$$" >/dev/null 2>&1 ) || { echo "object file sha256 MISMATCH against SHA256SUMS"; echo "FAIL"; exit 1; }
# Standalone check for object/M105_403757419044975201959422423846994970270257858463738130848861743562151165952.txt. Run from this folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/M105_403757419044975201959422423846994970270257858463738130848861743562151165952.txt"
CHK="$HERE/verify-it-yourself/check_det.py"
REC="$HERE/the-record-we-beat/records.json"
EXPECT=403757419044975201959422423846994970270257858463738130848861743562151165952
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
echo "== check_det.py: three exact determinant computations, +-1 entries, divisibility, Barba bound, comparison with records"
python3 -I "$CHK" "$OBJ" "$EXPECT" "$REC" | tee "$TMP/out.json"
python3 -I -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); ok=r['square'] and r['entries_plus_minus_one'] and r['three_methods_agree_on_abs_det'] and r['abs_det_divisible_by_2^(n-1)'] and r['D_equals_claimed'] and r['abs_det_le_Barba_bound'] and all(c['D_greater'] for c in r['comparison_with_records']); print('checker verdict:', 'PASS' if ok else 'FAIL', '(D=%s, larger than all listed records=%s)'%(r['D_normalised'], all(c['D_greater'] for c in r['comparison_with_records']))); sys.exit(0 if ok else 1)" "$TMP/out.json" || fail=1
echo "== negative control: one entry negated must NOT give the claimed determinant"
python3 -I "$CHK" "$OBJ" "$EXPECT" "$REC" --neg > "$TMP/neg.json"
if python3 -I -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); sys.exit(0 if r.get('D_equals_claimed') is False else 1)" "$TMP/neg.json"; then echo "negative control rejected as expected (determinant differs)"; else echo "negative control NOT rejected"; fail=1; fi
rm -f "$TMP/out.json" "$TMP/neg.json"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
