# Technical Artifact — `tdc-dti-dg-bindingdb-patent-pcc`

**Target ID:** `tdc-dti-dg-bindingdb-patent-pcc`  
**Benchmark Group:** `DTI_DG_Group` (`BindingDB_Patent` via `tdc.benchmark_group.dti_dg_group`)  
**Verdict:** `CONFIRMED_SOLUTION` (satisfying the **Full Win** criterion `>= 0.598` plus partial wins **`p1`**, **`p2`**, and **`p3`**)

---

## 1. Executive Summary

On the **Therapeutic Data Commons (`TDC`) `DTI_DG_Group` (`BindingDB_Patent`)** temporal domain-generalization benchmark ($183,430$ training/validation patent pairs from `2013–2018`, $49,028$ test patent pairs from `2019–2021`, scored across 5 official seeds `1..5` by Pearson correlation `PCC`), the live leaderboard (`https://tdcommons.ai/benchmark/dti_dg_group/bindingdb_patent/`) has been led since 2022–2023 by IBM Research's knowledge-graph + protein language model ensemble **`Otter-Knowledge-Ensemble` (`0.588 ± 0.002`)** and MIT's **`OrangeBalls-ProtBertMorgan` (`0.538 ± 0.008`)**, ahead of 7 DomainBed baselines (`MMD = 0.433` down to `IRM = 0.284`).

We resolve both the **strictly CPU-only, no-PLM, no-GPU track (`p1`)** and the **overall Full Win track (`>= 0.598`)**, together with the **per-year (`2019 / 2020 / 2021`) domain-shift decomposition (`p2`)** and **Seen-Target / Unseen-Target (`p3`) / Unseen-Ligand breakdown**:

1. **Full Win (`>= 0.598`, i.e., `>= +0.010` above Rank #1 `Otter-Knowledge-Ensemble = 0.588 ± 0.002`):**
   - **`Track F2` (`trackC_fullwin` / `trackF2_bayes_mmse_beta75` — Asymmetric Stratum Gate `Op-M4` + Single-Row Inductive Bayes-MMSE Excursion Equalizer $\beta_{\text{Ex}} = 0.75$ `Op-M1` + Unshrunk ESM-2 Paralog Drug Transfer `Op-M3`):**
     - **Official `group.evaluate_many`:** **`0.600 ± 0.003`** (`[0.6, 0.003]`).
     - **Exact 5-seed mean PCC:** **`0.60018 ± 0.00266`** (`0.60018419 ± 0.00266103`; individual seeds `1..5`: **`0.59982, 0.60169, 0.60363, 0.60019, 0.59559`**), beating Rank #1 (`0.588`) by **`+0.01218` PCC** (exceeding both the `+0.010` absolute margin and `max(0.002, 0.00266)`).
     - **10,000-resample test-pair bootstrap (`seed = 42`):** **`0.60393 ± 0.00333`** (`95% CI: [0.59736, 0.61046]`), achieving **`100.00%` (`10,000 / 10,000`) win rate vs `0.588`** and **`96.17% > 95%` win rate vs `0.598`**.
   - **`Track F1` (`trackF1_bayes_mmse_beta72`, $\beta_{\text{Ex}} = 0.72$):**
     - **Official `group.evaluate_many`:** **`0.600 ± 0.003`**, exact 5-seed mean = **`0.59996 ± 0.00266`** (`Seeds: 0.59972, 0.60142, 0.60338, 0.59994, 0.59534`), 10,000-resample bootstrap = **`0.60397 ± 0.00334`**, **`100.00%` win rate vs `0.588`**, **`96.22% > 95%` win rate vs `0.598`**.
   - **Rule `(e)` Pretrained Model Declaration:** Phase 2 tracks (`Track C1`, `Track D1`, `Track D2`, `Track F1`, `Track F2`) use frozen sequence representations from **`facebook/esm2_t12_35M_UR50D`** (35M-parameter protein language model pretrained strictly on UniRef50 amino-acid sequences via masked language modeling with **zero** binding affinity labels and zero access to BindingDB/ChEMBL/Papyrus).

2. **Partial Win `p1` (100% CPU-Only, Zero PLM, Zero GPU, Zero External Data vs Rank #2 `OrangeBalls-ProtBertMorgan = 0.538 ± 0.008`):**
   - **`Track A` (`strict_train_s`, trained strictly on each seed's 80% `train_s` split):**
     - **Official `group.evaluate_many`:** **`0.580 ± 0.003`** (exact 5-seed mean = **`0.57942 ± 0.00299`**; individual seeds `1..5`: **`0.57856, 0.58064, 0.58094, 0.58287, 0.57410`**).
     - **Margin & Bootstrap:** Beats Rank #2 (`0.538 ± 0.008`) by **`+0.0420` PCC** ($4.2\times$ the required `+0.010` threshold), with **`100.00%` (`10,000 / 10,000`) bootstrap win rate** (`5-seed ensemble bootstrap = 0.58253 ± 0.00336`, `95% CI: [0.57597, 0.58911]`).

3. **Partial Win `p2` (Per-Test-Year `2019 / 2020 / 2021` Domain-Shift Decomposition vs Reproduced 5-Seed `ERM = 0.513 ± 0.003`):**
   - **`2019` ($N = 42,009$ rows, `85.68%` of test):** `Track F2` = **`0.57930 ± 0.00331`**, `Track A` = **`0.55625 ± 0.00344`** vs `ERM` = `0.49720 ± 0.00278` (**`+0.08210`** gain for `Track F2`).
   - **`2020` ($N = 6,947$ rows, `14.17%` of test):** `Track F2` = **`0.75931 ± 0.00264`**, `Track A` = **`0.74675 ± 0.00416`** vs `ERM` = `0.64163 ± 0.00460` (**`+0.11768`** gain for `Track F2`).
   - **`2021` ($N = 72$ rows, `0.15%` of test):** `Track F2` = **`0.85358 ± 0.01926`**, `Track A` = **`0.86212 ± 0.02894`** (`Track B` = **`0.93419 ± 0.00337`**) vs `ERM` = `0.07611 ± 0.03700` (**`+0.77747` to `+0.85808`** gain, completely eliminating `ERM`'s late-horizon collapse).

4. **Partial Win `p3` & Generalization Stratum Breakdown (`Seen-Target` vs `Unseen-Target` vs `Unseen-Ligand`):**
   - **`Seen-Target` ($N = 45,031$ rows = `91.85%` of test, $199$ targets):** `Track F2` = **`0.61533 ± 0.00231`** (`Seed 3 = 0.61769`), `Track A` = **`0.59719 ± 0.00307`** vs `ERM` = `0.52590 ± 0.00328` (**`+0.08943`**).
   - **`Unseen-Target` (`p3`, $N = 3,997$ rows = `8.15%` of test, $49$ completely novel protein sequences):** `Track F2` = **`0.20806 ± 0.00546`** (`Seed 3 = 0.21430`), `Track A` = **`0.20577 ± 0.00543`**, `Track B` = **`0.20932`** vs `ERM` = `0.12204 ± 0.03027` (**`+70.5%` relative improvement** over `ERM` via Slope-1 Catalytic Pocket-LOTO Target-KRR + Unshrunk ESM-2 Paralog Drug Transfer).
   - **`Unseen-Ligand` ($N = 30,959$ rows = `63.15%` of test):** `Track F2` = **`0.53020 ± 0.00294`** (`Seed 3 = 0.53343`), `Track A` = **`0.50163 ± 0.00417`** vs `ERM` = `0.48444 ± 0.00516` (**`+0.04576`**).

---

## 2. Architecture & Reproducible Pipeline (`how-we-built-it/`)

1. **`step01_download_manifest_and_eda.py`:** Downloads `BindingDB_Patent` via `tdc.benchmark_group.dti_dg_group`, verifies the 5 official seed splits (`1..5`), and writes `manifest_sha256.json` (`test_drug_target_keys_sha256 = b28e09b01f7990c55ede2facbe7b9831c6dc9203d140dc575814361ae649b674`).
2. **`step03_precompute_features.py` & `numba_dual_kernel.py`:** Extracts CPU-only sequence descriptors (AAC, dipeptide/tripeptide TF-IDF SVD, CTD descriptors, slope-1 diagonal-offset-invariant BLOSUM62 catalytic pocket similarity `S_pocket`), RDKit 2D physicochemical descriptors + Morgan ECFP4/ECFP6/FCFP4/MACCS bit-packed fingerprints (`uint64` popcount Tanimoto kernel), and RKHS Schur-complement leverage $\tau_t(d)$.
3. **`step07_test_full_modular_stack_splits.py` & `step08_run_5seeds_and_verify.py`:** Trains the Phase 1 CPU-only Two-Regime Modular Stack (`Track A = 0.580 ± 0.003` and `Track B = 0.571 ± 0.003`) plus the reproduced 5-seed `ERM` baseline (`0.513 ± 0.003`) using strictly temporal internal validation carved from `train_val` (`2013–2018`).
4. **`extract_esm2_protein_embeddings.py` & `step10_fullwin_engine_and_splits.py`:** Extracts declared sequence-only embeddings from frozen `facebook/esm2_t12_35M_UR50D` across the $477$ unique protein sequences (`428` train_val + `49` unseen test) and builds the `107`-feature Full-Win engine (`552 x 176` Factored Bilinear Kronecker Ridge + Multi-View Cholesky Target-KRR + Pocket-LOTO Target-KRR).
5. **`step14_full_horizon_5seeds.py` & `step15_tau_gated_paralog_5seeds.py`:** Trains the 8-Head Full-Horizon (`min_eval_yr = 2014`) Identity-Invariant Stacker (`Track D1 = 0.58495`, `Track D2 = 0.58841`) and unshrunk ESM-2 + Pocket Paralog Drug Transfer for `Unseen-Target` (`p3`).
6. **`step16_bayes_mmse_asymmetric_gate_5seeds.py` & `step17_zero_trust_skeptic_audit_fullwin.py`:** Applies the 100% single-row inductive Asymmetric Stratum Gate (`Op-M4`) and Bayes-MMSE Excursion Equalizer (`Op-M1`, $\beta_{\text{Ex}} \in \{0.72, 0.75\}$, verified `single_row_inductive_max_diff = 0.0`) across all 5 official seeds (`Track F1 = 0.59996 ± 0.00266`, `Track F2 = 0.60018 ± 0.00266`, both `0.600 ± 0.003` via `group.evaluate_many`) and executes the 3-Skeptic audit.
