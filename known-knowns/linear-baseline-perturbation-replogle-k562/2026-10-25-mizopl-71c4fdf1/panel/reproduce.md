# Reproducibility Review (`reproduce.md`)

- Context: fresh skeptic review of the packaged files only
- Target: `linear-baseline-perturbation-replogle-k562` (`known-knowns`, Partial Progress `p2` only)
- Package path: `known-knowns/linear-baseline-perturbation-replogle-k562/2026-10-25-mizopl-71c4fdf1`

## 1. Plain-Text Per-Perturbation Predictions & Distances (`object/`)

1. Inspected `object/certificate_replogle_k562.json` (`54,328` bytes, `sha256: f7a404a7891275367e46e7e312084b42ce4e687274d7b72da6da4aa4f2794b5a`), `object/k562_p2_per_perturbation_metrics.tsv` (`176,975` bytes, `sha256: 0e2ae30e6f9f0942b4adf46e9a2798d74206321ddb13b8dc4027f2c0a6fdfd75`), and the 15 split-level plain-text top-1,000 gene expression TSVs (`object/k562_seed{1..5}_{dual,lpm}_predictions.tsv` and `object/k562_seed{1..5}_observed_top1000.tsv`, each `< 960,000` bytes).
2. Verified that every held-out K562 perturbation of each reported split (`seed 1`: `136` in-readout perturbations including `134` Panel A rows; `seed 2`: `134` in-readout perturbations including `128` Panel A rows; `seed 3`: `135`; `seed 4`: `135`; `seed 5`: `137`; `677` total across `seeds = 1..5`, `262` in Panel A `seeds = 1..2`) is keyed by `perturbation` ID, appears **exactly once** per split file, and carries its nearest training perturbation ID (`nearest_train_pert` and `nearest_train_pert_go_only`), nearest-neighbor distance (`nn_dist` and `nn_dist_go_only`), and `1,000` top-expressed gene predictions.
3. Confirmed that copied Source Data tables have been removed and replaced with upstream URLs and 64-hex SHA-256 digests (`single_perturbation_prediction.xlsx` `sha256: 09c6c198aff4e8a827064183f9cff13eb6f33e56f1689940527304bf78957efe`, `suppl-pearson_delta_performance_single_pert.xlsx` `sha256: 61658661412f385356a383c3ed506f4454c6db79b28c272151bb15a725b0faaa`, `gene2go_all.pkl` `sha256: f145c5e84a53048d87942a417d870a4f2d8db50200b96e492b358c13aba8c771`, and `replogle_k562_essential/perturb_processed.h5ad` `sha256: 550fde89ac85c258c9fd517638fe34fb42c0e748c9305fe6355761a2bb754170`), and the duplicate `the-record-we-beat/table_status.md` has been removed.

## 2. Standalone Verification & Negative Controls (`verify-it-yourself/run_checks.sh`)

Executed `sh verify-it-yourself/run_checks.sh`:
1. **Positive check**: `verify.py` parsed `object/certificate_replogle_k562.json`, recomputed all `677` per-perturbation $L_2$ errors and Pearson $R_{\Delta}$ correlations directly from the plain-text 1,000-gene TSVs (`k562_seed{1..5}_{dual,lpm}_predictions.tsv` against `k562_seed{1..5}_observed_top1000.tsv`), verified exact agreement with `k562_p2_per_perturbation_metrics.tsv`, and recomputed all `p2` quartile means, Spearman rank correlations, and paired Wilcoxon tests (`exit code 0`).
2. **Negative check 1 (corrupted certificate)**: Perturbing `l2_mean` by `+5.0` in a temporary copy of `certificate_replogle_k562.json` caused `verify.py` to fail with a non-zero exit code (`exit code 1`).
3. **Negative check 2 (corrupted plain-text prediction TSV)**: Perturbing a single predicted gene expression value by `+5.0` in a temporary copy of `k562_seed1_dual_predictions.tsv` caused `verify.py` to fail with a non-zero exit code (`exit code 1`).

pass: true
