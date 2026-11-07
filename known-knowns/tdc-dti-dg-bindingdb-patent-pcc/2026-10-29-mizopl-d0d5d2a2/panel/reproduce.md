# Skeptic 1 — Reproduce Audit (`tdc-dti-dg-bindingdb-patent-pcc`)

context: fresh review session

## 1. Independent Execution & Cryptographic Verification

- **Target ID:** `tdc-dti-dg-bindingdb-patent-pcc`
- **Submission ID:** `2026-10-29-mizopl-d0d5d2a2`
- **Command Executed:** `sh verify-it-yourself/run_checks.sh`
- **Negative Control Executed:** `/opt/homebrew/bin/python3 verify-it-yourself/verify.py --corrupt`

### Verified Certificate & Object Hashes
- `object/certificate.json`:
  `027ee0b610df47dca9bb52746493f7b2cf264724f42b32c5ae2a295f2b797b82`
- `object/certificate_phase1_cpu_p1_p2.json`:
  `74a7be4004be2b3f500c9690b4e502bfd5fadc05bf069a5b6909f6cd57aa673c`
- `object/manifest_sha256.json`:
  `97ed1afd16d55de3a4768f78143660ee77d63e1f3fb3eb5c737c65522795e386`
- Official TDC Dataset Commitments (cited by URL `https://dataverse.harvard.edu/api/access/datafile/4798216` and SHA-256; zero test labels copied inside `object/`):
  - `data/dti_dg_group.zip` (`9,515,670` bytes): `4708233b8536d856a9ee6522623e4d44bbf7d2efc1c8496e69f6cd2c6482457a`
  - `data/dti_dg_group/bindingdb_patent/train_val.csv` (`183,430` rows, `167,715,236` bytes): `1cb713579f1a9f6f5fe0374e8939da8ae0e6b187fd24c0b0197b54c81ec486b6`
  - `data/dti_dg_group/bindingdb_patent/test.csv` (`49,028` rows, `44,933,376` bytes): `3124f012b92c8c00de39a82ae0ef9d3dd5cc135732bd8bfd420629e1a13dec31`
  - `test_drug_target_keys_sha256` (`49,028` `(Drug, Target)` sequence pairs): `b28e09b01f7990c55ede2facbe7b9831c6dc9203d140dc575814361ae649b674`
  - `test_pair_ids_sha256` (`49,028` `(row_index, Drug_ID, Target_ID)` keys): `0b81510459589882c72484834aec0fac355536645a9b8fd414e1db991d5c51cb`

## 2. Keyed Prediction CSV Verification (`49,028` Rows per Seed)

Every prediction table in `object/` is keyed by `(row_index, Drug_ID, Target_ID, y_pred)` matching `group.get('BindingDB_Patent')['test']` in exact row order (`0..49,027`), split into `_part1.csv` (rows `0..24,513`, `24,514` rows, `~818 KB < 1 MB`) and `_part2.csv` (rows `24,514..49,027`, `24,514` rows, `~828 KB < 1 MB`):

| Track (`object/seed_{1..5}_{track}_part{1,2}.csv`) | Role | Official `group.evaluate_many` | Exact 5-Seed Mean `±` SD | Seed 1..5 Pearson $r$ (`PCC`) |
| :--- | :---: | :---: | :---: | :--- |
| **`trackA_strict_train` (Claimed `p1`)** | `claimed_primary` | **`0.580 ± 0.003`** | **`0.57942 ± 0.00299`** | `0.57856, 0.58064, 0.58094, 0.58287, 0.57410` |
| `trackB_trainval_refit` | `exploratory_ablation` | `0.571 ± 0.003` | `0.57106 ± 0.00260` | `0.57187, 0.57246, 0.56800, 0.57476, 0.56822` |
| `erm_baseline` | `reproduced_baseline` | `0.513 ± 0.003` | `0.51310 ± 0.00271` | `0.51183, 0.51470, 0.51221, 0.51735, 0.50940` |
| `trackF1_bayes_mmse72` | `exploratory_ablation` | `0.600 ± 0.003` | `0.59996 ± 0.00266` | `0.59972, 0.60142, 0.60338, 0.59994, 0.59534` |

## 3. Adversarial Corruption & Negative Control Check

- Running `/opt/homebrew/bin/python3 verify-it-yourself/verify.py --corrupt` or mutating any byte/digit in `object/*.json` or `object/seed_*.csv` is caught by `verify.py` (which prints `FAIL` and exits with code `1`).

pass: true
