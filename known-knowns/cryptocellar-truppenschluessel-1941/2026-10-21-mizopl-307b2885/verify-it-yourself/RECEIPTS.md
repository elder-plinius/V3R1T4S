# Verification Receipts — `2026-10-21-mizopl-307b2885` (`cryptocellar-truppenschluessel-1941`, Partial Win `p1`)

## 1. Clean Copy Execution (`sh verify-it-yourself/run_checks.sh`)

```text
[1/5] Object SHA-256 digests and byte sizes verified (6/6 files).
[2/5] Ostwald & Weierud (2021) TS procedure verified on 9/9 worked examples (410/410 chars).
[3/5] 50/50 (100.00%) key cells and 625/625 bigram functional equivalence verified.
[4/5] Plaintext recovery >= 95% verified on all 3 messages (97.84% greedy / 98.71% Viterbi).
[5/5] 200-shuffle null controls (+9.27 SD above mean, +6.42 SD above max) verified.
PASS
```

## 2. Corrupted Copy Rejection

When `object/p1_benchmark_certificate.json` is perturbed (e.g. changing a single character of `k1_recovered` or modifying any byte), `sh verify-it-yourself/run_checks.sh` exits with code `1` and prints `FAIL` on its final line.
