# Preregistration: elephant receiver identity (run 2026-11-18-1925)

Frozen by the lead agent (Andy) before any model on the acoustic features is scored on the real receiver labels. The code it names is frozen with it (PREREG.sha256 lists PREREG.md, code/core.py and the four programs below). The criterion text in target.md governs; this file fixes every choice the criterion leaves open.

null_test: required (criterion (3) and partial win p3 both need 1,000 within-caller label shuffles)

## Data
- data/20231225_dfall_obs_data_and_spectral_features_revision1_n469.csv and data/20240106_dfall_obs_data_and_cepstral_features_revision1_n469.csv (Dryad version 16; sha256 in data/SHA256SUMS). Calls with Cert_ID_Bin == 1: 437. Receiver = Elicitor1_ID, caller = CallerID.
- Spectral features: the paper's 94 (sprsMed, sprsMbw, sprsEqbw, sprsMc, V1-V74, Fw1-4, Mw1-4, F1-4, M1-4). Cepstral features: the same with V1-V12 (the paper's cepstral nPca = 12), 30 columns. No other column is a model input except CallerID where stated.

## Folds and draws
- core.make_folds: 7 folds stratified by caller x receiver (strata in sorted order; each stratum's calls shuffled and dealt round-robin from a random starting fold).
- Real statistic: mean accuracy over 100 fold draws, draw s (s = 0..99) using numpy default_rng([20261118, s]) for its folds and for every random choice made in that draw. Every model below is scored on the SAME 100 fold draws (folds computed from the real labels).

## Models
- habit: the bank's caller-habit baseline (core.habit_predict): most frequent receiver of the call's true caller in the training folds, ties at random, the overall most frequent receiver as fallback.
- rf (lens paper-rf; partial win p3): core.rf_predict, the paper's ranger forest re-implemented with scikit-learn trees: 500 trees, 6 features per split, leaf size 1, no depth limit, each tree on floor(0.6 n) training calls drawn without replacement, majority vote with random ties; spectral features only; caller not an input.
- pa (lens prior-acoustic; full win): core.pa_pipeline. Candidate receivers of a test call = the receivers its caller addressed in the training folds (none: overall most frequent, ties at random; one: that one). Score(r) = log(1 + n_caller,r) + lambda * A(r), where A(r) is minus the RMS z-score distance (z-scores from the training folds) from the test call to the caller's training calls addressed to r: the nearest one (family nn) or their mean (family centroid). lambda in {0, 0.25, 0.5, 1, 2, 4, 8}; feature set in {spectral, cepstral}. lambda = 0 is exactly the caller-habit rule. The combination is chosen per outer fold by leave-one-fold-out over the six training folds (summed inner accuracy; ties to the smaller lambda, then spectral before cepstral, nn before centroid). Nothing about the test fold is used.

## Criteria (target.md), as decided here
Full win (lens prior-acoustic), all three on the 100 real draws:
1. mean accuracy of pa STRICTLY GREATER than 0.295;
2. mean accuracy of pa minus mean accuracy of habit on the same draws >= 0.02;
3. mean accuracy of pa STRICTLY GREATER than the 99.9th percentile (numpy linear interpolation) of 1,000 within-caller shuffled reruns. Rerun j (j = 0..999), rng default_rng([20261118, 1, j]): receiver labels permuted among each caller's calls (core.shuffle_within_caller), folds re-made from the shuffled labels with core.make_folds, and the whole pa pipeline (including the nested selection) run once; its accuracy is one control value. Each control is one fold draw, while the real statistic averages 100 draws: the single-draw spread is wider, so this is conservative.
Partial win p3 (lens paper-rf):
- |mean rf accuracy - 0.275| <= 0.02 on the 100 real draws;
- report the habit mean on the same draws and the 99.9th percentile of 1,000 rf reruns with within-caller shuffled labels ON THE SAME FOLDS: rerun j uses the fold assignment of real draw (j mod 100) and rng default_rng([20261118, 2, j]); state whether 0.275 and the rf mean exceed the habit mean and that percentile.

## Reported but not criteria (decided now)
- Bootstrap-free uncertainty: standard deviation over the 100 draws for every model; the paired difference pa - habit per draw (mean, minimum, number of draws where pa > habit).
- The combinations chosen in the 700 outer folds; the share of calls where pa and habit predict differently; accuracy on calls whose caller has 2+ receivers in training.
- Context check (bank pitfall): the same 100 draws repeated with folds stratified by caller x receiver x Context2, for habit and pa (rng default_rng([20261118, 3, s])).

## Compute and stopping
4 worker processes. Programs: code/run_real.py (all 100 real draws, habit, rf, pa), code/null_pa.py (1,000 pa controls), code/null_rf.py (1,000 rf controls), code/context_check.py. If a criterion fails, it is reported as failed; no model, grid or feature is changed after the real results are seen. Any later idea is a new, separately frozen version.
