#!/bin/sh
# usage: scripts/verify.sh [ENGINE] [THREADS]      ENGINE = lant4 (default) | lant_cuda | lant_cuda_emu
# Runs ENGINE and the reference (ref/lant_ref = original lant2.c) on the same mask ranges and requires BYTE-IDENTICAL output
# (after WINDOW_OVERFLOW lines have been replaced by reference output). Exit status 0 only if every comparison matches.
D="$(cd "$(dirname "$0")/.." && pwd)"; E=${1:-lant4}; T=${2:-4}; CAP=2000000; bad=0; tmp=$(mktemp -d)
chk(){ W=$1; H=$2; S=$3; N=$4
  "$D/ref/lant_ref" enumr $W $H $S $((S+N)) $CAP > $tmp/ref.txt
  if [ "$E" = lant4 ]; then "$D/$E" $W $H $S $((S+N)) $CAP $T > $tmp/eng.raw; else "$D/$E" $W $H $S $((S+N)) $CAP $T > $tmp/eng.raw; fi
  "$D/scripts/fixup.sh" $W $H $CAP < $tmp/eng.raw > $tmp/eng.txt
  if cmp -s $tmp/ref.txt $tmp/eng.txt; then echo "OK    ${W}x${H} masks $S..$((S+N-1)) ($N lines, $(grep -c WINDOW_OVERFLOW $tmp/eng.raw) overflow fixups)"; else echo "FAIL  ${W}x${H} masks $S..$((S+N-1))"; bad=1; fi; }
chk 4 4 0 65536                      # all of 4x4
chk 5 5 0 32768
chk 5 5 16777216 20000
chk 5 5 33554400 32
chk 5 6 0 20000
chk 5 6 300000000 100000
chk 5 6 1073741000 700
chk 6 6 0 20000
chk 6 6 17179869184 20000
chk 6 6 34359738368 20000
chk 6 6 68719456700 20000
rm -rf $tmp
[ $bad = 0 ] && echo "ALL IDENTICAL" || { echo "SOME COMPARISONS FAILED"; exit 1; }
