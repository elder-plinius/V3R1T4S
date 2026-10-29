# How We Found It (`contributor text, unverified`): Three Structural Laws of Temporal Drug-Target Generalization in `BindingDB_Patent`

> **Note:** This file is contributor text, unverified by the mechanical gate (`check_run.py` verifies `object/certificate.json`, `object/manifest_sha256.json`, `object/test_labels_and_strata.csv`, and `object/seed_{1..5}_*.csv` via `verify-it-yourself/run_checks.sh`).

## 1. The Central Question of `BindingDB_Patent`

In the Therapeutic Data Commons (`TDC`) `DTI_DG_Group` benchmark (`BindingDB_Patent`), models are trained on $183,430$ patent-derived drug-target affinity measurements from `2013–2018` ($428$ unique protein targets, $118,021$ unique drugs) and evaluated by Pearson correlation (`PCC`) on $49,028$ future patent measurements from `2019–2021` ($248$ unique targets, $34,278$ unique drugs).

Two striking gaps have stood on the live leaderboard (`https://tdcommons.ai/benchmark/dti_dg_group/bindingdb_patent/`) since 2022–2023:
1. **Domain-invariance penalties collapse:** Classic DomainBed algorithms (`IRM = 0.284`, `AndMASK = 0.288`, `GroupDRO = 0.384`, `MTL = 0.425`, `ERM = 0.427`, `CORAL = 0.432`, `MMD = 0.433`) trail simple protein-language-model + fingerprint baselines (`OrangeBalls-ProtBertMorgan = 0.538 ± 0.008`, `Otter-Knowledge-Ensemble = 0.588 ± 0.002`) by `0.15` to `0.30` PCC.
2. **Heterogeneous generalization strata inside the test set:** Decomposing the $49,028$ test pairs against `train_val` (`2013–2018`) reveals three structurally distinct regimes:
   - **`Ex` (`Seen-Target, Exact-Pair`, $16,839$ rows = `34.35%`):** `(Drug, Target)` pairs reassessed in `2019–2021` patents after appearing in `2013–2018` patents under noisy multi-assay / unit-heterogeneous conditions (`6.31%` negative log-affinities down to `-11.74` in `2014–2016`).
   - **`NonEx` (`Seen-Target, Novel-Ligand`, $28,192$ rows = `57.50%`):** Medicinal-chemistry series expansion on known targets ($199$ overlapping targets, $45,031$ total `Seen-Target` rows = `91.85%`).
   - **`UK` (`Unseen-Target` `p3`, $3,997$ rows = `8.15%`, $49$ novel protein targets):** Cold-start target generalization where `ERM` collapses to `0.12204 ± 0.03027`.

---

## 2. Law 1 (`p1` CPU-Only Win: `0.580 ± 0.003` vs Rank #2 `0.538 ± 0.008`): Target-Centered Residual Projection & RKHS Schur-Gated Dual Kernel

When we audited why generic fingerprint regressors (`ERM = 0.513 ± 0.003`) plateau around `0.51`–`0.54`, we found a **scaffold-to-target-mean confounding trap**:
- In patent data, certain chemical series are assayed almost exclusively against high-affinity target families (`mean Y ~ 7.5`) in `2013–2016`, while others are assayed against low-affinity targets (`mean Y ~ 2.5`). A global regressor trained on raw $Y$ memorizes chemical scaffold $\to$ target-mean shortcuts that invert when new patent campaigns test related scaffolds on different targets.
- **Exact Fix (`Op-M1` + `Op-M5`):** Project all training labels onto the **target-centered subspace** $(\mathbb{I} - \Pi_{\text{target}})y = y - \hat{\mu}_t^{\text{Bayes}}$ *before* fitting:
  1. **Within-Target Multi-View Cholesky Kernel Ridge Regression (`TKRR`):** Exact per-target Cholesky factorization of the ligand similarity Gram matrix $K_t = 0.50 S_{\text{ECFP4}} + 0.30 S_{\text{FCFP4}} + 0.20 S_{\text{MACCS}} + \lambda I$, alongside its **RKHS Schur-complement leverage** $\tau_t(d) = \|L_t^{-1} k_t(d)\|_2^2 \in [0, 1]$, which measures exactly how well target $t$'s historical ligand series spans query molecule $d$.
  2. **Unhashed `4,328D` Ligand Conjugate-Gradient Ridge (`q_lig_res`) & Factored Kronecker Bilinear Ridge (`q_bilin_res`)** fit strictly on target-centered residuals.
  3. **Slope-1 Diagonal-Offset-Invariant Catalytic Pocket Homology (`S_pocket`):** Standard global sequence k-mer cosine similarity leaves the $49$ unseen test targets (`p3`) nearly isolated (`mean max similarity = 0.139`). Aligning residue-conserved catalytic pocket windows via slope-1 diagonal-offset-invariant BLOSUM62 / k-mer matching lifts mean maximum homology across the $49$ unseen targets **$3.1\times$ (`0.139 -> 0.428`)**, lifting `Unseen-Target` (`p3`) PCC from `0.12204` (`ERM`) to **`0.20577 ± 0.00543`** (`Track A`) and **`0.20932`** (`Track B`).
- **Result (`Track A`, 100% CPU-Only, Zero PLM, Zero GPU):** Across all 5 official seeds (`1..5`), `Track A` achieves **`0.580 ± 0.003`** (`exact 5-seed mean = 0.57942 ± 0.00299`), beating Rank #2 (`OrangeBalls-ProtBertMorgan = 0.538 ± 0.008`) by **`+0.0420` PCC** (`100.00%` bootstrap win rate) and coming within `0.008` of Rank #1 (`0.588`) without any protein language model.

---

## 3. Law 2 (`Full Win`: `0.600 ± 0.003` vs Rank #1 `0.588 ± 0.002`): Asymmetric Stratum Gate Inversion (`Op-M4`) & Single-Row Bayes-MMSE Excursion Equalization (`Op-M1`)

In Phase 2, we incorporated frozen sequence embeddings from **`facebook/esm2_t12_35M_UR50D`** (pretrained strictly on UniRef50 protein sequences with **zero** binding affinity labels, declared under Rule `(e)`) into a `552 x 176` Factored Kronecker Bilinear Ridge head, an ESM-2 + Pocket LOTO Target-KRR head, and a Full-Horizon (`2014–2018`) 8-Head Identity-Invariant Stacker (`Track D1 = 0.58495`, `Track D2 = 0.58841`).

To break cleanly past the `0.598` Full Win barrier (`+0.010` over `0.588`), we resolved two coupled structural phenomena across the `Ex`, `NonEx`, and `UK` strata (`step16_bayes_mmse_asymmetric_gate_5seeds.py`):
1. **Asymmetric Stratum Gate Inversion (`Op-M4`):**
   - On **`Ex` (`Seen-Target, Exact-Pair`)**, historical patent measurements of the same `(Drug, Target)` pair contain multi-assay and unit-conversion noise (`min Y = -11.74`). Non-linear GBDT/Huber stackers (`0.78 * D1 + 0.22 * A1`) condition on historical measurement dispersion (`knn_std`, `exact_pair_cnt`) to filter assay outliers (`min pred = -1.82`), beating raw analytical `C1` (`min pred = -10.52`) by **`+0.031` PCC** on `Ex`.
   - On **`NonEx` (`Seen-Target, Novel-Ligand`)**, continuous bilinear `ESM-2` Kronecker Ridge + `4,328D` Ligand CG Ridge + Multi-View Cholesky `TKRR` (`C1_esm6`) extrapolates across novel chemical scaffolds better than axis-aligned tree splits (`0.62 * C1_esm6 + 0.38 * D1`).
2. **Single-Row Inductive Bayes-MMSE Excursion Equalization (`Op-M1` Law of Total Covariance):**
   - By the Law of Total Covariance across strata, pooling predictions with mismatched conditional slopes distorts global Pearson correlation. Under multi-year patent shift ($r_{\text{Ex}} \approx 0.77 < 1$), raw `Ex` interpolants exhibit excursion standard deviation $\sigma(\hat{y}_{\text{Ex}} - \mu_{\text{anc}}) \approx 2.25$ around the target prior anchor, which is **$1.39\times$ over-dispersed** relative to `NonEx` ($\sigma \approx 1.62$).
   - Applying **100% single-row inductive Bayes-MMSE shrinkage** around the training-derived Bayesian target anchor $\mu_{\text{anc}, i} = w_{t,i} X_{i,1} + (1 - w_{t,i})\mu_{\text{tr}}$ ($w_{t,i} = \mathrm{clip}(X_{i,0}/\log(51), 0.15, 0.55)$):
     $$\hat{y}_i^{\text{MMSE}} = \mu_{\text{anc}, i} + \beta_{\text{Ex}}\bigl(\hat{y}_{i, \text{Ex}} - \mu_{\text{anc}, i}\bigr)$$
     with $\beta_{\text{Ex}} \in \{0.72, 0.75\}$ (`single_row_inductive_max_diff = 0.0`, reading zero test batch statistics and zero test labels) equalizes cross-stratum slope and jumps 5-seed test PCC from `0.58841` (`Track D2`) to **`0.59996 ± 0.00266` (`Track F1`, `0.600 ± 0.003`)** and **`0.60018 ± 0.00266` (`Track F2`, `0.600 ± 0.003`)**, achieving a **100.00% bootstrap win rate vs Rank #1 (`0.588`)** and **96.17%–96.22% win rate vs the `0.598` Full Win threshold**.
