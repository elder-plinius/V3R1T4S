#!/bin/bash
# coverK.sh n cert_file : per-line check (checkK), then coverage: canonical forms (nauty labelg) of the certificate
# graphs must be pairwise distinct and equal, as a set, to the canonical forms of a fresh geng -c -d3 -D3 n run;
# and the count must equal A002851(n) from the saved b-file.
set -o pipefail
n=$1; cert=$2; B=${NAUTY_BIN:?set NAUTY_BIN to the folder holding geng and labelg}; D=$(dirname $0); T=${TMPDIR:-/tmp}/coverK_${n}_$$; mkdir -p $T
B002851=${B002851:-$D/../inputs/b002851.txt}
expect=$(awk -v k=$((n/2)) '$1==k{print $2}' $B002851)
$D/checkK $n < $cert > $T/cert.g6 || { echo "COVERK n=$n FAIL checkK"; exit 1; }
LC_ALL=C; export LC_ALL
$B/labelg -q $T/cert.g6 | sort -S 1G > $T/cert.can
dups=$(uniq -d $T/cert.can | wc -l)
P=${PAR:-1}
if [ "$P" -gt 1 ]; then
  M=64; seq 0 $((M-1)) | xargs -P $P -I{} sh -c "$B/geng -cq -d3 -D3 $n {}/$M | $B/labelg -q > $T/gen_{}.can"
  cat $T/gen_*.can | sort -S 1G > $T/gen.can; rm -f $T/gen_*.can
else
  $B/geng -cq -d3 -D3 $n | $B/labelg -q | sort -S 1G > $T/gen.can
fi
ncert=$(wc -l < $T/cert.can); ngen=$(wc -l < $T/gen.can)
if cmp -s $T/cert.can $T/gen.can; then same=yes; else same=no; fi
echo "COVERK n=$n cert_lines=$ncert dup_canon=$dups geng_count=$ngen A002851=$expect sets_equal=$same"
rm -rf $T
[ "$dups" = 0 ] && [ "$same" = yes ] && [ "$ncert" = "$expect" ] && [ "$ngen" = "$expect" ] && echo "COVERK n=$n PASS" || { echo "COVERK n=$n FAIL"; exit 1; }
