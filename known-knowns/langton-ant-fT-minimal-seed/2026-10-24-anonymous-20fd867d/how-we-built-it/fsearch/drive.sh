#!/bin/bash
# iterative deepening per k: T bound grows from g(k+1); results to ../output/k<K>.txt ; progress to ../output/drive.log
cd "$(dirname "$0")"; OUT=../output; prev=${2:-0}; k=${1:-10}; kmin=${3:-1}
while [ $k -ge $kmin ]; do
  T=$prev
  while :; do
    echo "$(date -u +%FT%TZ) k=$k try T<=$T" >> $OUT/drive.log
    ulimit -t 1800; nice -n 19 ./fsearch $k $T > $OUT/k$k.try 2>>$OUT/drive.log
    if grep -q "best_t=" $OUT/k$k.try; then mv $OUT/k$k.try $OUT/k$k.txt; grep RESULT $OUT/k$k.txt >> $OUT/drive.log; prev=$(grep -o 'best_t=[0-9]*' $OUT/k$k.txt | cut -d= -f2); break; fi
    grep RESULT $OUT/k$k.try >> $OUT/drive.log || { echo "k=$k T=$T no RESULT (cpu cap?)" >> $OUT/drive.log; exit 1; }
    T=$(( T + (T/4>16 ? T/4 : 16) ))
  done
  k=$((k-1))
done
