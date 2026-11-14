# Pre-Registered Permutation Null Test — `plmfit-trastuzumab-cdrh3-binding-mcc`

- `target_id`: `plmfit-trastuzumab-cdrh3-binding-mcc`
- `controls`: 500
- `best_control`: 0.017453
- `real`: 0.421004
- `command`: `sh verify-it-yourself/run_checks.sh`
- `real_beats_all_controls`: yes

## 1. Protocol (`B = 500` Label Permutations on `N = 36,386` Test Sequences, `seed = 20261108`)

To confirm that both `Track B` (`trackB_cv_learned`) and `Track A` (`trackA_canonical`) exceed finite-sample label-permutation fluctuations across all `36,386` held-out multi-mutant test rows (`11,273` binders, `25,113` non-binders), we evaluated `B = 500` independent permutations of `binary_score` (`seed = 20261108`) against the 3-seed binary predictions stored in `object/seed_{42,43,44}_{trackB_cv_learned,trackA_canonical}_part{1,2}.csv`.

## 2. Permutation Null Summary (`object/certificate.json` -> `null_permutation_test`)

| Track | Evaluated Test Rows ($N$) | Observed 3-Seed `MCC` (`real`) | Null Mean `MCC` | Null SD `MCC` | Max Null (`best_control`) | Min Null | $Z$-Score | Controls Beaten | Empirical $p$-Value |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`Track B` (`trackB_cv_learned`, Claimed Full Win)** | `36,386` | **`0.421004`** | `0.000206` | `0.005140` | **`0.017453`** | `-0.016056` | **`+81.86`** | **`500 / 500`** | **`0.001996`** |
| **`Track A` (`trackA_canonical`, Parameter-Free Law)** | `36,386` | **`0.408391`** | `0.000256` | `0.005296` | **`0.019330`** | `-0.016084` | **`+77.07`** | **`500 / 500`** | **`0.001996`** |
