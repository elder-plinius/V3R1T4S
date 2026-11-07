# TDC DTI Domain-Generalization (`BindingDB_Patent`): CPU-Only Partial Win `p1` (`0.580 ± 0.003` Pearson $r$)

## What

Partial Win p1 on TDC DTI Domain-Generalization (BindingDB patent-year split: 2013-2018 train_val -> 2019-2021 test, N = 49,028 across official seeds 1..5): 100% CPU-only 4-Level Matryoshka Functional ANOVA + Universal Kriging Tanimoto Kernel Ridge Regression (TKRR) + Homology-Gated Stacker (Track A, zero PLM, zero GPU, zero external data, with all architectural and hyperparameter choices fixed on train_val inner temporal validation splits 2013-2016 -> 2017-2018 and 2013-2017 -> 2018 prior to the first test-set evaluation in step08) achieves official group.evaluate_many test Pearson r = 0.580 ± 0.003 (exact 5-seed mean 0.57942 ± 0.00299; seeds 0.57856, 0.58064, 0.58094, 0.58287, 0.57410), surpassing Rank #2 OrangeBalls-ProtBertMorgan (0.538 ± 0.008) by +0.04142 (>= +0.010 margin, 100.00% 10,000-resample bootstrap win rate) and reproduced 5-seed ERM (0.51310 ± 0.00270) by +0.06632.

---

## Check It Yourself

```sh
sh verify-it-yourself/run_checks.sh
```

- **Official TDC Dataset Download URL:** <https://dataverse.harvard.edu/api/access/datafile/4798216> (loaded via `from tdc.benchmark_group import dti_dg_group; group = dti_dg_group(path='data/'); bm = group.get('BindingDB_Patent')`; leaderboard page: <https://tdcommons.ai/benchmark/dti_dg_group/bindingdb_patent/>).
- **Official TDC Dataset SHA-256 Commitments (`object/manifest_sha256.json`):**
  - `data/dti_dg_group.zip` (`9,515,670` bytes): `4708233b8536d856a9ee6522623e4d44bbf7d2efc1c8496e69f6cd2c6482457a`
  - `data/dti_dg_group/bindingdb_patent/train_val.csv` (`183,430` rows, `167,715,236` bytes): `1cb713579f1a9f6f5fe0374e8939da8ae0e6b187fd24c0b0197b54c81ec486b6`
  - `data/dti_dg_group/bindingdb_patent/test.csv` (`49,028` rows, `44,933,376` bytes): `3124f012b92c8c00de39a82ae0ef9d3dd5cc135732bd8bfd420629e1a13dec31`
  - `test_drug_target_keys_sha256` (`49,028` `(Drug, Target)` sequence pairs in official test order): `b28e09b01f7990c55ede2facbe7b9831c6dc9203d140dc575814361ae649b674`
  - `test_pair_ids_sha256` (`49,028` `(row_index, Drug_ID, Target_ID)` keys in official test order): `0b81510459589882c72484834aec0fac355536645a9b8fd414e1db991d5c51cb`
- **Where the Object Lives (`object/`):**
  - `object/certificate.json` (`sha256: 027ee0b610df47dca9bb52746493f7b2cf264724f42b32c5ae2a295f2b797b82`)
  - `object/certificate_phase1_cpu_p1_p2.json` (`sha256: 74a7be4004be2b3f500c9690b4e502bfd5fadc05bf069a5b6909f6cd57aa673c`)
  - `object/manifest_sha256.json` (`sha256: 97ed1afd16d55de3a4768f78143660ee77d63e1f3fb3eb5c737c65522795e386`)
  - `object/seed_{1..5}_{track}_part1.csv` (rows `0..24,513`, `24,514` rows) and `object/seed_{1..5}_{track}_part2.csv` (rows `24,514..49,027`, `24,514` rows) for `track in {trackA_strict_train, trackB_trainval_refit, erm_baseline, trackF1_bayes_mmse72}` (`40` files total, each `~818–828 KB < 1 MB`). Every row is keyed by `row_index,Drug_ID,Target_ID,y_pred` matching `group.get('BindingDB_Patent')['test']` one-to-one (`pd.concat([pd.read_csv(part1), pd.read_csv(part2)], ignore_index=True)`).

---

## Compared To

### A. Pre-Test `train_val` Inner Temporal Validation (`step02`–`step07`)

Before the first test-set evaluation in `how-we-built-it/step08_run_5seeds_and_verify.py` (`2026-10-29 05:24:41`), all architectural levels, kernel weights, and hyperparameters of `Track A` were developed and frozen strictly on two inner temporal domain-generalization splits carved out of `train_val` (`2013–2018`, $183,430$ rows):

| Pre-Test Validation Script (`how-we-built-it/`) | Architecture Stage Evaluated on `train_val` Only | Inner Split A (`2013–2016 -> 2017–2018`, $n=58,283$) | Inner Split B (`2013–2017 -> 2018`, $n=24,499$) |
| :--- | :--- | :---: | :---: |
| `step02_inner_temporal_anatomy.py` | Smoothed Target Mean Baseline ($m=10$) | `0.45340` | `0.45172` |
| `step02_inner_temporal_anatomy.py` | Target Mean + Drug Residual Baseline | `0.50615` | `0.50157` |
| `step05_test_tkrr_and_cold_models.py` | Per-Target Multi-View Tanimoto KRR (`TKRR-Mix(1,2,4)`) | `0.57503` | `0.55863` |
| `step05b_test_homology_tkrr.py` | Schur-Coupled Same-Target + Homology-Transfer TKRR | `0.57548` | `0.56207` |
| `step06_test_universal_kriging_and_unseen.py` | 4-Level Matryoshka ANOVA + Pocket-Core (`S_pocket`) + Universal Kriging TKRR | `0.60856` | `0.58805` |
| **`step07_test_full_modular_stack_splits.py`** | **Full 4-Level CPU-Only Stacker (`Track A`, Frozen Pre-Test)** | **`0.62386`** | **`0.60613`** |

### B. 5-Seed Test Results vs. Live Leaderboard (`N = 49,028`, Patents `2019–2021`)

| Track / Entry | Role in Package | Uses PLM / External Data? | Official `group.evaluate_many` (`PCC`) | Exact 5-Seed Mean `±` SD | Seed 1..5 Pearson $r$ (`PCC`) | Bootstrap Win Rate vs Rank #2 (`0.538`) |
| :--- | :---: | :---: | :---: | :---: | :--- | :---: |
| **`Track A` (`trackA_strict_train`)** | **Claimed Primary (`Partial Win p1`)** | **No (`0` PLM, `0` GPU, `0` External Data)** | **`0.580 ± 0.003`** | **`0.57942 ± 0.00299`** | `0.57856, 0.58064, 0.58094, 0.58287, 0.57410` | **`100.00%`** |
| `Track B` (`trackB_trainval_refit`) | Exploratory CPU-Only Refit Ablation | No (`0` PLM, `0` GPU, `0` External Data) | `0.571 ± 0.003` | `0.57106 ± 0.00260` | `0.57187, 0.57246, 0.56800, 0.57476, 0.56822` | `100.00%` |
| `Reproduced ERM` (`erm_baseline`) | Reproduced 5-Seed Baseline | No | `0.513 ± 0.003` | `0.51310 ± 0.00271` | `0.51183, 0.51470, 0.51221, 0.51735, 0.50940` | — |
| `Track F1` (`trackF1_bayes_mmse72`, $\beta_{\text{Ex}}=0.72$) | Unclaimed Exploratory Phase-2 Ablation | Frozen `esm2_t12_35M_UR50D` (seq-only) | `0.600 ± 0.003` | `0.59996 ± 0.00266` | `0.59972, 0.60142, 0.60338, 0.59994, 0.59534` | `100.00%` (`96.22%` vs `0.598`) |
| Live Leaderboard #1: `Otter-Knowledge-Ensemble` | External Reference (IBM Research) | Knowledge-Graph + PLM Ensemble | `0.588 ± 0.002` | `0.588 ± 0.002` | — | — |
| Live Leaderboard #2: `OrangeBalls-ProtBertMorgan` | External Reference (MIT) | ProtBert PLM + Morgan FP | `0.538 ± 0.008` | `0.538 ± 0.008` | — | — |
| Live Leaderboard #3: `MMD` (DomainBed) | External Reference | No | `0.433 ± 0.010` | `0.433 ± 0.010` | — | — |
| Live Leaderboard #5: `ERM` (DomainBed) | External Reference | No | `0.427 ± 0.012` | `0.427 ± 0.012` | — | — |

---

## Not Claimed

1. **Formal Claim Narrowed to Partial Win `p1` (`Track A`):** Across the entire campaign, `6` test-set evaluations were executed (`1` in Phase 1 `step08_run_5seeds_and_verify.py` for the claimed CPU-only `Track A`, followed by `5` post-`step08` exploratory runs in `step11`, `step12`, `step14`, `step15`, and `step16`; see `test_evaluation_audit` in `object/certificate.json`). Because Phase-2 models (`step11`–`step16`) were developed after `step08` had already evaluated `Track A` on the test split, we do **not** claim the Full Win (`Track F1`, $\beta_{\text{Ex}}=0.72$, `0.59996 ± 0.00266 >= 0.5985`) and report `Track F1` strictly as an unclaimed exploratory Phase-2 ablation (`role: "exploratory_ablation"`).
2. **Diagnostic Stratum Breakdowns (`p2` and `p3`):** We report per-year (`2019 / 2020 / 2021`) domain-shift decomposition (`Track A`: `0.55625 / 0.74675 / 0.86212` vs. `Reproduced ERM`: `0.49720 / 0.64163 / 0.07611`) and `Seen-Target` (`0.59719`) vs. `Unseen-Target` (`0.20577` vs. `ERM = 0.12204`, `+68.6%` relative gain) vs. `Unseen-Ligand` (`0.50163` vs. `ERM = 0.48444`) as diagnostic analyses rather than separate headline claims.

---

## Credits

- **Contributors:** `@mizopl` (`we*` — human + autonomous proof & discovery shell `PROOFER v19`).
- **Benchmark & Upstream Data:** Therapeutics Data Commons (`TDC DTI_DG_Group: BindingDB_Patent`, Huang et al., *NeurIPS Datasets and Benchmarks* 2021; <https://tdcommons.ai/benchmark/dti_dg_group/bindingdb_patent/>).
