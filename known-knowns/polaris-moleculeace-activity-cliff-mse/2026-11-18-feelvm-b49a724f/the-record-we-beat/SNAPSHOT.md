# The record we beat (snapshots)

## 1. The comparison bar of partial win p2: the repo's own best model for this target

The MoleculeACE benchmark paper ships its corrected per-target results as a public CSV:

- URL: https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/results/MoleculeACE_results.csv
- fetched: 2026-11-18T00:37:28Z, HTTP 200 (single honest GET)
- file sha256 at fetch: 6aa88c897f16bbb328793a2917289e3972b3fc8b50cc56be840f6714ea9baae5;
  the extracted cell is quoted below; the CSV itself is NOT copied into this package.
- extracted rows (CHEMBL244_Ki, sorted by rmse):
  - CHEMBL244_Ki,SVM,ECFP,rmse 0.7152,cliff_rmse 0.7966  ← the repo's own best model for this
    target (best overall AND best cliff; asserted by sorting all 24 rows) — THE BAR
  - CHEMBL244_Ki,GBM,ECFP,rmse 0.7361,cliff_rmse 0.8208
  - CHEMBL244_Ki,RF,ECFP,rmse 0.7407,cliff_rmse 0.8231
  - … (22 further rows, all worse)
- Our faithful rerun of that exact config (SVR, C=10, epsilon=0.1, gamma=0.01, rbf, Morgan
  ECFP r=2 1024 bits — repo file Data/configures/benchmark/CHEMBL244_Ki/SVM_ECFP.yml,
  fetched 2026-11-18T03:0xZ, HTTP 200): overall RMSE 0.715157 (paper 0.7152), cliff RMSE
  0.796601 (paper 0.7966) — reproduced within 0.0002 / 0.00001; deterministic.
- Claim vs bar: cliff-subset MSE 0.5501943375378687 < 0.634573831368627 (−13.3%);
  non-cliff 0.33343039149183445 ≤ 0.39931062625682384 (better).

## 2. Context: the Polaris leaderboard cell (NOT the p2 bar; p1 was attempted and failed)

- URL: https://polarishub.io/benchmarks/molecularml/moleculeace-chembl244-ki
- fetched: 2026-11-18T00:33Z (survey) and re-fetched live 2026-11-18T03:41:00Z (single honest
  GET both times, HTTP 200)
- page sha256 of the 03:41Z fetch: 251d2bf0582c592ac90b772bf0174e1ebfd8c28f75df9b82df4a96ba825948a4
- extracted cell: exactly one listed entry, autosota-moleculeace-chembl244-ki,
  mean_squared_error 0.4749981512616306
- our object's overall test MSE 0.43675104854437247 is lower (−8.05%) but the p1 criterion
  (≥95% bootstrap fraction) was NOT met by the same frozen predictions (bootstrap fraction
  0.8739, 10,000 resamples, seed 20261118) — p1 is NOT claimed. No page content is copied here.

## 3. Context: nearest published per-target value on the same split

- GraphCliff (arXiv 2511.03170v2, fetched 2026-11-18T00:5xZ, HTTP 200; PDF sha256
  4d49e25bb5369f94616b3d8b0b58da2b90c0822282238024ac274c8fdc50938d): Table 5 part 2/3,
  CHEMBL244 (Ki) column —
  best overall RMSE 0.668 / cliff RMSE 0.752 (their method; their SVM/ECFP row 0.715 / 0.797
  matches the paper row). Our object: overall RMSE 0.6609 / cliff RMSE 0.7418 — better than
  both. Not the p2 bar, recorded for the novelty comparison.
- MAPCliff-WMGR (doi 10.1021/acs.jcim.5c01915): per-target source data behind an ACS bot
  challenge (HTTP 403 on a single honest GET at 2026-11-18T02:3xZ; not retried, never bypassed).
  Unverifiable here; flagged for a human check by hand.
