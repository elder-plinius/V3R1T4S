#!/bin/sh
# Exactly what this lens ran, in order.  PY is the project venv interpreter; CSV is the released
# file read read-only from run 2026-11-19-2355's data folder (sha256 93588112...a529de).
set -e
PY="$1"; CSV="$2"; HERE=$(dirname "$0"); OUT="$HERE/.."
"$PY" -I "$HERE/boot_mean.py" --selftest "$CSV" three_vs_rest            | tee "$OUT/score_selftest.out"
"$PY" -I "$HERE/fit_sealed.py" "$CSV" "$OUT/result" --config A           | tee "$OUT/fit_A.out"
"$PY" -I "$HERE/fit_sealed.py" "$CSV" "$OUT/result" --config B           | tee "$OUT/fit_B.out"
"$PY" -I "$HERE/make_nan_copy.py" "$CSV" three_vs_rest "$OUT/nan.csv"    | tee "$OUT/leak_test.out"
"$PY" -I "$HERE/fit_sealed.py" "$OUT/nan.csv" "$OUT/nanresult" --config A --tag NAN_ | tee -a "$OUT/leak_test.out"
"$PY" -I "$HERE/fit_sealed.py" "$OUT/nan.csv" "$OUT/nanresult" --config B --tag NAN_ | tee -a "$OUT/leak_test.out"
for f in configA_all_seed1 configA_all_seed2 configA_all_seed3 \
         configB_trainonly_seed1 configB_trainonly_seed2 configB_trainonly_seed3; do
  cmp "$OUT/result/pred_$f.csv" "$OUT/nanresult/pred_NAN_$f.csv" && echo "$f IDENTICAL"
done | tee -a "$OUT/leak_test.out"
"$PY" -I "$HERE/boot_mean.py" "$CSV" three_vs_rest 0.8791 --full 0.8991 --published 0.8995 \
  "$OUT/result/pred_configA_all_seed1.csv" "$OUT/result/pred_configA_all_seed2.csv" \
  "$OUT/result/pred_configA_all_seed3.csv" | tee "$OUT/scores.out"
"$PY" -I "$HERE/boot_mean.py" "$CSV" three_vs_rest 0.8791 --full 0.8991 --published 0.8995 \
  "$OUT/result/pred_configB_trainonly_seed1.csv" "$OUT/result/pred_configB_trainonly_seed2.csv" \
  "$OUT/result/pred_configB_trainonly_seed3.csv" | tee -a "$OUT/scores.out"
