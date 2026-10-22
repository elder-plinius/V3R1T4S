# Gate Decision: `polaris-moleculeace-activity-cliff-mse`

target_id: polaris-moleculeace-activity-cliff-mse
category: drug-discovery
reproduce_pass: true
novelty_pass: true
criterion_pass: true
confirmed_scope: A single fixed, deterministic, CPU-only CLSS recipe (claim/run_clss_moleculeace.py) fit strictly on stereo-stripped InChIKey[:14]-disjoint training splits (overlap == 0 across all 30/30 benchmarks) achieves test MSE 0.40802135 on moleculeace-chembl287-ki (claim/CHEMBL287_Ki_test_predictions.csv, sha256 05d8ae3a3797f666ed320364280c2ba0c099417174d42a0a4736f0366726623c, n_train = 1,061, n_test = 267, n_cliff = 103) vs live Polaris best 0.50318131 (-18.9117% relative) and MoleculeACE paper best 0.51009699 (-20.0110% relative) with 99.97% paired bootstrap win rate vs reproduced SVM+ECFP and 97.98% scalar bootstrap win rate vs Polaris best across 10,000 resamples (seed=0), while lowering cliff_mol==1 MSE (n = 103, at least 40) to 0.50213600 vs paper best 0.61875106 (-18.8468%) and non-cliff MSE to 0.34891276 vs 0.41681673 (-16.2911%, p2), and beating live Polaris best MSE on 29/30 MoleculeACE benchmarks (21/30 with at least 5% relative margin and at least 95% bootstrap win rate, p3) with 30-target macro-average cliff RMSE 0.7211 (overall RMSE 0.6303).

## Panel Summary

1. **REPRODUCE (`panel/reproduce.md`, `pass: true`):**
   - Wrote an independent standalone checker from the verbatim definition before inspecting `claim/author_checker_moleculeace.py` or `claim/run_clss_moleculeace.py`.
   - Verified all file sizes and `sha256` checksums (`claim/CHEMBL287_Ki_test_predictions.csv` `sha256: 05d8ae3a3797f666ed320364280c2ba0c099417174d42a0a4736f0366726623c`, `claim/CHEMBL287_Ki_manifest.json` `sha256: 5d7e9e04e787fb7c746f422bc530aad8d3d00561244f4d7c94562640f1be90b4`, `claim/moleculeace_30_sweep_manifest.json` `sha256: 42c12361b8406c2530934bbed45a1acf701e4e03b50514a44f1dd056c17405e8`, and all 30 benchmark and prediction CSVs).
   - Verified 100% alignment of `split == 'test'` rows, `y` (`log10(nM)`), Polaris API counts, and RDKit stereo-stripped `InChIKey[:14]` disjointness (`overlap == 0` across all `30 / 30` benchmarks).
   - Verified `CHEMBL287_Ki` test MSE = `0.40802135` (`-18.9117%` vs Polaris `0.50318131`, `-20.0110%` vs Paper `0.51009699`), `99.97%` paired bootstrap and `97.98%` scalar bootstrap win rates, Cliff MSE = `0.50213600` (`-18.8468%` vs Paper `0.61875106`), and double end-to-end CPU retraining determinism (`max_abs_diff = 4.441e-16`).

2. **NOVELTY (`panel/novelty.md`, `pass: true`):**
   - Performed single honest HTTP `GET` fetches of the live Polaris API (`https://polarishub.io/api/v1/benchmark/molecularml/moleculeace-chembl287-ki`) and live Polaris leaderboard pages (`moleculeace-chembl287-ki`, 3-entry `moleculeace-chembl234-ki`, 3-entry `moleculeace-chembl236-ki`, `moleculeace-chembl219-ki`, `moleculeace-chembl204-ki`, `moleculeace-chembl244-ki`), confirming our `0.40802135` strictly beats the listed record `0.50318131` on `moleculeace-chembl287-ki` and beats `29 / 30` live Polaris leaderboards.
   - Audited the last 24 months of literature (`Monroe` Aug 2026 `arXiv:2608.18982v1`, `MolPAIR` Sep 2026 `arXiv:2609.38744v1`, `GraphCliff` Aug 2026, `CheMeleon` Jun 2025 `arXiv:2506.15792v2`), confirming that our 30-target mean Activity-Cliff RMSE (`0.7211`) strictly beats `Monroe` (`0.737`), `CheMeleon_PFN` (`0.741`), `SVM+ECFP` (`0.7511`), and `GraphCliff` (`0.757`) with zero external pre-training.
   - Confirmed `0` occurrences in V3R1T4S `TROPHY_CASE.md` and `0 / 259` open pull requests (`#9`–`#567`).

3. **CRITERION (`panel/criterion.md`, `pass: true`):**
   - Verified every clause `(a)`–`(d)` of the full `success_criterion` and all three enumerated partial wins (`p1`, `p2`, `p3`) simultaneously, plus 400 label-permutation controls (`z = -13.61`), 400 prediction-shuffle controls (`z = -12.36`), 400 training-feature LOO KRR shuffle controls (`z = -11.37`), constant-mean negative controls (`1.0989`), and test-batch transductive invariance (`max_abs_diff = 0.0` on OOF).

status: CONFIRMED_SOLUTION
