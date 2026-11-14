# SRBench 2025 black-box: 522_pm10 beaten by GAM shape compression

## What

The fixed GAM-shape-compression procedure in code/gam_sr.py returns one closed-form expression per listed seed for dataset 522_pm10 with median test R2 0.331263, strictly above PS-Tree's live-table median 0.300852, at median complexity 145.5, at or below PS-Tree's median model size 4996.5.

The procedure: fit a generalized additive model by backfitting binned-mean smoothers on each training split (8 rounds, 20 quantile bins, 3 passes of [1,2,1]/4 smoothing), compress each univariate shape into at most 3 closed-form terms from a fixed per-feature library on a 60-point quantile grid, then refit all coefficients jointly by OLS on the training rows. One expression per split, 30 splits, no per-split hand edits. The object in this package is the 30 expressions with their per-split scores.

## Check it yourself

From this folder in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough time: 2 to 4 minutes on a laptop (it builds a throwaway venv, installs numpy, sympy and scikit-learn, downloads the 12 KB dataset and the table pointer, then re-scores all 30 expressions). See `RUN_IT_YOURSELF.md` for the full commands and expected output.

## Compared to

- Table: SRBench 2025 black-box track, `results/black-box-tuning/results.feather` at https://github.com/cavalab/srbench/tree/srbench_2025/results/black-box-tuning
- Cell: dataset 522_pm10, all 28 algorithms, median test R^2 over the 30 listed splits
- Leader: PS-Tree, median test R^2 0.300852, median model_size 4996.5
- Runner-up: QLattice, median test R^2 0.276510, median model_size 35
- Table fetched: 2026-11-13T06:02:15Z (HTTP 200), sha256 5b428264a346f6bbbeabded219f87454b9206afa70c19c012075c672533f342e; re-fetched 2026-11-13T06:21:11Z by the novelty skeptic and confirmed unchanged
- This claim: median test R^2 0.331263, median complexity 145.5 — strictly above the leader on R^2 at a far smaller size. Full record in `the-record-we-beat/`.
- Partial win p1 is also met: the point (0.3313, 145.5) is dominated by no algorithm's point and strictly dominates the Pareto-front point PS-Tree (0.3009, 4996.5).

## Not claimed

- This is one cell (522_pm10) of one benchmark track, not a general symbolic regression result. No claim is made about the other 11 datasets.
- The margin is +0.0304 on the median, with 21 of 30 splits above 0.300852 and per-split test R^2 ranging 0.1673 to 0.4076.
- The expressions are 19–21-term additive sums of compressed univariate shapes, not a new symbolic regression algorithm; the procedure is a fixed recipe, not a general method.
- A second lens in the same run (beam search over single small expressions, complexity <= 12, one expression plus an affine fit per split) reached median test R^2 0.1684 at median complexity 22 — below the bar and below the p2 bar (0.1758 at size <= 20). It is not part of this package.
- The same target's 1028_SWD cell was beaten by a different procedure in an earlier submission (PR #1044, median test R^2 0.3911 at size 75.5). That is a separate cell and a separate package.

## Credits

- SRBench 2025 black-box track and table: Imai Aldeia, Zhang, Bomarito, Cranmer, Fonseca, Burlacu, La Cava and de Franca (arXiv:2505.03977; https://github.com/cavalab/srbench).
- The table leader this claim beats: PS-Tree, as published in the SRBench 2025 black-box track; runner-up QLattice likewise.
- Dataset 522_pm10: PMLB (EpistasisLab), https://github.com/EpistasisLab/pmlb.
- Contributor: thefullnacho. The panel (three fresh contexts) verified this claim; see `panel/`.
