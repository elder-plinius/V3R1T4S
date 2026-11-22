#!/bin/sh
# final site-model CTM ladder (warm-started, stops when |dk|<1e-36 three times)
export VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2
PY=python3
cd {WORKDIR}
prev=-
for c in 20 30 40 50 60 70 80 90 100; do
  $PY -I ctmgen2.py site $c 400 256 $prev sitef_state_$c.json > sitef_$c.log 2>&1
  prev=sitef_state_$c.json
done
