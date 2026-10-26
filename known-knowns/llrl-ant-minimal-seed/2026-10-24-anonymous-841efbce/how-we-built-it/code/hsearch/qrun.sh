#!/bin/bash
# piece-queue runner for checker A: qrun.sh K TMAX NPIECES SPLITD ; claims pieces atomically via mkdir;
# output ../output/q_k<K>_T<T>/p<i>.txt (renamed from .tmp only when the piece finishes)
cd "$(dirname "$0")"; K=$1; T=$2; N=$3; SD=$4; D=../output/q_k${K}_T${T}; mkdir -p $D/claim
for i in $(seq 0 $((N-1))); do
  mkdir $D/claim/$i 2>/dev/null || continue
  nice -n 19 ./hsearch LLRL $K $T 256241 384 - $N $i $SD > $D/p$i.tmp 2>$D/p$i.err && mv $D/p$i.tmp $D/p$i.txt
done
