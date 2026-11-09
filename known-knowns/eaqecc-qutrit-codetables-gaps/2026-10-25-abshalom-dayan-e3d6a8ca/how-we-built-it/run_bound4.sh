#!/bin/sh
# Exact maximum Hermitian hull over every Construction X code [35,14,16]_9 of the 24 degree-4-place pairs
# (C1 = L(aQ + (16-4a)P_inf) [28,14,12] > C2 = L((a-1)Q + (16-4a)P_inf) [28,10,16], tail [7,4]), all 2^27 head sign
# patterns each, exact computation for patterns with bound >= 7 (hull 7 is what beats a listed cell). One process at
# a time, nice 10, capped at 3600 s each; each child's PID goes to out/pids.txt.
D="$(cd "$(dirname "$0")/.." && pwd)"; cd "$D"
for q in 0 18 36 54; do for a in 1 2 3 4 5 6; do f=X16d4_q${q}_a$a
  nice -n 10 perl -e 'alarm shift; exec @ARGV' 3600 code/hullbound4 bound 7 7 < data/$f.xin > out/bound4_$f.txt 2>&1 &
  echo "hullbound4 bound $f pid $! started $(date -u +%H:%M:%SZ)" >> out/pids.txt; wait $!
  echo "$f exit=$? $(date -u +%H:%M:%SZ) $(grep RESULT out/bound4_$f.txt)" >> out/run_bound4.log
done; done
echo "done $(date -u +%H:%M:%SZ)" >> out/run_bound4.log
