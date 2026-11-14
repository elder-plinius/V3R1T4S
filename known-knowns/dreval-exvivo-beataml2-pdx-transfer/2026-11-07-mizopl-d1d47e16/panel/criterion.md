# Skeptic 3: Target Criterion & Anti-Leakage Review — `dreval-exvivo-beataml2-pdx-transfer` (`p3`)

context: independent check of target criteria and p3 transfer-gap decomposition
target_id: dreval-exvivo-beataml2-pdx-transfer
package: 2026-11-07-mizopl-d1d47e16

## Checks Performed

1. **Primary, `p1`, and `p2` Criteria (Not Claimed):**
   - Primary criterion requires 10-split mean `R2_norm >= 0.02` on `BeatAML2` across all evaluated rows (`N = 19,823`). Unadjusted `SchurBilinearExVivoDRP` achieves `R2_norm = -0.09514 +- 0.00706` on all `19,823` rows (`+0.01186 +- 0.00550` on the `79` shared drugs, `N = 11,901`), so the primary criterion is not met.
   - `p1` (`BeatAML2` `Pearson_norm`): unadjusted `SchurBilinearExVivoDRP` achieves `+0.08461 +- 0.00873`, which is below same-environment `RandomForest_SameEnv` (`+0.23218 +- 0.00657`).
   - `p2` (`PDX_Bruna` `Pearson_norm`): unadjusted `SchurBilinearExVivoDRP` achieves `+0.10046 +- 0.01842`, which is below same-environment `GradientBoosting_SameEnv` (`+0.13012 +- 0.01639`).
2. **`p3` Criterion & What-Does-Not-Count Guardrails:**
   - Audited `how-we-built-it/stage3_exvivo_and_cross_study_eval.py`, `object/certificate.json`, and `object/stage3_p3_gap_decomposition.json` to confirm that **zero** `BeatAML2` or `PDX_Bruna` response values (`y_true` / `LN_IC50_curvecurator`) are used for training, fine-tuning, hyperparameter selection, response-scale calibration, or row filtering (`|y_true| <= 10` is completely removed).
   - Verified that each of the three factors `(i)`, `(ii)`, and `(iii)` is applied **on its own** to the exact same `SchurBilinearExVivoDRP` predictions on all `19,823` `BeatAML2` rows and all `1,046` `PDX_Bruna` rows, as well as cumulatively (`Step 0 -> Step 1 -> Step 2 -> Step 3`), and that every number in `README.md`, `HOW_WE_FOUND_IT.md`, `INDEX.csv`, `null_test.md`, and `the-record-we-beat/record.md` matches `object/certificate.json` and `object/stage3_p3_gap_decomposition.json` digit-for-digit.

pass: true
