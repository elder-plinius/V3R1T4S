# Verification Receipts (`verify-it-yourself/RECEIPTS.md`)

## 1. Standalone Package Verification (`sh verify-it-yourself/run_checks.sh`)

- **Verifier Script:** `verify-it-yourself/verify.py` (`SHA-256: 3583f9700c89ba0c00bf1d9eaaaaca0566166859880727be705d7b5acf8fbd18`)
- **Certificate Audited:** `object/certificate.json` (`SHA-256: b6be3abe5d0dcff18fcf18d8e7a16f64164d434290274613f79b76f80f598eb6`)
- **Predictions Audited (`109,236` Total Rows Across `172` Dataset Evaluations):**
  - `object/predictions_tm_polyreactivity.csv` (`4,499` rows across `76` dataset evaluations; `SHA-256: 63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`)
  - `object/predictions_binding_part1.csv` (`13,093` rows; `SHA-256: 8e748b57b03ae4b59f8218f29f36c9ca953c24180ded58335ba362716067535c`)
  - `object/predictions_binding_part2.csv` (`13,093` rows; `SHA-256: ba6c287e5b2b68005a7364e80fd35158d22ab28bc0f0cb1703d7a5008afb391c`)
  - `object/predictions_binding_part3.csv` (`13,093` rows; `SHA-256: f34f344dd88ca9f87c664bcfe667685dcbac65957591f48b4220ae94f22cf3c7`)
  - `object/predictions_binding_part4.csv` (`13,093` rows; `SHA-256: 34287e9f3492063ffefe6945c14675530b621eba63852bb3ac8f5d0c3aba750c`)
  - `object/predictions_binding_part5.csv` (`13,093` rows; `SHA-256: 0dc9735f13bfde50d6ee20a49a5ad81627ffc30f79c869287b03eb4097eb0ab3`)
  - `object/predictions_binding_part6.csv` (`13,093` rows; `SHA-256: 927068ffec0443c33ce4434fc2077db3e9665a2fca6738b1189329727ad7c5d3`)
  - `object/predictions_binding_part7.csv` (`13,093` rows; `SHA-256: 52f106d72ed81d0a3e4b4795ebd004ada3d1881d2a3c81751b60a6a3606b76be`)
  - `object/predictions_binding_part8.csv` (`13,086` rows; `SHA-256: f41772d054c180cb6f4dd900d615887973d0e16ee9909cc292cda986b306b912`)

```text
=== [1/6] Auditing Object SHA-256 Commitments & Upstream FLAb Data-File Hashes (190 Files) ===
  [PASS] object/certificate.json (b6be3abe5d0dcff1...), object/predictions_tm_polyreactivity.csv (63cf82e9994c98a2...), and 190 upstream FLAb file SHA-256 commitments verified.

=== [2/6] Auditing Zero-Shot Integrity & No-Copied-Sequences Prediction Tables (109,236 Total Rows) ===
  [PASS] All 109,236 rows across 172 dataset evaluations (4,499 in predictions_tm_polyreactivity.csv + 104,737 across predictions_binding_part1..8.csv) verified with zero copied sequence data.

=== [3/6] Auditing Frozen Method (CLSS_Reg8_AllBP_IMGT_Z) Across All 6 score/ Categories (Including Binding) ===
  [PASS] CLSS_Reg8_AllBP_IMGT_Z verified on score/tm (+0.4636 vs +0.2169), score/polyreactivity (+0.4467 vs +0.1936), and score/binding (-0.0060 for -Kd / +0.0060 for +Kd vs iglm 0.1742; binding not claimed).

=== [4/6] Auditing Full-Category vs score/-Subset Means & Excluded Datasets (Including All 80 data/binding CSVs) ===
  [PASS] Full-category and score/-subset means across thermostability (score/tm + data/thermostability 25-dataset union = +0.2834; p1 not claimed), polyreactivity (26-dataset union = +0.1671), binding (80 data/binding CSVs = -0.0987, 12/15 covered = -0.1123/-0.1640, 68/65 excluded = -0.0964/-0.0837), pharmacokinetics (+0.2287), and data/expression (+0.1913) verified.

=== [5/6] Auditing Claimed Partial Wins p2 (>=80% Sign Consistency) & p3 (Confound Control) for CLSS_Reg8_AllBP_IMGT_Z ===
  [PASS] Claimed Partial Wins p2 and p3 verified for single frozen method CLSS_Reg8_AllBP_IMGT_Z (Full Win and p1 not claimed).

=== [6/6] Auditing B=1,000 Permutation Null Battery for CLSS_Reg8_AllBP_IMGT_Z ===
  [PASS] Permutation null battery (B=1,000, p=0.000999) verified.

PASS
```

## 2. Full Benchmark Re-Verification (`python3 how-we-built-it/verify_full_benchmark.py`)

- **Command:** `python3 how-we-built-it/verify_full_benchmark.py` (`SHA-256: 51a3a05a27708532df677cb5c49043998eff57b8fa6edfc12a85b841f50dcf45`)
- **Wall Time:** `45.95 s` | **CPU Time:** `43.28 s` (single-thread Apple M1 CPU, 16 GB RAM)
- **Unique Antibody Fv/VHH Pairs Scored:** `54,131` across `190` upstream FLAb CSV files (`4,499` prediction rows saved to `object/predictions_tm_polyreactivity.csv` and `104,737` binding prediction rows sharded across `object/predictions_binding_part1..8.csv`)
- **Output Certificate:** `object/certificate.json` (`SHA-256: b6be3abe5d0dcff18fcf18d8e7a16f64164d434290274613f79b76f80f598eb6`)
