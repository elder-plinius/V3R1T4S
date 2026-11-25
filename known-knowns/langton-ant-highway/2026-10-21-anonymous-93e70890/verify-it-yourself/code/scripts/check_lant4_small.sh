#!/bin/sh
# Per-mask comparison lant4 (the user's engine, built from code/lant4pkg) vs lantx2 on a 6x6 range. Default: 2^16 masks around the global max. ~5 s.
cd "$(dirname "$0")/../.."; mkdir -p work
A=${1:-40920803348}; B=${2:-40920868884}
nice -n 19 bin/lant4 6 6 $A $B 2000000 1 | awk '{print $1,$2,$3,$4,$5,$7}' > work/l4.txt
nice -n 19 bin/lantx2 range 6 6 $A $B | awk '{print $1,$2,$3,$4,$5,$6}' > work/lx.txt
if cmp -s work/l4.txt work/lx.txt; then echo "lant4 vs lantx2 [$A,$B): PASS ($(wc -l < work/lx.txt) lines identical)"; else echo "lant4 vs lantx2: FAIL ($(diff work/l4.txt work/lx.txt | grep -c '^>') differing)"; exit 1; fi
