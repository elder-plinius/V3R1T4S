#!/bin/bash
# ctl.sh: first-SAT width of mcnf (m = w/2) for control rule masks at h=1,2 and Life h<=3, widths 2..8; compare with runs/2026-10-26-1706 control_rules.txt
K=${TOOLS:?set TOOLS to the folder holding the solver builds}/kissat/kissat; D=$(dirname $0)
for rule in "17 1" "64 4" "64 1" "8 0" "24 12" "72 12" "8 6" "40 0" "12 4" "8 12"; do set -- $rule; for h in 1 2 3; do
 [ $h = 3 ] && [ "$1 $2" != "8 12" ] && continue
 first=none; for w in 2 3 4 5 6 7 8; do m=$((w/2)); f=${WORK:-.}/m_$1_$2_$h_$w.cnf; $D/mcnf $h $w $m $1 $2 > $f; (ulimit -t 300; nice -n19 $K -q $f > $f.out); r=$?; rm -f $f
   if [ $r = 10 ]; then first=$w; cp $f.out $D/../output/model_B$1_S$2_h${h}_w$w.txt; rm -f $f.out; break; fi; rm -f $f.out; [ $r = 20 ] || { first="ERR$r@w$w"; break; }; done
 echo "rule B$1/S$2 h=$h mcnf_first_SAT_w=$first"; done; done
