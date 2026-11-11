# Reproduce (from this claim folder)

Requirements: Python 3 with gmpy2, mpmath, numpy (`PY` below), gcc, 4 cores, ~1 GB memory. No network.

```sh
cd object
gcc -O2 -march=native -o search677b search677b.c -lm
./search677b 1100000 20261109 my_search.txt         # "# COMPLETE kmin=3 kmax=147 total_candidates=2 ..." (k=29 line: cand=0)
PY -I verify_cands.py my_search.txt                  # "candidates: 2 exact-equal: 0 ..."
PY -I taskA_ratio_audit_k.py 400 29 29               # "TOTAL missing over k=29..29: 0" (|admissible_r| = 114817)
PY -I rig_margin.py 29 29 1000000 1 1000             # ~8 min: "TOTAL pairs=114817 failures=0 undecided=0"
for I in 0 1 2 3; do SHARD=$I/4 PY -I shard_margin.py 29 29 1000000 1 1000 > margin$I.txt & done; wait      # exact rational intervals; see object/out/ for the run time
for I in 0 1 2 3; do SHARD=$I/4 QEXP=495 PY -I shard_rig.py 29 29 1040 0.001 1000000 > shard$I.txt & done; wait   # see object/out/ for the run time
```
Each enumeration shard ends `TOTAL window candidates=... product solutions=0 (X0=1000000, QMAX=10^495)`; its k=29
line must equal object/out/deep_rig_shard*.txt apart from the time, and the shards' admissible_r counts must add up to
114817. Each margin shard's TOTAL line must say failures=0 undecided=0, and the shards' pair counts must add up to
114817. Without `QEXP=495`, deep_rig.py silently uses QMAX = 10^515. To judge a single triple:
`python3 -I checker/check677.py n m k`.
