# PREREG v2 — 2026-11-10 06:21 UTC (supersedes PREREG.md on the split definition only)

CORRECTION (checker bug, found by validation before any claim was packaged):
PREREG.md stated the split as "numpy RandomState(seed).permutation (sklearn
train_test_split equivalent)". That equivalence is FALSE in the installed
scikit-learn: sklearn's train_test_split indices differ from a plain
RandomState(seed).permutation (verified directly: test indices differ).
Re-scoring recorded EQL expressions on the numpy-permutation splits gave
R2 off by up to 0.145 from the recorded values. Re-scoring the same
expressions on sklearn's actual train_test_split splits, with X and y
standardized on train (scale_x=True, scale_y=True, as the 2025 runs used),
reproduces the recorded r2_test to +-0.0001 on all 6 tested seeds
(769: 0.3517 vs 0.3518; 860: 0.4274 vs 0.4274; 1685: 0.3474 vs 0.3473;
2433: 0.4235 vs 0.4235; 4426: 0.3353 vs 0.3352; 5051: 0.4569 vs 0.4570).
Complexity already matched exactly (59=59, 46=46, 61=61, 65=65).

CORRECTED split definition: the 30 splits are EXACTLY sklearn's
train_test_split(X, y, train_size=0.75, test_size=0.25, random_state=seed)
on the 1028_SWD rows in file order, one split per listed seed. The lens
procedures are UNCHANGED (same fixed code, same hyperparameters); only the
checker's split implementation is corrected, and the correction is validated
against recorded table values, not tuned to any lens result. All lens scores
computed under PREREG.md (numpy-permutation splits) are VOID and are being
re-run under this v2. The earlier medians (constructor 0.3820, smuggler
0.4045) must not be cited as results.

Everything else in PREREG.md stands unchanged: criterion verbatim, statistic
(median test R2 and median complexity over the 30 splits), thresholds
(full win: median R2 > 0.3800 AND median complexity <= 3270; p2: median R2 >
0.2430 AND median complexity <= 20), fixed procedures, null_test not needed
(explicit object, deterministic checker; constant-mean predictor is the
chance-level reference at R2 = 0).
