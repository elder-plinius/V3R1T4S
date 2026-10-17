# Criterion skeptic report: 2x4x7 rank 45, 169 reduced additions

Object: claim/object/2x4x7_m45_cr169_ZT_reduced.json. All claim files matched claim.SHA256SUMS (shasum -c, 8 of 8 OK, run inside the claim folder).
Checker: my own, written from the criterion before opening the author's (criterion_ws/chk.py). It was not compared with the author's checker.

## Clause by clause

1. "format <n,m,p> with max(n,m,p) <= 8": 2x4x7, max 7. MET.
2. "rank r equal to the best rank listed ... in fmm_sota.json (re-fetched live)": fetched once, HTTP 200. Entry {format [2,4,7], rank 45}. The object has 45 products. MET.
3. "(1) verified symbolically to compute the full product A*B exactly over Z":
   - Straight-line order: every term index is an input or an earlier fresh variable in all three maps; 0 forward references. Every coefficient is +1 or -1.
   - Expanded every fresh variable and every final form over the inputs with exact integers. Maximum absolute expanded coefficient is 1, with no non-ternary intermediate.
   - Full Brent identity for 2x4 times 4x7: sum over p of U[p][a] V[p][b] W[o][p] equals the Kronecker delta for all 8*28*14 triples. Output o = l*2+i is C[i][l], the transposed layout. 0 violations.
   - 20 random integer matrix pairs (entries -9..9): all 14 outputs equal A*B.
   - Output of my checker: `rank 45 errs [] per-map ({'fresh': 15, 'final': 20}, {'fresh': 67, 'final': 0}, {'fresh': 26, 'final': 41}) total 169 declared {'naive': 308, 'reduced': 169}`.
   - MET. The check is exact integer expansion plus the Brent identity, which is a complete symbolic proof for a bilinear scheme; I did not use sympy.
4. "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's live repository ... counted under the reduced convention":
   - Count is the sum over all fresh and final forms of (terms - 1), negation free. Total 169. Per map: U 35, V 67, W 67.
   - Calibration: I fetched Perminov's 2x4x7_m45_cr174_cn308_ZT_reduced.json once (HTTP 200). My counter gives 174 (U 35, V 69, W 70), matching its declared 174. It passed my ternary, straight-line and Brent checks.
   - The expanded U, V and W rows of the claim and of Perminov's file are identical (all three equal). So the 45 products are his scheme.
   - The claim's u program (fresh and final) is identical to his. The v and w programs differ: V saves 2 (67 against 69) and W saves 3 (67 against 70), total 5.
   - Tree listing fetched once (HTTP 200, not truncated): addition_reduced_ZT has 258 json files. The only 2x4x7 file, or any permutation, is _m45_cr174_. So the minimum cr for this format and rank is 174, and 169 < 174. MET.
   - Files named like _cNNN_ZT without cr (63 of them, for example 2x3x5_m25_c106_ZT) are the naive count, nz(U)+nz(V)+nz(W)-2r-np style. That is another convention and does not compare. None exists for 2x4x7 anyway. The naive count for this scheme is 308, from the declared complexity field and cn308 in the file name, and COVERAGE.md shows +308 for it.
   - I did not re-read reduced_known.json, README or CHANGELOG (outside my allowed fetch list). The author's record says they have no lower 2x4x7-45 entry. That part rests on the author's record, not on my check.
5. "AND below any lower count published ... on the live Lille per-format page's cited complexity variant":
   - Fetched https://fmm.univ-lille.fr/2x4x7.html once (HTTP 200). It gives rank 45 and an "Algorithm type" polynomial (X^2Y^4Z^2+...+22XYZ), which is a shape descriptor and not an operation count. The source cited is Novikov et al. (AlphaEvolve). The page has no commentary, complexity-variant or addition-count text (grep found 0 hits for commentar or addition). So no lower published count exists there. MET (vacuously).
6. "and in matmulcatalog's live COVERAGE.md 'adds' column":
   - Fetched once (HTTP 200). The 2x4x7 row reads `**45** in F2, R/Q/Z | +308`. The adds column is the naive nz(U)+nz(V)+nz(W)-2r-n*p count. It is 308, higher than 169, and not the reduced convention. No lower count. MET.
7. "If the Lille rank is attained only with non-ternary coefficients ...": not triggered. The object is ternary at rank 45. MET.
8. "The reference count is the MINIMUM cr over all files for that format and rank": 174, the only file. MET.
9. "Each scheme is claimed once; a scheme that also lowers the rank is a rank target": the rank is 45, equal to the best known, so it is not a rank claim. The scheme is Perminov's (same products), so there is no new scheme; the win is addition-count only, which the criterion allows. MET.

## Null models and corruptions (all rejected by my checker)
- Flipped one sign in w_fresh[3]: rejected (brent, eval, nonternary expansion).
- Dropped the last term of v_fresh[10]: rejected (brent, eval); the count fell to 168 and the check still failed.
- Swapped two W output indices (w[5], w[6]): rejected (brent, eval, nonternary expansion).
- Set one coefficient to 2: rejected (coef 2, brent, eval, nonternary).
- Forward reference in u_fresh[0]: rejected (forward ref, brent, eval).
The rejection of the sign flip, the dropped term and the swapped index shows the identity check is sensitive to single-term errors. The same checker accepts Perminov's own file.

## Limits
- Comparison is only against the live sources named in the brief. The claim's wording "fewer than any count published" is only as wide as those sources.
- Per-map: the saving is 5 additions over his program, in V and W only (U unchanged).
- Note on the "n": 3 field in the object JSON: it is an odd metadata value, not used by the check (formats were fixed as 2x4x7 by the input counts 8, 28, 45 and 14 outputs).

## Verdicts
Full criterion: met (as checkable from these sources).
p1 (the 3x3x3 rank-23 partial win): not what this claim is; the object is 2x4x7, so p1 as enumerated in the bank is not met by it. In the brief's reading (strictly fewer than Perminov's live 2x4x7 count, same convention), it is met: 169 < 174.

context: Claude Code subagent (Fable 5.1), fresh context
confirmed_scope: claim/object/2x4x7_m45_cr169_ZT_reduced.json (sha256 ba03797bb02013423a43e98b27ac46c6897018e12f9e90f0761e874c402070d7) is a ternary straight-line program over the inputs that exactly computes the 2x4 times 4x7 product with the 45 products of Perminov's rank-45 scheme (same U, V, W rows as his file), using 169 reduced additions (U 35, V 67, W 67) against his only 2x4x7 rank-45 count of 174, with no lower count on the Lille page or in the COVERAGE.md adds column (naive 308) as fetched 2026-10-15.
p1: true
pass: true
