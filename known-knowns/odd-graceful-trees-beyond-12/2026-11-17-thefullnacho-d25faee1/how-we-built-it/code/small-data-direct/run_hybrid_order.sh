#!/bin/sh
# usage: run_hybrid_order.sh n K
# Deterministic og_direct with a 1e5-node cap on K shards, then og_restart on the leftovers.
# Run from this folder after: cc -O2 -o og_direct og_direct.c && cc -O2 -o og_restart og_restart.c
# Needs python3 and networkx (dump_trees.py). The searches are randomised in the
# restart phase, so a rebuild gives different, equally valid labelings.
set -eu
n=$1
K=$2
[ -s trees_n$n.txt ] || python3 dump_trees.py $n > trees_n$n.txt
rm -f trees_n${n}_h*
split -n l/$K -d trees_n$n.txt trees_n${n}_h
for f in trees_n${n}_h*; do
  timeout 1800 nice -n 10 ./og_direct 100000 < "$f" > first_${f#trees_}.txt &
done
wait
cat first_n${n}_h*.txt > first_n$n.txt
# leftover trees have an empty label field
awk -F';' 'NF>=3 && $3=="" {print $1 ";" $2}' first_n$n.txt > left_n$n.txt
timeout 1200 nice -n 10 ./og_restart 100000 200 $n < left_n$n.txt > second_n$n.txt
python3 merge_hybrid.py first_n$n.txt second_n$n.txt cert_n$n.txt
echo "n=$n trees=$(wc -l < trees_n$n.txt) certlines=$(wc -l < cert_n$n.txt) left_after_first=$(wc -l < left_n$n.txt) unlabeled=$(grep -c UNLABELED cert_n$n.txt || true)"
