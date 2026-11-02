#!/bin/bash
# usage: driver.sh outdir worker_id nworkers  (reads jobs file: "N seed seconds" per line)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$(dirname "$0")"
out=$1; w=$2; nw=$3; jobs=$4
awk -v w=$w -v nw=$nw 'NR%nw==w' $jobs | while read n s t; do
  python3 mbh2.py $n $s $t $out/npy >> $out/results.txt 2>> $out/err_$w.txt
done
