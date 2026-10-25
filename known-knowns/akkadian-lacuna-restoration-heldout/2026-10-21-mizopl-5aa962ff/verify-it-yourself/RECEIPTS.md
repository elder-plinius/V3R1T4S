# Verification Receipts (`2026-10-21-mizopl-5aa962ff`)

- **Command**: `sh verify-it-yourself/run_checks.sh`
- **Execution Time**: `0.42s`
- **Output**:
```text
[1/5] Object SHA-256 digests and byte sizes verified (6/6 files).
[2/5] Verified 27,650 frozen positions (22,205 [MASK]-only, 2,723 kept-token, 2,722 random-token; 0 mismatches).
[3/5] Verified all (MBERT=0.87700, CLSS=0.92156), [MASK]-only (0.86463 vs 0.91263), single-word (0.86770 vs 0.91356), whole-word (0.87777 vs 0.92223), and Q-filtered (0.88239 vs 0.92162) subsets.
[4/5] Verified Partial Win p1 (> +0.01 overall margin and Table 2 genre subsets Lexical, Astrological Report, Royal or Monumental).
[5/5] Verified 400 label-permutation null controls (best_control Hit@5 = 0.25378 << real = 0.92156).
PASS
```
