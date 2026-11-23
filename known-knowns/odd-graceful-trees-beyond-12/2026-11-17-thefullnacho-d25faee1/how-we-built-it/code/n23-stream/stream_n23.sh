#!/bin/sh
# Stream all unlabeled trees on 23 vertices into 1,000,000-tree chunks and
# label them with the same hybrid search as run_hybrid_order.sh (5 workers).
# Run from a working directory that contains og_direct, og_restart, dump_trees.py
# and merge_hybrid.py (copy them from ../small-data-direct/).
set -eu
mkdir -p chunks
python3 dump_trees.py 23 | split -l 1000000 -d -a 2 - chunks/t
# then, for each chunk file, run og_direct with cap 100000 and og_restart on leftovers,
# as in ../small-data-direct/run_hybrid_order.sh, and concatenate the labeled chunks
# to cert_n23.txt (optionally gzip the result).
