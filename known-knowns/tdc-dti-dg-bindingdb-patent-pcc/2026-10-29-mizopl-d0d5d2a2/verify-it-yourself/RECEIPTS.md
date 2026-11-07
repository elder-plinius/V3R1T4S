# Verification Receipts: `tdc-dti-dg-bindingdb-patent-pcc` (`2026-10-29-mizopl-d0d5d2a2`)

## 1. Clean Verification Transcript (`sh verify-it-yourself/run_checks.sh`)

```text
Ground-truth rescoring against official TDC test.csv (49028 rows) & train_val.csv (183,430 rows) verified.
Verified TDC DTI_DG BindingDB_Patent package (status=CONFIRMED_PARTIAL, partial_win=p1): Claimed CPU-Only Track A = 0.57942 ± 0.00299 (+0.04142 vs Rank #2 0.538; +0.06632 vs Reproduced ERM 0.51310).
PASS
```

## 2. Corrupted Object Rejection Transcript (`/opt/homebrew/bin/python3 verify-it-yourself/verify.py --corrupt`)

```text
VERIFY ERROR: certificate.json/trackA_strict_train: mean/std 5-seed PCC mismatch
FAIL
```

## 3. Verified Object SHA-256 Commitments

- `object/certificate.json`: `027ee0b610df47dca9bb52746493f7b2cf264724f42b32c5ae2a295f2b797b82`
- `object/certificate_phase1_cpu_p1_p2.json`: `74a7be4004be2b3f500c9690b4e502bfd5fadc05bf069a5b6909f6cd57aa673c`
- `object/manifest_sha256.json`: `97ed1afd16d55de3a4768f78143660ee77d63e1f3fb3eb5c737c65522795e386`
- `object/seed_1_trackA_strict_train_part1.csv`: `3af8d229da5a2722f8b816f8072da8a1941b133fb472c30381d67c7ceb61673e`
- `object/seed_1_trackA_strict_train_part2.csv`: `e4b3575c94a5085f0f0176b1bb43e126f32abe77999c9511e73bf439f9455e2f`
- Official TDC `data/dti_dg_group.zip` (<https://dataverse.harvard.edu/api/access/datafile/4798216>): `4708233b8536d856a9ee6522623e4d44bbf7d2efc1c8496e69f6cd2c6482457a`
- Official TDC `data/dti_dg_group/bindingdb_patent/train_val.csv`: `1cb713579f1a9f6f5fe0374e8939da8ae0e6b187fd24c0b0197b54c81ec486b6`
- Official TDC `data/dti_dg_group/bindingdb_patent/test.csv`: `3124f012b92c8c00de39a82ae0ef9d3dd5cc135732bd8bfd420629e1a13dec31`
