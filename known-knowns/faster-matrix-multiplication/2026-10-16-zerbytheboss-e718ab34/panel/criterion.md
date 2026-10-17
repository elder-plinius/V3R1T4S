# CRITERION skeptic

context: subagent (fresh context; saw only this package, kit/ docs and the target file known-unknowns/algorithms/fmm-additive-complexity-records.md)

## Criterion (live, "What counts as a win")
SLP for <n,m,p>, max(n,m,p) <= 8, rank r = best rank in live fmm_sota.json; (1) verified symbolically over Z; (2) additions STRICTLY LESS than the minimum cr over all addition_reduced_ZT files for that format and rank (live), under Perminov's reduced convention, AND below any lower count on the Lille page's cited complexity variant and matmulcatalog COVERAGE.md 'adds'. Each scheme claimed once; a rank-lowering scheme is a rank target.

## Literal check
- Format <2,4,7>: max dim 7 <= 8. OK.
- Rank: live fmm_sota.json (fetched 2026-10-17T05:18:53Z) lists [2,4,7] rank 45; object has m=45. Equal, not lower. OK.
- Over Z, ternary: package check_slp.py and brent_check.py (stdlib) pass: tensor exact (output order C^T, the same order Perminov's own file uses), all coefficients +-1, straight-line order, 3136 Brent equations. Negative control rejected. OK.
- Count under reduced convention (form of length L costs L-1, negation free): U 35 + V 58 + W 68 = 161. Same counter on Perminov's live 2x4x7_m45_cr174_cn308_ZT_reduced.json (I fetched it) gives 35 + 69 + 70 = 174 (calibrated). A/B forms never share. OK.
- Live Perminov directory listing (GitHub API, 2026-10-17T05:18:50Z): only one 2x4x7 file, cr174 (rank 45). Minimum 174. 161 < 174 strictly (by 13 additions), and also strictly below open PR #229's 169 (by 8 additions). OK.
- Lille 2x4x7 page: rank 45 (AlphaEvolve, 2025), no operation-count variant found; COVERAGE.md 'adds' is the naive count (+308), higher than 161. Nothing lower. OK.
- Not a rank target (rank 45 = best known, not lower). Not a Z2-only scheme. Hidden quantifiers: none found; criterion needs only one format, no "all formats" requirement.
- Not a partial win p1/p2/p3 claim; it is the main criterion for one cell.
- Caveats (not failures): nothing proves optimality; Perminov's repo updates weekly, so re-fetch immediately before submission.

verdict: PASS

confirmed_scope: The ternary straight-line program object/2x4x7_m45_cr161_ZT_reduced.json computes the <2,4,7> matrix product exactly over Z at rank 45 (the best rank in fmm_sota.json) using 161 additions/subtractions under Perminov's reduced convention, strictly fewer than the 174 of the best file for 2x4x7 at rank 45 in Perminov's live addition_reduced_ZT directory on 2026-10-17 (and below the 169 of open PR #229), with no lower count on the Lille page or in COVERAGE.md; no claim of optimality or of other formats.

pass: true
