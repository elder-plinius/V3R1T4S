# REPRODUCE review: partial win p3 (elephant-rumble-receiver-identity-beyond-caller)

context: fresh subagent started for this claim only

Scope: only claim/ was read (CLAIM.md, target.md, PREREG.md, REPRODUCE.md, null_test.md, baseline/README.md, data/, output/, code/). claim/ was not modified: after all checks, `sha256sum -c SHA256SUMS` and `sha256sum -c PREREG.sha256` still pass. Scratch work ran on a copy.
Environment: Python 3.12.3, numpy 2.5.4, pandas 3.1.1, scikit-learn 1.9.1, OMP_NUM_THREADS=1, at most 2 processes. This matches REPRODUCE.md.

## Definitions checked against

target.md, p3: "A reproducibility result: re-implement the paper's random forest and land within 0.02 of 27.5%. Then report the caller-habit baseline and the 99.9th percentile of 1,000 within-caller label shuffles on the same folds, and state whether 27.5% exceeds them, with code a skeptic can rerun."

target.md, baseline: "predicts, for each test call, the receiver most often addressed by that call's true caller in the training folds, with ties broken at random and the overall most frequent receiver as the fallback."

PREREG.md: "Calls with Cert_ID_Bin == 1: 437. Receiver = Elicitor1_ID, caller = CallerID."; "core.make_folds: 7 folds stratified by caller x receiver"; "|mean rf accuracy - 0.275| <= 0.02 on the 100 real draws"; "the 99.9th percentile of 1,000 rf reruns with within-caller shuffled labels ON THE SAME FOLDS: rerun j uses the fold assignment of real draw (j mod 100) and rng default_rng([20261118, 2, j])"; percentile = "numpy linear interpolation".

## 1. Independent checker, written before reading code/

My checker read only the raw CSV and the saved JSON files.
- Selection: the spectral CSV has 469 rows. Cert_ID_Bin == 1 leaves 437 calls, with no missing caller or receiver: 99 callers and 115 receivers.
- Folds: there are 100 files in output/real/, each with 437 fold labels in 0..6, and all 100 fold assignments are distinct. Stratification holds in every draw: within every caller x receiver stratum, the counts per fold differ by at most 1, with 0 violations.
- Accuracies: every acc_habit and acc_rf was recomputed from the saved per-call predictions against Elicitor1_ID, and all 200 match exactly. habit mean = 0.49224256292906177 (sd 0.00743). rf mean = 0.26954233409610984 (sd 0.00794). Both equal output/summary.json bit for bit.
- Habit rule: for every test call in every fold of all 100 draws, I checked the saved habit prediction is in the argmax set of that caller's receivers in the training folds, or in the overall-mode set when the caller is absent from training. There were 0 violations. This also confirms that the per-call order is the CSV order of the 437 calls.
- Null (output/null_rf/): 1000 files, with rerun == j and fold_draw == j mod 100 for every j. All values lie on the 1/437 grid. Mean 0.21067, sd 0.01193, 99.9th percentile (linear) = 0.24256521739130454, max 0.2448512585812357. All equal summary.json and null_test.md.
- p3 statements: |0.26954 - 0.275| = 0.0055 <= 0.02. 0.275 < habit 0.4922, so 27.5% does NOT exceed the caller-habit baseline. 0.275 > 0.24257 (and the rf mean 0.26954 > max control 0.24485), so it DOES exceed the within-caller shuffle null. This matches the sentence in CLAIM.md.
- Limitation: null_rf files store only the accuracy, not per-call predictions or folds. The null statistics can therefore be recomputed only from the saved accuracies. Individual controls were checked by exact replay (section 3).

## 2. Code review (code/core.py, run_real.py, null_rf.py, summarize.py, replay.py)

- Forest vs data/20240104_vocal_labeling_code_for_upload_revision1.R, section 10, MODEL 1: ranger(num.trees=500, mtry=6, min.node.size=1, max.depth=0, replace=FALSE, sample.fraction=0.6), trained on droplevels(train) with the varkeep features. core.rf_predict matches this:
  - 500 sklearn DecisionTreeClassifier trees with max_features=6, min_samples_leaf=1 and no depth limit, Gini (ranger's default);
  - each tree is fit on int(0.6 n) training calls drawn without replacement;
  - prediction is a majority vote with random tie-breaks;
  - the classes are the training-fold receivers only.
  The features are 94 in total: sprsMed/Mbw/Eqbw/Mc, V1-V74 (the R code sets nPca <- 74), Fw/Mw/F/M 1-4, which is the same as varkeep. Caller is not an input. Mapping tree outputs to class indices is correct, because the labels are global integer indices and predict returns classes_.
- Leakage: rf_predict uses only X[tr] and recv[tr]. habit_predict uses only tr. The test fold reaches neither model. The folds are built from the labels, as in the paper (createFolds on caller_receiver strata). This is the criterion's prescribed design, not leakage.
- Null: null_rf.py rebuilds the folds of real draw j mod 100, which is make_folds as that draw rng's first use. It permutes receivers within each caller and reruns the identical forest. I regenerated all 100 saved fold assignments from default_rng([20261118, s]) and got 100/100 identical, so the null uses the same folds as the real draws.
- Minor differences, none of which is a criterion issue:
  - The paper fixes one createFolds split and reruns the forest 2000 times. This claim uses 100 fresh fold draws, which is what the target's criterion requires.
  - caret places a stratum's leftover calls in random distinct folds, while make_folds deals round-robin from a random start. The per-stratum balance is the same; fold sizes are uneven in both (draw 0: 51 to 71).
  - sklearn's max_features keeps searching past 6 features when no valid split is found, whereas ranger does not. This is negligible.
  - REPRODUCE.md step 2 says to redirect stdout, but summarize.py also rewrites output/summary.json in place. The rewritten file is byte-identical, so this is harmless, but it does write into output/.

## 3. REPRODUCE.md steps 1-3 (run on a copy)

- Step 1: `sha256sum -c SHA256SUMS` passes all 2226 lines. `sha256sum -c PREREG.sha256` passes for PREREG.md and the 5 frozen code files. data/SHA256SUMS passes. All 5 Dryad files match the sha-256 digests in data/dryad-files.json. The R script comes from Zenodo and is covered only by data/SHA256SUMS.
- Step 2: `python3 code/summarize.py` gives JSON equal to output/summary.json, and the rewritten file is byte-identical (cmp). Its internal assertions pass.
- Step 3: `replay.py real 0 50 99`, `replay.py null_rf 0 500 999`, `replay.py null_pa 0` and `replay.py context 0` all print IDENTICAL (byte for byte, ALL IDENTICAL), in about 85 s each with one process. No non-determinism was seen.

## 4. Independent forest and my own shuffles

I used a different code path: sklearn BaggingClassifier(DecisionTreeClassifier(max_features=6), 500 estimators, max_samples=int(0.6 n), bootstrap=False), with my own seeds, on the saved folds of 10 real draws (3, 17, 28, 41, 56, 64, 72, 88, 93, 99).
- Real labels: mean 0.2677 (sd 0.0090, range 0.256 to 0.281). The saved rf on the same 10 draws gives 0.2680. This agrees well within noise and lies within 0.02 of 0.275.
- Own within-caller shuffles: 10 controls, using my own rng and the folds of draws 0, 10, ..., 90. They give mean 0.2162 (saved null mean 0.2107) and max 0.2471. One of my 10 controls (0.2471) is slightly above the claim's max of 0.2449 and its 99.9th percentile of 0.2426. That is consistent with a single-draw spread of sd about 0.012 to 0.019, and shows the far tail is estimated imprecisely. Both 0.275 and the rf mean (0.2695) stay above every control I saw, so the conclusion "27.5% exceeds the within-caller shuffle null but not the caller-habit baseline" holds.

## Verdict

Every property and every claimed number in CLAIM.md was recomputed from the saved files and matches exactly:
- the selection of 437 calls;
- the stratification of all 100 draws;
- the accuracies;
- the habit rule;
- the null statistics.
The exact replays are byte-identical and deterministic, the forest matches the paper's MODEL 1 settings, and the test fold does not leak into training. An independent forest reproduces about 0.268. Nothing in the claim depends on an exhaustive search. No mismatch, missing object or non-determinism was found. One caveat: the null's tail is noisy at n = 1000, and null_rf keeps no per-call output. This does not change the stated conclusion.

pass: true
