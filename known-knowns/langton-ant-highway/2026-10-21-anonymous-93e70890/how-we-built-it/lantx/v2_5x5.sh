#!/bin/sh
# Validate lantx on all 2^25 5x5 masks against run 2026-10-16-0705 enum5 (lant.c), 32 chunks of 2^20, 5 workers.
# Usage: code/v2_5x5.sh  (resumable: a chunk is done when output/v2_5x5/cNN.res exists)
E5=../../../2026-10-16-0705/attempts/small-data/output/enum5
OUT=output/v2_5x5; mkdir -p $OUT
worker() {
  w=$1
  c=$w
  while [ $c -lt 32 ]; do
    cc=$(printf %02d $c)
    if [ ! -f $OUT/c$cc.res ]; then
      a=$((c*1048576)); b=$((a+1048576))
      nice -n 19 ./code/lantx range 5 5 $a $b | awk '{print $1,$2,$3,$4,$5,$6}' > $OUT/c$cc.lx
      zcat $E5/chunk_$cc.gz | awk '{print $1,$2,$3,$4,$5,$7}' > $OUT/c$cc.ref
      if cmp -s $OUT/c$cc.lx $OUT/c$cc.ref; then r=IDENTICAL; else r="DIFF $(diff $OUT/c$cc.ref $OUT/c$cc.lx | grep -c '^>')"; fi
      echo "chunk $cc lines $(wc -l < $OUT/c$cc.lx) ncap $(grep -c ' CAP$' $OUT/c$cc.lx) $r sha256 $(sha256sum < $OUT/c$cc.lx | cut -c1-64)" > $OUT/c$cc.res
      [ "$r" = IDENTICAL ] && rm -f $OUT/c$cc.lx $OUT/c$cc.ref
    fi
    c=$((c+5))
  done
}
for w in 0 1 2 3 4; do worker $w & done
wait
cat $OUT/c*.res
