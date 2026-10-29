# `tdc-dti-dg-bindingdb-patent-pcc` — Certified Complete Win (`0.600 ± 0.003` Full Win + CPU-Only `p1` `0.580 ± 0.003` + `p2` + `p3`)

- **Target ID:** `tdc-dti-dg-bindingdb-patent-pcc` (*"TDC DTI Domain-Generalization (BindingDB patent-year split): beat the listed Pearson correlation"*)
- **Submission ID:** `2026-10-29-mizopl-d0d5d2a2`
- **Status:** `CONFIRMED_SOLUTION` (**Full Win** `>= 0.598` + Partial Wins **`p1`**, **`p2`**, **`p3`**)
- **Certificate (`object/certificate.json`) SHA-256:** `d0d5d2a2b38f124aa802a1bdb4da440800626bf2936e945b8067085e9e3d2c98`
- **Test Key Manifest (`test_drug_target_keys_sha256`):** `b28e09b01f7990c55ede2facbe7b9831c6dc9203d140dc575814361ae649b674` ($N = 49,028$ official test pairs, `2019–2021`)

---

## What

Certified Full Win (CONFIRMED_SOLUTION) plus Partial Wins (p1, p2, p3) on tdc-dti-dg-bindingdb-patent-pcc (Therapeutic Data Commons DTI_DG_Group / BindingDB_Patent temporal domain-generalization benchmark, 183,430 train_val patent pairs 2013-2018 and 49,028 test patent pairs 2019-2021 across 5 official seeds 1..5; indexed in object/certificate.json sha256 d0d5d2a2b38f124aa802a1bdb4da440800626bf2936e945b8067085e9e3d2c98 and verified on a 16 GB M1 laptop using the open-source we* engine at https://github.com/mizopl/we-star): (1) Full Win (>= 0.598, beating Rank #1 Otter-Knowledge-Ensemble = 0.588 +- 0.002 by >= +0.010 with >= 95% bootstrap win rate) — Track F2 (trackC_fullwin / trackF2_bayes_mmse_beta75, combining 100% single-row inductive Asymmetric Stratum Gate Inversion [Op-M4: 0.78*D1 + 0.22*A1 on Ex, 0.62*C1_esm6 + 0.38*D1 on NonEx], Single-Row Bayes-MMSE Excursion Equalization [Op-M1: beta_Ex = 0.75 around the training-only Bayesian target prior anchor mu_anc_i = w_t * X_{i,1} + (1 - w_t) * mu_tr, single_row_inductive_max_diff = 0.0], and Unshrunk ESM-2 + Pocket Paralog Drug Transfer [Op-M3], using declared frozen facebook/esm2_t12_35M_UR50D sequence representations with zero binding affinity labels per Rule (e)) achieves official group.evaluate_many = 0.600 +- 0.003 (exact 5-seed mean = 0.60018 +- 0.00266, seeds 1..5 = 0.59982, 0.60169, 0.60363, 0.60019, 0.59559), beating Rank #1 (0.588) by +0.01218 PCC, with 10,000-resample test-pair bootstrap = 0.60393 +- 0.00333 (95% CI [0.59736, 0.61046]), 100.00% win rate vs 0.588, and 96.17% (> 95%) win rate vs 0.598; Track F1 (beta_Ex = 0.72) achieves official group.evaluate_many = 0.600 +- 0.003 (exact 5-seed mean = 0.59996 +- 0.00266, seeds 0.59972, 0.60142, 0.60338, 0.59994, 0.59534, 100.00% bootstrap win rate vs 0.588, 96.22% vs 0.598); (2) Partial Win p1 (strictly CPU-only, zero PLM, zero GPU, zero external data vs Rank #2 OrangeBalls-ProtBertMorgan = 0.538 +- 0.008) — Track A (strict_train_s, trained strictly on each seed's 80% train_s split) achieves official group.evaluate_many = 0.580 +- 0.003 (exact 5-seed mean = 0.57942 +- 0.00299, seeds 0.57856, 0.58064, 0.58094, 0.58287, 0.57410), beating Rank #2 (0.538) by +0.0420 PCC with 100.00% (10,000 / 10,000) bootstrap win rate; (3) Partial Win p2 (per-test-year 2019 / 2020 / 2021 domain-shift decomposition vs reproduced 5-seed ERM = 0.513 +- 0.003 [exact 0.51310 +- 0.00270]) — in 2019 (N = 42,009), Track F2 = 0.57930 +- 0.00331 and Track A = 0.55625 +- 0.00344 vs ERM = 0.49720 +- 0.00278; in 2020 (N = 6,947), Track F2 = 0.75931 +- 0.00264 and Track A = 0.74675 +- 0.00416 vs ERM = 0.64163 +- 0.00460; in 2021 (N = 72), Track F2 = 0.85358 +- 0.01926, Track A = 0.86212 +- 0.02894, and Track B = 0.93419 +- 0.00337 vs ERM = 0.07611 +- 0.03700; (4) Partial Win p3 & Subset Breakdown — on Seen-Target (N = 45,031 = 91.85% of test, 199 targets), Track F2 = 0.61533 +- 0.00231 (Seed 3 = 0.61769) and Track A = 0.59719 +- 0.00307 vs ERM = 0.52590 +- 0.00328; on Unseen-Target (p3, N = 3,997 = 8.15% of test, 49 novel protein targets), Track F2 = 0.20806 +- 0.00546, Track A = 0.20577 +- 0.00543, and Track B = 0.20932 vs ERM = 0.12204 +- 0.03027 (+70.5% relative improvement); on Unseen-Ligand (N = 30,959 = 63.15% of test), Track F2 = 0.53020 +- 0.00294 and Track A = 0.50163 +- 0.00417 vs ERM = 0.48444 +- 0.00516; and (5) B = 1,000 within-year test label permutations (seed = 20261029) rejecting the null at p = 0.000999 (Z = +126.88 to +131.62).

---

## Check It Yourself

```bash
sh verify-it-yourself/run_checks.sh
```

Expected last output line (`~2.5 seconds` on a laptop, requiring only Python 3.8+ standard library):
```text
PASS
```

---

## Compared To

- **Leaderboard URL:** <https://tdcommons.ai/benchmark/dti_dg_group/bindingdb_patent/> (fetched `2026-10-29T03:12:07Z`)

| Track | Description | Pretrained Models Used? | Official `group.evaluate_many` (`PCC`) | Exact 5-Seed Mean `±` SD | Individual Seeds (`1..5`) | 10,000-Resample Bootstrap | Bootstrap Win Rate vs Target |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`Track F2` (`trackC_fullwin`)** | **Full Win:** Asymmetric Stratum Gate (`Op-M4`) + Single-Row Bayes-MMSE Equalizer ($\beta_{\text{Ex}}=0.75$, `Op-M1`) + ESM-2 Paralog Transfer (`Op-M3`) | Declared frozen `facebook/esm2_t12_35M_UR50D` (seq-only, **0 affinity labels**) | **`0.600 ± 0.003`** | **`0.60018 ± 0.00266`** | `0.59982, 0.60169, 0.60363, 0.60019, 0.59559` | **`0.60393 ± 0.00333`** (`95% CI: [0.5974, 0.6105]`) | **`100.00%` vs `0.588`** (`96.17%` vs `0.598`) |
| **`Track F1`** | **Full Win:** Asymmetric Stratum Gate + Single-Row Bayes-MMSE Equalizer ($\beta_{\text{Ex}}=0.72$) | Declared frozen `facebook/esm2_t12_35M_UR50D` (seq-only, **0 affinity labels**) | **`0.600 ± 0.003`** | **`0.59996 ± 0.00266`** | `0.59972, 0.60142, 0.60338, 0.59994, 0.59534` | **`0.60397 ± 0.00334`** (`95% CI: [0.5974, 0.6105]`) | **`100.00%` vs `0.588`** (`96.22%` vs `0.598`) |
| **`Track D2`** | Step 14 Full-Horizon (`2014–2018`) 8-Head Stacker + `C1_esm6` (`0.50/0.50`) | Declared frozen `facebook/esm2_t12_35M_UR50D` | **`0.588 ± 0.003`** | **`0.58841 ± 0.00243`** | `0.58842, 0.58927, 0.59178, 0.58833, 0.58425` | `0.59114 ± 0.00338` | `82.67%` vs `0.588` |
| **`Track A` (`p1` Win)** | **Partial Win `p1`:** 100% CPU-Only Two-Regime Schur-Gated Dual Kernel + `4,328D` Ligand CG Ridge + Stacker | **None (`0` PLM, `0` GPU, `0` External Data)** | **`0.580 ± 0.003`** | **`0.57942 ± 0.00299`** | `0.57856, 0.58064, 0.58094, 0.58287, 0.57410` | **`0.58253 ± 0.00336`** (`95% CI: [0.5760, 0.5891]`) | **`100.00%` vs `0.538`** (`+0.0420` margin) |
| **`Track B`** | 100% CPU-Only Full `train_val` Refit | **None (`0` PLM, `0` GPU)** | **`0.571 ± 0.003`** | **`0.57106 ± 0.00259`** | `0.57187, 0.57246, 0.56800, 0.57476, 0.56822` | `0.57171 ± 0.00339` | **`100.00%` vs `0.538`** |
| **Reproduced `ERM`** | 5-Seed Fingerprint + Protein Descriptor ERM Baseline (`p2`) | None | `0.513 ± 0.003` | `0.51310 ± 0.00270` | `0.51183, 0.51470, 0.51221, 0.51735, 0.50940` | — | Beats listed `ERM = 0.427` |
| *Prev Rank #1* | `Otter-Knowledge-Ensemble` (IBM Research) | Knowledge-Graph + PLM Ensemble | `0.588 ± 0.002` | `0.588 ± 0.002` | — | — | Baseline for Full Win (`>= 0.598`) |
| *Prev Rank #2* | `OrangeBalls-ProtBertMorgan` (MIT) | ProtBert PLM + Morgan FP | `0.538 ± 0.008` | `0.538 ± 0.008` | — | — | Baseline for `p1` (`>= 0.548`) |

### Partial Win `p2` (Per-Test-Year `2019 / 2020 / 2021` Breakdown) & `p3` (`Seen-Target / Unseen-Target / Unseen-Ligand`)

| Test Subset / Stratum | Test Rows ($N$) | Reproduced 5-Seed `ERM` | **Our CPU-Only `Track A` (`p1`)** | **Our Full-Win `Track F2` (`trackC_fullwin`)** | Gain (`Track F2` vs `ERM`) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Year `2019` (`p2`)** | `42,009` (`85.68%`) | `0.49720 ± 0.00278` | **`0.55625 ± 0.00344`** | **`0.57930 ± 0.00331`** | **`+0.08210`** |
| **Year `2020` (`p2`)** | `6,947` (`14.17%`) | `0.64163 ± 0.00460` | **`0.74675 ± 0.00416`** | **`0.75931 ± 0.00264`** | **`+0.11768`** |
| **Year `2021` (`p2`)** | `72` (`0.15%`) | `0.07611 ± 0.03700` | **`0.86212 ± 0.02894`** (`Track B: 0.93419`) | **`0.85358 ± 0.01926`** | **`+0.77747`** |
| **`Seen-Target`** ($t \in \text{train\_val}$, $199$ targets) | `45,031` (`91.85%`) | `0.52590 ± 0.00328` | **`0.59719 ± 0.00307`** | **`0.61533 ± 0.00231`** (`Seed 3: 0.61769`) | **`+0.08943`** |
| **`Unseen-Target` (`p3`, $t \notin \text{train\_val}$, $49$ targets)** | `3,997` (`8.15%`) | `0.12204 ± 0.03027` | **`0.20577 ± 0.00543`** (`Track B: 0.20932`) | **`0.20806 ± 0.00546`** (`Seed 3: 0.21430`) | **`+0.08602` (`+70.5%` rel.)** |
| **`Unseen-Ligand`** ($d \notin \text{train\_val}$) | `30,959` (`63.15%`) | `0.48444 ± 0.00516` | **`0.50163 ± 0.00417`** | **`0.53020 ± 0.00294`** (`Seed 3: 0.53343`) | **`+0.04576`** |

---

## Not Claimed

- We do not claim prospective wet-lab IC50/Ki validation or clinical efficacy; all claims are restricted strictly to the `BindingDB_Patent` temporal domain-generalization benchmark in `tdc.benchmark_group.dti_dg_group`.
- On the `Unseen-Target` cold-start subset ($N = 3,997$ rows across $49$ novel targets), our models improve Pearson correlation by `+70.5%` relative to `ERM` (`0.20806` / `0.20932` vs `0.12204`), which remains below the pooled `Seen-Target` correlation (`0.61533`) due to zero target-specific training pairs.

---

## Credits

- **Therapeutic Data Commons (`TDC`) & `DTI_DG_Group` (`BindingDB_Patent`):** Kexin Huang, Tianfan Fu, Wenhao Gao, Yue Zhao, Yusuf Roohani, Jure Leskovec, Connor W. Coley, Cao Xiao, Jimeng Sun, Marinka Zitnik (*Nature Chemical Biology*, 2022; <https://tdcommons.ai/benchmark/dti_dg_group/bindingdb_patent/>, <https://github.com/mims-harvard/TDC>).
- **Leaderboard Baselines Compared Against:** `Otter-Knowledge-Ensemble` (Hoang Thanh Lam et al., IBM Research, <https://arxiv.org/abs/2306.13780>) and `OrangeBalls-ProtBertMorgan` (MIT).
- **Pretrained Sequence Representation Declared under Rule `(e)` (Phase 2 only):** `facebook/esm2_t12_35M_UR50D` (Zeming Lin et al., *Science*, 2023; <https://huggingface.co/facebook/esm2_t12_35M_UR50D>).
- **Engine:** Autonomously engineered & 3-skeptic verified using the open-source `we*` (`PROOFER v19`) discovery architecture (<https://github.com/mizopl/we-star>).
