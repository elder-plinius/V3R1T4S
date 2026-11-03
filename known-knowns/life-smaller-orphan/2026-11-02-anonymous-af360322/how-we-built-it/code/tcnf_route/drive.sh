#!/bin/bash
# drive.sh DEADLINE_EPOCH JOBS spec... ; spec = h:w:c[:BM:SM]  -> runs all 32 (2^h) cubes per spec, skipping done ones, JOBS in parallel
DL=$1;J=$2;shift 2;D=$(dirname $0)
for sp in "$@"; do IFS=: read h w c bm sm <<<"$sp"; for v in $(seq 0 $(( (1<<h)-1 ))); do echo "$h $w $c $v $DL ${bm:-8} ${sm:-12}"; done; done | xargs -P $J -L1 $D/cube.sh
