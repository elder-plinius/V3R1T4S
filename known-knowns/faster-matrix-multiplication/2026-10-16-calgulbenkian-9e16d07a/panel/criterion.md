# Criterion skeptic report: add-5x5x5-cr332

Claim folder hash check (shasum -c against claim.SHA256SUMS, run inside claim/): all 8 files OK.
Object: claim/object/5x5x5_m93_cr332_ZT_reduced.json, sha256 9e16d07a126b9ef0421ed870f464c1f7927b34aa019c8f5a7d7589c15cd37af2.
My own checker was written first (criterion_ws/chk.py, exact integer sparse expansion, no third-party libraries), before reading the author's scripts (which I did not use).

## Own checker output

Claim object:
    {'ok': True, 'tensor_mismatch': 0, 'random_ok': True, 'maxabs_expanded': 1, 'adds_UVW_total': (87, 88, 157, 332)}

- (1) Straight-line order: every form refers only to inputs or earlier fresh variables (a forward or out-of-range reference is rejected; none found). Every written coefficient is +1 or -1 (none else found). Shapes: 93 U factors, 93 V factors, 25 W outputs; fresh variables U 87, V 88, W 55.
- (2) Every fresh variable and every final form was expanded over its map's inputs with exact integers: max absolute expanded coefficient 1, so every intermediate and output is ternary (no cancellation through a non-ternary intermediate).
- (3) Full tensor identity for 5x5 times 5x5: sum over r of U_r[a] V_r[b] W[c][r] equals the Brent target exactly at all (a,b,c) (0 mismatching entries), with output index k*5+i taken as C[i][k] (transposed layout). The program itself, run straight-line on 20 random integer matrix pairs (entries -9..9), gave A*B exactly each time.
- (4) Addition count, reduced convention (sum over fresh and final forms of terms minus 1, negation free): U 87, V 88, W 157, total 332. Matches the file's own "reduced": 332 field.

## Calibration on Perminov's file

Fetched once (curl, honest User-Agent, no retries) 5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json. My counter gives U 103, V 105, W 175, total 383 = the cr383 in the file name, and the same checks pass on it (tensor mismatch 0, random ok, max expanded coefficient 1). So the counter and convention reproduce his number.
Comparison of the two objects: the expanded U, V and W rows (all 93 products, same order) are identical, so the scheme is his. Programs differ in all three maps: the claim's fresh counts are 87/88/55 against his 49/43/68; no map's program is identical to his (u, v, w fresh and final lists all differ). Per map: U 87 vs 103, V 88 vs 105, W 157 vs 175.

## Null models and corruptions (all rejected by my checker)

- Flipped one sign in a W fresh form: rejected (final form expands to a non-ternary coefficient).
- Dropped one term from a U fresh form: rejected (tensor mismatch).
- Shifted one V factor's index by one: rejected (tensor mismatch).
- Forward/out-of-range reference in a U fresh form: rejected (straight-line order).
- Coefficient 2 written in a U fresh form: rejected (coefficient and non-ternary expansion).
- Dropped one term from a W output form: rejected (tensor mismatch).
- Swapped two W outputs (layout error): rejected (tensor mismatch).
- Duplicated index in a fresh form (expands to coefficient 2): rejected (non-ternary expansion).

## Clauses of the criterion

1. "an explicit straight-line program ... for a format <n,m,p> with max(n,m,p) <= 8": MET. Format <5,5,5>, max dimension 5; explicit list of linear forms, 93 products, 25 outputs.
2. "rank r equal to the best rank listed for that format in fmm_sota.json (re-fetched live)": MET. Fetched fmm_sota.json once; the only entry with format [5,5,5] has rank 93 (exponent 2.816262); the object has rank 93.
3. "(1) is verified symbolically to compute the full product A*B exactly over Z": MET. Exact integer expansion of the full tensor (0 mismatches) plus 20 random exact integer evaluations. (The identity was done on the exact integer tensor rather than with a symbolic algebra package; it is the same statement.)
4. "(2) STRICTLY LESS than the smallest reduced addition count for that format and rank in Perminov's live repository ... counted under Perminov's 'reduced' convention": MET for the addition_reduced_ZT directory. The live git tree (fetched once, not truncated, 195 files under schemes/results/addition_reduced_ZT/) holds exactly one 5x5x5 file, cr383, so the minimum cr is 383 and 332 < 383. Only that one file has "cr" in its name for this format. The other 5x5x5 rank-93 count in the tree, schemes/results/naive_addition_reduced_ZT/5x5x5_m93_c843_ZT, is a naive count (nonzeros-based, 843, matching the cn843 in the cr383 file name) under another convention, so it does not compare with a reduced count; the reduced count there is the cr value, and 843 would be beaten by 332 anyway. The tree also lists schemes/reduced_known.json, README.md and CHANGELOG.md; per my brief I did not fetch these, so I did not independently check them for a lower 5x5x5 count. The author's table-record says reduced_known.json has no 5x5x5-93 entry and README/CHANGELOG state no lower count; I report that as the author's statement, not my evidence. Convention (each binary +/- one, negation free, no other scalar) is satisfied and calibrated above.
5. "AND below any lower count published ... on the live Lille per-format page's cited complexity variant": MET vacuously. Fetched https://fmm.univ-lille.fr/5x5x5.html once: rank 93 entry taken from Moosbauer and Poole (arXiv, February 2025), with tensor/LRP/evaluation-scheme downloads; the text has no complexity variant and no operation or addition count (0 hits for complexity, additions, operations, flops). There is no count there to be below. I did not open the linked evaluation-scheme archive (not in my permitted fetches).
6. "... and in matmulcatalog's live COVERAGE.md 'adds' column": MET. The row for <5,5,5> shows 93 and "+846 adds". The legend defines adds as nz(U)+nz(V)+nz(W) minus 2r minus n*p, a naive count (convention different from reduced, so not strictly comparable); even taken at face value 332 < 846. (Note 846 differs from the 843 naive count of Perminov's file; a different scheme or accounting, not material.)
7. "If the Lille rank is attained only with non-ternary coefficients, compare in the same coefficient class": not triggered; the candidate is ternary and the comparison class (Perminov's ZT directory) is ternary.
8. "The reference count is the MINIMUM cr value over all files for that format and rank": 383, single file.
9. "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": MET. Rank 93 equals the live best; the rank is not lowered.

Limits of this check: I did not judge literature novelty or whether another source holds a lower 5x5x5 reduced count (another skeptic does that); the scheme itself is Perminov's (identical product rows), so the win is purely in the straight-line program for his scheme.

## Verdicts

Full criterion: met on the sources named (live fmm_sota.json rank 93; Perminov's only 5x5x5 reduced file at 383; Lille page cites no count; COVERAGE adds +846 naive), with the caveat that reduced_known.json, README and CHANGELOG were not fetched by me.
Partial win p1 (3x3x3 rank 23, fewer than 58 additions) is a different format; not met and not claimed. Under the brief's reading of p1 (strictly fewer than Perminov's live 5x5x5 count, same convention): 332 < 383, met, but it is subsumed by the full criterion here, so the full criterion is the operative verdict.

confirmed_scope: The file claim/object/5x5x5_m93_cr332_ZT_reduced.json (sha256 9e16d07a126b9ef0421ed870f464c1f7927b34aa019c8f5a7d7589c15cd37af2) is a ternary straight-line program that exactly computes the 5x5 by 5x5 product with Perminov's 93 products using 332 reduced additions (U 87, V 88, W 157), against 383 for the only 5x5x5 file in his live addition_reduced_ZT directory (recounted by me), with no count for this rank on the Lille 5x5x5 page and a naive +846 in COVERAGE.md.

context: Claude Code subagent (Fable 5.1), fresh context
p1: true
pass: true
