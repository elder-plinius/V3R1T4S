# How we found it (contributor text, unverified)

The night's target was SRBench 2025 black-box, dataset 1028_SWD — picked
because the leader was low (PS-Tree, median test R^2 0.3800 at median size
3270) and the runner-up EQL sat only 0.0064 behind at size 59, so a modest
expression had a real chance. The previous eight nights had all been spent on
a small-MNIST record that plateaued around 96.5%, and the last run's report
had recommended a fresh quarry.

The first lens was a plain dictionary sparse regression: a 146-term library
(single-feature transforms and pairwise products), forward stepwise selection
by inner-validation R^2, at most 12 terms, OLS refit. It landed at median
test R^2 0.3776 — 0.0024 short of the bar, but a Pareto-front point that
dominates four published algorithms.

The second lens imported the symbolic-distillation idea: fit an RBF kernel
ridge as a teacher on each training split, then fit the same dictionary
procedure to the teacher's predictions instead of the raw targets. The
smoothed targets let the short forms land better: median test R^2 0.3911,
median complexity 75.5.

Along the way the checker caught a real bug in the run itself: the first
version assumed sklearn's train_test_split was a plain numpy RandomState
permutation. It is not — the indices differ — and re-scoring recorded EQL
expressions proved it (off by up to 0.145). The split was corrected to
sklearn's actual function, both lenses were re-run in full under a new
prereg, and the checker then reproduced recorded table values to within
0.0001. The first run's numbers were discarded, not cited.

The claim went to a three-skeptic panel (three fresh contexts): reproduction,
novelty (including a live re-fetch of the table), and criterion. All three
passed. The margin is narrow and the report says so.
