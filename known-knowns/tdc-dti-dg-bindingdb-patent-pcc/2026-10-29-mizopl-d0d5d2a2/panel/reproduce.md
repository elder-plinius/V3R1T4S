# V3R1T4S Skeptic 1 (REPRODUCE) Audit Report

- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Verdict:** PASS
- **Target ID:** `tdc-dti-dg-bindingdb-patent-pcc`
- **Submission ID:** `2026-10-29-mizopl-d0d5d2a2`
- **Verification Scripts Audited:** `verify-it-yourself/verify.py`, `how-we-built-it/step16_bayes_mmse_asymmetric_gate_5seeds.py`, `how-we-built-it/step17_zero_trust_skeptic_audit_fullwin.py`
- **Certificates Audited:** `object/certificate.json`, `object/certificate_phase1_cpu_p1_p2.json`, `object/skeptic_audit_certificate_fullwin.json`, `object/manifest_sha256.json`

---

## 1. Cryptographic Integrity & SHA-256 Verification

Independently computed SHA-256 digests of the official `PyTDC` (`1.1.15`) `BindingDB_Patent` benchmark files, the ordered `49,028`-pair test `(Drug, Target)` key list, the certificates, and all 35 saved 5-seed prediction CSVs in `object/` match the manifest and certificates byte-for-byte:

| File / Artifact | Computed SHA-256 | Certificate Match |
| :--- | :--- | :---: |
| `data/dti_dg_group/bindingdb_patent/train_val.csv` ($183,430$ rows) | `1cb713579f1a9f6f5fe0374e8939da8ae0e6b187fd24c0b0197b54c81ec486b6` | **PASS** |
| `data/dti_dg_group/bindingdb_patent/test.csv` ($49,028$ rows) | `3124f012b92c8c00de39a82ae0ef9d3dd5cc135732bd8bfd420629e1a13dec31` | **PASS** |
| `test_drug_target_keys_sha256` ($49,028$ `(Drug, Target)` keys) | `b28e09b01f7990c55ede2facbe7b9831c6dc9203d140dc575814361ae649b674` | **PASS** |
| `object/certificate.json` | `d0d5d2a2b38f124aa802a1bdb4da440800626bf2936e945b8067085e9e3d2c98` | **PASS** |
| `object/certificate_phase1_cpu_p1_p2.json` | `b37d6be07df1da22e36283cefb2b6ca8d29cf7c8995ab6cf3fa8511cc11fa5c3` | **PASS** |
| `object/test_labels_and_strata.csv` | `a85c43bc162a9725832a307d1cf6686266c8a2232ca5ad824ceac4a7b5a61039` | **PASS** |

---

## 2. Single-Row Inductive & Zero-Leakage Code Audit

Static and runtime audit of `how-we-built-it/step08_run_5seeds_and_verify.py`, `how-we-built-it/step14_full_horizon_5seeds.py`, `how-we-built-it/step16_bayes_mmse_asymmetric_gate_5seeds.py`, and `how-we-built-it/step17_zero_trust_skeptic_audit_fullwin.py` confirmed:

1. **Strict Seed-Specific Training (`Rule (d)`):** In every seed `s in [1, 2, 3, 4, 5]`, `tr_df, val_df = group.get_train_valid_split(benchmark="BindingDB_Patent", split_type="default", seed=s)`. All target empirical means, Bayesian target anchors $\mu_{\text{anc}, i}$, Cholesky `TKRR` factors, `4,328D` Ligand CG Ridge weights, `552 x 176` Kronecker Bilinear weights, and GBDT/Huber stackers for `Track A`, `Track C1`, `Track D1`, `Track D2`, `Track F1`, and `Track F2` are fit strictly on `tr_df` (`2013–2018`).
2. **100% Single-Row Inductive Test Prediction (`single_row_inductive_max_diff = 0.0`):** `synthesize_bayes_mmse_asymmetric` in `step16_bayes_mmse_asymmetric_gate_5seeds.py` computes each test prediction $\hat{y}_i$ using only row $i$'s training-derived feature vector $X_{i, \cdot}$ and scalar training mean $\mu_{\text{tr}}$. Evaluating rows `[0, 17, 1024, 15000, 32000, 49027]` one row at a time vs in a `49,028`-row batch yields `max_abs_diff = 0.0`.
3. **Zero NaN/Inf & Exact Row Alignment:** Every saved prediction CSV (`seed_{1..5}_*.csv`) has exactly `49,028` finite `float32` rows matching the official `bm["test"]` ordering.

---

## 3. Independent Reproduction of All 5-Seed Metrics

| Track | Official `group.evaluate_many` | Exact 5-Seed Mean `±` SD | Seed 1 | Seed 2 | Seed 3 | Seed 4 | Seed 5 | Match |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`Track F2` (`trackC_fullwin`, $\beta_{\text{Ex}}=0.75$)** | **`0.600 ± 0.003`** | **`0.60018 ± 0.00266`** | `0.59982` | `0.60169` | `0.60363` | `0.60019` | `0.59559` | **PASS** |
| **`Track F1` ($\beta_{\text{Ex}}=0.72$)** | **`0.600 ± 0.003`** | **`0.59996 ± 0.00266`** | `0.59972` | `0.60142` | `0.60338` | `0.59994` | `0.59534` | **PASS** |
| **`Track D2` (`Step 14` Blend)** | **`0.588 ± 0.003`** | **`0.58841 ± 0.00243`** | `0.58842` | `0.58927` | `0.59178` | `0.58833` | `0.58425` | **PASS** |
| **`Track A` (CPU-Only `p1`, Zero PLM)** | **`0.580 ± 0.003`** | **`0.57942 ± 0.00299`** | `0.57856` | `0.58064` | `0.58094` | `0.58287` | `0.57410` | **PASS** |
| **`Track B` (`train_val` Refit, Zero PLM)** | **`0.571 ± 0.003`** | **`0.57106 ± 0.00259`** | `0.57187` | `0.57246` | `0.56800` | `0.57476` | `0.56822` | **PASS** |
| **Reproduced `ERM` Baseline** | `0.513 ± 0.003` | `0.51310 ± 0.00270` | `0.51183` | `0.51470` | `0.51221` | `0.51735` | `0.50940` | **PASS** |

All per-year (`2019`, `2020`, `2021`) and subset (`Seen-Target`, `Unseen-Target`, `Unseen-Ligand`) breakdowns match `object/certificate.json` and `object/certificate_phase1_cpu_p1_p2.json` to `< 1e-5`. **Verdict: PASS.**

pass: true
