#!/bin/bash
# Production run: certificates for connected cubic graphs, orders 4..22. Slices via geng res/mod.
set -e
B=${NAUTY_BIN:?set NAUTY_BIN to the folder holding geng}
C=$(dirname $0)
R=${OUT:-./regen_result}   # never point this at claim/result
mkdir -p $R/slices
for n in 4 6 8 10 12 14 16 18; do
  $B/geng -cq -d3 -D3 $n | $C/glab -c > $R/cert_$n.txt 2> $R/glab_$n.log
done
for n in 20 22; do
  M=64
  seq 0 $((M-1)) | xargs -P 6 -I{} sh -c "$B/geng -cq -d3 -D3 $n {}/$M | $C/glab -c -s {} > $R/slices/c${n}_{}.txt 2> $R/slices/c${n}_{}.log"
  : > $R/cert_$n.txt; : > $R/glab_$n.log
  for i in $(seq 0 $((M-1))); do cat $R/slices/c${n}_$i.txt >> $R/cert_$n.txt; cat $R/slices/c${n}_$i.log >> $R/glab_$n.log; done
done
echo DONE
