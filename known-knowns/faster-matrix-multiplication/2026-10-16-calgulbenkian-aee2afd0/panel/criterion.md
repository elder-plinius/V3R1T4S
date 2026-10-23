# Criterion skeptic report: add-4x5x6-cr348

Checker: my own script written from the criterion before reading the author's (a checker and a comparison script, neither shipped in this package). All claim-folder files match the claim folder's hash list (8 of 8 OK).

## My checker, on the claim object (object/4x5x6_m90_cr348_ZT_reduced.json)
1. Straight-line order and coefficients: every reference points to an input or an earlier fresh variable; every coefficient is +1 or -1; no duplicate references in a form. Errors found: 0.
2. Exact integer expansion of every fresh variable and every final form over the inputs (20 inputs of A for U, 30 of B for V, 90 products for W): every expanded coefficient is in {-1, 0, 1}, so no non-ternary intermediate. Errors: 0.
3. Full tensor identity for 4x5 times 5x6 (all 20*30*24 index combinations, 90 products, output k*4+i read as C[i][k]): 0 violations. Evaluation on 20 random integer matrix pairs: 0 wrong entries.
4. Count (sum of terms minus 1 over all fresh and final forms): U 81 + V 104 + W 163 = 348. The object's own metadata also says reduced 348.

## Calibration on Perminov's file (4x5x6_m90_cr380_fv180_cn1023_ZT_reduced.json, fetched once, sha256 dfad4654...aaebb, matching the author's record)
- My counter gives U 87 + V 119 + W 174 = 380. It passes the same ternary, order and tensor checks. So my counter reproduces his cr380.
- Expanded U rows, V rows and W rows (90 products, 24 outputs) are identical to the claim's. Only the programs differ.
- No map's program is identical to his: fresh counts U 81 vs 41, V 104 vs 52, W 59 vs 87. The claim is lower in all three maps (81<87, 104<119, 163<174).
- The scheme is his (and Kauers-Wood via Lille); the claim states this and does not claim a new scheme.

## Null models (my checker rejects each)
- Flip one sign in a w output: rejected (1 ternary error flag, 21 tensor violations, 20 random misses).
- Drop a term from a v fresh form: rejected (6 tensor violations, 59 random misses; count would be 347, which shows a count alone is not enough).
- Swap two w outputs (index swap): rejected (20 tensor violations).
- Coefficient 2 in a u fresh form: rejected (19 errors).
- Forward reference in a u fresh form: rejected.
- Duplicate reference (a+a) in a fresh form: rejected (non-ternary expansion).

## Clauses
- "explicit straight-line program ... for a format with max(n,m,p) <= 8": 4x5x6, max 6. Met.
- "rank r equal to the best rank listed in fmm_sota.json (re-fetched live)": my fetch of the digest lists format [4,5,6] rank 90 (only entry for that sorted format). Object has 90 products. Met.
- "(1) verified symbolically to compute A*B exactly over Z": exact integer expansion plus full tensor identity, 0 violations. Met.
- "(2) STRICTLY LESS than the smallest reduced addition count ... in Perminov's addition_reduced_ZT ... the reference count is the MINIMUM cr over all files for that format and rank": my fetch of the live tree (not truncated) shows exactly one file for 4x5x6 in schemes/results/addition_reduced_ZT: cr380. Other 4x5x6 files are in other folders (ZT, known, serendipitous_base). 348 < 380. Met. I did not myself fetch reduced_known.json, README or CHANGELOG; I rely on the author's table record (the-record-we-beat/README.md), which says reduced_known.json has no 4x5x6-90 entry and README and CHANGELOG state no lower count. That part is the author's report, not my check.
- The file also in the tree, naive_addition_reduced_ZT/4x5x6_m90_c998_ZT, is a naive count (c998, no cr) in another folder and another convention (a plain nonzero-entry count of the matrices, no shared subexpressions). It does not compare with a reduced cr. It is also above 348 numerically (998 vs 348), so even a loose comparison does not hurt the claim.
- "counted under Perminov's reduced convention": one per binary +/-, negation free, no non-unit scalars. My counter reproduces his 380, so it is the same convention. Met.
- "below any lower count ... on the live Lille per-format page's cited complexity variant": the fetched page for 4x5x6 gives rank 90, a polynomial (Algorithm type), the source (Kauers and Wood, arXiv 2505.05896) and file links. It cites no complexity variant and no operation count. Nothing lower exists to beat. Met (vacuously, with nothing to compare).
- "and in matmulcatalog's live COVERAGE.md adds column": row for 4x5x6 shows 90 (Alphaevolve) and adds +775, defined in the file as nz(U)+nz(V)+nz(W) - 2r - n*p (a naive count, not a reduced SLP count). Not the same convention. Even so, 348 < 775. Met.
- "If the Lille rank is attained only with non-ternary coefficients": not the case here; the object is ternary and the rank-90 file is in the ZT (integer) directory. Not triggered.
- "Each scheme is claimed once: a scheme that also lowers the rank is a rank target": rank is 90, the same as the live best. Not a rank claim. Met.

## Hidden quantifiers and stretched definitions
- "Strictly fewer" is against one file, which is the only one in the directory, so min equals that file.
- The comparison is addition count at fixed rank only. No claim about depth, stability or fresh-variable count; the object has more fresh variables (244 vs 180) than his, which the criterion does not constrain.
- The JSON key n is 3 in both files; I did not interpret it and it did not matter to any check, since I fixed the format 4x5x6 myself from the inputs and outputs.
- Format orientation: I fixed 4x5 times 5x6 with the stated row-major and transposed output layout; the identity holds exactly. A different orientation would not satisfy it (swap null above fails).
- Literature novelty beyond the named sources is not judged here.

## Verdicts
Full criterion: met. A genuine win, not subsumed by any source I fetched (Perminov's only file 380; Lille cites no count; COVERAGE uses a naive count of 775).
p1 (strictly fewer than Perminov's live 4x5x6 count, same convention): met on the same evidence, 348 < 380 (note the enumerated p1 in the bank is stated for 3x3x3 and it is applied here as the same-format analogue; the literal bank p1 about rank-23 3x3x3 is not claimed).

p1: true
confirmed_scope: claim/object/4x5x6_m90_cr348_ZT_reduced.json (sha256 aee2afd0dd35ce54d64786b5439fc37101e55a8a758cfd2a8e572e4431396c8c) is a ternary straight-line program that I verified exactly over Z to compute the 4x5 by 5x6 product with 90 products and 348 reduced additions (U 81, V 104, W 163), below the 380 of the only 4x5x6 file in Perminov's live addition_reduced_ZT directory, with the same 90 products as that file, as of my fetches on 2026-10-15.
context: Claude Code subagent (Fable 5.1), fresh context
pass: true
