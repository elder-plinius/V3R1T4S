# Skeptic 3 — Target Criterion & Isolated `p3` Decomposition Audit (`dreval-cross-study-ctrpv2-to-gdsc2`)

- reviewer: Criterion & Rigor Skeptic (`criterion`)
- context: fresh independent skeptic review session (zero shared context)
- target_id: `dreval-cross-study-ctrpv2-to-gdsc2`
- submission_id: `2026-10-29-mizopl-f732aed6`
- internal_panel_verdict: `CONFIRMED_PARTIAL` (`partial_win: p3`)

## 1. Audit of Partial Win `p3` Criterion

The target file `known-unknowns/disease-research/dreval-cross-study-ctrpv2-to-gdsc2.md` defines `p3` as:
> **p3:** Measured decomposition of the CTRPv2 -> GDSC2 transfer gap into contributions from (i) concentration-range differences, (ii) cell-line overlap differences, and (iii) response-scale calibration, by re-scoring the SAME predictions after each correction, showing which single correction closes the most gap.

Verified that `object/stage3_p3_gap_decomposition.json`, `README.md`, `HOW_WE_FOUND_IT.md`, `how-we-built-it/artifact.md`, and `verify-it-yourself/verify.py`:
1. Apply `(i)` concentration-range restriction, `(ii)` cell-line overlap restriction, and `(iii)` response-scale calibration **each in isolation on the exact same `SchurBilinearExVivoDRP` predictions** (and in parallel on `RandomForest_SameEnv` and `RawPlatformKRR_Ablation`) with the official `y_pred_naive` and `SS_tot = sum(((y - y_naive) - mean(y - y_naive))^2)` denominator held fixed.
2. Explicitly state which mechanism closes the most gap:
   - **Across all `40,292.4` rows/split:** **Mechanism `(iii)` (response-scale / assay-offset calibration, fitted on GDSC2 labels)** is the largest full-dataset contributor (`+0.42333` `R2_norm` from `-0.42457` to `-0.00124 ± 0.00758` for 1-parameter additive offset calibration, closing `99.71%` of the gap to zero and `71.02%` of the `0.59610` gap to `CTRPv2 LCO`, `MSE = 4.48488`; `+0.43342` to `+0.00885 ± 0.00760` for 2-parameter linear OLS calibration; `+0.44239` to `+0.01781 ± 0.00353` for 2-parameter affine residual calibration).
   - **Among label-free restrictions using zero GDSC2 labels:** **Mechanism `(i-a)` (in-window concentration-range restriction `ln(min_dose_uM) <= y_pred <= ln(max_dose_uM)`, `19,118.6` rows/split)** is the largest contributor (`+0.46402` `R2_norm` to `+0.03945 ± 0.01189`, closing `109.29%` of the gap to zero and `77.84%` of the gap to `CTRPv2 LCO`, `MSE = 2.63072` [`-58.77%`], `Pearson_norm = +0.36026`).
   - **Smallest contributor:** **Mechanism `(ii)` (cell-line overlap restriction, `5,345.4` rows/split)** closes only `+0.01346` `R2_norm` (`-0.41111` vs `-0.42457`, `3.17%` of the gap to zero).
3. Explicitly note wherever any calibration parameter or subset filter uses GDSC2 labels.
4. Scope the entire package (`object/` and `how-we-built-it/`) strictly to `dreval-cross-study-ctrpv2-to-gdsc2`.

pass: true
