# How We Found It: TDC DTI Domain-Generalization (`BindingDB_Patent`)

*(contributor text, unverified)*

## 1. Pre-Test `train_val` Inner Temporal Validation (`step02`–`step07`)

To respect the domain-generalization premise (`2013–2018` `train_val` $\to$ `2019–2021` `test`), we carved two internal temporal validation splits strictly out of `train_val` ($183,430$ rows) before running any test-set evaluation:
- **Inner Temporal Split A (`2013–2016` $\to$ `2017–2018`, $n_{\text{tr}}=125,147$, $n_{\text{va}}=58,283$)**
- **Inner Temporal Split B (`2013–2017` $\to$ `2018`, $n_{\text{tr}}=158,931$, $n_{\text{va}}=24,499$)**

Across `step02`–`step07` (`2026-10-29 04:12:50`–`05:20:09`, all completed before the first test evaluation in `step08` at `05:24:41`), every architectural component and hyperparameter of our CPU-only `Track A` (`p1`) was validated on Inner Splits A and B:

1. **Temporal Target & Ligand Shift Anatomy (`how-we-built-it/step02_inner_temporal_anatomy.py`):**
   - Smoothed target mean baseline ($m=10$) achieved `0.45340` (Split A) and `0.45172` (Split B). Adding smoothed drug residuals raised inner temporal PCC to `0.50615` (Split A) and `0.50157` (Split B).
2. **Per-Target Multi-View Tanimoto Kernel Ridge Regression (`how-we-built-it/step05_test_tkrr_and_cold_models.py`):**
   - Solving exact Cholesky-factored Tanimoto KRR per target over `ECFP4` ($0.45$) + `ECFP6` ($0.20$) + `FCFP4` ($0.25$) + `MACCS` ($0.10$) with mixed polynomial kernel $K_{\text{mix}} = 0.40 K + 0.40 K^2 + 0.20 K^4$ and count-scaled diagonal regularization $\lambda / \sqrt{c_d}$ jumped inner temporal PCC to **`0.57503`** (Split A) and **`0.55863`** (Split B).
3. **Schur-Complement Leverage $\tau_{\text{same}}$ & Homology-Transfer TKRR (`how-we-built-it/step05b_test_homology_tkrr.py`):**
   - Gating same-target TKRR with cross-target homology TKRR using the exact RKHS variance reduction $\tau_{\text{same}}(d, t) = \|L_t^{-1} k_t(d)\|_2^2 \in [0, 1]$ improved inner temporal PCC to `0.57548` (Split A) and `0.56207` (Split B).
4. **Catalytic Pocket-Core Local Alignment `S_pocket` (`how-we-built-it/step06b_inspect_unseen_target_homology.py`) & 4-Level Matryoshka Functional ANOVA + Universal Kriging TKRR (`how-we-built-it/step06_test_universal_kriging_and_unseen.py`):**
   - Replacing global sequence length normalization with 5-mer diagonal seed voting + banded BLOSUM62 Smith-Waterman normalized by a 210-AA catalytic pocket self-score (`S_pocket`) and decomposing $y(d, t) = f_{\text{target}}(t) + f_{\text{ligand}}(d) + f_{\text{bilin}}(d, t) + f_{\text{UK-TKRR}}(d, t)$ jumped inner temporal PCC to **`0.60856`** (Split A) and **`0.58805`** (Split B).
5. **Full 4-Level CPU-Only Homology-Gated Stacker (`how-we-built-it/step07_test_full_modular_stack_splits.py`):**
   - Combining the 4-level Universal Kriging TKRR features with seen-target and cold-target LightGBM/Ridge heads on OOF inner-temporal splits reached **`0.62386`** on Inner Split A (`Seen-Target: 0.63177`, `Unseen-Target: 0.37098`) and **`0.60613`** on Inner Split B (`Seen-Target: 0.61844`, `Unseen-Target: 0.27386`).

---

## 2. First Test Evaluation (`step08`) vs. Post-`step08` Exploratory Phase-2 Runs (`step11`–`step16`)

- **Run #1 (`how-we-built-it/step08_run_5seeds_and_verify.py`, `2026-10-29 05:24:41` — Claimed Primary `Track A` for `p1`):**
  - Evaluated the frozen `step07` CPU-only stacker (`Track A` / `trackA_strict_train`), `Track B` (`trackB_trainval_refit`), and reproduced 5-seed `ERM` (`erm_baseline`) across official seeds `1..5`.
  - `Track A` achieved **`0.580 ± 0.003`** (`0.57942 ± 0.00299`), beating Rank #2 `OrangeBalls-ProtBertMorgan` (`0.538 ± 0.008`) by **`+0.04142 >= +0.010`** (`100.00%` bootstrap win rate) with zero PLM and zero external data.
- **Runs #2–#6 (`step11`, `step12`, `step14`, `step15`, `step16` — Unclaimed Exploratory Phase-2 Ablations):**
  - Subsequent Phase-2 experiments explored adding frozen `esm2_t12_35M_UR50D` sequence embeddings and an Empirical Bayes MMSE exact-repeat gate (`Track F1`, $\beta_{\text{Ex}} = 0.72$ chosen on inner temporal split `0.62903`, achieving `0.59996 ± 0.00266` on test). Because those runs occurred after `step08` had already scored the test set, we narrow our formal claim to **Partial Win `p1` (`Track A`)** and report `Track F1` strictly as an unclaimed exploratory ablation.
