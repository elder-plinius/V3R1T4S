#!/bin/bash
# ladder: for n, start at m0, warm-start each m from the previous solution (+1 random vector); stop at first failure
cd "$(dirname "$0")/../out"; n=$1; m=$2; secs=$3; prev=""
while :; do ../code/mc2 $n $m $secs $((n*1000+m)) lad_${n}_${m} $prev >/dev/null || break; echo "n=$n m=$m FOUND $(date -u +%T)"; prev=lad_${n}_${m}; m=$((m+1)); done
echo "n=$n stop at m=$m"
