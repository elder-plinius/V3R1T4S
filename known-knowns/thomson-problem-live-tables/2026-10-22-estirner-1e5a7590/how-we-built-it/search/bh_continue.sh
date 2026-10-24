#!/bin/bash
# Continuation of bh_chains.sh: chains D and E restart from a given seed file (the best of chains A-C),
# same engine, same greedy acceptance, new RNG seeds. Usage: bh_continue.sh <seedfile> <outdir>
set -u
SEEDFILE=$1; OUT=$2; BIN=$(dirname "$0")/thomson_bb; N=743; ITS=${ITS:-15}
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
run_chain D 0.010 0.02 2024000
run_chain E 0.005 0.02 2025000
echo "$(date -u +%FT%TZ) continuation done" >> "$OUT/chains.log"
