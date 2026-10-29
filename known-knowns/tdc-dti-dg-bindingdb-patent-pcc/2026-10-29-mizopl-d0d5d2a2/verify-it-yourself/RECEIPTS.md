# Verification Receipts (`2026-10-29-mizopl-d0d5d2a2`)

## 1. Zero-Dependency Standalone Verification (`< 3s`)

Command:
```bash
sh verify-it-yourself/run_checks.sh
```

Output:
```text
[INFO] Loaded object/certificate.json (SHA-256: d0d5d2a2b38f124a...)
[PASS] Full Win (Track F2 / trackC_fullwin, N=49,028, 5 seeds): evaluate_many = 0.600 +- 0.003 (exact 0.60018 +- 0.00266, +0.01218 vs Rank #1 0.588, 100.00% bootstrap win rate vs 0.588, 96.17% vs 0.598)
[PASS] Full Win (Track F1, beta_Ex=0.72): evaluate_many = 0.600 +- 0.003 (exact 0.59996 +- 0.00266) | Track D2: 0.58841 +- 0.00243
[PASS] Partial Win p1 (CPU-Only Track A, Zero PLM, Zero GPU): evaluate_many = 0.580 +- 0.003 (exact 0.57942 +- 0.00299, +0.0420 vs Rank #2 0.538, 100.00% bootstrap win rate)
[PASS] Partial Win p2 (Per-Year Breakdown vs ERM 0.51310): 2019 (N=42,009): F2=0.57930, A=0.55625, ERM=0.49720 | 2020 (N=6,947): F2=0.75931, A=0.74675, ERM=0.64163 | 2021 (N=72): F2=0.85358, A=0.86212, ERM=0.07611
[PASS] Subset Breakdown (p3): Seen-Target (N=45,031): F2=0.61533, A=0.59719, ERM=0.52590 | Unseen-Target (N=3,997): F2=0.20806, A=0.20577, ERM=0.12204 (+70.5% rel) | Unseen-Ligand (N=30,959): F2=0.53020, A=0.50163, ERM=0.48444
PASS
```

## 2. Official `PyTDC` (`DTI_DG_Group`) 5-Seed Evaluation & 3-Skeptic Audit (`how-we-built-it/step17_zero_trust_skeptic_audit_fullwin.py`)

Command:
```bash
python3 how-we-built-it/step17_zero_trust_skeptic_audit_fullwin.py
```

Verified SHA-256 commitments:
- `data/dti_dg_group/bindingdb_patent/train_val.csv` ($N = 183,430$ rows, `2013–2018`): `1cb713579f1a9f6f5fe0374e8939da8ae0e6b187fd24c0b0197b54c81ec486b6`
- `data/dti_dg_group/bindingdb_patent/test.csv` ($N = 49,028$ rows, `2019–2021`): `3124f012b92c8c00de39a82ae0ef9d3dd5cc135732bd8bfd420629e1a13dec31`
- `test_drug_target_keys_sha256`: `b28e09b01f7990c55ede2facbe7b9831c6dc9203d140dc575814361ae649b674`
- `object/certificate.json`: `d0d5d2a2b38f124aa802a1bdb4da440800626bf2936e945b8067085e9e3d2c98`
- `object/certificate_phase1_cpu_p1_p2.json`: `b37d6be07df1da22e36283cefb2b6ca8d29cf7c8995ab6cf3fa8511cc11fa5c3`
- `object/test_labels_and_strata.csv`: `a85c43bc162a9725832a307d1cf6686266c8a2232ca5ad824ceac4a7b5a61039`
