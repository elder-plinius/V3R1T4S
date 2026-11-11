# How the object was built (run 2026-11-09-0917)

- `PREREG.md`: the run's pre-registration (frozen 2026-11-09T09:19:35Z before any attack program; the judge of steps 1-5).
- `claim/`: the claim as the panel saw it (`CLAIM.md`, `REPRODUCE.md`, the Lean specs of the statement and its
  negation). The claim's `object/` is this package's `object/` (byte-identical, 29 files; a stray Python bytecode
  cache that appeared in the claim folder during the panel is not part of the claim and is not copied); its
  `checker/check677.py` is `verify-it-yourself/check677.py`; its `source/` (the fetched problem page and catalog) is
  described in `the-record-we-beat/STATUS_RECORD.md`.
- `lens-reports/`: the run's two lens reports (extender-r3: enumeration; rigor: small X, ratio audit and margins).
- `PATCH_NOTE.md`, `deep_rig_patch.diff`: the 2026-10-24 patch of deep_rig.py (same program here), also in the claim.

Commands of the run (Python 3.13 with gmpy2, mpmath, numpy; 4 cores; every job after the PREREG):

```sh
gcc -O2 -march=native -o search677b object/search677b.c -lm
./search677b 1100000 20261109 out/search_N1.1e6.txt              # COMPLETE kmin=3 kmax=147 total_candidates=2 (k=29: cand=0)
python3 -I object/verify_cands.py out/search_N1.1e6.txt            # candidates: 2 exact-equal: 0
python3 -I object/taskA_ratio_audit_k.py 400 29 29                  # TOTAL missing over k=29..29: 0 (114817 ratios)
python3 -I object/rig_margin.py 29 29 1000000 1 1000                # TOTAL pairs=114817 failures=0 undecided=0 (451 s)
for I in 0 1 2 3; do SHARD=$I/4 QEXP=495 python3 -I object/shard_rig.py 29 29 1040 0.001 1000000 > out/deep_rig_shard$I.txt & done; wait   # 5384-5402 s each
for I in 0 1 2 3; do SHARD=$I/4 python3 -I object/shard_margin.py 29 29 1000000 1 1000 > out/rig_margin_exact_k29_shard$I.txt & done; wait  # 3218-3230 s each
python3 -I object/sum_shards.py out                                 # k=29: 114817 / 3332527 / 3288852, product_solutions=0
# wrapper test (object/out/wrap_test/): rig_margin_exact.py 5 12 ... unsharded, as SHARD=0/1 and as 3 shards
```
