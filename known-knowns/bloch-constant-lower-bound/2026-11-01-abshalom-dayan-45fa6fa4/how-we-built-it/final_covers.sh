#!/bin/bash
# sequential, one worker. usage: final_covers.sh cap "T eta tag" ...
CAP=$1; shift
for x in "$@"; do set -- $x
  echo "== T=$1 eta=$2 tag=$3 start $(date -u +%H:%M:%S)"
  NOQUICK=1 nice -n 10 perl -e 'alarm shift; exec @ARGV' $CAP code/search cover ${LIBD:-lib} ${CD:-cover}/$3 $1 $2 0 256 $CAP 1 1 40 2>/dev/null | tail -1 | cut -c1-200
  echo "   search exit ${PIPESTATUS[0]}"
  python3 -I code/cover_check.py ${CD:-cover}/$3 | cut -c1-120
  nice -n 10 perl -e 'alarm shift; exec @ARGV' 300 code/check ${LIBD:-lib} ${CD:-cover}/$3 $1 $2 | tail -1 | cut -c1-260
done
echo ALLDONE $(date -u +%H:%M:%S)
