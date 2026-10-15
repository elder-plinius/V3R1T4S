# How the object was built (exact commands, paths relative to a working folder)

The search is randomised and time-capped, so rerunning it gives a portfolio of similar quality, not the same bytes.
The object is verified by `verify-it-yourself/` regardless of how it was found.

Setup: `python3 -m venv venv && venv/bin/pip install -r how-we-built-it/requirements.txt` (numpy, highspy,
python-flint; Python 3.9). `INST` is a folder holding QOBLIB's `06-portfolio/instances/po_a200_t10_orig/`
`stock_prices.txt.gz` and `covariance_matrices.txt.gz`. `C=how-we-built-it/code`. Every job ran under `nice -n 15`
with a hard time cap and one BLAS thread (`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1`).

1. Continuous relaxation, residual-aware rounding and exact descent (two runs):
   `venv/bin/python -I $C/relax_round.py $C $INST 50 0.01 po_a200_t10_orig 12 330 rr1` (seed 7) and
   `RR_SEED=101 venv/bin/python -I $C/relax_round.py $C $INST 50 0.01 po_a200_t10_orig 14 290 rr2`.
2. Iterated local search books (`quoter.py CODE INST B LAMBDA NAME START SEED KICK SECONDS OUT`):
   b1, b2 from PR #87's file (seeds 11, 12; kicks 3, 8; 720 s); b4 from rr1's best at that moment (seed 21, kick 4,
   420 s); b5 from rr2's best (seed 31, kick 4, 240 s); c1–c3 with `quoter2.py` from b4/b5 (seeds 51–53).
3. Chain-DP crossover over 11 solutions (c1–c3, b1, b2, b4, b5, the b1 snapshot, rr1, rr2, PR #87):
   `venv/bin/python -I $C/pool_dp.py $C $INST 50 0.01 po_a200_t10_orig dp1 60 <the 11 .sol files>` → −606279.
4. Rounds of per-period ILS + DP + polish (12 rounds, 9 periods × 60 s each, 3 workers):
   `venv/bin/python -I $C/rounds.py venv/bin/python $C $C $INST 50 0.01 po_a200_t10_orig dp1_polished.sol run1 12 60 3`
   → `run1/base_r11.sol`, objective −691624 = `object/a200_t10_orig_b050_l1e-02_solution.sol` (same sha256).

`spectrum.py` is the check that showed every period's risk matrix has rank 29. The pre-registration files of the
run are `PREREG.md`, `PREREG.v2.md` (second lens changed after a smoke test) and `PREREG.v3.md` (budget raised to heavy
by the operator); none changed the cell, the judge or the threshold.
