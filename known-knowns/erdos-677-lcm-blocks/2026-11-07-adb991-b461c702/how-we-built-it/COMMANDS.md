# How the object was built (run 2026-11-06-0918)

- `PREREG.md`: the run's pre-registration (frozen 2026-11-06 before any attack program; the judge of steps 1-5).
- `claim/`: the claim as the panel saw it (`CLAIM.md`, `REPRODUCE.md`, the Lean specs of the statement and its
  negation). The claim's `object/` is this package's `object/` (byte-identical, 23 files); its `checker/check677.py`
  is `verify-it-yourself/check677.py`; its `source/` (the fetched problem page) is described in
  `the-record-we-beat/STATUS_RECORD.md`.
- `lens-reports/`: the run's two lens reports (extender-r2: enumeration; rigor: ratio audit and margins).
- `PATCH_NOTE.md`, `deep_rig_patch.diff`: the 2026-10-24 patch of deep_rig.py (same program here).

Commands of the run (Python 3.13 with gmpy2, mpmath, numpy; 4 cores; every job after the PREREG):

```sh
gcc -O2 -march=native -o search677b object/search677b.c -lm
./search677b 1100000 20261106 out/search_N1.1e6.txt          # COMPLETE kmin=3 kmax=147 total_candidates=2
python3 -I object/verify_cands.py out/search_N1.1e6.txt         # candidates: 2 exact-equal: 0
python3 -I object/taskA_ratio_audit_k.py 400 26 28               # TOTAL missing over k=26..28: 0
python3 -I object/rig_margin.py 26 28 1000000 1 1000             # TOTAL pairs=58926 failures=0 undecided=0
for k in 26 27 28; do python3 -I object/rig_margin_exact.py $k $k 1000000 1 1000; done   # failures=0 undecided=0 (2198, 1990, 2560 s)
for I in 0 1 2 3; do SHARD=$I/4 QEXP=495 python3 -I object/shard_rig.py 26 28 1040 0.001 1000000 > out/deep_rig_shard$I.txt & done; wait
python3 -I object/sum_shards.py out ...                          # k=26: 21262 / 1989788 / 490397; k=27: 16402 / 417007 / 411576;
                                                                # k=28: 21262 / 2241996 / 553418; product_solutions=0 (out/shard_sums.txt)
```

The four shards ran about 5700 s each (all three k), with the margin jobs running alongside during the first hour.
`object/out/shard_sums.txt` also compares k = 26 and 27 with the unsharded run of 2026-10-29 (run 2026-10-29-0821,
whose outputs are not shipped): equal.
