# Independent re-implementation of MassBalanceMachine's Norway test RMSEs (partial win p3)

## What

Code of the claimant's own (record building from the shipped ML_MB_Norway CSVs at commit 32d8175, the 14-BREID test split, the repository's test-only 9.99 winter-record rule, the summed-monthly aggregated-MSE objective and the per-season record scorer), retrained only on the 18 training glaciers with xgboost 3.2.0, MBM's published hyperparameters and base_score 0.5, gives test RMSEs Ba 0.9962 (n 1065), Bw 0.5881 (n 999) and Bs 0.7001 (n 1028) m w.e., within 0.01 of notebook 3.1.1's printed 1.00 / 0.59 / 0.70 and within 1e-7 of the shipped MBM booster scored the same way, which meets bank partial win p3 and nothing wider (not p1, p2, the full criterion or MBM's hyperparameter selection).

Target: `massbalancemachine-norway-test-glaciers-rmse`, partial win p3 only: "Reproduce MBM's three test RMSEs
within 0.01 m w.e. from the shipped CSVs with an independent re-implementation (validates the split and scorer)."

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. It takes a few seconds and needs only the Python standard library. It recomputes the three
RMSEs from object/test_record_predictions_primary.csv and checks the counts, the 0.01 tolerance, the values the
re-implementation printed and the file's sha256. To rebuild the object from the shipped data (about a minute with xgboost 3.2.0), see
RUN_IT_YOURSELF.md.

## Compared to

| what | Ba (n) | Bw (n) | Bs (n) | source | fetched |
|---|---|---|---|---|---|
| MBM, published (notebook 3.1.1 cell 36) | 1.00 (1065) | 0.59 (999) | 0.70 (1028) | https://github.com/khsjursen/ML_MB_Norway @ 32d8175 | 2026-11-08T17:30:39Z |
| this re-implementation | 0.9962 (1065) | 0.5881 (999) | 0.7001 (1028) | object/, how-we-built-it/ | |
| shipped MBM booster, scored by our scorer | 0.9962 | 0.5881 | 0.7001 | how-we-built-it/output/primary_output.txt, check (b) | |

The details of the fetch are in the-record-we-beat/record.md.

## Not claimed

- No claim on p1, p2 or the full criterion. The re-implementation is MBM's own configuration, not a better model.
- It shares the xgboost library and MBM's hyperparameters. It does not re-implement gradient boosting itself.
- The match depends on xgboost's histogram method: tree_method exact misses the tolerance (how-we-built-it/output/lens2_output.txt).
- Grid configurations scored on the test glaciers in the robustness check (lens2_output.txt) are diagnostics. They
  are not claims.

## Credits

- Sjursen, Bolibar, van der Meer, Andreassen, Biesheuvel, Dunse, Huss, Maussion, Rounce and Tober, "Machine learning
  improves seasonal mass balance prediction for unmonitored glaciers", The Cryosphere 19:5801 (2025),
  https://tc.copernicus.org/articles/19/5801/2025/. Code and data: https://github.com/khsjursen/ML_MB_Norway.
- Stake mass-balance data: NVE (Elvehoy et al. 2025, https://doi.org/10.58059/sjse-6w92). Climate features: ERA5-Land.
- xgboost: https://github.com/dmlc/xgboost.
- V3R1T4S PR #1022 (another contributor) reproduced MBM by scoring the shipped model in its p2 package.
  This package re-implements and retrains MBM.
- Credit name for this package: SapereAudeAI.
