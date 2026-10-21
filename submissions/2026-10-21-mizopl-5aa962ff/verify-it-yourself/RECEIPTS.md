# Verification Receipts (`2026-10-21-mizopl-5aa962ff`)

- **Command**: `sh verify-it-yourself/run_checks.sh`
- **Execution Time**: `0.42s`
- **Output**:
```text
[1/5] Object SHA-256 digests and byte sizes verified (6/6 files).
[2/5] Verified 27,650 frozen masked positions against seed=42 test tensors (0 mismatches).
[3/5] Verified MBERT+Akk (Hit@5=0.87700, MRR=0.82369) and CLSS-Akk-v3 (Hit@5=0.92156, MRR=0.85593, Hit@1=0.80098, Hit@10=0.94517).
[4/5] Verified Partial Win p1 (> +0.01 overall margin and Table 2 genre subsets Lexical, Astrological Report, Royal or Monumental).
[5/5] Verified 400 label-permutation null controls (best_control Hit@5 = 0.25606 << real = 0.92156).
PASS
```
