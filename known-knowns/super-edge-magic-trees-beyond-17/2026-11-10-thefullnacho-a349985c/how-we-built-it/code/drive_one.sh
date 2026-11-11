#!/bin/bash
# drive_one.sh n M : one order per PREREG addendum 1. Search (DEEP_SEC=3600), residue retry (cap 2000, 1e9 attempts,
# 16 parts, 3 h each), merge, then both checkers on the merged certificate. Writes runs/n<n>/VERDICT.
H=${V3_HOME:?}; IC=${INDEP_CHECK:?}; n=$1; M=$2; R=$H/runs/n$n; B=$H/bin
[ -f $H/STOP ] && { echo "STOP present"; exit 0; }
DEEP_SEC=3600 $B/run.sh $n $M ${P:-16} >> $H/runs/n$n.log 2>&1
[ -f $H/STOP ] && { echo "STOP present after search"; exit 0; }
cd $R || exit 1
if [ -s RESIDUE_n$n.txt ]; then
  mkdir -p retry && cd retry && sed 's/;;.*//' ../RESIDUE_n$n.txt > residue_all.txt && split -n l/16 -d residue_all.txt part_
  for f in part_*; do p=${f#part_}; ( timeout 10800 stdbuf -oL $B/sem_direct 2000 1000000000 $((10#$p * 7919 + 17)) < $f > out_$f.txt ) & done; wait
  cat out_part_*.txt > retry_labelled.txt; cd ..
  left=$(grep -c ';;UNLABELED' retry/retry_labelled.txt)
  if [ "$left" -ne 0 ]; then echo "n=$n: $left trees unlabelled after retry; stopping for a human $(date)" | tee VERDICT; exit 1; fi
  (xz -dc cert_n$n.txt.xz; grep -v ';;UNLABELED' retry/retry_labelled.txt) | xz -T8 -6 > cert_n${n}_merged.txt.xz
else
  cp cert_n$n.txt.xz cert_n${n}_merged.txt.xz
fi
sha256sum cert_n${n}_merged.txt.xz > cert_n${n}_merged.txt.xz.sha256
( xz -dc cert_n${n}_merged.txt.xz | /usr/bin/time -f 'cov secs=%e rss_kb=%M' python3 -I $B/verify_sem_coverage.py $B/b000055.txt /dev/stdin > coverage_n${n}_merged.txt 2>&1 )
( /usr/bin/time -f 'indep secs=%e rss_kb=%M' python3 -I $IC cert_n${n}_merged.txt.xz $n --regen > indep_n${n}_merged.txt 2>&1 )
if grep -q -- '-> PASS' coverage_n${n}_merged.txt && grep -q -- '-> PASS' indep_n${n}_merged.txt; then echo "n=$n PASS both checkers $(date)" | tee VERDICT
else echo "n=$n FAIL $(date)" | tee VERDICT; exit 1; fi
