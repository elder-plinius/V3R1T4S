# `linear-baseline-perturbation-replogle-k562` — Partial Progress `p2` (Functional-Distance Stratification on Replogle K562)

- **Target ID**: `linear-baseline-perturbation-replogle-k562` (`known-knowns`, **Partial Progress `p2` only**)
- **Primary Paper**: Constantin Ahlmann-Eltze, Wolfgang Huber, and Simon Anders, *"Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines"*, **Nature Methods** 22, 1657–1661 (2025).
- **Upstream Benchmark Repository**: `https://github.com/const-ae/linear_perturbation_prediction-Paper` (commit `bfa6eeea2bd145a1af2ec0127a2e808cc38456a9`)
- **Dataset**: `replogle_k562_essential` (Harvard Dataverse `https://dataverse.harvard.edu/api/access/datafile/7458695`, `perturb_processed.h5ad` `sha256: 550fde89ac85c258c9fd517638fe34fb42c0e748c9305fe6355761a2bb754170`) + static 2023 GEARS Gene Ontology dictionary `gene2go_all.pkl` (`https://dataverse.harvard.edu/api/access/datafile/6153417`, `sha256: f145c5e84a53048d87942a417d870a4f2d8db50200b96e492b358c13aba8c771`)
- **Contributor**: `@mizopl`
- **Date**: `2026-10-25`

---

## What

Confirmed Partial Progress (p2) on linear-baseline-perturbation-replogle-k562: saved plain-text per-perturbation predictions for every held-out K562 perturbation across seeds 1..2 (n = 262 Panel A perturbations: 134 in seed 1, 128 in seed 2) and seeds 1..5 (n = 677 in-readout perturbations) stratify the performance gap between Hollow-LOO Dual-Lens and the paper's self-trained linear baseline (lpm_selftrained, K = 10 PCA, lambda = 0.1) by nearest-training-perturbation functional distance, showing that the gap is concentrated in close/in-distribution functional neighborhoods (Q1 delta L2 = -1.404930 or -32.33%, delta R_delta = +0.224525) and narrows monotonically for out-of-distribution perturbations (Q4 delta L2 = -0.404255 or -10.40%, delta R_delta = +0.123755; Spearman r_s = +0.345058, p = 9.7126e-09 on hybrid distance; Spearman r_s = +0.420798, p = 1.1506e-12 on static 2023 gene2go_all.pkl Gene Ontology distance).

*Note: "Confirmed" in the quoted scope above is our internal verification panel's status (`panel/gate.md`): partial progress `p2` is claimed here, and confirming it is the repository review's decision.*

### 1. Plain-Text Per-Perturbation Predictions & Nearest-Training-Neighbor Distances (`object/`)

Every held-out K562 perturbation across each split we report (`seed = 1`: `136` in-readout perturbations including `134` Panel A rows; `seed = 2`: `134` in-readout perturbations including `128` Panel A rows; `seed = 3`: `135`; `seed = 4`: `135`; `seed = 5`: `137`; `677` total across `seeds = 1..5`, `262` in Panel A `seeds = 1..2`) is stored in plain-text tab-separated files in `object/`, keyed by `perturbation` ID (each perturbation ID appearing once per split), with its nearest training perturbation ID and functional distance:

| Plain-Text File in `object/` | Rows (excl. header) | Columns | Bytes | SHA-256 Digest | Contents |
| :--- | ---: | ---: | ---: | :--- | :--- |
| `k562_p2_per_perturbation_metrics.tsv` | `677` | `29` | `176,975` | `0e2ae30e6f9f0942b4adf46e9a2798d74206321ddb13b8dc4027f2c0a6fdfd75` | Per-perturbation nearest training perturbation IDs, functional distances (`nn_dist`, `nn_dist_go_only`, `nn_dist_go_idf`), quartile assignments, and $L_2$ / $R_{\Delta}$ scores across `seeds = 1..5` (`in_panel_a = 1` flags the `262` Panel A rows in `seeds = 1, 2`) |
| `k562_seed1_dual_predictions.tsv` | `136` | `1,007` | `951,158` | `9dbbb12e4011364dcac9988632320262b6119d64d0e6b20239a4ac250afd2aa3` | `Seed 1` per-perturbation predictions for `hollow_loo_dual_lens` over the top-1,000 genes + `nearest_train_pert`, `nn_dist`, `nearest_train_pert_go_only`, `nn_dist_go_only` |
| `k562_seed1_lpm_predictions.tsv` | `136` | `1,007` | `950,957` | `b91b17552364c0acac43499b47b8e8698bcd65783264a7e3ee2c9756ba0c044c` | `Seed 1` per-perturbation predictions for `lpm_selftrained` over the top-1,000 genes + nearest training perturbation distances |
| `k562_seed1_observed_top1000.tsv` | `137` | `1,002` | `951,780` | `d964d97dfc65a09890110fb4596217537e56b664b75bd036e6d00512c44a011b` | `Seed 1` ground-truth `ctrl` + observed pseudobulk expression over the top-1,000 genes |
| `k562_seed2_dual_predictions.tsv` | `134` | `1,007` | `937,139` | `a14fab6b90b7719f2eebe70d6c57c4773f1f4ca30440c32d2418edb23c7dbec8` | `Seed 2` per-perturbation predictions for `hollow_loo_dual_lens` over the top-1,000 genes + nearest training perturbation distances |
| `k562_seed2_lpm_predictions.tsv` | `134` | `1,007` | `937,208` | `fab23f0ddd673e66819ea2792ec351927bdc3bec20662525bf17662626bbd9c9` | `Seed 2` per-perturbation predictions for `lpm_selftrained` over the top-1,000 genes + nearest training perturbation distances |
| `k562_seed2_observed_top1000.tsv` | `135` | `1,002` | `938,124` | `78d131122b2280ba46b8f0bcdff9ecd2943a9456f0b4a2ee16698d2e5412f484` | `Seed 2` ground-truth `ctrl` + observed pseudobulk expression over the top-1,000 genes |
| `k562_seed3_dual_predictions.tsv` | `135` | `1,007` | `944,256` | `faf3358e10486079d6419f7c9fbb4974f67c4b8eb94f1d41da0b9a88f8df63a7` | `Seed 3` per-perturbation predictions for `hollow_loo_dual_lens` |
| `k562_seed3_lpm_predictions.tsv` | `135` | `1,007` | `943,931` | `5a18eda705f5a34e3ae8b22f886be93c0ea55d32acaf7989eb108e55f14ed595` | `Seed 3` per-perturbation predictions for `lpm_selftrained` |
| `k562_seed3_observed_top1000.tsv` | `136` | `1,002` | `944,961` | `fffe82c29e5ef1cb33bebbe3f525069112b3206fb43d4eea1e7f4db8beca0d3c` | `Seed 3` ground-truth `ctrl` + observed expression |
| `k562_seed4_dual_predictions.tsv` | `135` | `1,007` | `943,961` | `d1afaee4f487ec05c3d383b29d490b505a8356cf8a363930164bf2ace981701f` | `Seed 4` per-perturbation predictions for `hollow_loo_dual_lens` |
| `k562_seed4_lpm_predictions.tsv` | `135` | `1,007` | `944,044` | `ff76aadecbd6c2f4a75f9a0ea41a3041e052d85987e69f90acdcd5019e24d753` | `Seed 4` per-perturbation predictions for `lpm_selftrained` |
| `k562_seed4_observed_top1000.tsv` | `136` | `1,002` | `944,925` | `7f5b69bf9d1b1a6dc49258a0f820e5cecb55180a84d912056740d40d6a16fdba` | `Seed 4` ground-truth `ctrl` + observed expression |
| `k562_seed5_dual_predictions.tsv` | `137` | `1,007` | `958,184` | `c66091521c9562e48b8c77f49bd2c1052ae9287f15bc0522676baaafabfbebc3` | `Seed 5` per-perturbation predictions for `hollow_loo_dual_lens` |
| `k562_seed5_lpm_predictions.tsv` | `137` | `1,007` | `957,709` | `ce4fdca99efea2ed28db4f9cc543e8715c103eeff2efda40d3366ddec062314d` | `Seed 5` per-perturbation predictions for `lpm_selftrained` |
| `k562_seed5_observed_top1000.tsv` | `138` | `1,002` | `958,859` | `820ce21019b9ec330086e5003c2f8993744b495771b2b2c4a98ebee4928e6b5c` | `Seed 5` ground-truth `ctrl` + observed expression |

### 2. Dated Pre-Registration of the GO Embedding & Quartile Cut Points (`how-we-built-it/PREREG.md`)

1. **Static 2023 Gene Ontology Dictionary (`gene2go_all.pkl`)**: The Gene Ontology similarity matrices (`S_go_idf` TF-IDF cosine similarity, `S_go_jaccard` binary Jaccard similarity, and `S_go_comb = 0.65 * S_idf_mat + 0.35 * S_jac_mat` in `how-we-built-it/lens1_lens2_engine.py` lines 33–79 and `how-we-built-it/certify_all_splits_and_controls.py` line 303, committed `2026-10-25` in git commit `853db39`) are computed deterministically from the static 2023 Harvard Dataverse file `gene2go_all.pkl` (`https://dataverse.harvard.edu/api/access/datafile/6153417`, `sha256: f145c5e84a53048d87942a417d870a4f2d8db50200b96e492b358c13aba8c771`, deposited May 2023 for Roohani et al., *Nature Biotechnology* 2024) before any K562 expression matrix or train/test split is loaded.
2. **Dated Pre-Registration of Quartiles (`2026-10-25T22:10:00Z`, Git Commit `853db39`)**: `how-we-built-it/PREREG.md` (`timestamp_utc: 2026-10-25T22:10:00Z`, git blob `e33417a34d39c57941d0f27858ba22c7c77f9404` in commit `853db39`) pre-registered partitioning held-out perturbations into four equal-sized **quartiles** ($Q_1 \dots Q_4$) of nearest-training-neighbor distance $d_{\text{NN}}(p) = 1 - \max_{q \in \mathcal{P}_{\text{train}}} S(p, q)$ via standard cumulative probability quantiles $q \in \{0.25, 0.50, 0.75\}$ (`pd.qcut(nn_dist, q=4)`). Neither $d_{\text{NN}}$ nor its `25th/50th/75th` percentiles ever touch held-out target expression vectors $y_{\text{test}}$ or test scores.
3. **Training-Set-Only (`train-LOO`) Cut Points & Pure 2023 GO Distance**: Even when the numerical quartile thresholds $(\tau_{0.25}^{\text{train}}, \tau_{0.50}^{\text{train}}, \tau_{0.75}^{\text{train}})$ are computed **strictly on the training perturbations $\mathcal{P}_{\text{train}}$ alone** via leave-one-out nearest-training-neighbor distances (so not even the unlabeled held-out perturbation IDs enter the threshold calculation), or when distances are computed from **pure static 2023 `gene2go_all.pkl` GO annotations (`nn_dist_go_only` and `nn_dist_go_idf`) with zero expression data**, the same monotonic narrowing from $Q_1$ to $Q_4$ holds across all specifications.

---

## Check It Yourself

Run the standalone verification and negative-control suite (`~3s`):

```sh
sh verify-it-yourself/run_checks.sh
```

`run_checks.sh` runs `verify-it-yourself/verify.py` on `object/certificate_replogle_k562.json`, verifies all 16 plain-text TSVs in `object/`, recomputes all `677` per-perturbation $L_2$ and $R_{\Delta}$ scores directly from the plain-text 1,000-gene prediction TSVs against the observed TSVs, recomputes all `p2` quartile stratifications and Spearman / Wilcoxon statistics, and verifies that corrupting either `certificate_replogle_k562.json` or `k562_seed1_dual_predictions.tsv` causes `verify.py` to fail with a non-zero exit code.

---

## Compared To

### 1. Upstream Source Data Links & SHA-256 Digests

Per review guidance, copied Source Data tables have been replaced with stable upstream links and SHA-256 digests (`the-record-we-beat/PAPER_NUMBERS.md`):
- `source_data/single_perturbation_prediction.xlsx`: `https://github.com/const-ae/linear_perturbation_prediction-Paper/raw/bfa6eeea2bd145a1af2ec0127a2e808cc38456a9/source_data/single_perturbation_prediction.xlsx` (`565,586` bytes, `sha256: 09c6c198aff4e8a827064183f9cff13eb6f33e56f1689940527304bf78957efe`)
- `source_data/suppl-pearson_delta_performance_single_pert.xlsx`: `https://github.com/const-ae/linear_perturbation_prediction-Paper/raw/bfa6eeea2bd145a1af2ec0127a2e808cc38456a9/source_data/suppl-pearson_delta_performance_single_pert.xlsx` (`569,165` bytes, `sha256: 61658661412f385356a383c3ed506f4454c6db79b28c272151bb15a725b0faaa`)

### 2. Overall K562 Re-Run Summary (`seeds = 1..2` Panel A `n = 262`, and `seeds = 1..5` `n = 677`)

| Split Set | Method | Mean $L_2 \downarrow$ | Median $L_2 \downarrow$ | Mean $R_{\Delta} \uparrow$ | Median $R_{\Delta} \uparrow$ |
| :--- | :--- | ---: | ---: | ---: | ---: |
| **K562 Panel A (`seeds = 1..2`, $n = 262$)** | `mean` baseline | `4.193494` | `3.821090` | `0.407911` | `0.421439` |
| **K562 Panel A (`seeds = 1..2`, $n = 262$)** | `lpm_selftrained` (linear baseline re-run) | `4.097028` | `3.805564` | `0.435544` | `0.426480` |
| **K562 Panel A (`seeds = 1..2`, $n = 262$)** | `lens1_only` (Cis + De-Spiked Bilinear) | `4.058933` | `3.668053` | `0.462273` | `0.478233` |
| **K562 Panel A (`seeds = 1..2`, $n = 262$)** | `lens2_only` (Hollow-LOO GO + CoExp Resolvent) | `3.462915` | `3.240305` | `0.583020` | `0.604997` |
| **K562 Panel A (`seeds = 1..2`, $n = 262$)** | **`hollow_loo_dual_lens` (Lens 1 + Lens 2)** | **`3.320307`** | **`3.044310`** | **`0.620623`** | **`0.644965`** |
| **K562 5-Seed (`seeds = 1..5`, $n = 677$)** | `mean` baseline | `4.249815` | `3.872448` | `0.413024` | `0.423646` |
| **K562 5-Seed (`seeds = 1..5`, $n = 677$)** | `lpm_selftrained` (linear baseline re-run) | `4.168029` | `3.871448` | `0.437119` | `0.434981` |
| **K562 5-Seed (`seeds = 1..5`, $n = 677$)** | **`hollow_loo_dual_lens` (Lens 1 + Lens 2)** | **`3.332314`** | **`3.085892`** | **`0.633310`** | **`0.666277`** |

### 3. Partial Progress `p2`: Functional-Distance Stratification Tables on K562

#### A. Pre-Registered Hybrid GO + Training Co-Expression Distance (`nn_dist`, Equiprobable Quartiles `q = [0.25, 0.50, 0.75]` vs. Training-Only `train-LOO` Cut Points, `seeds = 1..2` Panel A, $n = 262$)

| Stratification Rule | Quartile | $n$ | Distance Range $[d_{\min}, d_{\max}]$ | Mean $d_{\text{NN}}$ | `lpm_selftrained` Mean $L_2$ | `hollow_loo_dual_lens` Mean $L_2$ | $\Delta L_2$ (Rel. %) | `lpm_selftrained` Mean $R_{\Delta}$ | `hollow_loo_dual_lens` Mean $R_{\Delta}$ | $\Delta R_{\Delta}$ |
| :--- | :--- | ---: | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Equiprobable `qcut(q=4)`** (`[0.483539, 0.590076, 0.647287]`) | **`Q1_closest`** | `66` | `[0.130572, 0.483470]` | `0.354995` | `4.345813` | `2.940883` | **`-1.404930` (`-32.33%`)** | `0.581483` | `0.806009` | **`+0.224525`** |
| **Equiprobable `qcut(q=4)`** | **`Q2_mid_close`** | `65` | `[0.483747, 0.589717]` | `0.541724` | `4.092773` | `3.315902` | **`-0.776871` (`-18.98%`)** | `0.431387` | `0.651365` | **`+0.219978`** |
| **Equiprobable `qcut(q=4)`** | **`Q3_mid_far`** | `65` | `[0.590436, 0.646506]` | `0.614727` | `4.061245` | `3.544353` | **`-0.516892` (`-12.73%`)** | `0.354264` | `0.526659` | **`+0.172395`** |
| **Equiprobable `qcut(q=4)`** | **`Q4_farthest`** | `66` | `[0.647547, 0.833828]` | `0.692054` | `3.887674` | `3.483419` | **`-0.404255` (`-10.40%`)** | `0.373746` | `0.497501` | **`+0.123755`** |
| **Training-Only `train-LOO` Cut Points** | **`Q1_closest`** | `79` | `[0.130572, 0.503754]` | `0.377619` | `4.325056` | `3.039465` | **`-1.285591` (`-29.72%`)** | `0.569239` | `0.793780` | **`+0.224541`** |
| **Training-Only `train-LOO` Cut Points** | **`Q2_mid_close`** | `50` | `[0.506827, 0.589286]` | `0.552608` | `4.075776` | `3.260467` | **`-0.815309` (`-20.00%`)** | `0.418481` | `0.637179` | **`+0.218699`** |
| **Training-Only `train-LOO` Cut Points** | **`Q3_mid_far`** | `72` | `[0.589699, 0.652018]` | `0.616394` | `4.008532` | `3.528547` | **`-0.479984` (`-11.97%`)** | `0.347932` | `0.514965` | **`+0.167034`** |
| **Training-Only `train-LOO` Cut Points** | **`Q4_farthest`** | `61` | `[0.650528, 0.833828]` | `0.695604` | `3.923587` | `3.487279` | **`-0.436308` (`-11.12%`)** | `0.379794` | `0.507510` | **`+0.127716`** |

- **Continuous correlation (`nn_dist`, $n = 262$)**: Spearman $r_s(d_{\text{NN}}, \Delta L_2) = +0.345058$ ($p = 9.7126 \times 10^{-9}$), Spearman $r_s(d_{\text{NN}}, \Delta R_{\Delta}) = -0.198624$ ($p = 1.2297 \times 10^{-3}$).

#### B. Pure Static 2023 `gene2go_all.pkl` Gene Ontology Distance (`nn_dist_go_only`, Zero Expression Data, `seeds = 1..2` Panel A, $n = 262$, and `seeds = 1..5`, $n = 677$)

| Split Set & Rule | Quartile | $n$ | Distance Range $[d_{\min}, d_{\max}]$ | Mean $d_{\text{GO}}$ | `lpm_selftrained` Mean $L_2$ | `hollow_loo_dual_lens` Mean $L_2$ | $\Delta L_2$ (Rel. %) | `lpm_selftrained` Mean $R_{\Delta}$ | `hollow_loo_dual_lens` Mean $R_{\Delta}$ | $\Delta R_{\Delta}$ |
| :--- | :--- | ---: | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Panel A (`n = 262`) `qcut(q=4)`** (`[0.354418, 0.580865, 0.765714]`) | **`Q1_closest`** | `66` | `[0.000000, 0.354296]` | `0.225593` | `4.577535` | `3.310295` | **`-1.267239` (`-27.68%`)** | `0.493951` | `0.758099` | **`+0.264148`** |
| **Panel A (`n = 262`) `qcut(q=4)`** | **`Q2_mid_close`** | `65` | `[0.354785, 0.580775]` | `0.468277` | `4.138862` | `3.097663` | **`-1.041199` (`-25.16%`)** | `0.462431` | `0.691719` | **`+0.229288`** |
| **Panel A (`n = 262`) `qcut(q=4)`** | **`Q3_mid_far`** | `65` | `[0.580956, 0.764319]` | `0.675110` | `3.965552` | `3.498909` | **`-0.466643` (`-11.77%`)** | `0.429642` | `0.568819` | **`+0.139177`** |
| **Panel A (`n = 262`) `qcut(q=4)`** | **`Q4_farthest`** | `66` | `[0.766179, 0.937220]` | `0.830265` | `3.704805` | `3.373694` | **`-0.331111` (`-8.94%`)** | `0.356469` | `0.464147` | **`+0.107679`** |
| **5-Seed (`n = 677`) `qcut(q=4)`** (`[0.364690, 0.597259, 0.774486]`) | **`Q1_closest`** | `170` | `[0.000000, 0.364690]` | `0.233772` | `4.630310` | `3.189286` | **`-1.441024` (`-31.12%`)** | `0.499079` | `0.779276` | **`+0.280197`** |
| **5-Seed (`n = 677`) `qcut(q=4)`** | **`Q2_mid_close`** | `169` | `[0.364807, 0.597259]` | `0.482243` | `4.325292` | `3.259316` | **`-1.065975` (`-24.65%`)** | `0.462424` | `0.711596` | **`+0.249172`** |
| **5-Seed (`n = 677`) `qcut(q=4)`** | **`Q3_mid_far`** | `171` | `[0.600642, 0.774486]` | `0.696820` | `3.892691` | `3.417903` | **`-0.474787` (`-12.20%`)** | `0.421920` | `0.567065` | **`+0.145144`** |
| **5-Seed (`n = 677`) `qcut(q=4)`** | **`Q4_farthest`** | `167` | `[0.775336, 0.937220]` | `0.836290` | `3.820233` | `3.464144` | **`-0.356089` (`-9.32%`)** | `0.364001` | `0.473329` | **`+0.109328`** |

- **Continuous correlation (`nn_dist_go_only`)**:
  - `seeds = 1..2` Panel A ($n = 262$): Spearman $r_s(d_{\text{GO}}, \Delta L_2) = +0.420798$ ($p = 1.1506 \times 10^{-12}$), Spearman $r_s(d_{\text{GO}}, \Delta R_{\Delta}) = -0.410288$ ($p = 4.6401 \times 10^{-12}$).
  - `seeds = 1..5` ($n = 677$): Spearman $r_s(d_{\text{GO}}, \Delta L_2) = +0.489635$ ($p = 4.1704 \times 10^{-42}$), Spearman $r_s(d_{\text{GO}}, \Delta R_{\Delta}) = -0.432494$ ($p = 3.1338 \times 10^{-32}$).
- **Direct Answer to `p2`**: The performance gap between the non-linear graph-resolvent model (`hollow_loo_dual_lens`) and the linear baseline (`lpm_selftrained`) **does not widen** for out-of-distribution perturbations; instead, it is largest in close functional neighborhoods ($Q_1$: $-32.33\%$ $L_2$ reduction on hybrid distance, $-27.68\%$ on static 2023 GO distance) and **narrows monotonically** for functionally isolated perturbations ($Q_4$: $-10.40\%$ on hybrid distance, $-8.94\%$ on static 2023 GO distance), where graph neighborhood propagation smoothly contracts toward the shrinkage bilinear + direct cis-attenuation fallback (`Lens 1`).

---

## Not Claimed

1. **Full Target Win & Partial Progress `p1` (RPE1) Not Claimed**: Full target win and `p1` (`replogle_rpe1_essential`) are not claimed in this package.
2. **Partial Progress `p3` Not Claimed**: `p3` requires re-running the linear baseline and two published deep-learning models (`scGPT`, `GEARS`, `Geneformer`, `scFoundation`, `CPA`, `scVI`) across all five splits of both Replogle datasets; because this package re-runs only the linear and graph-resolvent models, `p3` is not claimed.
3. **Deep-Model Training**: We do not retrain deep foundation models (`scGPT`, `scFoundation`, `Geneformer`, `GEARS`, `CPA`, `scVI`).

---

## Credits

- **Original Benchmark & Paper Authors**: Constantin Ahlmann-Eltze, Wolfgang Huber, and Simon Anders (*Nature Methods* 2025; `https://github.com/const-ae/linear_perturbation_prediction-Paper`).
- **Dataset Creators**: Joseph M. Replogle et al. (*Cell* 2022) and Yusuf Roohani, Kexin Huang, and Jure Leskovec (*Nature Biotechnology* 2024, `gears` Harvard Dataverse data distribution).
- **Package Engineering**: `@mizopl` (`we*`).
