#!/bin/bash
# usage: drive2.sh "k T" ...   runs 5 workers per k, nice 19, CPU limit 450 s per worker
cd "$(dirname "$0")"
for kt in "$@"; do set -- $kt; k=$1; T=$2
  s=$(date +%s)
  for w in 0 1 2 3 4; do ( ulimit -t 450; nice -n 19 ./lcone $k $T 5 $w > logs/k${k}_w$w.out 2> logs/k${k}_w$w.err; echo "exit=$?" >> logs/k${k}_w$w.err ) & done
  wait
  echo "k=$k T=$T wall=$(( $(date +%s)-s ))s" >> logs/drive2.log
done
