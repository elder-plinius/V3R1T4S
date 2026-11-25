#!/bin/sh
# 5x5 masks [7340032, 8388608) (chunk 07, 2^20 masks): lantx2 vs saved lant.c output. ~30 s single thread.
cd "$(dirname "$0")/../.."; mkdir -p work
nice -n 19 bin/lantx2 range 5 5 7340032 8388608 | awk '{print $1,$2,$3,$4,$5,$6}' > work/5x5c07.lx
zcat ${1:-data/validation/enum5_chunk07_lantc.gz} | awk '{print $1,$2,$3,$4,$5,$7}' > work/5x5c07.ref
if cmp -s work/5x5c07.lx work/5x5c07.ref; then echo "5x5 chunk07: PASS (1048576 lines identical) sha256 $(sha256sum < work/5x5c07.lx | cut -c1-64)"; else echo "5x5 chunk07: FAIL ($(diff work/5x5c07.ref work/5x5c07.lx | grep -c '^>') differing lines)"; exit 1; fi
