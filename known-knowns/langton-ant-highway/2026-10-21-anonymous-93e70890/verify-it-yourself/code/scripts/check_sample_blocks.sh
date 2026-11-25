#!/bin/sh
# Recompute some 1%-sample units with lantx2 and compare with data/sample/sample_units.txt exactly.
# Usage: code/scripts/check_sample_blocks.sh [PASS CHUNK]...   default: 0 0  1 777  2 2439  3 4095  (~1-2 s each)
cd "$(dirname "$0")/../.."; mkdir -p work/s
U=${UNITS:-data/sample/sample_units.txt}
[ $# -eq 0 ] && set -- 0 0 1 777 2 2439 3 4095
bad=0
while [ $# -ge 2 ]; do
  p=$1; c=$2; shift 2
  rm -f work/s/p${p}_c$(printf %04d $c).sum
  # one chunk only: worker index c of 4096 workers
  nice -n 19 bin/lantx2 sample $p $c 4096 work/s
  got=$(cat work/s/p${p}_c$(printf %04d $c).sum)
  exp=$(grep "^pass $p chunk $c " $U)
  if [ "$got" = "$exp" ]; then echo "unit pass $p chunk $c: IDENTICAL ($got)"; else echo "unit pass $p chunk $c: MISMATCH"; echo " got: $got"; echo " exp: $exp"; bad=1; fi
done
[ $bad = 0 ] && echo "SAMPLE BLOCKS: PASS" || { echo "SAMPLE BLOCKS: FAIL"; exit 1; }
