status: CONFIRMED_SOLUTION
confirmed_scope: The ternary straight-line program object/2x5x6_m47_cr177_ZT_reduced.json computes the <2,5,6> matrix product exactly over Z at rank 47 (the best rank in fmm_sota.json) using 177 additions/subtractions under Perminov's reduced convention, strictly fewer than the 181 of the best file for 2x5x6 at rank 47 in Perminov's live addition_reduced_ZT directory on 2026-10-17, with no lower count on the Lille page or in COVERAGE.md; no claim of optimality or of other formats.
gate_utc: 2026-10-17T06:18:00.000000Z

REPRODUCE passed: all 3600 Brent equations hold, every expanded coefficient is in -1, 0, 1, count 177 (U 38, V 64, W 75), mutation tests all caught. NOVELTY passed: no <2,5,6> rank-47 scheme with 177 or fewer additions found in Perminov (min 181), fmm_sota.json, the Lille page, COVERAGE.md, V3R1T4S PRs, or recent literature. CRITERION passed: literal check of the live criterion, strictly fewer than 181, rank equals the best known rank 47.
