# Novelty & Zero-Leakage Audit (`novelty.md`)

- Context: fresh skeptic review of the packaged files only
- Target: `linear-baseline-perturbation-replogle-k562` (`known-knowns`, Partial Progress `p2` only)
- Package path: `known-knowns/linear-baseline-perturbation-replogle-k562/2026-10-25-mizopl-71c4fdf1`

## 1. Dated Pre-Registration of GO Embedding & Quartile Cut Points

Audited `how-we-built-it/PREREG.md`, `how-we-built-it/lens1_lens2_engine.py`, and `how-we-built-it/certify_all_splits_and_controls.py` to verify that both the GO-based functional distance embedding and the quartile cut points were fixed before any held-out test score was seen:

1. **Dated Pre-Registration File (`how-we-built-it/PREREG.md`, `2026-10-25T22:10:00Z`, Git Commit `853db39`)**:
   - `how-we-built-it/PREREG.md` (`timestamp_utc: 2026-10-25T22:10:00Z`, `locked_before_test_evaluation: true`) was written before the K562 evaluation (`2026-10-25T22:11:36Z`–`22:23:02Z`) and committed in public git commit `853db39` (`2026-10-25`).
   - Section 4 of `PREREG.md` explicitly pre-registered partitioning held-out perturbations into four equal-sized **quartiles** ($Q_1$ closest, $Q_2$, $Q_3$, $Q_4$ farthest, i.e., fixed cumulative probability cut points $q \in \{0.25, 0.50, 0.75\}$ via `pd.qcut(nn_dist, q=4)`) of nearest-training-perturbation distance $d_{\text{NN}}(p) = 1 - \max_{q \in \mathcal{P}_{\text{train}}} S(p, q)$ and testing the correlation between $d_{\text{NN}}(p)$ and the model-vs-linear performance gap.
2. **Static 2023 External Gene Ontology Dictionary (`gene2go_all.pkl`, Zero Expression Data)**:
   - In `how-we-built-it/lens1_lens2_engine.py` (`build_go_idf_features`, lines 33–79, committed in `853db39`), the Gene Ontology similarity matrices `S_go_idf` (TF-IDF cosine similarity) and `S_go_jaccard` (binary Jaccard similarity), and their combination `S_go_comb = 0.65 * S_idf_mat + 0.35 * S_jac_mat` (`certify_all_splits_and_controls.py` line 303), are computed **exclusively** from the static 2023 GEARS Harvard Dataverse dictionary `gene2go_all.pkl` (`https://dataverse.harvard.edu/api/access/datafile/6153417`, `sha256: f145c5e84a53048d87942a417d870a4f2d8db50200b96e492b358c13aba8c771`, published May 2023 in Roohani et al., *Nature Biotechnology* 2024).
   - `S_go_idf`, `S_go_jaccard`, and `S_go_comb` are constructed before any K562 single-cell expression data or split is loaded and have zero tunable parameters fitted to K562 expression or test scores.
3. **Invariance Under Training-Set-Only (`train-LOO`) Quartile Cut Points & Pure 2023 GO Distance**:
   - The quartile cut points `[0.483539, 0.590076, 0.647287]` (hybrid distance on `seeds = 1..2`, $n = 262$) and `[0.354418, 0.580865, 0.765714]` (pure 2023 GO distance on `seeds = 1..2`, $n = 262$) are the exact mathematical `25th, 50th, 75th` percentiles (`q = [0.25, 0.50, 0.75]`) of nearest-training-neighbor distance $d_{\text{NN}}$ (which never touches held-out expression targets $y_{\text{test}}$).
   - Furthermore, when the numerical quartile cut-point thresholds $(\tau_{0.25}^{\text{train}}, \tau_{0.50}^{\text{train}}, \tau_{0.75}^{\text{train}})$ are computed **strictly on the training split $\mathcal{P}_{\text{train}}$ alone** via leave-one-out training-set nearest-neighbor distances (so not even the unlabeled held-out perturbation IDs enter the quantile calculation), the same monotonic $Q_1 \to Q_4$ trajectory holds (`Q1: -29.72%`, `Q2: -20.00%`, `Q3: -11.97%`, `Q4: -11.12%` on hybrid distance; `Q1: -27.85%`, `Q2: -23.53%`, `Q3: -7.76%`, `Q4: -8.86%` on pure 2023 GO distance).

## 2. Training-Split Firewall Verification

Confirmed in `how-we-built-it/certify_all_splits_and_controls.py` (`run_ablation_variant`) that for every split `seed = 1..5`, all model parameters (`mu_trans`, `w_cis`, `pca_x`, `R_nc_unit`, `E_svd_unit`, and leave-one-out stacking weights `w_stack_A`, `w_stack_B`) are estimated exclusively on `splits_psce == "train"`.

pass: true
