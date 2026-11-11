#!/bin/bash
# finish25.sh : PREREG addendum 2 for n = 25. Waits for the step-1 retry to end, runs a second pass on every residue
# tree that still has no labeling (28 parts, 12 h each), merges only if every residue tree is labelled, then runs the
# two checkers one after the other and writes VERDICT. Stop: touch $V3_HOME/STOP before the second pass starts.
set -u
H=${V3_HOME:?}; IC=${INDEP_CHECK:?}; B=$H/bin; R=$H/runs/n25; D=$R/retry; n=25
log() { echo "$(date '+%F %T') $*"; }
log "waiting for the step-1 retry (sem_direct processes) to finish"
while pgrep -x sem_direct >/dev/null; do sleep 60; done
log "step-1 retry finished"
[ -f $H/STOP ] && { log "STOP present"; exit 0; }
cd $D || exit 1
cat out_part_*.txt | grep -v ';;UNLABELED' > step1_labelled.txt
python3 -I $B/check_sem.py step1_labelled.txt | tail -1
python3 -I - <<'EOF'
done = {l.split(';')[1] for l in open('step1_labelled.txt') if l.strip()}
left = [l for l in open('residue_all.txt') if l.strip() and l.split(';')[1].strip() not in done]
open('pass2_input.txt', 'w').writelines(left)
print(f"step 1 labelled {len(done)}; left for pass 2: {len(left)}")
EOF
mkdir -p pass2 && cd pass2 && rm -f part_* out_*
if [ -s ../pass2_input.txt ]; then
  split -n l/28 -d ../pass2_input.txt part_
  for f in part_*; do p=${f#part_}; ( timeout 43200 stdbuf -oL $B/sem_direct 2000 1000000000 $((10#$p * 104729 + 99991)) < $f > out_$f.txt ) & done
  wait
fi
cd $D
cat pass2/out_part_*.txt 2>/dev/null | grep -v ';;UNLABELED' > step2_labelled.txt
cat step1_labelled.txt step2_labelled.txt > retry_labelled.txt
python3 -I $B/check_sem.py retry_labelled.txt | tail -1
missing=$(python3 -I - <<'EOF'
have = {l.split(';')[1] for l in open('retry_labelled.txt') if l.strip()}
want = [l.split(';')[1].strip() for l in open('residue_all.txt') if l.strip()]
print(sum(1 for w in want if w not in have))
EOF
)
log "after pass 2: $missing residue trees without a labeling"
if [ "$missing" -ne 0 ]; then echo "n=$n: $missing residue trees unlabelled after pass 2; stopping for Alex $(date)" | tee $R/VERDICT; exit 1; fi
cd $R
log "merging"
(xz -dc cert_n$n.txt.xz; cat retry/retry_labelled.txt) | xz -T8 -6 > cert_n${n}_merged.txt.xz
sha256sum cert_n${n}_merged.txt.xz > cert_n${n}_merged.txt.xz.sha256
log "checker 1: verify_sem_coverage"
( xz -dc cert_n${n}_merged.txt.xz | /usr/bin/time -f 'cov secs=%e rss_kb=%M' python3 -I $B/verify_sem_coverage.py $B/b000055.txt /dev/stdin > coverage_n${n}_merged.txt 2>&1 )
log "checker 2: indep_check --regen"
( /usr/bin/time -f 'indep secs=%e rss_kb=%M' python3 -I $IC cert_n${n}_merged.txt.xz $n --regen > indep_n${n}_merged.txt 2>&1 )
if grep -q -- '-> PASS' coverage_n${n}_merged.txt && grep -q -- '-> PASS' indep_n${n}_merged.txt; then echo "n=$n PASS both checkers $(date)" | tee VERDICT
else echo "n=$n FAIL $(date)" | tee VERDICT; exit 1; fi
