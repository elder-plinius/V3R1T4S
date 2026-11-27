#!/bin/sh
# GPU job 7 (<= 300 s): from the gap-0 (tie) point of 64_6371 (job 6): mf4 continuation (keep weight 1.0), exact
# single-pixel polish, mf4 continuation (keep weight 0.3).
L=search-engineer
PY=python
echo start $(date -u)
$PY -I $L/code/selfcheck.py > $L/out/job7_selfcheck.log 2>&1 || { echo SELFCHECK FAILED; exit 3; }
START_X=$L/out/mf4_x_64_6371_gap0.npy KEEPW=1.0 $PY -I $L/code/mf4.py 64 6371 110 9 4 1.0 20 0 2 > $L/out/mf4_64_6371_e1_from_k1.log 2>&1; echo mf4k1 $(date -u)
$PY -I $L/code/polish.py 64 6371 $L/out/mf4_x_64_6371_gap0.npy 55 9 0 > $L/out/polish_64_6371.log 2>&1; echo polish $(date -u)
START_X=$L/out/mf4_x_64_6371_gap0.npy KEEPW=0.3 $PY -I $L/code/mf4.py 64 6371 75 9 3 0.5 20 0 3 > $L/out/mf4_64_6371_e1_from_k03.log 2>&1; echo mf4k03 $(date -u)
