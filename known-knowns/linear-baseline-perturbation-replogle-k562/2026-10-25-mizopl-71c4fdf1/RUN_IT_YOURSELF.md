# Run It Yourself (`RUN_IT_YOURSELF.md`)

## 1. Fast Standalone Verification of Saved Plain-Text Predictions (`~3s`)

From the package root (`known-knowns/linear-baseline-perturbation-replogle-k562/2026-10-25-mizopl-71c4fdf1/`):

```sh
sh verify-it-yourself/run_checks.sh
```

This executes `verify-it-yourself/verify.py` against `object/certificate_replogle_k562.json` and the 16 plain-text TSVs in `object/`:
- Verifies that every held-out K562 perturbation across all 5 splits (`seed = 1..5`, `n = 677` in-readout perturbations; `n = 262` Panel A perturbations in `seeds = 1..2`) appears keyed by `perturbation` ID, each once per split, in `object/k562_seed{1..5}_{dual,lpm}_predictions.tsv` with its nearest training perturbation ID and functional distance (`nn_dist` and `nn_dist_go_only`).
- Recomputes all `677` per-perturbation $L_2$ errors and Pearson $R_{\Delta}$ correlations directly from the plain-text 1,000-gene predicted expression matrices against `object/k562_seed{1..5}_observed_top1000.tsv`.
- Recomputes all `p2` functional-distance quartile tables (`Q1_closest` .. `Q4_farthest`), Spearman rank correlations, and paired Wilcoxon tests from `object/k562_p2_per_perturbation_metrics.tsv`.
- Runs two negative-control corruption checks (corrupting `certificate_replogle_k562.json` and corrupting `k562_seed1_dual_predictions.tsv`) and verifies that `verify.py` exits non-zero on both.

---

## 2. Optional Full Raw-Data Regeneration (`~4.2 min`)

If you wish to regenerate `object/certificate_replogle_k562.json` and all 16 plain-text TSVs in `object/` from the upstream Harvard Dataverse archives and Source Data:

1. Download the upstream files listed in `the-record-we-beat/PAPER_NUMBERS.md` into a local `./data` directory:
   - `./data/single_perturbation_prediction.xlsx` (`sha256: 09c6c198aff4e8a827064183f9cff13eb6f33e56f1689940527304bf78957efe`)
   - `./data/suppl-pearson_delta_performance_single_pert.xlsx` (`sha256: 61658661412f385356a383c3ed506f4454c6db79b28c272151bb15a725b0faaa`)
   - `./data/gears_pert_data/gene2go_all.pkl` (`sha256: f145c5e84a53048d87942a417d870a4f2d8db50200b96e492b358c13aba8c771`)
   - `./data/gears_pert_data/essential_all_data_pert_genes.pkl` (`sha256: 46c3dfe354d8ad5c0da22c69f3d0ca451987b1a61ed9d984279b22b9565ff8d7`)
   - `./data/gears_pert_data/go_essential_all/go_essential_all.csv` (`sha256: 99622d9215462e7bbea99a5f6c0b1e86febfef9f57226269418053484fcb3f9f`)
   - `./data/gears_pert_data/replogle_k562_essential/perturb_processed.h5ad` (`sha256: 550fde89ac85c258c9fd517638fe34fb42c0e748c9305fe6355761a2bb754170`)
2. Run the certification and export script:
   ```sh
   REPLOGLE_DATA_DIR=./data python3 how-we-built-it/certify_all_splits_and_controls.py
   ```
