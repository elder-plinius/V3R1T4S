# Pre-registration v5 — the seed repeat was not independent; a genuine second split generation

Written 2026-10-23T23:25:30Z, **before** the corrected second split generation exists. Supersedes only PREREG.v4 §3.2.

## What went wrong

PREREG.md §3.4 requires a seed repeat on "a second split generation (seed 20261023)". I generated it by
calling drevalpy 1.3.5's own `split_dataset` with `random_state=20261023`. The confirmatory results on it
were nearly identical split-by-split to seed 42 (PotencyTransfer 0.2829 vs 0.2834, 0.2930 vs 0.2929,
0.4661 vs 0.4659, ...), which two independent partitions cannot produce. Checked directly:

**In all 10 folds the test drug sets are identical between seed 42 and seed 20261023**; only the
validation drugs differ (about 5 of 49-50 shared). Cause: `datasets/dataset.py::_leave_group_out_cv` shuffles
rows with the seed and then calls `GroupKFold(n_splits)`, with the comment "shuffle, since GroupKFold does
not implement this". But GroupKFold assigns groups to folds by group size over the sorted group labels,
so row order never affects the assignment. **In drevalpy 1.3.5 the seed does not randomise LDO test
folds**, and anyone requesting a "new" LDO split generation by changing the seed receives the same held-out
drugs. (This also bears directly on the bank's partial win p3.) Recorded as a defect in published tooling.

## Consequences, stated before anything new is run

- The seed-20261023 runs already made are **void as the pre-registered repeat**. PotencyTransfer's value
  there (normalized R^2 0.2250 by drevalpy's evaluation) is reported only as a *validation-split
  sensitivity* observation: changing ~90% of the validation drugs left the result essentially unchanged.
- The baseline re-run on that folder was stopped part-way and is discarded.
- Seed 42 remains the official split generation; it is package-generated and is what the public report used.

## The corrected second split generation

drevalpy 1.3.5's own `split_dataset(n_cv_splits=10, mode="LDO", split_validation=True, validation_ratio=0.1,
random_state=20261023)`, with exactly one change: `GroupKFold` inside `drevalpy.datasets.dataset` is replaced
for this call by `GroupKFold(n_splits, shuffle=True, random_state=20261023)` (scikit-learn 1.9.1). This is the
minimal change that makes the package's own stated intent take effect; everything else — validation and
early-stopping splits, file format, loading — is drevalpy's code. The split generator is
`attempts/reproduction/code/make_splits_independent.py`.

**Independence check, committed now:** the generation is accepted only if no test fold coincides with a
seed-42 test fold, and the mean best-match Jaccard overlap between its test folds and seed 42's is below
0.25 (random 10-fold partitions of 545 drugs give about 0.1).

On this generation, through the unmodified pipeline loading the saved splits: NaiveMeanEffectsPredictor,
MultiOmicsNeuralNetwork, GradientBoosting, SimpleNeuralNetwork and the frozen PotencyTransfer (PREREG.v4,
unchanged). PREREG.md §3 condition 4 is evaluated **only** on this generation. A miss here is a miss.
