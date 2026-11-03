# Verification Receipts (`verify-it-yourself/RECEIPTS.md`)

## 1. Standalone Package Verification (`sh verify-it-yourself/run_checks.sh`)

- **Verifier Script:** `verify-it-yourself/verify.py` (`SHA-256: 891335835b8ec6cecba04373a4ae820915abdcaac76747884e7905207ec7ee50`)
- **Certificate Audited:** `object/certificate.json` (`SHA-256: d59325d4892db661c638af2d7d2bdf6e35a6c06f95e869d2bc361470def74ecb`)
- **Predictions Audited:** `object/predictions_tm_polyreactivity.csv` (`SHA-256: 63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`)

```text
=== [1/6] Auditing Object SHA-256 Commitments & Upstream FLAb Data-File Hashes ===
  [PASS] object/certificate.json (d59325d4892db661...), object/predictions_tm_polyreactivity.csv (63cf82e9994c98a2...), and 94 upstream FLAb file SHA-256 commitments verified.

=== [2/6] Auditing Zero-Shot Integrity & No-Copied-Sequences Prediction Table (4,499 Rows) ===
  [PASS] All 4,499 rows across 76 dataset evaluations verified with zero copied sequence data.

=== [3/6] Auditing Single Claimed Method (CLSS_Reg8_AllBP_IMGT_Z) on score/tm & score/polyreactivity ===
  [PASS] Single claimed method CLSS_Reg8_AllBP_IMGT_Z verified on score/tm (+0.4636 vs +0.2169, margin +0.2467) and score/polyreactivity (+0.4467 vs +0.1936, margin +0.2531).

=== [4/6] Auditing Full-Category vs score/-Subset Means & Omitted Datasets ===
  [PASS] Full-category and score/-subset means plus untouched categories (pharmacokinetics +0.2287, data/expression +0.1913) verified.

=== [5/6] Auditing Partial Wins p2 (>=80% Sign Consistency) & p3 (Confound Control) for CLSS_Reg8_AllBP_IMGT_Z ===
  [PASS] Partial Wins p1, p2, and p3 verified for single claimed method CLSS_Reg8_AllBP_IMGT_Z.

=== [6/6] Auditing B=1,000 Permutation Null Battery for CLSS_Reg8_AllBP_IMGT_Z ===
  [PASS] Permutation null battery (B=1,000, p=0.000999) verified.

PASS
```

## 2. Full Benchmark Re-Verification (`python3 how-we-built-it/verify_full_benchmark.py`)

- **Command:** `python3 how-we-built-it/verify_full_benchmark.py` (`SHA-256: 88644033fd678cd8f369fb3b60f5977ff96cff39ba849d70268d4cc2c159b85f`)
- **Wall Time:** `19.65 s` | **CPU Time:** `19.39 s` (single-thread Apple M1 CPU, 16 GB RAM)
- **Unique Antibody Fv/VHH Pairs Scored:** `8,900` (`4,499` prediction rows saved to `object/predictions_tm_polyreactivity.csv`)
- **Output Certificate:** `object/certificate.json` (`SHA-256: d59325d4892db661c638af2d7d2bdf6e35a6c06f95e869d2bc361470def74ecb`)
