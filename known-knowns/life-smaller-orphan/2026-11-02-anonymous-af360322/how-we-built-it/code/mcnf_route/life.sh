#!/bin/bash
# life.sh DEADLINE spec... (spec h:w): mcnf Life (B3/S23, masks 8/12), m=w/2, CaDiCaL LRAT + lrat-check; appends to output/life.tsv
DL=$1; shift; D=$(cd $(dirname $0); pwd); CAD=${TOOLS:?set TOOLS to the folder holding the solver builds}/cadical-zig/cadical-cli; LC=${TOOLS:?set TOOLS to the folder holding the solver builds}/drat-trim/lrat-check
for sp in "$@"; do IFS=: read h w <<<"$sp"; grep -q "^h=$h	w=$w	" $D/../output/life.tsv 2>/dev/null && continue
 left=$((DL-$(date +%s)-20)); [ $left -lt 60 ] && exit 0; f=${WORK:-.}/mc_$h_$w; $D/mcnf $h $w $((w/2)) 8 12 > $f.cnf
 s=$(date +%s%N); (ulimit -t $left; ulimit -v ${MEMKB:-2000000}; exec nice -n19 timeout $left $CAD -q --lrat=true --binary=false $f.cnf $f.lrat >/dev/null); r=$?; e=$(date +%s%N)
 if [ $r = 20 ]; then left=$((DL-$(date +%s)-10)); ver=$( (ulimit -t $left; exec nice -n19 timeout $left $LC $f.cnf $f.lrat) 2>&1 | grep -oE "c VERIFIED|failed|ERROR"|head -1|tr ' ' _); e2=$(date +%s%N)
   [ "$ver" = c_VERIFIED ] && echo -e "h=$h\tw=$w\tm=$((w/2))\tresult=20\tsolve_ms=$(( (e-s)/1000000 ))\tcheck=$ver\tcheck_ms=$(( (e2-e)/1000000 ))\tclauses=$(head -1 $f.cnf|cut -d' ' -f4)" >> $D/../output/life.tsv
 elif [ $r = 10 ]; then echo -e "h=$h\tw=$w\tresult=10 UNEXPECTED_SAT" >> $D/../output/life.tsv; fi; rm -f $f.*; done
