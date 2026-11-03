#!/bin/bash
# residue r of MOD for order N; output is the checkpoint (complete iff it has "fnv ")
N=$1; r=$2; MOD=$3; f=out/B${N}_r${r}of${MOD}.txt
grep -q '^fnv ' "$f" 2>/dev/null && exit 0
${GENG:-geng} -cq $N $r/$MOD | ./totBgo nbr 150 > "$f.tmp" && mv "$f.tmp" "$f"
