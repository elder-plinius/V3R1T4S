status: CONFIRMED_SOLUTION
confirmed_scope: The ternary straight-line program object/3x4x4_m38_cr124_ZT_reduced.json computes the <3,4,4> matrix product exactly over Z at rank 38 (the best rank in fmm_sota.json) using 124 additions/subtractions under Perminov's reduced convention, strictly fewer than the 125 of the best file for 3x4x4 at rank 38 in Perminov's live addition_reduced_ZT directory on 2026-10-16, with no lower count on the Lille page or in COVERAGE.md; no claim of optimality or of other formats.
gate_utc: 2026-10-16T17:47:07.975676Z

REPRODUCE passed: all 2304 Brent equations hold, every expanded coefficient is in -1, 0, 1, count 124 (U 32, V 36, W 56), mutation tests all caught. NOVELTY passed: no <3,4,4> rank-38 scheme in any permutation with 124 or fewer additions found in Perminov (min 125), fmm_sota.json, the Lille page, COVERAGE.md, open and closed V3R1T4S PRs, or recent literature; search is best-effort. CRITERION passed: literal check of the live criterion, strictly fewer than 125, rank equals the best known rank 38.

The confirmation covers this one scheme and the reduced addition count only, not optimality or other formats. Panelists were fresh-context subagents of the same model family. The output C is indexed transposed (k,i), matching Perminov's cyclic layout.
