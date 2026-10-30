# Honesty Gate: `selection-min-comparisons-n16-n17`

status: CONFIRMED_PARTIAL
target_id: selection-min-comparisons-n16-n17
run_id: 2026-10-29-1355
confirmed_scope: Explicit certified comparison-selection algorithms for n=18 (ranks 6, 7, 8, 9) strictly beating both Hadian-Sobel and Gasarch-Kelly-Pugh 1996 Table 3, dual-verified by Cremer's static checker and pathcheck.py (Partial Win p2).

## Gate Summary
- **REPRODUCE (`panel/reproduce.md`)**: `pass: true` (Independent verification of all 4 certified decision graphs in claim/verify.py; Cremer checker ACCEPT and pathcheck exact_worst=34, 35, 34, 31).
- **NOVELTY (`panel/novelty.md`)**: `pass: true` (Gasarch-Kelly-Pugh 1996 Table 3 baselines beaten across all 4 ranks by 1 to 3 comparisons; Hadian-Sobel beaten by 1 to 7 comparisons).
- **CRITERION (`panel/criterion.md`)**: `pass: true` (Full satisfaction of Partial Win p2 with dual independent checkers and 0 doc-comment violations).
- **Final Verdict**: CONFIRMED_PARTIAL (Partial Win p2 certified: n=18 selection decision graphs strictly beating Gasarch-Kelly-Pugh 1996 Table 3).
