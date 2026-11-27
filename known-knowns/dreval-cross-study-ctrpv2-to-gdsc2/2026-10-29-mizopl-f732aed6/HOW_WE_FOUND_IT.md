> *Note: contributor text, unverified — narrative explanation of how we found the result; all machine-verified claims live in `object/` and `verify-it-yourself/verify.py`.*

# How We Found It — Isolated `p3` Decomposition of the `CTRPv2 -> GDSC2` Transfer Gap

- **Target ID:** `dreval-cross-study-ctrpv2-to-gdsc2`
- **Submission ID:** `2026-10-29-mizopl-f732aed6`
- **Internal 3-Skeptic Panel Status:** `CONFIRMED_PARTIAL` (`partial_win: p3`)
- **Certificate (`object/certificate.json`) SHA-256:** `2b12c375e5851cdcccb0a617aaa10ffb61daca5e1fdd1d972984fe55658b0d69`
- **Official `GDSC2/GDSC2.csv` SHA-256:** `87c284eaf50c41e4ffd870220f67230b826068c3d08085a9a83caec62024bcbd` (<https://zenodo.org/api/records/23159774/files/GDSC2.zip/content>)

---

## 1. Why Unadjusted Cross-Study `R^2_norm` Is Negative on `CTRPv2 -> GDSC2`

In `drevalpy` (`drevalpy/evaluation.py`), normalized $R^2$ is computed against the `NaiveMeanEffectsPredictor` baseline $y_{\text{naive},i} = \mu_0 + \alpha_{\text{cell}(i)} + \beta_{\text{drug}(i)}$ fitted on the `CTRPv2` training fold:
$$R^2_{\text{norm}} = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}}, \qquad \text{SS}_{\text{res}} = \sum_{i=1}^N (y_i - \hat{y}_i)^2, \qquad \text{SS}_{\text{tot}} = \sum_{i=1}^N \Big((y_i - y_{\text{naive},i}) - \overline{(y - y_{\text{naive}})}_N\Big)^2$$

Notice the structural asymmetry between the numerator and denominator:
1. **Assay Scale & Offset Shift (Mechanism `iii`):** `CTRPv2` measures ATP luminescence (`CellTiter-Glo`), whereas `GDSC2` measures nucleic-acid fluorescence / metabolic reduction (`Syto60` / `Resazurin`). Across the `40,292.4` evaluated shared-drug pairs per split, the mean cross-study assay shift is $\Delta_{\text{assay}} = \overline{y_{\text{true}} - y_{\text{naive}}} = -0.88040\text{ ln}(\mu\text{M})$. Because $\text{SS}_{\text{tot}}$ subtracts $\Delta_{\text{assay}}$ while $\text{SS}_{\text{res}}$ does not, even `NaiveMeanEffectsPredictor` itself ($\hat{y} = y_{\text{naive}}$) incurs $\text{SS}_{\text{res}} = \text{SS}_{\text{tot}} + N \Delta_{\text{assay}}^2$ and scores $R^2_{\text{norm}} = -0.17305 \pm 0.00289$ (`MSE = 5.25449 ± 0.02253`). Furthermore, because `CTRPv2` includes `370` mostly inactive screening probes alongside the `118` active oncology drugs shared with `GDSC2`, models trained on all `CTRPv2` drugs inherit an upward drug-mean shrinkage bias (`mean(y_pred - y_naive) = +0.52841 ln(uM)`) on the `118` shared oncology drugs, bringing the total constant offset to $\overline{y_{\text{true}} - \hat{y}} = -1.40881\text{ ln}(\mu\text{M})$ (`42.33%` of $\text{SS}_{\text{tot}}$).
2. **Concentration-Range Truncation (Mechanism `i`):** `CTRPv2` screens compounds up to a median maximum concentration of `66.0 uM` ($\ln 66 = +4.19$), whereas `GDSC2` caps screening at a median maximum concentration of `10.0 uM` ($\ln 10 = +2.30$). Roughly half of `CTRPv2`-trained predictions (`21,173.8` of `40,292.4` rows/split) lie outside `GDSC2`'s tested dose window $[\ln d_{\min}, \ln d_{\max}]$.
3. **Cell-Line Overlap vs Disjoint Cell Lines (Mechanism `ii`):** Out of `47,296` shared-drug pairs in `GDSC2` (`509` cell lines $\times$ `118` shared drugs), each split excludes the `352–386` overlapping cell lines in that split's 90% `CTRPv2` training fold, leaving `40,292.4 ± 389.4` evaluated rows across `427–436` GDSC2 test cell lines (`52–61` held-out CTRPv2-overlapping cell lines [`5,345.4` rows/split] and `375` disjoint GDSC2-only cell lines [`34,947.0` rows/split]). Because `SchurBilinearExVivoDRP` projects each cell line's expression profile via within-sample van der Waerden normal scores + 35-Hallmark pathway activity, performance on disjoint GDSC2-only cell lines (`R2_norm = -0.42686`) is nearly identical to performance on overlapping CTRPv2 cell lines (`R2_norm = -0.41111`).

---

## 2. Unified Isolated `p3` Decomposition Table (Same Predictions, Fixed Official `SS_tot`)

| Mechanism Applied in Isolation on the Same Predictions | Uses GDSC2 Labels? | Rows / Split (Mean) | `SchurBilinearExVivoDRP` `R2_norm` (Mean `±` SD) | $\Delta R^2_{\text{norm}}$ vs Baseline | Gap to `0` Closed (`0.42457`) | Gap to `CTRPv2 LCO` Closed (`0.59610`) | `SchurBilinearExVivoDRP` `MSE` (Mean `±` SD) | `Pearson_norm` | `RandomForest` (`y_pred_rf`) `R2_norm` / `MSE` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Unadjusted, all evaluated test pairs)** | **No (0 params)** | `40,292.4` | `-0.42457 ± 0.02711` | `0.00000` | `0.00%` | `0.00%` | `6.38104 ± 0.11786` | `+0.13294` | `-0.64155` / `7.35283` |
| **`(i-a)` Concentration-Range: In-Window Predictions ($\ln d_{\min} \le \hat{y} \le \ln d_{\max}$)** | **No (label-free)** | `19,118.6` | **`+0.03945 ± 0.01189`** | **`+0.46402`** | **`109.29%`** | **`77.84%`** | **`2.63072 ± 0.03831`** | **`+0.36026`** | `-0.34128` / `3.74344` |
| **`(i-b)` Concentration-Range: Both $y_{\text{true}}$ and $\hat{y}$ Inside GDSC2 Tested Window** | **Yes (subset filter)** | `15,092.6` | `-0.26165 ± 0.02018` | `+0.16293` | `38.37%` | `27.33%` | `2.67210 ± 0.04841` | `+0.33574` | `-0.46761` / `3.58623` |
| **`(i-c)` Concentration-Range: Clamp $\hat{y}$ to GDSC2 Window $\text{clip}(\hat{y}, \ln d_{\min}, \ln d_{\max})$** | **No (label-free)** | `40,292.4` | **`+0.29926 ± 0.00492`** | **`+0.72383`** | **`170.49%`** | **`121.43%`** | **`3.13883 ± 0.02118`** | `+0.10796` | `+0.21942` / `3.49642` |
| **`(i-d)` Concentration-Range: Matched `max_dose` Shared Drugs ($|\log_{10}(d_{\max,\text{G}}/d_{\max,\text{C}})| \le \log_{10} 2$)** | **No (label-free)** | `267.9` | `-0.36227 ± 0.06663` | `+0.06230` | `14.67%` | `10.45%` | `2.01755 ± 0.04505` | `-0.02431` | `-0.98541` / `2.94037` |
| **`(ii-a)` Cell-Line Overlap: Restricted to Held-Out CTRPv2-Overlapping Cell Lines (`52–61` lines/split)** | **No (label-free)** | `5,345.4` | `-0.41111 ± 0.03577` | `+0.01346` | `3.17%` | `2.26%` | `6.30638 ± 0.16803` | `+0.13517` | `-0.57451` / `7.03713` |
| **`(ii-b)` Cell-Line Disjoint: Restricted to GDSC2-Only Cell Lines (`375` lines/split)** | **No (label-free)** | `34,947.0` | `-0.42686 ± 0.02678` | `-0.00229` | `-0.54%` | `-0.38%` | `6.39172 ± 0.11602` | `+0.13225` | `-0.65213` / `7.40050` |
| **`(iii-a)` Response-Scale Calibration: Additive Assay Offset $\hat{y} + c_0$ (`1` param/split)** | **Yes (1 param fit on GDSC2 $y$)** | `40,292.4` | **`-0.00124 ± 0.00758`** | **`+0.42333`** | **`99.71%`** | **`71.02%`** | **`4.48488 ± 0.03641`** | `+0.13294` | `-0.45166` / `6.50229` |
| **`(iii-b)` Response-Scale Calibration: Linear OLS $c_0 + c_1 \hat{y}$ (`2` params/split)** | **Yes (2 params fit on GDSC2 $y$)** | `40,292.4` | **`+0.00885 ± 0.00760`** | **`+0.43342`** | **`102.09%`** | **`72.71%`** | **`4.43967 ± 0.03586`** | `+0.14302` | `-0.41881` / `6.35524` |
| **`(iii-c)` Response-Scale Calibration: Affine Residual $y_{\text{naive}} + a + b(\hat{y} - y_{\text{naive}})$ (`2` params/split)** | **Yes (2 params fit on GDSC2 $y$)** | `40,292.4` | **`+0.01781 ± 0.00353`** | **`+0.44239`** | **`104.20%`** | **`74.21%`** | **`4.39953 ± 0.01975`** | `+0.13294` | `+0.00784` / `4.44420` |

### Summary of Largest Contributor
- **Largest Full-Dataset Contributor (All `40,292.4` Rows/Split):** **Mechanism `(iii)` (response-scale calibration fitted on GDSC2 labels)** closes **`99.71%–104.20%`** of the negative $R^2_{\text{norm}}$ gap to zero (`+0.42333` to `+0.44239` $R^2_{\text{norm}}$) and **`71.02%–74.21%`** of the `0.59610` gap to in-study `CTRPv2 LCO`.
- **Largest Label-Free Contributor (Zero GDSC2 Labels Used):** **Mechanism `(i-a)` (in-window concentration-range restriction $\ln d_{\min} \le \hat{y} \le \ln d_{\max}$, `19,118.6` rows/split)** closes **`109.29%`** of the gap to zero (`+0.46402` $R^2_{\text{norm}}$ to `+0.03945 ± 0.01189`) and **`77.84%`** of the gap to `CTRPv2 LCO`, while cutting MSE by **`58.77%`** (`6.38104 -> 2.63072`).
- **Smallest Contributor:** **Mechanism `(ii)` (cell-line overlap restriction)** closes only **`3.17%`** of the gap to zero (`+0.01346` $R^2_{\text{norm}}$).
