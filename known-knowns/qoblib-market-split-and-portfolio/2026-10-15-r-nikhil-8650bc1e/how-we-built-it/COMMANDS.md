# How the object was built (exact commands, paths relative to a working folder)

The search is randomised and time-capped, so rerunning it gives a portfolio of similar quality, not the same bytes.
The object is verified by `verify-it-yourself/` regardless of how it was found.

Setup: `python3 -m venv venv && venv/bin/pip install -r how-we-built-it/requirements.txt` (Python 3.9). `INST` is a
folder holding QOBLIB's `06-portfolio/instances/po_a200_t10_s00/` `stock_prices.txt.gz` and
`covariance_matrices.txt.gz`. `C=how-we-built-it/code` (the original runs kept these files in three folders: `q/` =
pfmodel.py, quoter2.py; `x/` = period_ils.py, pool_dp2.py; `l/` = relax_round2.py, rounds2.py, cell_pipeline.sh; pass
`$C` for each). Every job ran under `nice -n 15` with a hard time cap and one BLAS thread
(`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1`).

Stage A (2026-10-14, 22:12–22:33 UTC): the one-command cell pipeline `cell_pipeline.sh` with WORKERS=3 and 6 rounds:
1. `RR_SEED=7 venv/bin/python -I $C/relax_round2.py $C $INST 50 0.01 po_a200_t10_s00 8 300 rr` — continuous relaxation
   on the instance's 29 factors (HiGHS; −814741.5) + residual-aware rounding + exact descent → −487360.
2. Two iterated-local-search books from `rr_best.sol` (`quoter2.py ... rr_best.sol 61 4 300 qa 80` and
   `... 62 8 300 qb 80`) → −516814 and −501881.
3. `pool_dp2.py $C $INST 50 0.01 po_a200_t10_s00 dp 120 rr_best.sol qa_best.sol qb_best.sol` — exact chain DP mixing
   periods across the three solutions, then exact polish → −520405.
4. `venv/bin/python -I $C/rounds2.py venv/bin/python $C $C $INST 50 0.01 po_a200_t10_s00 dp_polished.sol rounds 6 45 3`
   — rounds of per-period ILS (each period re-optimised with both neighbours fixed, 45 s) + chain DP over all pools
   → −618978.

Stage B (2026-10-15, 03:21–07:34 UTC): 60 more rounds from Stage A's result, new seeds, 2 workers:
`SEED_OFFSET=60000 venv/bin/python -I $C/rounds2.py venv/bin/python $C $C $INST 50 0.01 po_a200_t10_s00 lead_618978.sol rounds_b 60 45 2`
→ 22 new bases, last at round 53: `rounds_b/base_r53.sol`, objective −644342 = `object/a200_t10_s00_b050_l1e-02_solution.sol`
(same sha256).

Pre-registration: `PREREG.md` (cell, judge, threshold), `PREREG.v2.md` (budget raised to heavy by the operator; freeze
time moved) and `PREREG.v3.md` (session paused past the planned freeze; freeze at 09:01:05 UTC). None changed the cell,
the judge or the threshold.
