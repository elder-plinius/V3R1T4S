#!/bin/bash
# piece-queue runner for checker B: runner.sh K T NPIECES SPLITD ; claims pieces atomically via mkdir, output ../output/k<K>_T<T>/p<i>.txt
cd "$(dirname "$0")"; K=$1; T=$2; N=$3; SD=$4; D=../output/k${K}_T${T}; mkdir -p $D/claim
for i in $(seq 0 $((N-1))); do
  mkdir $D/claim/$i 2>/dev/null || continue
  LCB_SPLITD=$SD nice -n 19 ./lcb_fast LLRL $K $T $N $i > $D/p$i.tmp 2>$D/p$i.err && mv $D/p$i.tmp $D/p$i.txt
done
