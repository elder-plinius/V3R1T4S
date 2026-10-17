status: CONFIRMED_SOLUTION
confirmed_scope: The ternary straight-line program object/2x4x7_m45_cr161_ZT_reduced.json computes the <2,4,7> matrix product exactly over Z at rank 45 (the best rank in fmm_sota.json) using 161 additions/subtractions under Perminov's reduced convention, strictly fewer than the 174 of the best file for 2x4x7 at rank 45 in Perminov's live addition_reduced_ZT directory on 2026-10-17 (and below the 169 of open PR #229), with no lower count on the Lille page or in COVERAGE.md; no claim of optimality or of other formats.
gate_utc: 2026-10-17T05:22:00.000000Z

REPRODUCE passed: all 3136 Brent equations hold, every expanded coefficient is in -1, 0, 1, count 161 (U 35, V 58, W 68), mutation tests all caught. NOVELTY passed: no <2,4,7> rank-45 scheme in any permutation with 161 or fewer additions found in Perminov (min 174), fmm_sota.json, the Lille page, COVERAGE.md, open and closed V3R1T4S PRs (open #229 is 169), or recent literature; search is best-effort. CRITERION passed: literal check of the live criterion, strictly fewer than 174 (and 169), rank equals the best known rank 45.

The confirmation covers this one scheme and the reduced addition count only, not optimality or other formats. Panelists were fresh-context subagents of the same model family. The output C is indexed transposed (k,i), matching Perminov's cyclic layout.
