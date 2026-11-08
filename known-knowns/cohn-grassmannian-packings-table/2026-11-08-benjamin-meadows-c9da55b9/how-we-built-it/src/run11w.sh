#!/bin/bash
while read m n N to; do
  timeout $((to + 60)) python3 refix5.py $m $n $N $to >> logs/q11w.log 2>&1
  echo "done $m-$n-$N" >> logs/q11w.prog
done < $1
