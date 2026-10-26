# Pre-registration v2 — pin drevalpy 1.3.5

Written 2026-10-23T21:49:20Z. Supersedes section 2's package line of `PREREG.md` (sha256
`e5adc0f58042e8bd3c14ee6daa2ea296d6d6b9ea779c9867a837d479bcff5131`); every other clause of
`PREREG.md` stands unchanged. **No model output from this run had been scored when this was
written** — the only computations so far are a descriptive variance decomposition on development
data and split-identity checks.

## Why the change

`PREREG.md` pinned drevalpy 1.6.0. Inspection after freezing showed that **1.6.0 does not contain
`MultiOmicsNeuralNetwork`**, the published LDO leader the criterion requires me to re-run in my own
environment (1.6.0 replaced the MultiOmics* family with MultiView*). drevalpy **1.3.5**
(PyPI, uploaded 2025-07-01) is the last release before the public report's `last-modified` of
2025-10-17 and ships **exactly the 11 model families on the public leaderboard**, including
`MultiOmicsNeuralNetwork` and `ProteomicsRandomForest`. It is therefore the best available
reconstruction of the environment that produced the published numbers.

Checks made before switching, all recorded in `attempts/reproduction/output/`:
1. `_normalize_metrics_by_mean_effects` is **byte-identical** in 1.3.5 and 1.6.0.
2. The NaiveMeanEffectsPredictor differs only in routing cell-line effects through tissue in 1.6.0;
   for a seen cell line both reduce to the cell-line mean, and in LDO every cell line is seen, so
   the normalization ruler is the same.
3. Both versions read Zenodo record 23159774 into the same 235,974 measured pairs and 545 drugs.
4. Both versions generate **identical** seed-42 LDO splits (test and validation drug sets per split;
   all-splits hash `0bc801329cc6bada`).

## What changes

- All development and all confirmatory runs use **drevalpy 1.3.5** in `$ENV/bin/python`
  (Python 3.12, torch with CUDA). My model, NaiveMeanEffectsPredictor and MultiOmicsNeuralNetwork
  run in this one environment, as the criterion's "same-environment" clause requires.
- The data version (record 23159774) may differ from the one behind the October 2025 report. The
  same-environment re-runs of the baselines are therefore the operative comparison; the published
  0.0235 remains a hard bar regardless.

## Added commitment: reproduction before attack

Before my model's first confirmatory run, NaiveMeanEffectsPredictor and MultiOmicsNeuralNetwork are
re-run through the 1.3.5 pipeline on CTRPv2 LDO, 10 splits, seed 42. If either deviates from the
published value by more than its published across-split SD, that discrepancy is reported and
investigated before any claim, because it would mean this environment does not reproduce the record.
