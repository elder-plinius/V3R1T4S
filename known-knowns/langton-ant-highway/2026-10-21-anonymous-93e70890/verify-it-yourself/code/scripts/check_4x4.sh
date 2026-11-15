#!/bin/sh
# All 65,536 4x4 masks: lantx2 vs saved lant2 output (columns mask tcap vx vy dir status). ~2 s.
cd "$(dirname "$0")/../.."; mkdir -p work
nice -n 19 bin/lantx2 range 4 4 0 65536 | awk '{print $1,$2,$3,$4,$5,$6}' > work/4x4.lx
awk '{print $1,$2,$3,$4,$5,$7}' ${1:-data/validation/enum4_lant2.txt} > work/4x4.ref
if cmp -s work/4x4.lx work/4x4.ref; then echo "4x4: PASS (65536 lines identical)"; else echo "4x4: FAIL ($(diff work/4x4.ref work/4x4.lx | grep -c '^>') differing lines)"; exit 1; fi
