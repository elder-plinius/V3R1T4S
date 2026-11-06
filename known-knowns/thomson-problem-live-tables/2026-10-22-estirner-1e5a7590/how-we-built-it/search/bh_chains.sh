#!/bin/bash
# Greedy seeded basin hopping for Thomson N=743 on the GPU (one job at a time).
# Each chain starts from the CCD Riesz posted file; each iteration = 12 rounds x 280 replicas of
# "relocate each point with prob PK, jitter the rest by SIG*spacing, 6000 FP32 BB steps, FP64 energy".
# The iteration's best replaces the chain seed only if it is lower (greedy acceptance).
# Usage: bh_chains.sh <seedfile> <outdir> ; output: <outdir>/chains.log, <outdir>/<chain>_best.xyz
set -u
SEEDFILE=$1; OUT=$2; BIN=$(dirname "$0")/thomson_bb; N=743; ITS=${ITS:-10}
mkdir -p "$OUT"
run_chain(){ name=$1; pk=$2; sig=$3; base=$4
  cp "$SEEDFILE" "$OUT/${name}_cur.xyz"; cur=1e300
  for it in $(seq 1 $ITS); do
    s=$((base+it))
    line=$(SEED="$OUT/${name}_cur.xyz" PK=$pk SIG=$sig "$BIN" $N 280 6000 12 $s "$OUT/${name}_it" | sed -n 2p)
    e=$(echo "$line" | awk '{print $5}')
    acc=no
    if awk -v a="$e" -v b="$cur" 'BEGIN{exit !(a<b)}'; then acc=yes; cur=$e; cp "$OUT/${name}_it_best.xyz" "$OUT/${name}_cur.xyz"; cp "$OUT/${name}_it_best.xyz" "$OUT/${name}_best.xyz"; fi
    echo "$(date -u +%FT%TZ) chain=$name pk=$pk sig=$sig it=$it rngseed=$s iter_best=$e accepted=$acc chain_best=$cur" | tee -a "$OUT/chains.log"
  done
}
run_chain A 0.005 0.02 2021000
run_chain B 0.010 0.02 2022000
run_chain C 0.003 0.05 2023000
echo "$(date -u +%FT%TZ) done" >> "$OUT/chains.log"
