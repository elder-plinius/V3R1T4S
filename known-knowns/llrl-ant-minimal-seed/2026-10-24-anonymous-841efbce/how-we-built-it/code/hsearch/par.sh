#!/bin/bash
# checker A split driver: par.sh K TMAX W SPLITD -> ../output/k<K>_T<TMAX>_w<i>.txt ; pids in ../output/pids_k<K>.txt
cd "$(dirname "$0")"; K=$1; T=$2; W=$3; SD=$4; : > ../output/pids_k$K.txt
for w in $(seq 0 $((W-1))); do
  nice -n 19 ./hsearch LLRL $K $T 256241 384 - $W $w $SD > ../output/k${K}_T${T}_w$w.txt 2>../output/k${K}_T${T}_w$w.err &
  echo "$! k=$K w=$w start $(date -u +%FT%TZ)" >> ../output/pids_k$K.txt
done
