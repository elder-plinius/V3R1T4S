#!/bin/sh
# Resumable 1% sample job: NW workers, each loops passes 0..3 over chunks c = w, w+NW, ... (unit = pass x chunk).
# Stop: touch output/s/STOP (workers exit after the current unit). Restart: rm output/s/STOP; rerun this script.
# Usage: code/run_sample.sh NW
NW=${1:-4}
X=../indep-checker/code/lantx
OUT=output/s; mkdir -p $OUT
echo "start $(date -u +%FT%TZ) pid $$ NW $NW" >> output/run_sample.log
for w in $(seq 0 $((NW-1))); do
  ( for p in 0 1 2 3; do [ -f $OUT/STOP ] && break; nice -n 19 $X sample $p $w $NW $OUT; done ) &
  echo "worker $w subshell pid $!" >> output/run_sample.log
done
wait
echo "end $(date -u +%FT%TZ)" >> output/run_sample.log
