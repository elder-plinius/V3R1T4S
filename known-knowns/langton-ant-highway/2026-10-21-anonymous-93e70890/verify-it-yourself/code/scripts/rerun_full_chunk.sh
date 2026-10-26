#!/bin/sh
# Rerun a whole user chunk C (2^24 masks): lant4 raw-output sha256 vs the user's chunk sha256, and lantx2 all-CAP/maxtcap.
# Usage: code/scripts/rerun_full_chunk.sh C [THREADS]   (~10 min with 1 thread per program; THREADS speeds up lant4 only)
cd "$(dirname "$0")/../.."; mkdir -p work
C=$1; T=${2:-1}; a=$((C*16777216)); b=$((a+16777216))
U=$(cat data/user-chunk-sums/chunk_$C.sum); us=$(echo "$U" | awk '{for(i=1;i<NF;i++) if($i=="sha256") print $(i+1)}')
sha=$(nice -n 19 bin/lant4 6 6 $a $b 2000000 $T | sha256sum | cut -c1-64)
echo "user : $U"; echo "lant4 sha256 $sha"; [ "$sha" = "$us" ] && echo "SHA256 MATCH" || echo "SHA256 DIFFERENT"
nice -n 19 bin/lantx2 range 6 6 $a $b | awk 'BEGIN{mt=-1}{n++; if($6=="CAP")cap++; if($2>mt){mt=$2;mm=$1}} END{print "lantx2 lines",n,"CAP",cap,"maxtcap",mt,"first mask at max",mm}'
