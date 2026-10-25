# V3R1T4S Skeptic Panel Report — CRITERION

role: CRITERION
target_id: immrep22-tcr-epitope-microauc
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
confirmed_scope: Multi-Chain (alpha/beta/alphabeta) OOB + Analytical LOO + CSLS Hubness-Corrected CLSS Ensemble trained strictly on claim/training_data/ achieves 17-epitope _Average MicroAUC = 0.882173 in claim/clss_tcr_stats.txt (856 bytes, sha256 3c17d9f39dc9b72c93441d4cc5d4b9fae9d986fe09f8abf3b27fe971d0212090) via the official claim/evaluation/evaluate.py vs the best published tcrexab = 0.847347 (+0.034826 >= +0.0200, winning 15/17 epitopes with 1-sided Wilcoxon p = 6.7139e-04 and 9/17 epitopes over all 22 published methods), single-epitope SPRWYFYYL MicroAUC = 0.877874 vs published column max 0.837823 (+0.040050 >= +0.0300, p1), companion Task 2 _Average Rank = 2.859120 vs published best 3.284289 (-0.425169 <= -0.2500, p2), 17-epitope negative-sampling provenance audit across clss_tcr, tcrexab, tcrexb, and tcrexa (p3), zero control-repertoire overlap, and Levenshtein d_Lev >= 2 MicroAUC = 0.868783 (+0.037753 over d_Lev >= 2 tcrexab 0.831030 and +0.021436 over full-set 0.847347), after reproducing tcrexab (0.846619), tcrexb (0.831443), and tcrexa (0.785032) within <= 0.0024.

---

## 1. Clause-by-Clause Literal Verification Against `success_criterion` and `partial_wins`

### Clause (1): Trained Only on `claim/training_data/` & Strictly Pointwise Inductive Scoring
- **Training data isolation:** Direct inspection and execution of `claim/run_clss_immrep22.py` (`17,429` bytes, `sha256: b81aafaf11cb11fb69fe22a372b4138420927bc0c41857839604f983b00e87ba`) confirms that for each epitope `ep` in the 17 benchmark epitopes, all featurizers (`DictVectorizer` for k-mer/gene tokens and `tcrex` physicochemical descriptors, plus Cholesky BLOSUM62 loop embeddings), Kernel Ridge Regression models ($\lambda = 0.4$ with analytical leave-one-out residuals), CSLS hubness-corrected local similarity states ($k_{\text{bg}} = 10$, $k_p = 3$, $k_n = 5$), and `300`-tree `RandomForestClassifier` / `ExtraTreesClassifier` models (`random_state=0`, `oob_score=True`) are fit exclusively on `claim/training_data/{ep}.txt`. Zero external VDJdb / IEDB / McPAS records and zero rows from `claim/negativeData_controls/TCR_COV*.tsv` are added during training.
- **Strictly pointwise inductive test prediction:** In `claim/run_clss_immrep22.py`, expert weights $w_j \propto \max(0, \text{AUC}_{\text{OOF}, j} - 0.52)^4$, standardization statistics (`oof_means`, `oof_stds`), and cross-epitope calibration statistics (`oof_neg_mean`, `oof_comb_std`) are computed solely from training OOF/LOO predictions. Independent verification scoring single test rows (`te_df.iloc[[0]]` and `te_df.iloc[[5]]`) vs the full test batch `te_df` and comparing against saved `claim/clss_tcr_scores/{ep}.txt` confirmed floating-point identity:
  - `SPRWYFYYL`: batch vs saved max abs diff = `2.220e-16`, `row0` single vs batch diff = `2.442e-15`, `row5` single vs batch diff = `4.663e-15` (all `<= 1e-12`).
  - `LTDEMIAQY`: batch vs saved max abs diff = `4.441e-16`, `row0` single vs batch diff = `1.776e-15`, `row5` single vs batch diff = `1.499e-15` (all `<= 1e-12`).

### Clause (2): Reproduction of Published Baselines in the Same Environment Within `<= 0.01`
- All three `immrep_tcrex` variants (`tcrexab`, `tcrexb`, `tcrexa`) were reproduced via `claim/run_baselines.py` (`11,210` bytes, `sha256: 2dbe214f97f5e3de31c883206ecc77477c6bbf9268569c0f4f1c5db22c446839`) and scored with `claim/evaluation/evaluate.py` (`5,115` bytes, `sha256: 04fa0346aa914bab770f9adbd6326581026e0fa9b94ad734f3957c54be6778ed`) against `claim/evaluation/microaucs.csv` (`8,251` bytes, `sha256: 28321870009bf2f122907da498ed912d227d8ad74b6f92d37d9ddfb9d043bec5`):
  - `tcrexab` (`claim/baseline_tcrexab_stats.txt`, `839` bytes, `sha256: 60cc308ece58807383b2e1357cd3fedec23b56a49bd51c58ea7eca4d94b2f41c`): rerun `_Average` MicroAUC = `0.846619` vs published `0.847347` (`|diff| = 0.000728 <= 0.01`); `_Average` Rank = `3.373043` vs published `3.284289`.
  - `tcrexb` (`claim/baseline_tcrexb_stats.txt`, `853` bytes, `sha256: cdce89c95e8c7cc53d74754d4bdc85c2aa4511e5632c2c1d6b45a535f2320713`): rerun `_Average` MicroAUC = `0.831443` vs published `0.830093` (`|diff| = 0.001351 <= 0.01`); `_Average` Rank = `3.422460` vs published `3.441607`.
  - `tcrexa` (`claim/baseline_tcrexa_stats.txt`, `816` bytes, `sha256: 63e094fa4fcf07ece8b6532e0631f1fa11987e8bed5b5b22381af09a2eb7021d`): rerun `_Average` MicroAUC = `0.785032` vs published `0.787385` (`|diff| = 0.002353 <= 0.01`); `_Average` Rank = `4.212662` vs published `4.223326`.

### Clause (3): Full `success_criterion` (`_Average` MicroAUC >= `0.867347` via `claim/evaluation/evaluate.py`)
- Fresh execution of `claim/evaluation/evaluate.py` on `claim/clss_tcr_scores/` against `claim/true_set/` produced a byte-for-byte identical output to `claim/clss_tcr_stats.txt` (`856` bytes, `sha256: 3c17d9f39dc9b72c93441d4cc5d4b9fae9d986fe09f8abf3b27fe971d0212090`, max abs diff `0.000e+00`):
  - **CLSS `_Average` MicroAUC = `0.882173`** vs best published `tcrexab = 0.847347`, a gain of **`+0.034826`** (`>= +0.0200` required; `+0.035554` over rerun `tcrexab = 0.846619`).
  - CLSS outperforms published `tcrexab` on **`15 / 17` epitopes** (1-sided Wilcoxon signed-rank statistic `140.0`, $p = 6.713867 \times 10^{-4}$; `10,000`-resample paired bootstrap win rate `100.00%`, 95% CI of gain `[+0.015417, +0.059228]`, $P(\text{gain} \ge 0.02) = 91.65\%$).
  - CLSS exceeds the **column maximum across all 22 published methods** in `claim/evaluation/microaucs.csv` on **`9 / 17` epitopes**: `LTDEMIAQY` (`0.791680` vs `0.782400`, `+0.009280`), `TTDPSFLGRY` (`0.811604` vs `0.809833`, `+0.001771`), `NQKLIANQF` (`0.661972` vs `0.653521`, `+0.008451`), `GPRLGVRAT` (`0.918004` vs `0.891266`, `+0.026738`), `CINGVCWTV` (`0.896715` vs `0.884659`, `+0.012056`), `SPRWYFYYL` (`0.877874` vs `0.837823`, `+0.040050`), `GLCTLVAML` (`0.990843` vs `0.969502`, `+0.021341`), `YLQPRTFLL` (`0.850342` vs `0.832831`, `+0.017510`), and `ATDALMTGF` (`0.962433` vs `0.940221`, `+0.022212`).

### Clause (4): Single-Epitope `>= +0.03` Win (`partial_wins` `p1`)
- On **`SPRWYFYYL`** (`claim/clss_tcr_scores/SPRWYFYYL.txt`, `6,909` bytes, `sha256: 3313dcb9c20f839a32a16cfc4a2633e89137354f26501c18e0ea92966093f23c`), CLSS achieves MicroAUC = **`0.877874`** vs the all-22-method column maximum `0.837823` (`tcrexb`), a gain of **`+0.040050 >= +0.0300`** (`+0.066631` over published `tcrexab = 0.811243` in `claim/evaluation/microaucs.csv`), accompanied by a `+0.034826` improvement in the 17-epitope mean.

### Clause (5): Companion Epitope-Ranking Metric (`partial_wins` `p2`)
- On `claim/clss_tcr_scores/testSet_Global.txt` (`625,929` bytes, `sha256: 7b67dfa02719ef08e73884a6f451356b586875575a11af393c915e1665827177`), `claim/evaluation/evaluate.py` reports **`_Average` Rank = `2.859120`** vs the best published `_Average` Rank in `claim/evaluation/epitoperank.csv` (`4,788` bytes, `sha256: 286e0acde8a47fd0197ff1a4d4b0715fab8869c7b51374df3ecd1a406381c2f8`, `tcrexab = 3.284289`), an average rank improvement of **`-0.425169 <= -0.2500`** with no MicroAUC regression.

### Clause (6): Negative-Sampling Provenance Audit (`p3`) & Near-Duplicate (`d_Lev <= 1`) / Leakage Audit
- Verified via `claim/audit_immrep22_p3_and_leakage.py` (`12,474` bytes, `sha256: 305485ac445f7b0e2e87dc45e16b5bf1792010067cb389205c8909a7a3bf78a1`) and `claim/immrep22_audit_manifest.json` (`40,666` bytes, `sha256: 84eaaa159f0f802d4080c1b2de2fc7a42edab71a0f7a56ca14f505413d4d2c9b`):
  - **Control-repertoire disjointness:** `control_neg_train_test_overlap == 0` across all `17 / 17` epitopes (`0` shared healthy-donor control negatives from `claim/negativeData_controls/TCR_COV*.tsv`).
  - **3-way negative-source decomposition (`p3`) across 17 epitopes (`619` positives, `1,802` swapped-epitope VDJdb negatives, `1,250` healthy-donor control negatives):**
    - `clss_tcr`: `all_neg = 0.882173` | `swapped_neg_only = 0.901893` | `control_neg_only = 0.854062` (`diff = -0.047830`)
    - `tcrexab`: `all_neg = 0.846619` | `swapped_neg_only = 0.870747` | `control_neg_only = 0.813029` (`diff = -0.057718`)
    - `tcrexb`: `all_neg = 0.831443` | `swapped_neg_only = 0.851989` | `control_neg_only = 0.801029` (`diff = -0.050959`)
    - `tcrexa`: `all_neg = 0.785032` | `swapped_neg_only = 0.805848` | `control_neg_only = 0.760076` (`diff = -0.045772`)
    CLSS beats `tcrexab` on both swapped-epitope negatives (`+0.031146`) and healthy-donor control negatives (`+0.041033`).
  - **Near-duplicate Levenshtein (`d_Lev <= 1`) exclusion:** Removing all test TCRs with $d_{\text{Lev}}(\text{CDR3}\alpha) + d_{\text{Lev}}(\text{CDR3}\beta) \le 1$ relative to any same-epitope training positive (`82` positive test TCRs across the 17 epitopes, including `21` exact positive matches and `39` total same-epitope exact pairs), CLSS achieves `min_lev_ab >= 2` mean MicroAUC = **`0.868783`** vs `tcrexab` **`0.831030`**, a gain of **`+0.037753 >= +0.0200`**, and still **`+0.021436 >= +0.0200`** above full-set published `tcrexab` (`0.847347`).

### Null Model & Negative Controls
- **Label-permutation null model (`400` random permutations per epitope across all 17 epitopes):** mean `_Average` MicroAUC = `0.500024` (`std = 0.016884`, `min = 0.454321`, `max = 0.547190`), with `0 / 400` permutations reaching `0.882173` ($z = +22.63$).
- **Negated-score control:** negating predicted scores yields `_Average` MicroAUC = `0.118008` (`< 0.20`), confirming non-vacuous directional calibration.

pass: true
