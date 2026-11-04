#!/bin/bash
# mdrive.sh (copy of cube5x8 drive_stagger.sh for mcnf cubes) DEADLINE_EPOCH JOBS STAGGER_S spec... ; like drive.sh, but the first JOBS cube starts are delayed by i*STAGGER_S seconds
# (avoids several cube CNFs being generated/loaded at once; MemAvailable dipped to 0.25 GB on 2026-10-28 15:02). Done cubes are skipped first.
DL=$1;J=$2;ST=$3;shift 3;D=$(cd $(dirname $0);pwd)
i=0
for sp in "$@"; do IFS=: read h w c bm sm <<<"$sp"; for v in $(seq 0 $(( (1<<h)-1 ))); do
  [ -s $D/../output/cubes/h${h}w${w}r${bm:-8}_${sm:-12}/c${c}v${v}.res ] && continue
  d=0; [ $i -lt $J ] && d=$((i*ST)); i=$((i+1))
  echo "$d $h $w $c $v $DL ${bm:-8} ${sm:-12}"; done; done | xargs -P $J -L1 bash -c 'sleep $0; exec '"$D"'/mcube.sh "$@"'
