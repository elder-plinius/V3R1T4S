# Verification Receipts (`verify-it-yourself/RECEIPTS.md`)

## 1. Standalone Package Verification (`sh verify-it-yourself/run_checks.sh`)

```text
=== [1/5] Auditing Object SHA-256 Commitments ===
  [PASS] object/certificate.json (e1d0aaa2449c9f1b...) and object/predictions_tm_polyreactivity.csv (f0693a6c25d5d628...) verified.

=== [2/5] Auditing Zero-Shot Integrity & Per-Antibody Prediction Table (723 Antibodies) ===
  [PASS] All 723 antibody sequences across 15 tm and 6 polyreactivity datasets verified.

=== [3/5] Auditing Full Win Criteria (Unweighted & Size-Weighted) Across Thermostability & Polyreactivity ===
  [PASS] Full Win verified across Thermostability (+0.5160 / +0.4636 / +0.3528 vs +0.2169) and Polyreactivity (+0.5052 / +0.4467 / +0.3987 vs +0.1936).

=== [4/5] Auditing Partial Wins p1 (4 Universes), p2 (>=80% Sign Consistency), and p3 (Confound Control) ===
  [PASS] Partial Wins p1, p2, and p3 verified.

=== [5/5] Auditing B=1,000 Permutation Null Batteries & LOCO Cross-Validation ===
  [PASS] Permutation null batteries (B=1,000) and LOCO cross-validation verified.

PASS
```

## 2. Full Benchmark Re-Verification (`python3 how-we-built-it/verify_full_benchmark.py`)

- **Command:** `python3 how-we-built-it/verify_full_benchmark.py`
- **Wall Time:** `14.69 s` | **CPU Time:** `14.02 s` (single-thread Apple M1 CPU, 16 GB RAM)
- **Unique Antibody Fv/VHH Pairs Scored:** `5,961`
- **Output Certificate:** `object/certificate.json` (`SHA-256: e1d0aaa2449c9f1b8f5f83beb8d4dc717ad3f40893b281f1576d73273219c1c5`)
