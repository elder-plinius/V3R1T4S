#!/bin/sh
# six seeds x 100 s for n = 8, then three seeds x 200 s for n = 9 (outputs in out/)
mkdir -p out
for s in 1 2 3 4 5 6; do python3 anneal_own.py 8 100 $s out/n8_seed$s.txt; done
for s in 1 2 3; do python3 anneal_own.py 9 200 $s out/n9_seed$s.txt; done
