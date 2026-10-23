# NOVELTY review

context: subagent; one isolated candidate, format (2,5,6), rank 47.

pass: true

The defensible result is a **179-addition schedule for the existing ternary AlphaEvolve rank-47 decomposition, two additions below the smallest applicable published schedule found in the checked current sources (181)**. This is a fixed-object/current-source comparison. It does not establish a globally optimal addition count, a new tensor decomposition, or a rank improvement.

Candidate SHA-256: `6e554e0ee89a3fda23f7c59d261ca1f27bcb089e141db911246437ca50e931e9`.

## Independent object check

My independent expansion in [novelty-data/audit.py](novelty-data/audit.py) verifies all 3,600 integer bilinear coefficients, expands to ternary coefficients, and counts every fresh-variable and final-output binary operation. It gives U=38, V=65, W=76, total 179. Negation and copying cost zero. The expanded rank-one terms agree, allowing sign transfers and term order, with both the existing AlphaEvolve decomposition and the published reduced-181 decomposition. The inspected known schedules have U/V/W counts 40/65/76 and 42/66/79. Their component-wise minimum is still 181. Thus the improvement is entirely in left-input preprocessing, with sharing counted explicitly.

Results and the independently parsed Lille raw program are in [novelty-data/audit-results.json](novelty-data/audit-results.json). The audit uses no earlier run or reviewer findings; only the supplied claim and the primary responses saved in this review's own data directory.

## Binding current comparisons

| Source | Observed applicable result | Consequence |
|---|---|---|
| [Live fmm_sota.json](https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json) | `[2,5,6]`, rank 47 | Candidate matches the listed best rank. This table is a known-rank table, not a proof of minimal rank. |
| [Perminov full recursive tree](https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1) | `truncated:false`; all six dimension permutations searched, every rank-47 reduced file considered | Exactly one matching reduced file: `2x5x6_m47_cr181_fv63_cn332_ZT_reduced.json`; minimum cr=181. |
| [Reduced-181 program](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x5x6_m47_cr181_fv63_cn332_ZT_reduced.json) | Independently counted 181=40+65+76 | 179 is strictly lower by 2. |
| [reduced_known.json](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json) | No matching permutation at rank 47; `(2,5,6)-48` lists Z2=227 | The rank-48 characteristic-two entry is not an integer rank-47 comparison. |
| [README](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md) and [CHANGELOG](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md) | README lists rank 47; no equal/lower applicable addition result found in either document | No defeating additional record. |
| [Lille per-format page](https://fmm.univ-lille.fr/2x5x6.html), linked [raw evaluation](https://fmm.univ-lille.fr/2x5x6_raw.mpl.bz2) and [LRP](https://fmm.univ-lille.fr/2x5x6_LRP.mpl.bz2) | Page cites AlphaEvolve, rank 47, and has no separate cited complexity variant. Raw schedule uses the same ternary decomposition and has 332 direct-form additions | 332 is not treated as its best reduced cost; known reductions of that same tensor are compared separately at 181 and 187. |
| [matmulcatalog COVERAGE](https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md) and complete untruncated program tree | Cell has rank 47 and `+332`, defined as the nonzero/direct-form count. Actual AlphaEvolve SLP has 187 additions (only free scalar -1); the imported Perminov SLP has 181 | Actual program inspection avoids mistaking 332 for the strongest comparison. Both actual schedules are above 179. |

The catalogue's `(2,6,5)` derived rank-47 tensor is independently confirmed to be an axis permutation of the same AlphaEvolve tensor. Its recorded 334 count is direct-form and it supplies no lower reduced schedule. The other matching catalogue/Perminov serendipitous-base tensors use larger integer or rational coefficients; they supply no counted ternary SLP establishing an applicable equal/lower result. Their larger coefficient multiplications cannot be made free in this comparison.

The full selection and status summaries are [novelty-data/comparison-summary.json](novelty-data/comparison-summary.json). All required binding tables and programs returned HTTP 200. No required table is pending.

## Compositions, preprocessing, and recent primary literature

All single-axis block partitions were checked against the live rank table, including rank-exact outer-product cases when a dimension is 1. The best such composition has rank 50; these do not produce a competing rank 47 program. Rank 47 is prime, so a nontrivial tensor-product construction from two algorithms of ranks greater than 1 cannot attain that exact rank. This is a check of these concrete composition mechanisms, not an exhaustive exclusion of every possible algebraic construction. The catalogue's recombination was inspected explicitly, as above. Shared preprocessing is already included in the 181/187 schedules and in the 179 candidate.

The 24-month search window was 2024-10-14 through 2026-10-14. Primary papers were read rather than relying on search snippets or secondary summaries:

- [Perminov, Parallel Heuristic Exploration, arXiv 2512.13365](https://arxiv.org/html/2512.13365), **Table 1**, directly lists `(2,5,6)` rank 47, naive332, GV189, GP-5=186, GP-40=184, proposed181. Table 6's component-mixing improvements do not list this format. This provides a directly relevant published reduced comparison.
- [AlphaEvolve, arXiv 2506.13131](https://arxiv.org/html/2506.13131) gives rank 47 for this format; its tensor and published reductions were checked above. [Ternary Meta Flip Graphs2511.20317](https://arxiv.org/html/2511.20317), [Small Formats2603.02398](https://arxiv.org/html/2603.02398), and [Serendipitous Product2606.02480](https://arxiv.org/html/2606.02480) provide rank/coefficient-search context, without an applicable equal/lower full-program addition result found.
- [Fast and Stable Arbitrary Precision Approximate Matrix Multiplication2610.13905](https://arxiv.org/html/2610.13905), Tables 1–2, does include `(2,5,6)` **border rank46** and improved leading coefficients. These are approximate schemes with parameter-dependent coefficients and remainders, not an exact integer rank 47 ternary SLP, so they do not defeat this claim.
- [Feasible Trilinear Aggregation2508.01748](https://arxiv.org/html/2508.01748), [Automatic Fast and Accurate Generation2506.19405](https://arxiv.org/html/2506.19405), [An Exact 56-Addition Rank 23 3x3 Scheme2604.27645](https://arxiv.org/html/2604.27645), and [matmulcatalog2606.13408](https://arxiv.org/html/2606.13408) were also checked for applicable explicit programs or compositions. None inspected establishes an equal/lower179 count for the exact target. Alternative-basis kernel counts must include conversions into and out of the ordinary coordinates required by this claim.

The independent `werekorren/fmm_add_reduction` primary repository was additionally examined. Its initial recursive listing was honestly marked `truncated:true`; complete directory-level listings were then fetched. The large hells-bells programs are confined to their listed other shapes, and complete `grey`, `moosbauer`, `other` and `unsorted` inventories expose no matching rank 47 target program. This optional repository check is not represented as a complete untruncated global recursive listing.

**Literature access gaps:** the claim's LITERATURE_ACCESS.md records a genuine earlier IACR 2024/2063 PDF 403 at 2026-10-14T12:01:02Z. I did not request that PDF again, fetch an alternate copy, or claim to have reviewed its full text. Its relevant Greedy-Potential comparison is covered in the accessible later primary paper's Table 1, but the original full-text gap remains. The optional arXiv 2609.32388 HTML endpoint returned 404 in this review and was not retried; its surfaced primary abstract concerns a 3x3 rank 23 kernel and does not establish a target result. These gaps prevent a claim of exhaustive literature clearance; they do not block the fully accessible binding-table comparison.

## Existing submissions and trophy status

[Open PRs](https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=1) were fully paginated: page 1 has 100, page 2 has 19, 119 unique PR numbers; the terminal page has no next link. Titles and bodies were checked for all six target permutations. No matching target claim was found. The live [TROPHY_CASE.md](https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md) contains no applicable target record. Other addition claims have different formats and do not constitute equal/lower target results. No external submission was made.

## Access receipts and decision boundary

Each public source was fetched once per distinct URL, with UTC request time, real HTTP status, response-body SHA-256 and byte count retained in its `.fetch.json`. All 45 receipts are collated in [novelty-data/source-manifest.csv](novelty-data/source-manifest.csv) and [novelty-data/source-manifest.json](novelty-data/source-manifest.json), covering 2026-10-14T12:28:08Z through 12:34:32Z. A preliminary sandbox request failed at DNS before HTTP; ordinary escalated network authorization then allowed the current reads. No claimed HTTP 403 or 404 was retried or represented as successful.

Accept only this wording: **the identified 179-addition SLP beats the smallest applicable result found in the required live tables and inspected accessible primary sources, 181, at their recorded fetch times**. Any known applicable result of 179 or less, including an implicit correctly counted composition or shared schedule, would fail the claim. No such defeat was found. The inaccessible optional literature and non-exhaustive search over all conceivable equivalent tensors remain explicit limits.

pass: true
