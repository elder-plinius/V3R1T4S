# Reproduce (from this claim folder)

Requirements: Python 3 with gmpy2, mpmath, numpy (`PY` below), gcc, 4 cores, ~1 GB memory. No network.

```sh
cd object
gcc -O2 -march=native -o search677b search677b.c -lm
./search677b 1100000 20261106 my_search.txt         # "# COMPLETE kmin=3 kmax=147 total_candidates=2 ..."
PY -I verify_cands.py my_search.txt                  # "candidates: 2 exact-equal: 0 ..."
PY -I taskA_ratio_audit_k.py 400 26 28               # "TOTAL missing over k=26..28: 0"
PY -I rig_margin.py 26 28 1000000 1 1000             # ~4 min:  "TOTAL pairs=58926 failures=0 undecided=0"
PY -I rig_margin_exact.py 26 28 1000000 1 1000       # ~1.5 h:  same TOTAL line
PY -I rig_margin_exact.py 26 26 1000000 1 1000      # run per k (26, 27, 28), ~30 min each
for I in 0 1 2 3; do SHARD=$I/4 QEXP=495 PY -I shard_rig.py 26 28 1040 0.001 1000000 > shard$I.txt & done; wait   # ~2 h on 4 cores
```
Each shard ends `TOTAL window candidates=... product solutions=0 (X0=1000000, QMAX=10^495)`; its per-k lines must equal
object/out/deep_rig_shard*.txt apart from the time, and the shards' admissible_r counts must add up to 21262, 16402, 21262. To judge a single triple: `python3 -I checker/check677.py n m k`.
