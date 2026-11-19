#!/bin/sh
# Calibration (k=s=3, n=9..14) and the claim (k=3, s=5, n=17..21): UNSAT with C = n-sk+s-1 colours (DRAT proof,
# checked by drat-trim) and SAT with C+1 colours (model saved). Run from this folder.
B=${TOOLS_BIN:?set TOOLS_BIN to the folder holding the cadical and drat-trim binaries}
mkdir -p out
for spec in "9 3 3" "10 3 3" "11 3 3" "12 3 3" "13 3 3" "14 3 3" "17 3 5" "18 3 5" "19 3 5" "20 3 5" "21 3 5" "22 3 5"; do
  set -- $spec; n=$1 k=$2 s=$3; C=$((n - s*k + s - 1)); C1=$((C + 1)); tag=n${n}_k${k}_s${s}
  python3 gen_cnf.py $n $k $s $C out/${tag}_c${C}.cnf
  
  $B/cadical -q --no-binary out/${tag}_c${C}.cnf out/${tag}_c${C}.drat > out/${tag}_c${C}.solver.txt 2>&1; rc=$?

  echo "$tag C=$C cadical exit $rc ($(grep '^s ' out/${tag}_c${C}.solver.txt))"
  $B/drat-trim out/${tag}_c${C}.cnf out/${tag}_c${C}.drat -L out/${tag}_c${C}.lrat > out/${tag}_c${C}.drattrim.txt 2>&1
  echo "$tag C=$C drat-trim: $(tr -d "\\r" < out/${tag}_c${C}.drattrim.txt | grep -E "^s ")"
  python3 gen_cnf.py $n $k $s $C1 out/${tag}_c${C1}.cnf > /dev/null
  $B/cadical -q out/${tag}_c${C1}.cnf -w out/${tag}_c${C1}.model > out/${tag}_c${C1}.solver.txt 2>&1
  echo "$tag C+1=$C1 cadical: $(grep '^s ' out/${tag}_c${C1}.solver.txt)"
done
