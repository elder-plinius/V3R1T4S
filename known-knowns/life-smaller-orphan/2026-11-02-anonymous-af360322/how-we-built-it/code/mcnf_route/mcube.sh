#!/bin/bash
# mcube.sh h w c val DEADLINE_EPOCH [BM SM]: mcnf (m=w/2) cube with units on target column c = val; CaDiCaL LRAT + lrat-check; one result file per finished cube.
# Result file output/cubes/h${h}w${w}r${BM}_${SM}/c${c}v${val}.res (only written on a finished verdict; killed runs leave nothing -> rerun later).
h=$1;w=$2;c=$3;val=$4;DL=$5;BM=${6:-8};SM=${7:-12}
B=$(cd $(dirname $0)/..; pwd); CAD=${TOOLS:?set TOOLS to the folder holding the solver builds}/cadical-zig/cadical-cli; LC=${TOOLS:?set TOOLS to the folder holding the solver builds}/drat-trim/lrat-check
od=$B/output/cubes/h${h}w${w}r${BM}_${SM}; mkdir -p $od; res=$od/c${c}v${val}.res; [ -s $res ] && exit 0
now=$(date +%s); left=$((DL-now-30)); [ $left -lt ${MINLEFT:-60} ] && exit 0
f=${WORK:-.}/mcube_${h}_${w}_${BM}_${SM}_${c}_${val}; [ -e $f.cnf ] && exit 0; $B/code/mcnf $h $w $((w/2)) $BM $SM $c $val > $f.cnf
s=$(date +%s%N); (ulimit -t $left; ulimit -v ${MEMKB:-1800000}; exec nice -n19 timeout $left $CAD -q --lrat=true --binary=false $f.cnf $f.lrat > $f.out); r=$?; e=$(date +%s%N)
ver=NA; ct=0
if [ $r = 20 ]; then left=$((DL-$(date +%s)-20)); s2=$(date +%s%N)
  ver=$( (ulimit -t $left; exec nice -n19 timeout $left $LC $f.cnf $f.lrat) 2>&1 | grep -oE "c VERIFIED|FAILED|failed|ERROR" | head -1 | tr ' ' '_'); e2=$(date +%s%N); ct=$(( (e2-s2)/1000000 ))
  [ -z "$ver" ] && ver=NO_VERDICT_OR_TIMEOUT
  [ "$ver" = c_VERIFIED ] || { rm -f $f.*; exit 0; }   # unfinished check -> no result file, rerun later
elif [ $r = 10 ]; then cp $f.out $od/c${c}v${val}.model; else rm -f $f.*; exit 0; fi
echo -e "h=$h\tw=$w\trule=$BM/$SM\tenc=mcnf\tm=$((w/2))\tcube_col=$c\tval=$val\tresult=$r\tsolve_ms=$(( (e-s)/1000000 ))\tproof_kb=$(du -k $f.lrat|cut -f1)\tcheck=$ver\tcheck_ms=$ct\tclauses=$(head -1 $f.cnf|cut -d' ' -f4)\tdone=$(date -Is)" > $res
rm -f $f.*
