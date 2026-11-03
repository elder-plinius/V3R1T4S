#!/bin/bash
# usage: run_order.sh n shards ; shards a tree file round-robin, runs sem_direct (cap 300) under nice + timeout
n=$1; S=$2; D=$(dirname "$0")/..; T=$D/../../trees/trees_n$n.txt
for ((i=0;i<S;i++)); do awk -v S=$S -v i=$i 'NR%S==i' $T | nice -n 10 timeout 2400 $D/code/sem_direct 300 1000000 $((i+1)) > $D/part_n${n}_$i.txt & done
wait
cat $D/part_n${n}_*.txt > $D/cert_n$n.txt && rm -f $D/part_n${n}_*.txt
echo "n=$n done $(date -u +%T) lines $(wc -l < $D/cert_n$n.txt) unlabeled $(grep -c UNLABELED $D/cert_n$n.txt)"
