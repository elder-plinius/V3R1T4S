#!/bin/bash
# Usage: run_chunks.sh K J ; worker K of J runs seg699 on chunks [a, a+10^6-1], a = (J*m+K)*10^6 for a < 10^9,
# skipping chunks already finished. A chunk counts only when renamed from .part to .txt (finished, uncapped).
K=$1; J=$2; C=1000000
for ((a=K*C; a<1000000000; a+=J*C)); do b=$((a + C - 1))
  [ -f chunks/s_${a}_${b}.txt ] && continue
  ./code/seg699 $a $b 0 > chunks/s_${a}_${b}.part && mv chunks/s_${a}_${b}.part chunks/s_${a}_${b}.txt
done
