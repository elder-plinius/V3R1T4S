# Skeptic 3 (CRITERION) Adversarial Audit Report — `tdc-dti-dg-bindingdb-patent-pcc`

- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Verdict:** PASS
- **Target ID:** `tdc-dti-dg-bindingdb-patent-pcc`
- **Submission ID:** `2026-10-29-mizopl-d0d5d2a2`
- **Claimed Verdict:** `CONFIRMED_SOLUTION` (satisfying **Full Win** + partial wins **`p1`**, **`p2`**, **`p3`**)

---

## 1. Clause-by-Clause Verification Against `target.md`

| Clause in `target.md` | Requirement | Verified Evidence | Status |
| :--- | :--- | :--- | :---: |
| **5 Saved Prediction Files & Manifest** | Seeds `1–5` from `tdc.BenchmarkGroup(name='DTI_DG_Group')`, `group.get('BindingDB_Patent')`, no re-splitting, 1 prediction per official test pair in official order (`N = 49,028`), manifest with SHA-256 of test `(SMILES, sequence)` key list and TDC files. | Saved in `object/seed_{1..5}_trackC_fullwin.csv`, `seed_{1..5}_trackF2_bayes_mmse75.csv`, `seed_{1..5}_trackF1_bayes_mmse72.csv`, `seed_{1..5}_trackA_strict_train.csv`, and `seed_{1..5}_erm_baseline.csv` + `object/manifest_sha256.json`. | **PASS** |
| **Clause `(a)` Byte-Identical Test Set** | Test set byte-identical to `DTI_DG_Group`'s own (`49,028` rows). | `test.csv` SHA-256 `3124f012...`, `test_drug_target_keys_sha256` `b28e09b01f7990c55ede2facbe7b9831c6dc9203d140dc575814361ae649b674` verified in `step17_zero_trust_skeptic_audit_fullwin.py` and `verify.py`. | **PASS** |
| **Clause `(b)` Higher 5-Seed Mean PCC via `group.evaluate`** | Recomputed through `group.evaluate` / `group.evaluate_many`, strictly higher than live Rank #1 (`Otter-Knowledge-Ensemble = 0.588 ± 0.002`). | `Track F2` (`trackC_fullwin`) achieves **`0.600 ± 0.003`** via `group.evaluate_many` (exact 5-seed mean = **`0.60018 ± 0.00266`**); `Track F1` achieves **`0.600 ± 0.003`** (exact **`0.59996 ± 0.00266`**). | **PASS** |
| **Clause `(c)` Margin `>= +0.010`, `> max(std)`, & `>= 95%` 10k Bootstrap** | Improvement `>= 0.010` absolute (`>= 0.598`), exceeds `max(0.002, our_std)`, and 10,000-resample test-pair bootstrap above listed best in `>= 95%` of resamples. | `Track F2` margin over `0.588` is **`+0.01218 >= +0.010`** (`> max(0.002, 0.00266)`). Over `10,000` test-pair bootstrap resamples (`0.60393 ± 0.00333`), `Track F2` beats `0.588` in **`100.00%` (`10,000 / 10,000`)** of resamples and beats `0.598` in **`96.17% > 95%`** of resamples (`Track F1`: `100.00%` vs `0.588`, `96.22%` vs `0.598`). | **PASS** |
| **Clause `(d)` Strict `train_val` (`2013–2018`) Training & Internal Validation** | Training used only official `train_val` rows (`2013–2018`) of the same seed, with validation carved out of `train_val`. | Model selection used internal temporal validationsplits (`Split A: <=2016 -> 2017–2018`, `Split B: <=2017 -> 2018`, and Full-Horizon OOF `2014–2018`) carved strictly from `train_val`. Each seed `1..5` fits strictly on `tr_df` from `group.get_train_valid_split(..., seed=s)`. | **PASS** |
| **Clause `(e)` Zero External Affinity Data & Declared Pretrained Sequence Model** | No BindingDB/ChEMBL/Papyrus affinity records; sequence/structure models pretrained WITHOUT affinity labels allowed if declared. | Zero external affinity data used. Phase 1 (`Track A = 0.580 ± 0.003`) uses **zero** pretrained models (`100%` CPU-only descriptors/fingerprints). Phase 2 (`Track F1/F2 = 0.600 ± 0.003`) explicitly declares frozen **`facebook/esm2_t12_35M_UR50D`** (trained strictly on UniRef50 protein sequences with zero affinity labels). | **PASS** |

---

## 2. Audit of Partial Wins `p1`, `p2`, and `p3`

1. **`p1` (CPU-Only, No PLM, No GPU vs Rank #2 `OrangeBalls-ProtBertMorgan = 0.538 ± 0.008`):**
   - `Track A` (`strict_train_s`) uses only CPU-computed RDKit fingerprints/descriptors, sequence k-mer/CTD/pocket-alignment features, Cholesky `TKRR`, CG Ridge, and LightGBM/XGBoost/CatBoost/Huber stackers. It achieves **`0.580 ± 0.003`** (`exact 0.57942 ± 0.00299`), beating `0.538` by **`+0.0420` PCC** (`100.00%` bootstrap win rate). **Status: PASS.**
2. **`p2` (Per-Test-Year `2019 / 2020 / 2021` Domain-Shift Decomposition vs Reproduced `ERM`):**
   - Independently verified across all 5 seeds on `2019` ($N=42,009$: `Track F2 = 0.57930`, `Track A = 0.55625` vs `ERM = 0.49720`), `2020` ($N=6,947$: `Track F2 = 0.75931`, `Track A = 0.74675` vs `ERM = 0.64163`), and `2021` ($N=72$: `Track F2 = 0.85358`, `Track A = 0.86212`, `Track B = 0.93419` vs `ERM = 0.07611`). **Status: PASS.**
3. **`p3` & Subset Breakdown (`Seen-Target` vs `Unseen-Target` vs `Unseen-Ligand`):**
   - Independently reported and verified on `Seen-Target` ($N=45,031$: `Track F2 = 0.61533 ± 0.00231`, `Track A = 0.59719 ± 0.00307` vs `ERM = 0.52590`), `Unseen-Target` ($N=3,997 \ge 100$, $49$ novel targets: `Track F2 = 0.20806 ± 0.00546`, `Track A = 0.20577 ± 0.00543`, `Track B = 0.20932` vs `ERM = 0.12204 ± 0.03027`, a `+70.5%` relative improvement over `ERM`), and `Unseen-Ligand` ($N=30,959$: `Track F2 = 0.53020 ± 0.00294`, `Track A = 0.50163 ± 0.00417` vs `ERM = 0.48444`). **Status: PASS.**

---

## 3. Digit-for-Digit Prose-to-Certificate Audit (`K12` / `X12`)

Every metric, standard deviation, seed score, bootstrap win rate, row count, and SHA-256 hash across `README.md`, `INDEX.csv`, `the-record-we-beat/record.md`, `how-we-built-it/artifact.md`, `HOW_WE_FOUND_IT.md`, `null_test.md`, and `panel/*.md` matches `object/certificate.json` (`d0d5d2a2...`) and `object/certificate_phase1_cpu_p1_p2.json` (`b37d6be0...`) digit-for-digit (`0` discrepancies).

**`Verdict: PASS`**

pass: true
