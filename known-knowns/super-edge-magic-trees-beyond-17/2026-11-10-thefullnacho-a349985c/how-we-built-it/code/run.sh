#!/bin/bash
# run.sh n M P : run all M chunks of order n with P parallel workers (skips chunks already done), then verify coverage.
# Launch only via: nohup setsid nice -n 19 ionice -c3 $V3_HOME/bin/run.sh n M P > log 2>&1 &
n=$1; M=$2; P=${3:-16}; H=${V3_HOME:?set V3_HOME to the worker folder (bin/, runs/)}; R=$H/runs/n$n; mkdir -p $R/done
[ $P -gt 30 ] && P=30
echo $$ > $R/run.pid; echo "$M" > $R/M; date +%s > $R/started_$(date +%s)
echo "start n=$n M=$M P=$P $(date)"
seq 0 $((M-1)) | xargs -P $P -I{} $H/bin/chunk.sh $n {} $M
nd=$(ls $R/done | wc -l); echo "chunks done $nd/$M $(date)"
if [ "$nd" -eq "$M" ] && [ ! -f $H/STOP ]; then
  for ((i=0;i<M;i++)); do xz -dc $R/chunks/$i/cert.txt.xz; done > $R/cert_n$n.txt
  python3 $H/bin/verify_sem_coverage.py $H/bin/b000055.txt $R/cert_n$n.txt > $R/coverage_n$n.txt
  cat $R/coverage_n$n.txt; xz -T4 -6 -f $R/cert_n$n.txt; sha256sum $R/cert_n$n.txt.xz > $R/cert_n$n.txt.xz.sha256
  cat $R/RESIDUE_chunk*.txt 2>/dev/null > $R/RESIDUE_n$n.txt; echo "residue trees: $(wc -l < $R/RESIDUE_n$n.txt)"
  echo "ALL DONE $(date)"
fi
