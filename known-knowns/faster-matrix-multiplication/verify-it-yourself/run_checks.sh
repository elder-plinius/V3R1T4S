#!/bin/sh
# Check the seven shipped scheme files (the five records and the superseded 1843 and 2196): Brent equations (exact
# via CRT-bounded modular arithmetic), rank, sha256 against INDEX.csv, and three negative controls.  python3 + numpy.  Exit 0 iff everything passes.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
SECTION=known-knowns/faster-matrix-multiplication
CONTRACT="$HERE/../check_harness_contract.py"
[ -f "$CONTRACT" ] || { echo "missing known-knowns/check_harness_contract.py (keep the shared helper with this family)"; exit 2; }
require() {  # input files must be present
  for o in "$@"; do
    [ -f "$HERE/$o" ] || { echo "missing $SECTION/$o"; exit 2; }
  done
}
require schemes/13x14x14_r1558_Q.json schemes/13x14x15_r1677_Q.json schemes/14x14x15_r1716_Q.json \
        schemes/14x15x15_r1842_Q.json schemes/15x16x16_r2180_Q.json \
        schemes/14x15x15_r1843_Q.json schemes/15x16x16_r2196_Q.json
TMP=${TMPDIR:-/tmp}/v3r1t4s-fmm.$$
mkdir -p "$TMP"
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
fail=0
for f in "$HERE"/schemes/*.json; do
  b=$(basename "$f"); echo "== $b"
  exp=$(grep ",schemes/$b," "$HERE/INDEX.csv" | sed 's/.*,//'); got=$($SHA "$f" | cut -d' ' -f1)
  [ "$got" = "$exp" ] && echo "sha256 matches INDEX.csv" || { echo "sha256 MISMATCH ($got)"; fail=1; }
  rank=$(grep ",schemes/$b," "$HERE/INDEX.csv" | cut -d, -f3)
  out=$(python3 "$HERE/verify-it-yourself/fmmcheck.py" "$f") || fail=1
  echo "$out"
  echo "$out" | tail -1 | grep -q "rank_nonzero_terms=$rank " && echo "rank $rank as claimed" || { echo "RANK MISMATCH (claimed $rank)"; fail=1; }
done
echo "== negative controls on the smallest scheme (each must FAIL)"
if python3 "$HERE/verify-it-yourself/mutate.py" "$HERE/schemes/13x14x15_r1677_Q.json" "$TMP" >/dev/null; then
  for m in drop_term bump_coeff swap_vw; do
    if [ ! -s "$TMP/$m.json" ]; then echo "control $m: missing or empty mutant"; fail=1; continue; fi
    rc=0
    python3 "$HERE/verify-it-yourself/fmmcheck.py" "$TMP/$m.json" > "$TMP/$m.out" 2> "$TMP/$m.err" || rc=$?
    if python3 "$CONTRACT" fmm --file "$TMP/$m.json" --stdout "$TMP/$m.out" --stderr "$TMP/$m.err" --exit-code "$rc"; then
      echo "control $m: expected semantic rejection"
    else
      echo "control $m: unexpected result (exit $rc)"; fail=1
    fi
  done
else
  echo "negative-control mutation failed"; fail=1
fi
rm -rf "$TMP"
[ $fail = 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECK FAILED"
exit $fail
