#!/bin/sh
# Check the two shipped VNN-COMP 2026 witnesses: sha256 against INDEX.csv, the standalone checker (downloads the
# official ONNX model and properties at a pinned commit, sha256-checked), and three negative controls per instance.
# python3 with numpy and onnxruntime (onnx optional).  Network access to raw.githubusercontent.com.
# Optional: OFFICIAL=1 also runs the competition's own validator (needs `pip install vnnlib==1.0.2`).
# Exit 0 iff everything passes.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
SECTION=known-knowns/vnncomp-2026-unsolved-instances
PY=${PYTHON:-python3}
for o in witnesses/model_30_idx_1703_eps_1/witness_plain.txt witnesses/model_30_idx_1703_eps_1/witness_v2.txt \
         witnesses/model_30_idx_178_eps_1/witness_plain.txt witnesses/model_30_idx_178_eps_1/witness_v2.txt; do
  [ -f "$HERE/$o" ] || { echo "missing $SECTION/$o"; exit 2; }
done
TMP=${TMPDIR:-/tmp}/v3r1t4s-vnn.$$
mkdir -p "$TMP"
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
fail=0
echo "== sha256 of the witnesses against INDEX.csv"
for f in witnesses/model_30_idx_1703_eps_1/witness_plain.txt witnesses/model_30_idx_1703_eps_1/witness_v2.txt \
         witnesses/model_30_idx_178_eps_1/witness_plain.txt witnesses/model_30_idx_178_eps_1/witness_v2.txt; do
  got=$($SHA "$HERE/$f" | cut -d' ' -f1)
  grep -q "$got" "$HERE/INDEX.csv" && echo "$f: matches INDEX.csv" || { echo "$f: sha256 NOT in INDEX.csv ($got)"; fail=1; }
done
echo "== standalone checker"
$PY "$HERE/verify-it-yourself/vnncheck.py" --cache "$TMP/cache" || fail=1
echo "== negative controls (each must FAIL)"
for i in 1703 178; do
  $PY "$HERE/verify-it-yourself/mutate.py" \
      "$TMP/cache/benchmarks/traffic_signs_recognition_2023/2.0/vnnlib/model_30_idx_${i}_eps_1.00000.vnnlib.gz" \
      "$HERE/witnesses/model_30_idx_${i}_eps_1/witness_plain.txt" "$TMP/mut$i" >/dev/null || fail=1
  for m in on_bound outside centre; do
    if $PY "$HERE/verify-it-yourself/vnncheck.py" --cache "$TMP/cache" --instance $i --witness "$TMP/mut$i/$m.txt" > "$TMP/$i.$m.out" 2>&1; then
      echo "control idx_$i $m: PASSED (BAD)"; fail=1
    else
      echo "control idx_$i $m: $(grep -E 'strict:|zero tolerance' "$TMP/$i.$m.out" | grep -c False) failed check(s), $(tail -1 "$TMP/$i.$m.out" | cut -c1-13) (expected)"
    fi
  done
done
if [ "${OFFICIAL:-0}" = 1 ]; then
  echo "== official validator (SCORING/counterexamples_v2.py, unmodified)"
  $PY "$HERE/verify-it-yourself/official_validate.py" --cache "$TMP/cache" || fail=1
fi
rm -rf "$TMP"
[ $fail = 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECK FAILED"
exit $fail
