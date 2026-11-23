# Claim

**One sentence:** On the official MoleculeACE activity-cliff split of CHEMBL244_Ki (Polaris
benchmark `moleculeace-chembl244-ki`, coagulation factor X), the prediction file
`result/M1_predictions.json` (6-member SVR ensemble, frozen recipe in `result/spec_m1.json`,
trained on the official 2476-row train split only) achieves mean_squared_error 0.5501943375378687
on the 296 test molecules with cliff_mol==1, which is strictly lower than the 0.634573831368627
of the faithfully reproduced repo-config SVM/ECFP baseline (`result/B_predictions.json`,
C=10, epsilon=0.1, gamma=0.01, rbf, ECFP radius 2 / 1024 bits — the repo's own best
descriptor+model for this target), while being better (not worse) on the 325 non-cliff test
molecules (0.33343039149183445 vs 0.39931062625682384).

**Target id:** polaris-moleculeace-activity-cliff-mse · **Partial win claimed:** p2

**Criterion (verbatim, from the bank entry `polaris-moleculeace-activity-cliff-mse`):**

> p2: "A cliff-subset result: on one target, lower MSE than a faithfully reproduced MoleculeACE
> paper baseline (the repo's own best descriptor+model for that target, run by the attacker and
> reported with its code) restricted to the test molecules with cliff_mol==1, with at least 40
> such molecules, while not being worse on the non-cliff subset."

**Scope guards (verified in code, see REPRODUCE.md):**
- Test set = rows with split=='test' in CHEMBL244_Ki.csv, exactly the Polaris API split[1]
  index list (2476 train / 621 test; 296 cliff test >= 40).
- Label column 'y' as Polaris targetCols defines; CSV sha256
  b296c5956c9b3659fa039f057ebcb617919acd759c9255ed72bee917d99b4ef2.
- No test molecule shares a stereo-stripped InChIKey with any train molecule.
- The recipe uses only CHEMBL244_Ki train rows (no other target's data, no ChEMBL lookups,
  no label-derived cliff_mol used as input feature; cliff_mol is only the subset mask).
- All model selection was out-of-fold on train (5-fold, seed 20261118); test reads used:
  1 baseline read + 1 candidate read (+400 null-test label-shuffle controls per PREREG.v2 §4).

**Objects:**
- `result/M1_predictions.json` — 621 predicted y, official test order, slug + csv sha + indices
- `result/spec_m1.json` — the frozen recipe (members, weights, combiner)
- `result/B_predictions.json` — the baseline's predictions (same format)
- `output/M1_read_result.json`, `output/null_test_244.json` — machine-readable verdicts
- `baseline/baseline_B_chembl244.json` — step-3c baseline record (expected values from the
  paper's corrected results CSV, tolerance, reproduced status)
- `data/CHEMBL244_Ki.csv` — the exact CSV used (public, molML/MoleculeACE main)
- `data/MoleculeACE_results_CHEMBL244_rows.csv` — the paper's corrected per-target results rows
- `verify/verify_p2.py` — standalone checker written from the definition
- `REPRODUCE.md` — exact commands (integrity, baseline, M1 retrain, verifier, null test)

**Scout's table record:** Polaris leaderboard
https://polarishub.io/benchmarks/molecularml/moleculeace-chembl244-ki fetched twice:
2026-11-18T00:33Z and re-fetched live 2026-11-18T03:41Z (HTTP 200 both, page sha256
251D2BF0582C592AC90B772BF0174E1EBFD8C28F75DF9B82DF4A96BA825948A4 for the refetch) —
listed entries: exactly 1 (autosota-moleculeace-chembl244-ki, mean_squared_error
0.4749981512616306). NOTE: the p2 criterion does NOT
compare against this leaderboard; the comparison bar is the reproduced repo-config baseline
(paper row: CHEMBL244_Ki / SVM / ECFP, rmse 0.715, cliff_rmse 0.797, from
https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/results/MoleculeACE_results.csv).
For context only: the read-per-target literature on this split and subset —
MoleculeACE paper SVM/ECFP cliff RMSE 0.797 (the baseline),
GraphCliff (arXiv 2511.03170v2, Nov 2025) best on 244: overall RMSE 0.668 / cliff RMSE 0.752
(our M1: overall 0.6609 / cliff 0.7418 — better than both);
MAPCliff-WMGR (JCIM 10.1021/acs.jcim.5c01915) per-target source data behind an ACS bot check
(HTTP 403 on honest GET, not retried) = PENDING TABLE CHECK, human to check by hand.

**Status source for NOVELTY:** https://polarishub.io/benchmarks/molecularml/moleculeace-chembl244-ki
