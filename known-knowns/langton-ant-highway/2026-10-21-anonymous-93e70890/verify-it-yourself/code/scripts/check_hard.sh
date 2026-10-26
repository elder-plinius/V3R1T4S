#!/bin/sh
# The 4096 per-chunk maxtcap masks (from check_summaries.py) rerun with lantx2; each must be CAP with tcap == chunk maxtcap. ~5 s.
cd "$(dirname "$0")/../.."
python3 code/scripts/check_summaries.py ${1:-data/user-chunk-sums} > work/summaries.txt || { cat work/summaries.txt; echo "HARD: FAIL (summaries)"; exit 1; }
nice -n 19 bin/lantx2 list 6 6 work/hard_list.txt > work/hard_lantx2.txt
paste -d' ' work/hard_expected.txt work/hard_lantx2.txt | awk '{n++; if($4!=$2){print "ORDER", $0; bad++} else if($9!="CAP"||$5!=$3){print "MISMATCH", $0; bad++}}
  END{printf "hard cases %d mismatches %d\n", n, bad+0; if(n!=4096||bad>0){print "HARD: FAIL"; exit 1} else print "HARD: PASS"}'
