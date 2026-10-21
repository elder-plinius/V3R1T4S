# CRITERION skeptic

context: subagent (fresh context; saw only this package, kit/ docs and the target file known-unknowns/algorithms/fmm-additive-complexity-records.md)

## Criterion (live, "What counts as a win")
SLP for <n,m,p>, max(n,m,p) <= 8, rank r = best rank in live fmm_sota.json; (1) verified symbolically over Z; (2) additions STRICTLY LESS than the minimum cr over all addition_reduced_ZT files for that format and rank (live), under Perminov's reduced convention, AND below any lower count on the Lille page's cited complexity variant and matmulcatalog COVERAGE.md 'adds'. Each scheme claimed once; a rank-lowering scheme is a rank target.

## Literal check
- Format <3,4,4>: max dim 4 <= 8. OK.
- Rank: live fmm_sota.json (fetched 2026-10-16T17:45Z) lists [3,4,4] rank 38; object has m=38. Equal, not lower. OK.
- Over Z, ternary: package check_slp.py and brent_check.py (stdlib) pass: tensor exact (output order C^T, the same order Perminov's own file uses), all coefficients +-1, straight-line order, 2304 Brent equations. Negative control rejected. OK.
- Count under reduced convention (form of length L costs L-1, negation free): U 32 + V 36 + W 56 = 124. Same counter on Perminov's live 3x4x4_m38_cr125_cn224_ZT_reduced.json (I fetched it) gives 33+36+56 = 125 (calibrated). A/B forms never share. OK.
- Live Perminov directory listing (GitHub API, 2026-10-16T17:45Z): only two 3x4x4 files, cr125 (rank 38) and cr133 (rank 38). Minimum 125. 124 < 125 strictly. OK.
- Lille 3x4x4 page: rank only, no operation-count variant found; COVERAGE.md 'adds' is the naive count (+216), higher than 124. Nothing lower. OK.
- Not a rank target (rank 38 = best known, not lower). Not a Z2-only scheme. Hidden quantifiers: none found; criterion needs only one format, no "all formats" requirement.
- Not a partial win p1/p2/p3 claim; it is the main criterion for one cell. It does not satisfy p3 (needs three formats) and the claim does not say so.
- Caveats (not failures): margin is one addition; nothing proves optimality; Perminov's repo updates weekly, so re-fetch immediately before submission; reduced_known.json 'Z 198' is a different measure and rightly not compared.

verdict: PASS

confirmed_scope: The ternary straight-line program object/3x4x4_m38_cr124_ZT_reduced.json computes the <3,4,4> matrix product exactly over Z at rank 38 (the best rank in fmm_sota.json) using 124 additions/subtractions under Perminov's reduced convention, strictly fewer than the 125 of the best file for 3x4x4 at rank 38 in Perminov's live addition_reduced_ZT directory on 2026-10-16, with no lower count on the Lille page or in COVERAGE.md; no claim of optimality or of other formats.

pass: true
