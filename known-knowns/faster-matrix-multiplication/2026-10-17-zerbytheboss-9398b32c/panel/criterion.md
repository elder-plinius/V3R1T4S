# CRITERION Skeptic Audit — `fmm-additive-complexity-records` (`4x5x5`)

- `context`: subagent (fresh invocation)
- `target_id`: `fmm-additive-complexity-records`
- `audit_utc`: `2026-10-17T17:00:10Z`

## Literal Success Criterion Audit

1. **Format & Rank Eligibility (`max(n,m,p)` at most `8` and `r == fmm_sota.json` rank)**:
   - Format is `4x5x5` (`max(4, 5, 5) = 5`, at most `8`).
   - Multiplicative rank is `r = 76`, matching the exact best rank `76` in `sedoglavic/fmm_digest/master/fmm_sota.json`, Lille `4x5x5.html`, and `matmulcatalog` `COVERAGE.md`.
2. **Exact Symbolic Verification Over `Z` (`10,000` Brent Equations)**:
   - All `(4 * 5) * (5 * 5) * (4 * 5) = 20 * 25 * 20 = 10,000` Brent equations hold identically over `Z` with `0` errors, and all step coefficients lie in `{-1, 1}` (ternary SLP with no non-unit scalar multiplications).
3. **Strict Improvement Under Perminov's Reduced Addition Convention**:
   - Each binary addition/subtraction step in `U` (`75` steps), `V` (`84` steps), and `W` (`121` steps) operates solely on previously available variables with no duplicate or out-of-order dependencies.
   - Total reduced additions `cr = 75 + 84 + 121 = 280`, which is strictly less than:
     - Perminov's live `addition_reduced_ZT` record `4x5x5_m76_cr299_fv112_cn530_ZT_reduced.json` and `reduced_known.json` (`299`, margin `-19`),
     - `matmulcatalog` `COVERAGE.md` (`+549`), and
     - Merged V3R1T4S PR `#222` (`281`, margin `-1`).
4. **Hidden Quantifiers, Stretched Definitions, and Null Models**:
   - No hidden scalar multiplications or stretched counting rules; every binary `+/-` is counted strictly under Perminov's `reduced` convention. Null model is not applicable to exact algebraic straight-line programs.

confirmed_scope: An explicit ternary straight-line program in object/4x5x5_m76_cr280_ZT_reduced.json multiplies a 4x5 matrix by a 5x5 matrix over Z at the best known rank r = 76 using 280 reduced additions and subtractions (U 75, V 84, W 121), verified across all 10000 Brent equations over Z, strictly below Perminov's live addition_reduced_ZT record of 299 and merged V3R1T4S PR #222 at 281.

pass: true
