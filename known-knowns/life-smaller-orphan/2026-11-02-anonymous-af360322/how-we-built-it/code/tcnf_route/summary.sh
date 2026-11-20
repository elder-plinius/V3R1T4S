#!/bin/bash
# summary.sh: per size directory, count cubes UNSAT+VERIFIED out of 2^h; COVERED iff all values 0..2^h-1 present with result=20 check=c_VERIFIED
cd $(dirname $0)/../output/cubes
for d in */; do d=${d%/}; h=$(echo $d|sed -E 's/h([0-9]+)w.*/\1/'); n=$((1<<h)); ok=0; sat=0; miss=""
 for v in $(seq 0 $((n-1))); do f=$(ls $d/c*v$v.res 2>/dev/null|head -1); if [ -n "$f" ] && grep -q "result=20" $f && grep -q "check=c_VERIFIED" $f; then ok=$((ok+1)); elif [ -n "$f" ] && grep -q result=10 $f; then sat=$((sat+1)); else miss="$miss $v"; fi; done
 tot=$(cat $d/*.res 2>/dev/null | grep -oE 'solve_ms=[0-9]+' | cut -d= -f2 | awk '{s+=$1}END{printf "%.0f",s/1000}')
 st=PARTIAL; [ $ok = $n ] && st="ALL_UNSAT_VERIFIED(covered)"; [ $sat -gt 0 ] && st="HAS_SAT_CUBE($sat)"
 echo "$d: $ok/$n UNSAT+LRAT-verified, sat=$sat, solve_total=${tot}s, $st${miss:+ missing:$miss}"; done
