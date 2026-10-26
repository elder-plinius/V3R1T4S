#!/bin/sh
# Tamper tests: each modifies a COPY of an input (under work/tamper/) and reruns a check; every check MUST FAIL.
cd "$(dirname "$0")/../.."; T=work/tamper; rm -rf $T; mkdir -p $T; ok=0; n=0
expect_fail() { n=$((n+1)); if "$@" > $T/out.txt 2>&1; then echo "TAMPER $n NOT DETECTED: $*"; tail -2 $T/out.txt; else echo "tamper $n detected: $(tail -1 $T/out.txt)"; ok=$((ok+1)); fi; }
# 1. one tcap changed in the 4x4 reference
awk 'NR==12345{$2=$2+1}1' data/validation/enum4_lant2.txt > $T/enum4.txt
expect_fail code/scripts/check_4x4.sh $T/enum4.txt
# 2. one direction changed in the 5x5 reference slice
zcat data/validation/enum5_chunk07_lantc.gz | awk 'NR==500000{$5=($5+1)%4}1' | gzip > $T/e5.gz
expect_fail code/scripts/check_5x5_slice.sh $T/e5.gz
# 3. a chunk summary removed
cp -r data/user-chunk-sums $T/s3; rm $T/s3/chunk_1234.sum
expect_fail python3 code/scripts/check_summaries.py $T/s3
# 4. one chunk summary claims an uncaptured mask
cp -r data/user-chunk-sums $T/s4; sed -i 's/ UNCAP 0 / UNCAP 1 /' $T/s4/chunk_77.sum
expect_fail python3 code/scripts/check_summaries.py $T/s4
# 5. one chunk's maxtcap off by one (hard case must then mismatch)
cp -r data/user-chunk-sums $T/s5; awk '{for(i=1;i<NF;i++) if($i=="maxtcap") $(i+1)=$(i+1)+1}1' data/user-chunk-sums/chunk_2439.sum > $T/s5/chunk_2439.sum
expect_fail code/scripts/check_hard.sh $T/s5
# 6. one sample unit's linehash altered
sed 's/^\(pass 0 chunk 0 .*linehash \)./\10/' data/sample/sample_units.txt > $T/u6.txt
grep -q "^pass 0 chunk 0 .*linehash 0" data/sample/sample_units.txt && sed -i 's/^\(pass 0 chunk 0 .*linehash \)./\11/' $T/u6.txt
UNITS=$T/u6.txt expect_fail code/scripts/check_sample_blocks.sh 0 0
# 7. one sample unit claims a max above the user's chunk max
awk '$2==1 && $4==9 {for(i=1;i<NF;i++) if($i=="maxtcap") $(i+1)=999999}1' data/sample/sample_units.txt > $T/u7.txt
QUICK=1 expect_fail python3 code/scripts/check_sample_summary.py $T/u7.txt
# 8. one sample unit missing
grep -v "^pass 3 chunk 4000 " data/sample/sample_units.txt > $T/u8.txt
QUICK=1 expect_fail python3 code/scripts/check_sample_summary.py $T/u8.txt
echo "tamper tests detected: $ok of $n"
[ $ok = $n ] && echo "TAMPER: PASS (every tamper detected)" || { echo "TAMPER: FAIL"; exit 1; }
