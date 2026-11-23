# Verification Receipts (`2026-10-30-mizopl-akkfresh`)

- **Command**: `sh verify-it-yourself/run_checks.sh`
- **Execution Time**: `0.48s`
- **Output**:
```text
[1/5] Object SHA-256 digests and byte sizes verified (10/10 files).
[2/5] Verified 38,151 frozen positions (30,545 [MASK]-only, 3,833 kept-token, 3,773 random-token; 0 mismatches).
[3/5] Verified all (MBERT=0.88158, CLSS=0.91421), [MASK]-only (0.86855 vs 0.90506), single-word (0.91944 vs 0.93514), whole-word (0.87594 vs 0.90963), and D8/Q-filtered (0.88143 vs 0.91411) subsets.
[4/5] Verified Full Win (Clause 1 & 2) and Partial Win p1 (> +0.01 overall margin and Table 2 genres Lexical, Astrological Report, Royal Inscription).
[5/5] Verified 400 label-permutation null controls (best_control Hit@5 = 0.21918 << real = 0.91421).
PASS
```
