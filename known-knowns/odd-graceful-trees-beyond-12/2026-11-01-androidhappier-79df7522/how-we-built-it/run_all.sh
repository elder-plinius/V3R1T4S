#!/bin/sh
# Search S1 over every tree of order 2..22. Generator: networkx nonisomorphic_trees (how-we-built-it/gen_trees.py).
# Run from the package folder. Writes cert_N.txt and search_N.log for N = 2..22 into ./rebuild/.
# PY selects the Python that has networkx installed (default python3); the run used networkx 3.7.
# Differs from the run's own script only in this PY default and the output folder (the run used a fixed local
# interpreter path and out/).
PY=${PY:-python3}
mkdir -p rebuild
cc -O3 -fopenmp -o rebuild/oglabel how-we-built-it/oglabel.c || exit 1
for n in $(seq 2 22); do
  s=$(date +%s)
  $PY how-we-built-it/gen_trees.py $n | ./rebuild/oglabel $n 200 20000 > rebuild/cert_$n.txt 2> rebuild/search_$n.log
  echo "n=$n seconds=$(( $(date +%s)-s ))" >> rebuild/search_$n.log
  cat rebuild/search_$n.log
done
echo ALLDONE
