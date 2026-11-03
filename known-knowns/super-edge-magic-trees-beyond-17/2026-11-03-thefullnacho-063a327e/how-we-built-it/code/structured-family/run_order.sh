#!/bin/bash
# usage: run_order.sh n shards ; alpha route (cap 300, 2000 attempts), then sem-direct-free residue file
n=$1; S=$2; D=$(dirname "$0")/..; T=$D/../../trees/trees_n$n.txt
for ((i=0;i<S;i++)); do awk -v S=$S -v i=$i 'NR%S==i' $T | nice -n 10 timeout 2400 $D/code/alpha_sem 300 ${ATT:-2000} $((i+11)) > $D/part_n${n}_$i.txt & done
wait
cat $D/part_n${n}_*.txt > $D/alpha_n$n.txt && rm -f $D/part_n${n}_*.txt
echo "n=$n done $(date -u +%T) lines $(wc -l < $D/alpha_n$n.txt) noalpha $(grep -c NOALPHA $D/alpha_n$n.txt)"
