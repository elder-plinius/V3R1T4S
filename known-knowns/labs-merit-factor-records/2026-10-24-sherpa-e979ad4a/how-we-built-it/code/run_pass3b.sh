#!/bin/bash
# Pass 3 per PREREG.v5.md: L = 401 until 20:38 UTC (in the run it first waited for the previous GPU job to finish).
cd "$(dirname "$0")/../../../code/gpu" || exit 1
OUT=../../attempts/gpu-skew-saw/output3; mkdir -p $OUT
NOW=$(date -u +%s); STOP=$(date -u -d "$(date -u +%F) 20:38:00" +%s); SECS=$((STOP - NOW))
echo "== L=401 start $(date -u +%FT%TZ) seconds $SECS"
if [ $SECS -lt 120 ]; then echo "not enough time left, skipped"; exit 0; fi
timeout $((SECS + 120)) ${PYTHON:-python3} search.py --L 401 --seconds $SECS --mode saw --walk 4000 --prandom 0.5 --pcross 0.9 \
  --heads auto --r1 25-29 --r2 12-14 --r3 9-11 --exploit 0.7 --top-arms 6 --seed 3401 --out $OUT/L401.jsonl > $OUT/L401.log 2>&1
echo "   exit $? $(tail -1 $OUT/L401.log | cut -c1-160)"
echo "PASS3 DONE $(date -u +%FT%TZ)"
