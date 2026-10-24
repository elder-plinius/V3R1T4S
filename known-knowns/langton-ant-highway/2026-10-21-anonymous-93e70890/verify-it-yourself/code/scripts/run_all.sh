#!/bin/sh
# Everything except the full-chunk rerun, ~5 min single-threaded: build, summaries, 4x4, 5x5 slice, hard cases,
# lant4 vs lantx2 small range, 4 sample units, sample summary (with Python selection recount), tamper tests.
cd "$(dirname "$0")/../.."; mkdir -p work; fail=0
for c in "code/scripts/build.sh" "python3 code/scripts/check_summaries.py" "code/scripts/check_4x4.sh" "code/scripts/check_5x5_slice.sh" \
         "code/scripts/check_hard.sh" "code/scripts/check_lant4_small.sh" "code/scripts/check_sample_blocks.sh" \
         "python3 code/scripts/check_sample_summary.py" "code/scripts/tamper_tests.sh"; do
  echo "== $c"; s=$(date +%s); timeout 450 $c || fail=1; echo "   ($(( $(date +%s) - s )) s)"
done
[ $fail = 0 ] && echo "RUN_ALL: PASS" || { echo "RUN_ALL: FAIL"; exit 1; }
