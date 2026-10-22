#!/bin/sh
_PKG=$(cd "$(dirname "$0")/.." && pwd)
if command -v shasum >/dev/null 2>&1; then _S="shasum -a 256"; else _S="sha256sum"; fi
( cd "$_PKG" && grep "  object/" SHA256SUMS > "${TMPDIR:-/tmp}/objsums.$$" && $_S -c "${TMPDIR:-/tmp}/objsums.$$" >/dev/null 2>&1 ) || { echo "object file sha256 MISMATCH against SHA256SUMS"; echo "FAIL"; exit 1; }
# Standalone check for object/G49_p2.json. Run from this folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/G49_p2.json"
CHK="$HERE/verify-it-yourself/check_gram.py"
REC="$HERE/the-record-we-beat/records.json"
RECNORM=635974777627126753067532288
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
echo "== check_gram.py: Gram conditions, positive definiteness, exact determinant, rational congruence, realised rows"
python3 -I "$CHK" "$OBJ" "$RECNORM" "$REC" | tee "$TMP/out.json"
python3 -I -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); keys=['symmetric','diagonal_is_n','offdiag_congruent_to_n_mod_2','triple_congruences_mod_4','positive_definite','det_by_elimination_equals_bareiss','det_is_perfect_square','equals_stated_value','greater_than_record','det_le_Barba_bound_squared','n_is_perfect_square','Q_Qt_equals_G_exactly','M0_entries_plus_minus_one','M0_Mt0_equals_leading_block_of_G','M0_rows_at_least_n_minus_2']; bad=[k for k in keys if r.get(k) is not True]; print('checker verdict:', 'PASS' if not bad else 'FAIL', '(failed: %s)'%bad if bad else ''); sys.exit(0 if not bad else 1)" "$TMP/out.json" || fail=1
echo "== negative control: G with one off-diagonal pair changed must NOT pass"
python3 -I "$CHK" "$OBJ" "$RECNORM" "$REC" --neg > "$TMP/neg.json"
if python3 -I -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); keys=['triple_congruences_mod_4','Q_Qt_equals_G_exactly','M0_Mt0_equals_leading_block_of_G']; sys.exit(0 if any(r.get(k) is False for k in keys) else 1)" "$TMP/neg.json"; then echo "negative control rejected as expected"; else echo "negative control NOT rejected"; fail=1; fi
rm -f "$TMP/out.json" "$TMP/neg.json"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
