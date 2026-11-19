#!/bin/bash
# usage: batch_ms2.sh candidates_file : multistage compose (stage-0 pre-rewind 32, then 0, then 128) + verify (live CSYNTH re-fetched)
cd "${RUN_DIR:?set RUN_DIR to the harvest run folder}"   # absolute path removed for publication
grep '^IMPROVE' "$1" | while read tag oa _ new _ cur _ ia ic _ rot _ lane _ ph _ per; do
  [ -f attempts/verified/$oa.json ] && continue
  [ -f attempts/compose_tmp/$oa.fail4 ] && continue
  res=""
  for pre in 32 0 128; do
    r=attempts/compose_tmp/$oa.p$pre.rle; j=attempts/compose_tmp/$oa.p$pre.json
    timeout 180 nice -n 19 venv/bin/python code/compose_ms.py --in-apg $ia --rot $rot --lane $lane --ph $ph --target $oa --out $r --pre $pre > attempts/compose_tmp/$oa.p$pre.mlog 2>&1 && [ -f $r ] || { res="CFAIL $oa"; continue; }
    timeout 180 nice -n 19 venv/bin/python code/verify_synthesis.py --rle $r --target $oa --out $j > /dev/null 2>&1
    if grep -q '"ok": true' $j 2>/dev/null; then cp $r attempts/verified/$oa.rle; cp $j attempts/verified/$oa.json; res="WIN $oa $new cur $cur pre $pre"; break; fi
    res="VFAIL $oa"
  done
  echo "$res"; case "$res" in WIN*) ;; *) touch attempts/compose_tmp/$oa.fail4;; esac
done; echo DONE
