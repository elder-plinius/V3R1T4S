#!/bin/bash
# chunk.sh n i M : one resumable work unit (gentreeg residue class i mod M) for order n. Done marker: $R/done/$i
n=$1; i=$2; M=$3; H=${V3_HOME:?set V3_HOME to the worker folder (bin/, runs/)}; B=$H/bin; R=$H/runs/n$n; C=$R/chunks/$i
[ -f $R/done/$i ] && exit 0
[ -f $H/STOP ] && exit 0
ulimit -v ${VLIM_KB:-500000} # 16 workers x 500 MB virtual = 8 GB hard ceiling
rm -rf $C; mkdir -p $C $R/done; cd $C || exit 1
t0=$(date +%s)
$B/gentreeg -q -p $n $i/$M | awk -f $B/p2e.awk > trees.txt || exit 1
stdbuf -oL $B/alpha_sem 300 ${ALPHA_ATT:-200} $((i+1)) < trees.txt > s0_alpha.txt
grep ';;NOALPHA' s0_alpha.txt | sed 's/;;NOALPHA.*//' > r0.txt
stdbuf -oL $B/sem_direct 300 ${DIRECT_ATT:-100000} $((i+100001)) < r0.txt > s1_direct.txt
grep ';;UNLABELED' s1_direct.txt | sed 's/;;UNLABELED.*//' > r1.txt
$H/venv/bin/python $B/caterpillar_sem.py r1.txt > s2_cat.txt
grep ';;UNLABELED' s2_cat.txt | sed 's/;;UNLABELED.*//' > r2.txt
if [ -s r2.txt ]; then timeout ${DEEP_SEC:-900} stdbuf -oL $B/sem_direct 2000 10000000 $((i+200001)) < r2.txt > s3_deep.txt; fi
$H/venv/bin/python $B/assemble_chunk.py trees.txt s0_alpha.txt s1_direct.txt s2_cat.txt s3_deep.txt > stats.txt || exit 1
[ -f $H/STOP ] && exit 0
echo "$(cat stats.txt) secs $(( $(date +%s) - t0 ))" > stats.txt
if [ -s residue.txt ]; then cp residue.txt $R/RESIDUE_chunk$i.txt; fi
xz -T1 -6 -f cert.txt && rm -f trees.txt s0_alpha.txt s1_direct.txt s2_cat.txt s3_deep.txt r0.txt r1.txt r2.txt
cp stats.txt $R/done/$i
