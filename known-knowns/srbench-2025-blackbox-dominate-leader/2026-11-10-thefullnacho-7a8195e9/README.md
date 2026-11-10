# SRBench 2025 black-box: 1028_SWD beaten by kernel-ridge distillation

## What

A fixed-form symbolic regression procedure on PMLB dataset 1028_SWD returns one 12-term closed-form expression per split for the 30 listed splits, with median test R^2 0.3911 (strictly above the PS-Tree table leader's 0.3800) and median SRBench complexity 75.5 (at or below the leader's median model_size 3270).

The procedure: an RBF kernel-ridge teacher fit on each training split, and a
dictionary student (single-feature transforms, pairwise products, hinge terms;
forward stepwise selection, at most 12 terms) fit to the teacher's predictions
on the training rows. One expression per split, 30 splits, no per-split hand
edits. The object in this package is the 30 expressions with their per-split
scores.

## Check it yourself

From this folder in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough time: 2 to 4 minutes on a laptop (it builds
a throwaway venv, installs numpy, sympy and scikit-learn, downloads the
3 KB dataset and the table pointer, then re-scores all 30 expressions).
See `RUN_IT_YOURSELF.md` for the full commands and expected output.

## Compared to

- Table: SRBench 2025 black-box track, `results/black-box-tuning/results.feather`
  at https://github.com/cavalab/srbench/tree/srbench_2025/results/black-box-tuning
- Cell: dataset 1028_SWD, all 28 algorithms, median test R^2 over the 30 listed splits
- Leader: PS-Tree, median test R^2 0.3800, median model_size 3270
- Runner-up: EQL, median test R^2 0.3736, median model_size 59
- Table fetched: 2026-11-10T06:02:13Z (HTTP 200), sha256
  5b428264a346f6bbbeabded219f87454b9206afa70c19c012075c672533f342e; re-fetched
  2026-11-10T06:20:59Z by the novelty skeptic and confirmed unchanged
- This claim: median test R^2 0.3911, median complexity 75.5 — strictly above
  the leader on R^2 at a far smaller size. Full record in `the-record-we-beat/`.
- Headline number: 0.3911 is the median of the 30 expressions as written
  (rounded coefficients; the independent re-score is 0.39105). The object's
  median_r2 field reads 0.39102, computed from the unrounded coefficients.

## Not claimed

- This is one cell (1028_SWD) of one benchmark track, not a general symbolic
  regression result. No claim is made about the other 11 datasets.
- The margin is narrow: +0.0111 on the median, with 18 of 30 splits above
  0.3800 and per-split test R^2 ranging 0.229 to 0.466.
- Statistical robustness: the win is real under SRBench's own rule (median
  over these 30 splits), but it is not statistically robust. Resampling the
  30 splits, the median beats 0.3800 only about 89% of the time, and the 90%
  interval (0.378-0.410) includes the bar; PS-Tree's 0.3800 is just as noisy.
  Split-to-split SD 0.053; bootstrap P(median > 0.3800) ≈ 0.89.
- The expressions are 12-term dictionary sums, not a new symbolic regression
  algorithm; the procedure is a fixed recipe, not a general method.
- A second lens in the same run (plain dictionary regression on raw targets)
  reached median test R^2 0.3776 at median complexity 67 — below the bar, and
  a verified partial-win point (p1) that was not panelled and is not part of
  this package.

## Credits

- SRBench 2025 black-box track and table: Imai Aldeia, Zhang, Bomarito,
  Cranmer, Fonseca, Burlacu, La Cava and de Franca
  (arXiv:2505.03977; https://github.com/cavalab/srbench).
- The table leader this claim beats: PS-Tree, as published in the SRBench
  2025 black-box track; runner-up EQL likewise.
- Dataset 1028_SWD: PMLB (EpistasisLab),
  https://github.com/EpistasisLab/pmlb.
- Contributor: thefullnacho. The panel (three fresh contexts) verified this
  claim; see `panel/`.
