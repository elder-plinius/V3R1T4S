# Criterion skeptic: partial win p3 (elephant-rumble-receiver-identity-beyond-caller)

context: fresh subagent started for this claim only

Scope of review: only claim/ (CLAIM.md, target.md, PREREG.md, null_test.md, baseline/README.md, output/, code/, data/). Nothing in claim/ was modified. A `code/__pycache__` folder that my replay run created was deleted, and `sha256sum -c SHA256SUMS` still passes.

## What was claimed
Only p3 is claimed. The full win was attempted and failed: in output/summary.json, c1 is true and c2 and c3 are false. CLAIM.md says so and does not claim it. p1 and p2 are not claimed.

## Integrity checks (rerun by me)
- `SHA256SUMS`, `PREREG.sha256` and `data/SHA256SUMS` all check OK. The local digests of the four Dryad files and README.md match the sha-256 digests in data/dryad-files.json.
- Subset: the spectral n469 file has 469 rows. Of these, Cert_ID_Bin == 1 for 437 and 0 for 32. None of the 437 has a missing CallerID or Elicitor1_ID, and none of the 469 has a missing value in the 94 features. This is the paper's `mydfsub <- droplevels(mydata[Cert_ID_Bin==1,])`, and its output filenames say n437. The features are the paper's varkeep with nPca = 74, so the subset and inputs are right.
- Exact replay (code/replay.py) of real draw 0 and null_rf reruns 0 and 7 reproduced the saved files byte for byte.
- An independent script I wrote (not the claimant's) recomputed from the saved per-call predictions:
  - rf mean 0.269542 (sd 0.0079, range 0.247 to 0.291);
  - null_rf: n = 1000, 99.9th percentile (numpy linear) 0.242565, max 0.244851, mean 0.2107. No control reaches the rf mean or 0.275. Every rerun j uses the folds of draw j mod 100.
  - The folds of all 100 draws are balanced within every caller x receiver stratum (no stratum has fold counts differing by more than 1).
- Caller-habit baseline: core.habit_predict matches target.md word for word. It predicts the true caller's most frequent receiver in the training folds, breaks ties at random, and falls back to the overall most frequent receiver (overall ties also at random, which target.md leaves open). My own implementation, which averages over ties analytically on the saved folds, gives 0.4924. The saved random-tie value is 0.4922. Same data, same folds, same metric: this is consistent with the baseline record in baseline/README.md.

## Clause-by-clause against p3
1. "Re-implement the paper's random forest". I compared code/core.py with data/20240104_vocal_labeling_code_for_upload_revision1.R, section 10, MODEL 1.
   - Matches the paper: 500 trees; mtry 6; min.node.size 1 with no depth limit; sample.fraction 0.6 without replacement (floor of 0.6 n); majority vote with random ties; the same 94 spectral features; caller not an input; the 437-call subset; accuracy = correct / 437.
   - Differences:
     - (a) The trees are scikit-learn CART (gini), not ranger. scikit-learn keeps searching beyond max_features when none of the sampled features gives a valid split, which ranger does not. This is a minor implementation difference.
     - (b) The paper draws one set of folds with caret::createFolds (outside the loop) and averages 2000 forest reruns on it. The claim uses 100 fresh fold draws, which is the evaluation scheme target.md prescribes. So the claim's statistic averages over fold uncertainty that the paper's 27.5% does not.
     - (c) The fold generator is not caret's. core.make_folds deals each stratum round-robin from a random start fold, so small strata go to consecutive folds. Caret samples distinct random folds. Both put the calls of each stratum in distinct folds and keep the stratum balance. However, round-robin gives more uneven fold sizes (46 to 83 calls across the saved draws).
   - Sensitivity check: I ran the frozen rf_predict on 6 caret-style (factor-branch createFolds) fold draws. Accuracies were 0.254, 0.259, 0.272, 0.261, 0.268 and 0.279, mean about 0.265. That is within noise of 0.2695 and still within 0.02 of 0.275.
   - None of these differences changes the verdict, but the claim is "a re-implementation", not an exact replication of ranger plus caret.
2. "Within 0.02 of 27.5%": |0.2695 - 0.275| = 0.0055 <= 0.02. Met. The draw-to-draw sd (0.008) means the paper's single fold set could itself sit about ±0.008 from its own expected value. The margin is comfortable.
3. "Report the caller-habit baseline": 0.4922 on the same 100 draws. Reported.
4. "99.9th percentile of 1,000 within-caller label shuffles on the same folds": met literally.
   - code/null_rf.py rebuilds the real draw's folds, permutes Elicitor1_ID among each caller's calls (so each caller's receiver frequencies are kept), and reruns the frozen forest. The result is 0.2426.
   - Each control is a single draw, while the real statistic is a 100-draw mean. This makes the null wider, the conservative direction.
5. "State whether 27.5% exceeds them": 0.275 > 0.2426 (exceeds the shuffle null) and 0.275 < 0.4922 (does not exceed the habit baseline). CLAIM.md states exactly this. Correct.
6. "Code a skeptic can rerun": yes. The replay reproduced the saved files byte for byte.

## Preregistration and timing
- PREREG.md and the five programs it names hash to PREREG.sha256. PREREG.md fixes the following before results: the p3 tolerance test, the "same folds" construction (draw j mod 100, seed [20261118, 2, j]), numpy linear-interpolation percentiles, and the habit rule.
- File mtimes in claim/ are copy times. So the 2026-11-18T19:28:49Z freeze is asserted, not independently verifiable from this folder.
- code/summarize.py and code/replay.py came after the results.
  - summarize.py only aggregates the saved outputs, using the preregistered percentile and comparisons. It also asserts that the saved accuracies equal those recomputed from the per-call predictions.
  - replay.py only re-executes the frozen functions.
  - Neither one changes a model, fold, seed or threshold, so their late writing does not matter for p3.
- The extra "maximum 0.2449" in CLAIM.md is descriptive and adds no new decision.

## Hidden quantifiers and stretched definitions
- "The paper's random forest" is stretched slightly: it is CART trees and a different fold generator with fresh folds, not ranger with one caret fold set. This is disclosed in spirit by "re-implementation", and my sensitivity check suggests it does not change the result.
- "Same folds" holds. Folds are built from the real labels and reused for the shuffled labels, which is what p3 says.
- The claim is not subsumed by anything stronger, because the full win failed. p3 is a modest reproducibility-plus-null result. It is genuine, and it is not a claim that the forest beats caller habit (it does not: 0.2695 < 0.4922).

confirmed_scope: On the 437 Cert_ID_Bin == 1 calls of the Dryad n469 spectral file, a scikit-learn re-implementation of the paper's section-10 MODEL 1 forest (500 trees, mtry 6, leaf size 1, 60% subsampling without replacement, caller not an input) scores a mean receiver accuracy of 0.2695 over 100 fresh caller x receiver stratified 7-fold draws, within 0.02 of the paper's 27.5%; on the same draws the bank's caller-habit baseline scores 0.4922, and the 99.9th percentile of 1,000 single-draw reruns with receiver labels shuffled within caller on the same folds is 0.2426, so 27.5% exceeds that within-caller shuffle null but not the caller-habit baseline.

pass: true
