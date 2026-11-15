#!/bin/sh
# Per-mask comparison of the user's engine (box copy of lant4, 1 thread) and lantx2 on a 6x6 range.
# Usage: code/cmp_lant4.sh START END TAG
L4=/workspace/langton6x6-package/lant4
X=../indep-checker/code/lantx2
mkdir -p output/lant4cmp
nice -n 19 $L4 6 6 $1 $2 2000000 1 | awk '{print $1,$2,$3,$4,$5,$7}' > output/lant4cmp/$3.l4
nice -n 19 $X range 6 6 $1 $2 | awk '{print $1,$2,$3,$4,$5,$6}' > output/lant4cmp/$3.lx
n=$(wc -l < output/lant4cmp/$3.lx); c=$(grep -c ' CAP$' output/lant4cmp/$3.lx)
if cmp -s output/lant4cmp/$3.l4 output/lant4cmp/$3.lx; then r=IDENTICAL; else r="DIFF $(diff output/lant4cmp/$3.l4 output/lant4cmp/$3.lx | grep -c '^>')"; fi
echo "range [$1,$2) $3 lines $n lantx2_CAP $c lant4_vs_lantx2 $r sha256_lx $(sha256sum < output/lant4cmp/$3.lx | cut -c1-64)" | tee -a output/lant4cmp/summary.txt
