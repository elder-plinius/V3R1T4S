#!/bin/sh
# Program A (neighbours-only totalistic CA, A357953) on all connected graphs with 9 nodes, 8 geng residue classes.
# Run from this folder after: gcc -O2 -o totA totA.c      GENG defaults to geng on PATH (nauty 2.8.8 was used).
G=${GENG:-geng}
mkdir -p out
for r in 0 1 2 3 4 5 6 7; do
  ( "$G" -cq 9 $r/8 | ./totA > out/A_n9_part$r.txt; echo "exit $?" >> out/A_n9_part$r.txt ) &
done
wait
