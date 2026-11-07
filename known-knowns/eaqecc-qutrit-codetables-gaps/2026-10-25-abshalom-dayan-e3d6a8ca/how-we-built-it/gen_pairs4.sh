#!/bin/sh
# Degree-4-place Construction X pairs C1 = L(aQ + bP_inf) (degree 16) > C2 = L((a-1)Q + bP_inf) (degree 12), for the
# four orbit representatives 0, 18, 36, 54 and a = 1..6 (b = 16 - 4a); then exact d of C1 and C2 by bz9.
D="$(cd "$(dirname "$0")/.." && pwd)"; cd "$D"
date -u +%H:%M:%SZ
for q in 0 18 36 54; do for a in 1 2 3 4 5 6; do b=$((16 - 4 * a))
  nice -n 10 python3 code/deg4.py pair $q $a $b data/X16d4_q${q}_a$a.xin || echo "FAILED q=$q a=$a"
  for c in C1 C2; do printf "q=%s a=%s %s: " $q $a $c; nice -n 10 perl -e 'alarm shift; exec @ARGV' 600 code/bz9 < data/X16d4_q${q}_a${a}_$c.code | cut -c1-60; done
done; done
date -u +%H:%M:%SZ
