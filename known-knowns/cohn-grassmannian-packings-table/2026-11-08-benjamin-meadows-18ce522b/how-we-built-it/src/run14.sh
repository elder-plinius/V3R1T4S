#!/bin/bash
while read m n N to; do
  timeout $((to + 90)) python3 refix6.py $m $n $N $to >> logs/q14_$2.log 2>&1
  echo "done $m-$n-$N" >> logs/q14_$2.prog
done < $1
