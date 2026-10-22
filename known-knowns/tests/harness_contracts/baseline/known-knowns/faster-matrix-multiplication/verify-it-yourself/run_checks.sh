#!/bin/sh
# Check the seven shipped scheme files (the five records and the superseded 1843 and 2196): Brent equations (exact
# via CRT-bounded modular arithmetic), rank, sha256 against INDEX.csv, and three negative controls.  python3 + numpy.  Exit 0 iff everything passes.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
SECTION=known-knowns/faster-matrix-multiplication
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
python3 "$HERE/verify-it-yourself/mutate.py" "$HERE/schemes/13x14x15_r1677_Q.json" "$TMP" >/dev/null
for m in drop_term bump_coeff swap_vw; do
  if python3 "$HERE/verify-it-yourself/fmmcheck.py" "$TMP/$m.json" > "$TMP/$m.out" 2>&1; then echo "control $m: PASSED (BAD)"; fail=1;
  else echo "control $m: $(tail -1 "$TMP/$m.out" | cut -c1-40)... (expected)"; fi
done
rm -rf "$TMP"
[ $fail = 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECK FAILED"
exit $fail
