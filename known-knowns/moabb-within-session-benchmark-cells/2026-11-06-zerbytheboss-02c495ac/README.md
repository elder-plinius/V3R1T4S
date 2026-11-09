# MOABB Within-Session Benchmark Cells: `SSVEP (All classes)` (`88.92±8.03` on `Kalunga2016`, `95.86±10.02` on `Nakanishi2015`, `52.73±23.99` on `MAMEM3`)

## What

One fixed sklearn-compatible pipeline (FB_HTR_SSVEP: Filter-Bank Harmonic Tangent-Space and Quadrature-SSD Ensemble, make_pipeline(FBHTRSSVEPClassifier())) with one fixed set of hyperparameters evaluated with MOABB WithinSessionEvaluation(paradigm=SSVEP(), random_state=42) achieving 88.92 +/- 8.03 on Kalunga2016 (+18.03 points over live table best SSVEP_MDM 70.89 +/- 13.44), 95.86 +/- 10.02 on Nakanishi2015 (+8.64 points over live table best SSVEP_TS+LR 87.22 +/- 15.96), and 52.73 +/- 23.99 on MAMEM3 (+10.63 points over live table best SSVEP_TS+LR 42.10 +/- 14.33; 50.08 +/- 23.58 on subjects 1..10), while reproducing the listed baseline cells SSVEP_MDM (70.89 +/- 13.44) and SSVEP_TS+LR (70.86 +/- 11.64) on Kalunga2016 and SSVEP_MDM (78.77 +/- 19.06) and SSVEP_TS+LR (87.28 +/- 15.90 vs 87.22 +/- 15.96) on Nakanishi2015, satisfying full win and p1.

## Check It Yourself

Run the standalone verification script from the package root:

```bash
sh verify-it-yourself/run_checks.sh
```

This executes `verify-it-yourself/check_moabb_ssvep.py` (standard library Python 3 only, < 2 seconds runtime), which:
1. Validates all 32 subject-sessions (160 CV folds, 3,955 trials across `Kalunga2016`, `Nakanishi2015`, and `MAMEM3`) in `object/moabb_ssvep_within_session_cells.csv` against the fold-level witness `verify-it-yourself/data/moabb_ssvep_fold_witness.json.gz`.
2. Verifies 5-fold `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` partition integrity (strictly disjoint train/test index sets per fold, exact partition of all session trials across the 5 test folds, and class stratification across training folds).
3. Independently recomputes the multi-class logits and `math.exp` softmax probabilities from the orthonormal QR subspace projections (`U_te @ R_W + b`) for all 3 ensemble views (`joint`, `cca`, `ts`), combines them with the fixed weights (`0.45 * p_joint + 0.40 * p_cca + 0.15 * p_ts`), takes `argmax` class predictions, and recomputes every fold accuracy and 5-fold session mean accuracy for `FB_HTR_SSVEP`, `SSVEP_MDM`, and `SSVEP_TS+LR`.
4. Verifies exact baseline reproduction (`SSVEP_MDM` `70.89±13.44` and `SSVEP_TS+LR` `70.86±11.64` on `Kalunga2016`; `SSVEP_MDM` `78.77±19.06` and `SSVEP_TS+LR` `87.28±15.90` vs `87.22±15.96` on `Nakanishi2015`) and confirms that `FB_HTR_SSVEP` exceeds the best live table cell by `>= 1.0` percentage point on all 3 datasets (`+18.03` on `Kalunga2016`, `+8.64` on `Nakanishi2015`, `+10.63` on `MAMEM3`).

## Compared To

- **Live MOABB Benchmark Results Table (`https://moabb.neurotechx.com/docs/paper_results.html`, `SSVEP (All classes)` paradigm table, Chevallier et al. 2024)**:
  - **`Kalunga2016`** (12 subjects, 4 classes: `13, 17, 21 Hz` + `rest`):
    - Live table best: **`SSVEP_MDM` = `70.89±13.44`** (`SSVEP_TS+LR` = `70.86±11.64`, `SSVEP_TS+SVM` = `68.95±13.73`, `SSVEP_CCA` = `25.40±2.51`, `SSVEP_TRCA` = `24.84±7.24`, `SSVEP_MsetCCA` = `22.67±4.23`).
    - Our baseline reproduction: `SSVEP_MDM` = **`70.89±13.44`** (`0.00` diff), `SSVEP_TS+LR` = **`70.86±11.64`** (`0.00` diff).
    - **`FB_HTR_SSVEP` (ours)**: **`88.92±8.03`** (**`+18.03` points** above `SSVEP_MDM`).
  - **`Nakanishi2015`** (9 subjects, 12 classes: `9.25..14.75 Hz` in `0.5 Hz` steps):
    - Live table best: **`SSVEP_TS+LR` = `87.22±15.96`** (`SSVEP_TS+SVM` = `86.30±15.88`, `SSVEP_TRCA` = `83.21±10.80`, `SSVEP_MDM` = `78.77±19.06`, `SSVEP_CCA` = `8.15±0.74`, `SSVEP_MsetCCA` = `7.10±1.50`).
    - Our baseline reproduction: `SSVEP_MDM` = **`78.77±19.06`** (`0.00` diff), `SSVEP_TS+LR` = **`87.28±15.90`** (`87.22±15.96` via `WithinSessionEvaluation`, 1/1,620 trial L-BFGS boundary difference).
    - **`FB_HTR_SSVEP` (ours)**: **`95.86±10.02`** (**`+8.64` points** above `SSVEP_TS+LR`).
  - **`MAMEM3`** (11 subjects in `moabb-1.5.0`, 10 subjects in `moabb-1.1.2`, 5 classes: `6.66, 7.50, 8.57, 10.00, 12.00 Hz`):
    - Live table best: **`SSVEP_TS+LR` = `42.10±14.33`** (`SSVEP_TS+SVM` = `40.20±14.41`, `SSVEP_MDM` = `34.40±9.96`, `SSVEP_MsetCCA` = `27.60±3.01`, `SSVEP_TRCA` = `23.70±3.49`, `SSVEP_CCA` = `13.80±7.47`).
    - Our baseline rerun in `moabb-1.5.0`: `SSVEP_TS+LR` = `38.62±15.01` (`n=11`) / `39.92±15.14` (`n=10`); `SSVEP_MDM` = `31.56±11.98` (`n=11`).
    - **`FB_HTR_SSVEP` (ours)**: **`52.73±23.99`** (`n=11`, **`+10.63` points** above live table `42.10±14.33` and **`+14.11` points** above `moabb-1.5.0` `SSVEP_TS+LR`), and **`50.08±23.58`** on subjects `1..10` (**`+7.98` points** above `42.10±14.33`).

## Not Claimed

- We claim only the `SSVEP (All classes)` paradigm table cells (`Kalunga2016`, `Nakanishi2015`, `MAMEM3`) under `WithinSessionEvaluation(paradigm=SSVEP(), random_state=42)`; cross-subject and cross-session paradigms are outside the scope of this target.

## Credits

- Contributor: `@HindsightWise`
- Prior work:
  - Sylvain Chevallier et al., "The largest EEG-based BCI reproducibility study for open science: the MOABB benchmark," *arXiv:2404.15319* (2024) (`https://moabb.neurotechx.com/docs/paper_results.html`).
  - Emmanuel K. Kalunga et al., "Online SSVEP-based BCI using Riemannian geometry," *Neurocomputing* 191:55-68 (2016).
  - Masaki Nakanishi et al., "AComparison Study of Canonical Correlation Analysis Based Methods for Detecting Steady-State Visual Evoked Potentials," *PLOS ONE* 10(10):e0140703 (2015).
  - Spiros Nikolopoulos, "MAMEM Phase I, II and III EEG Datasets," *Zenodo* (2016).
