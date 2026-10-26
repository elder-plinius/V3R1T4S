#!/bin/bash
# Iterated warm-start augmentation: from code file $1 (M words), try M+1 with gcmc for $3 seconds per step, seed base $2.
cur=$1; seedb=$2; secs=$3; tag=$4
M=$(grep -c '^[ACGT]' "$cur")
while true; do
  M1=$((M+1)); out=aug_${tag}_M${M1}.out
  ./gcmc 15 11 $M1 $((seedb+M1)) $secs ck_aug_${tag}_M${M1}.txt "$cur" > $out 2>&1
  if grep -q '^# FOUND' $out; then grep '^WORD' $out | sed 's/WORD //' > code_aug_${tag}_M${M1}.txt; cur=code_aug_${tag}_M${M1}.txt; M=$M1; echo "M=$M1 found $(date -u +%T)"; else echo "M=$M1 not found in ${secs}s $(date -u +%T)"; break; fi
done
