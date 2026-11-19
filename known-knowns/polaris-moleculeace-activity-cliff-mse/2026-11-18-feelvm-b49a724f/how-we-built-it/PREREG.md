# PREREG — polaris-moleculeace-activity-cliff-mse, primary target moleculeace-chembl2835-ki

Frozen 2026-11-18T00:52Z (before any test-set read; no test evaluation has happened at freeze time).

## Criterion (verbatim, from bank/target.md)

"Pick one named MoleculeACE benchmark (full Polaris slug). Success means a saved prediction file (one
predicted y per test molecule, in the official test order, with the benchmark slug, the sha256 of the
MoleculeACE CSV used, and the exact test-row indices) such that (a) the test set is EXACTLY the rows with
split=='test' in the public MoleculeACE CSV for that target and the label column is the same 'y' column
(log10-transformed nM) the Polaris benchmark uses, with the Polaris train/test counts from
https://polarishub.io/api/v1/benchmark/molecularml/<slug> matching, (b) the skeptic's own
sklearn.metrics.mean_squared_error on that file is strictly LOWER (direction: min) than EVERY
mean_squared_error listed in the leaderboard table at https://polarishub.io/benchmarks/molecularml/<slug>,
re-fetched live immediately before claiming, (c) the margin is at least 5% relative to the current best AND
a paired bootstrap over test molecules (10,000 resamples, same resamples for both prediction sets where
the attacker's and a reproduced baseline's predictions are available; otherwise 10,000 resamples of the
attacker's squared errors) puts the attacker's MSE below the listed best in at least 95% of resamples, and
(d) no test molecule, nor any molecule with the same InChIKey (ignoring stereo) as a test molecule,
appeared in training, and no label for a test molecule was looked up from ChEMBL or any other source. The
model must be fit on the official train split only; multi-target transfer is allowed only from OTHER
MoleculeACE targets' train splits and must be declared, with the union checked for test-molecule leakage."

Partial win p1 (the one this run attacks first): "The same strict improvement (live-refetched, >=5%
relative, bootstrap-confirmed) on any ONE of the 28 single-entry benchmarks."

## Named benchmark

moleculeace-chembl2835-ki (CHEMBL2835_Ki.csv, JAK1). CSV: molML/MoleculeACE main
MoleculeACE/Data/benchmark_data/CHEMBL2835_Ki.csv (sha256 recorded in data/csv_sha256.txt at fetch).
Official split: 489 train / 126 test rows from the CSV 'split' column; Polaris API nTrainDatapoints 489
(fetched 2026-11-18T00:36Z, matches).

## Statistic and exact checker

sklearn.metrics.mean_squared_error(data.y_test, y_hat) on the 126 rows with split=='test' in CSV file
order, label column 'y'. Paired bootstrap: 10,000 resamples (numpy Generator seed 20261118), resampling
test-row indices with replacement; fraction of resamples with attacker MSE < listed best must be ≥ 0.95.
Listed best value at freeze time: 0.16617421498738597 (autosota-moleculeace-chembl2835-ki, sole entry,
fetched live 2026-11-18T00:33Z; re-fetched immediately before any claim).

## Thresholds (frozen)

1. mse < 0.16617421498738597 (strictly lower than every listed entry), AND
2. mse ≤ 0.157865 (= 0.95 × listed best, ≥5% relative margin), AND
3. bootstrap fraction ≥ 0.95, AND
4. InChIKey (stereo-stripped) disjointness: no train-universe molecule (JAK1 train rows + declared
   borrowed rows from OTHER MoleculeACE targets' train splits) shares a stereo-stripped InChIKey with any
   test row, verified in code before the claim, AND
5. null test passes: the frozen final recipe, retrained 400 times with train labels shuffled (test labels
   untouched, seed sequence 20261118+k), MSE on test beats EVERY control (400/400 worse than the real run).
   null_test: required.
6. Test-read budget: model/hyperparameter selection ONLY on out-of-fold train CV (5-fold, seed 20261118).
   Declared test reads, all reported in the report: (i) step-3c baseline reproduction reads (RF/ECFP and
   SVM/ECFP paper recipes, expected RMSE 0.3876 / 0.420-ish from the paper's corrected results CSV and
   GraphCliff's independent run); (ii) at most THREE frozen-recipe candidate reads, each pre-declared in the
   attempt NOTES with its OOF-CV evidence BEFORE the read. No other test reads. If no candidate clears
   thresholds 1-3, the outcome is negative, honestly reported.

## Baseline gate (step 3c)

Baseline: MoleculeACE paper's own per-target result for CHEMBL2835_Ki, RF/ECFP RMSE 0.3876 (mean over the
paper's optimized-config runs; source data/MoleculeACE_results.csv = the corrected-data results shipped in
the repo, consistent with the 2023 erratum). Code basis: molML/MoleculeACE benchmark config + our faithful
RDKit ECFP implementation (bit count/radius/hyperparameters mirrored from the repo config where available).
Tolerance: our reproduced RMSE within 0.349–0.426 (±10% relative) = reproduced; a miss is a finding, never
retuned to pass. SVM/ECFP secondary baseline: paper RMSE 0.420-ish expected (0.4199 from results CSV, to
be read from the file in the baseline script, not from memory).

## Fallback (pre-declared)

If JAK1 candidates fail the thresholds, the run may (a) attack p1 on a second single-entry target chosen by
the OOF-CV evidence (CHEMBL4616_EC50 or CHEMBL218_EC50, where paper-best also beats the listed best), with
the same protocol and one prereg amendment note (PREREG.v2.md) written before that target's first test
read, or (b) record a negative result. No silent target hopping.

## Novelty comparison to be re-checked live at claim time

Leaderboard table (live), MoleculeACE corrected results CSV (RF/ECFP 0.3876 → MSE 0.150236), GraphCliff
per-target table (0.396), MAPCliff-WMGR source data (ACS, human to check if paywalled).
