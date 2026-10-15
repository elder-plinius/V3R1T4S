#!/bin/sh
# extender lens: the claimed cell's pipeline, applied unchanged to another cell (live leads only, no claim in this run).
#   1. relax_round2.py: continuous relaxation (rank read from the instance) + residual-aware rounding + exact descent
#   2. two quoter2 ILS books from its best, in parallel
#   3. pool_dp2.py chain-DP mix + polish
#   4. rounds2.py: per-period ILS rounds + DP
#   5. checker/pf_eval.py judges the final portfolio (exact rationals)
# usage: sh cell_pipeline.sh RUN_DIR INSTANCE_DIR B LAMBDA INSTANCE_NAME CELL_TAG ROUNDS
# env: PY (venv python), TIMEOUT_BIN (GNU-compatible timeout), WORKERS (per-period workers in the rounds, default 3)
set -u
RUN=$1; INST=$2; B=$3; LAM=$4; NAME=$5; TAG=$6; ROUNDS=$7
Q=$RUN/attempts/quoter/code; L=$RUN/attempts/extender/code; X=$RUN/attempts/crossover/code
OUT=$RUN/attempts/extender/cells/$TAG
mkdir -p "$OUT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
log() { echo "$(date -u +%H:%M:%S) $*" >> "$OUT/pipeline.log"; }
log "start $TAG inst=$INST B=$B lambda=$LAM"
RR_SEED=7 nice -n 15 "$TIMEOUT_BIN" 400 "$PY" -I "$L/relax_round2.py" "$Q" "$INST" "$B" "$LAM" "$NAME" 8 300 "$OUT/rr" > "$OUT/rr.out" 2>&1
log "relax_round2 exit $? : $(grep -E 'QP status|END' "$OUT/rr.log" | tr '\n' ' ')"
[ -f "$OUT/rr_best.sol" ] || { log "no rounding output; stop"; exit 1; }
nice -n 15 "$TIMEOUT_BIN" 330 "$PY" -I "$Q/quoter2.py" "$Q" "$INST" "$B" "$LAM" "$NAME" "$OUT/rr_best.sol" 61 4 300 "$OUT/qa" 80 > "$OUT/qa.out" 2>&1 &
PA=$!
nice -n 15 "$TIMEOUT_BIN" 330 "$PY" -I "$Q/quoter2.py" "$Q" "$INST" "$B" "$LAM" "$NAME" "$OUT/rr_best.sol" 62 8 300 "$OUT/qb" 80 > "$OUT/qb.out" 2>&1 &
PB=$!
log "books pids $PA $PB"
wait $PA $PB
log "books: $(tail -1 "$OUT/qa.log") | $(tail -1 "$OUT/qb.log")"
nice -n 15 "$TIMEOUT_BIN" 300 "$PY" -I "$X/pool_dp2.py" "$Q" "$INST" "$B" "$LAM" "$NAME" "$OUT/dp" 120 "$OUT/rr_best.sol" "$OUT/qa_best.sol" "$OUT/qb_best.sol" > "$OUT/dp.out" 2>&1
log "dp: $(grep -E 'DP mix|polish' "$OUT/dp.out" | tr '\n' ' ')"
"$TIMEOUT_BIN" 7200 "$PY" -I "$L/rounds2.py" "$PY" "$Q" "$X" "$INST" "$B" "$LAM" "$NAME" "$OUT/dp_polished.sol" "$OUT/rounds" "$ROUNDS" 45 "${WORKERS:-3}" > "$OUT/rounds.out" 2>&1
FINAL=$(grep "END best" "$OUT/rounds/rounds.log" | awk '{print $NF}')
log "rounds: $(grep 'END' "$OUT/rounds/rounds.log")"
cp "$FINAL" "$OUT/final.sol"
python3 -I "$RUN/checker/pf_eval.py" "$INST" "$OUT/final.sol" > "$OUT/final_pf_eval.txt" 2>&1
log "pf_eval exit $? : $(tail -2 "$OUT/final_pf_eval.txt" | tr '\n' ' ')"
log "end"
