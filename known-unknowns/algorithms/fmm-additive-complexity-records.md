# Fast matrix multiplication: fewer additions for a fixed best-known rank (straight-line program records)

⚡ **Algorithms** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

For a fixed FMM scheme rank, the number of additions/subtractions in the straight-line program (SLP) that evaluates the scheme is a secondary but citable record: <2,2,2>:7 needs 15 (proved optimal), <3,3,3>:23 was reduced to 58 additions in Perminov, arXiv:2512.21980 (Dec 2025; cf. arXiv:2601.05272 claiming 59 total operations under its own convention), and the repository now holds a 55-addition file (3x3x3_m23_cr55_cn122_ZT_reduced.json; CHANGELOG 19/10/2026: 'Add November 2025 benchmark schemes with fewer additions required'), and Perminov's repository publishes addition-reduced ternary schemes for every format up to 16x16x16 (schemes/results/addition_reduced_ZT, reduced_known.json; tool ternary_addition_reducer) while the Lille catalogue cites 'best-known complexity' variants per format (e.g. 4x4x4:48 by Dumas-Pernet-Sedoglavic-Stapleton-Tichavsky 2026) and matmulcatalog publishes an 'adds' column (naive count nz(U)+nz(V)+nz(W)-2r-np) and warns its SLP counts are upper bounds from a greedy heuristic. Addition reduction is a well-posed combinatorial optimisation (common-subexpression elimination over ternary linear maps) where heuristics still find improvements, so laptop-scale search is realistic. This entry owns ALL addition-count wins (including for <3,3,3>:23 and <4,4,4>:48); rank improvements belong to the catalogue/moonshot entries. Live check 2026-10-20: addition_reduced_ZT holds 329 files (195 on 2026-10-08), several formats with multiple counts (3x3x3_m23_cr55_cn122, cr56_cn120, cr57_cn119, cr58_cn119/120/122 and cr60; 2x2x9_m32_cr50 and cr59; 4x4x4_m49_cr156_cn474 and cr159_fv100_cn474, i.e. the ternary 4x4 files are rank 49, not 48); reduced_known.json (read 2026-10-08, not re-read) lists '3x3x3-23': Z 60, Z2 60 and '4x4x4-49': Z 325, Z2 196.

## What counts as a win

Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format <n,m,p> with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, docs/additions.md, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

## Partial wins

- **p1:** A rank-23 SLP for <3,3,3> with strictly fewer additions than the live reduced count for 3x3x3 in Perminov's repository (55 in the live directory on 2026-10-20; 58 in arXiv:2512.21980), verified symbolically, under the same counting convention.
- **p2:** A rank-48 SLP for <4,4,4> over Q with strictly fewer total operations than the 'best-known complexity' variant cited on https://fmm.univ-lille.fr/4x4x4.html (Dumas-Pernet-Sedoglavic-Stapleton-Tichavsky 2026), counted under that paper's convention (additions plus scalar multiplications), verified symbolically.
- **p3:** Strict reduced-addition improvements for at least three distinct formats with max dim <= 8 in one shift, each verified symbolically and each below the live addition_reduced_ZT count.

## How a win is checked

Parse the SLP (sequence of assignments t_k = +/- t_i +/- t_j over inputs A_ij, B_jl, intermediate sums, r products, and output assignments). Evaluate it with sympy (or exact integer evaluation at many random integer matrices plus one symbolic pass) and confirm every output equals the corresponding entry of A*B. Count the additions under the stated convention (exclude negations, exclude the r multiplications). Load the reference scheme from Perminov's addition_reduced_ZT directory (and reduced_known.json), recount its additions with the same counter to calibrate the convention, and compare. Re-fetch the repository, the Lille page and COVERAGE.md. Minutes on this Mac.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/dronperminov/FastMatrixMultiplication>

## Sources

- <https://github.com/dronperminov/FastMatrixMultiplication>
- <https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md>
- <https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/additions.md>
- <https://github.com/dronperminov/ternary_addition_reducer>
- <https://github.com/werekorren/fmm_add_reduction>
- <https://github.com/jgdumas/plinopt>
- <https://arxiv.org/abs/2512.21980>
- <https://arxiv.org/abs/2512.13365>
- <https://arxiv.org/abs/2601.05272>
- <https://fmm.univ-lille.fr/4x4x4.html>
- <https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md>
- <https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/README.md>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Run Perminov's ternary_addition_reducer and werekorren's fmm_add_reduction with many random seeds and different pairing heuristics on each addition_reduced_ZT scheme for max dim <= 8; the tools are heuristic, so parallel restarts on 10 cores often shave a few additions.
- Change the scheme, not just the SLP: walk the flip graph among rank-equal schemes (the 'alternative scheme finding' in Perminov's repo) and reduce additions for each; sparser U, V, W typically give shorter SLPs.
- Exact CSE as an optimisation problem: encode common-subexpression elimination for the three linear maps (U, V, W^T) as an ILP or SAT instance for small formats (<2,2,3>, <2,3,3>, <3,3,3>) with a bound one below the record, to either find a shorter SLP or certify optimality for the given scheme.
- Exploit the W map's structure: outputs share many subexpressions; try the 'alternative basis' trick (Karstadt-Schwartz) with change of basis counted separately only if the record's convention allows it; otherwise keep the standard basis.
- Search over the sign/orientation choices of the ternary scheme (U, V, W defined up to scaling of each product by +/-1 and permutation) to maximise shared subexpressions before CSE.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Convention mismatch: additions-only vs total operations vs 'alternative basis' counts; a candidate must be compared under the reference's convention after recounting the reference with the same counter.
- Counting bugs: negations are free but a subtraction is one operation; reusing a subexpression across U and V is allowed only if it is actually the same linear form of the same inputs (A-forms and B-forms never share).
- Rank must equal the catalogue's best rank for the format; fewer additions at a higher rank is not a record here.
- Perminov's repo updates weekly and may already contain a lower count in a file the attacker did not look at; re-fetch the directory listing and CHANGELOG at verification time.
- An SLP that is correct only modulo 2 (from working over GF(2)) is not a valid integer SLP; verify over Z.
- Multiple files per format: compare against the smallest cr in the live directory, not the first one found.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/algorithms/fmm-additive-complexity-records.md
```

Already set up? Say `run V3R1T4S on fmm-additive-complexity-records`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `fmm-additive-complexity-records`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
