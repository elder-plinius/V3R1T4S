# Skeptic 3 — Criterion & Zero-Leakage Audit (`plmfit-trastuzumab-cdrh3-binding-mcc`)

context: fresh review session

## 1. Verification Against Target Success Criteria & Partial Wins (`p1`–`p4`)

1. **Strict Inductive Split (`173` `train` + `1` `validation` = `174` training rows $\to$ `36,386` `one_vs_rest == 'test'` rows):**
   - Verified in `how-we-built-it/bet11_dual_canonical_and_cv_learned_solver.py` and `how-we-built-it/bet8_lotus_jensen_zero_magic_cv.py`: `tr_indices` contains only rows with `one_vs_rest in ("train", "validation")` (`174` rows), and `te_indices` (`36,386` rows) is never passed to any fitting, hyperparameter selection, or threshold selection function.
   - Zero raw sequences (`aa_seq`) and zero ground-truth labels (`binary_score`) are included inside `object/*.csv`.
2. **Primary Success Criterion (`MCC >= 0.3898 + 0.02 = 0.4098`, `>= 3` seeds, 95% bootstrap CI excluding `0.3898`):**
   - **`Track B` (`trackB_cv_learned`):** Achieves 3-seed `Test MCC = 0.421004 +- 0.001735` across seeds `[42, 43, 44]` (`0.422296, 0.418551, 0.422164`), exceeding `0.3898` by **`+0.031204`** (`>= +0.02`) and `0.4098` by **`+0.011204`**, with 1,000-resample bootstrap 95% CI **`[0.412067, 0.430182]`** (`ci_excludes_0_3898: true`, lower bound `0.412067 > 0.4098`).
   - **`Track A` (`trackA_canonical`, parameter-free canonical law from `L-PTCB-008`):** Achieves 3-seed `Test MCC = 0.408391 +- 0.000411` (`95% CI [0.398892, 0.417982] > 0.3898`, margin `+0.018591` over `0.3898`).
3. **Partial Win `p1` (`<= 10M` Parameters):**
   - Uses frozen `facebook/esm2_t6_8M_UR50D` (`7,512,474` parameters, pretrained on `UniRef50` generic protein sequences with zero DMS or antibody binding labels) plus `864` downstream linear/empirical-Bayes parameters = **`7,513,338 <= 10,000,000` parameters**.
4. **Partial Win `p2` (Threshold-Free `AUROC` & `Average Precision` with Released Prediction Files):**
   - `Track B`: `Test AUROC = 0.789510 +- 0.000669`, `Test AP = 0.624177 +- 0.000884`.
   - `Track A`: `Test AUROC = 0.785602 +- 0.000461`, `Test AP = 0.622932 +- 0.000615`.
5. **Partial Win `p3` (1-Body Position-Wise vs. 2-Body Pairwise Epistatic Ablation Within the 10-aa Loop):**
   - `Track B`: `1-Body MCC = 0.410402 +- 0.001592` $\to$ `2-Body MCC = 0.421004 +- 0.001735` (**`+0.010601` MCC**, **`+0.004567` AUROC**, **`+0.001972` AP**).
   - `Track A`: `1-Body MCC = 0.401879 +- 0.000887` $\to$ `2-Body MCC = 0.408391 +- 0.000411` (**`+0.006512` MCC**, **`+0.004844` AUROC**, **`+0.001947` AP**).
6. **Partial Win `p4` (Cross-Validation Threshold-Selection Audit vs. Test-Oracle Threshold):**
   - `Track B`: `inductive_tau_cv_mean = 1.344167 +- 0.037100` (`OOF_MCC = 0.770801`, `OOF_AUROC = 0.930331`), `test_oracle_mcc_mean = 0.422756`, **`inductive_to_oracle_mcc_gap = 0.001752`**.
   - `Track A`: `inductive_tau_cv_mean = 1.230833 +- 0.042931` (`OOF_MCC = 0.778202`, `OOF_AUROC = 0.924590`), `test_oracle_mcc_mean = 0.409793`, **`inductive_to_oracle_mcc_gap = 0.001402`**.
7. **Full Session Test-Evaluation Accounting (`L-PTCB-001`..`L-PTCB-011`):**
   - All `11` micro-bet evaluations conducted during the campaign are logged in `object/certificate.json` (`session_test_evaluations_audit`) and `README.md`.

pass: true
