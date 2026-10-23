context: subagent (fork_turns none; isolated capsule)
role: NOVELTY
label: PROVED-HERE

The exact circuit in `claim/scheme.json` uses 156 binary additions/subtractions for the ordered product of a 3×4 matrix and a 4×5 matrix, with rank 47. It strictly improves the lowest applicable full public schedule established by this audit, 159 additions, by 3. The conclusion is about this exact ordered object and the source comparisons below. It does not assert a globally minimal addition count or an exhaustive literature theorem.

Audit completed UTC: 2026-10-14T14:00:11.311552+00:00.
Candidate SHA256: e227d795fa1418070e30f21b18eac6a55d7426e51cfc8f8ef99c57b831d021f2.

## Independent exact-object comparison

`panel/novelty-data/audit.py` expands every fresh variable into its original linear coordinates and checks every coefficient of the full multiplication tensor over Z. It counts literal binary sums independently. The candidate has U=38, V=44, W=74, total 156. Its normalized signed term multiset is the same as Perminov’s rank-47 ternary tensor and the actual object from public PR 24. Thus this is a shorter evaluation schedule for a pre-existing tensor, not a new rank decomposition.

The current `fmm_sota.json` entry is format `[3,4,5]`, rank 47. The complete Perminov and matmulcatalog Git trees both return `truncated: false`. Exact whole-format filename matching covers all six permutations of 3,4,5, rather than substring matching larger dimensions. The applicable inventory is saved in `applicable-inventory.json`.

Perminov has 11 files for these formats, 9 at rank 47, including two equivalent Mathematica representations and the Lille-derived tensor text. There is exactly one applicable rank-47 reduced file, `schemes/results/addition_reduced_ZT/3x4x5_m47_cr161_cn277_ZT_reduced.json`; therefore the live minimum filename `cr` is 161. Its actual literal counts are 39+48+74=161, and its full tensor is exact over Z. The two `.m` objects were parsed as data and independently matched to the JSON’s signed terms. `reduced_known.json` gives `Z:276` and `Z2:242` for `3x4x5-47`; the Z2 value is a different coefficient class. The complete live README and CHANGELOG contain no lower addition schedule for this cell.

The current Lille 3×4×5 page cites Fawzi et al.’s AlphaTensor decomposition and links the tensor, LRP, and evaluation program. It contains no cited complexity variant for this cell. All three linked objects were fetched. `lille-audit.py` parses the actual evaluation program without executing source code, expands its 47 products, and checks the full multiplication tensor over Z. Its costs are U=45, V=52, W=82, total 179, including two charged doublings; it has a different signed decomposition from the candidate. This is an actual-object comparison, not an inference from the rank-only page.

Matmulcatalog’s live COVERAGE entry is rank 47 and `+287` in its adds column; the document explicitly identifies that column as a naive nonzero count. All 15 matching rank-47 objects across six ordered formats were fetched, including the actual `slp` fields. The catalog’s copied Perminov reduced circuit costs 161. Its two explicit Perminov SLPs have actual binary counts 41+49+78=168; their scalar instructions are only free negations. The AlphaTensor Z SLP has 47+52+86=185 binary additions plus four nonunit scalar instructions; those four doublings must be charged, giving 189 as a ternary program. The F2-only SLP costs 168 and fails the full Z tensor check, so it is not an applicable Z competitor. Catalog `slp` forms were checked against their stored factors rather than trusting metadata. No inspected applicable catalog SLP reaches 156.

These exact results and first mismatch data are in `audit-results.json` and `lille-audit-results.json`.

## Equivalent public circuits, mixing, and compositions

Signed term normalization removes free pairwise term signs and term order. Axis normalization re-labels the three matrix vertex spaces, including the dual-output transposition. Matching public whole-stage schedules can be combined because their complete signed decomposition matches. The best public combination for this tensor is U=39 from Perminov/PR24, V=46 from PR24, and W=74 from Perminov/PR24: 159 additions. The catalog’s corresponding stages are 41,49,78 and give no improvement. The candidate’s 38,44,74 therefore improves both input stages of the best available complete public combination.

Addition costs are orientation-sensitive although rank is permutation-invariant. `axis-audit.py` explicitly constructs reverse-edge linear circuits, saves all six public PR24 axis variants, verifies every full multiplication tensor, then mechanically converts every variant back to the claimed ordered format. Its scalar control is `y=x0+x1`: original cost 1; transpose `[y,y]` uses two free aliases and costs 0. No sign formula is used as a substitute for an actual circuit.

| Ordered format | Actual transformed PR24 stage costs | Total | Actual total after conversion back to 3×4×5 |
|---|---|---|---|
| 3×4×5 | 39+46+74 | 159 | 159 |
| 3×5×4 | 42+46+74 | 162 | 159 |
| 4×3×5 | 39+42+73 | 154 | 159 |
| 4×5×3 | 46+42+74 | 162 | 159 |
| 5×3×4 | 42+39+73 | 154 | 159 |
| 5×4×3 | 46+39+74 | 159 | 159 |

The 154-addition public variants compute different ordered products. Their exact conversion back costs 159, so they do not supply a 156-or-less schedule for the claimed A*B. The rank table’s description explicitly uses unordered formats; the claim’s definition and actual Lille/Perminov programs specify ordered A and B dimensions. Treating unordered rank indexing as addition-cost invariance would be incorrect. The lower variants and every back-converted object are retained, not discarded. A preliminary internal sign estimate of 159→156 for 3×5×4 was wrong; the explicit construction corrects it to 162.

The simple whole-axis block splits were computed from current known ranks and cover every split position of this shape. The smallest rank is 49. Sharing input preprocessing can reduce linear cost but cannot make these unchanged product lists have rank 47. Nontrivial Kronecker products of factor programs of rank greater than 1 cannot have prime product rank 47. The catalog’s actual rank-47 derived/recombination objects across every axis were also checked; their stated naive counts are 288–296 and they contain no shorter hidden SLP. These are concrete composition screens, not an exclusion of all possible future tensor constructions.

`obvious-cse.py` additionally applies deterministic signed-pair common-subexpression factoring to the opened public dense tensors, including the Moosbauer rank-47 decomposition. Its smallest constructed count is 170. This is labelled HEURISTIC screening and is not used as a lower bound or an optimality certificate. Component mixing, axis circuits and rank-split details are retained in `equivalence-composition-results.json`, `axis-audit-results.json` and `obvious-cse-results.json`.

## Current public claims and primary literature

KNOWN: The fresh trophy file contains no same-cell additive result. The open PR endpoint returns 7 entries and no next-page link. The closed endpoint returns 100 entries on page 1, then 15 on page 2 with no next link. This is the entire 122-PR inventory: 7 open, 115 closed, zero merged. Titles and bodies were screened for every axis permutation. The only same-cell claim is PR 24, now closed; closing a public claim does not erase its object or its novelty relevance. Its file inventory has 21 files and no pagination link. The actual object was fetched at the pinned head commit `0ba21f7ed30eb301b4c84eb834b43a30d61e7739`, SHA256 `197ffad82f4cdd3ea6899fe41fc93c1b7c16917cfa5dba26199fe8143c06292d`, and independently verified at 39+46+74=159. The saved older partial PR inventory in `claim/data/` was not used as current evidence.

The last-24-month search used queries for the exact format, additive complexity, rank 47, counts 154–158, Perminov’s reduction work, and alternative bases. Primary materials actually opened include:

- Perminov, *Parallel Heuristic Exploration for Additive Complexity Reduction in Fast Matrix Multiplication*, https://arxiv.org/html/2512.13365. Its exact 3×4×5 rank47 row has previous 276, naive277, GV170 and GP10/GP40/parallel161. This supplies accessible primary comparison context for the older reduction literature.
- Perminov’s 58-addition 3×3 paper, https://arxiv.org/html/2512.21980, and 2026 meta-flip/serendipitous paper, https://arxiv.org/html/2606.02480; these do not provide a lower schedule for the target cell.
- The primary author repository https://github.com/werekorren/fmm_add_reduction for *The Number of the Beast*. Its first recursive tree was truncated, so direct nonrecursive root and targeted complete subtrees were used. The Moosbauer 345-r47 `.m` and `.exp` objects were fetched; the actual 47-term tensor was verified over Z. Its explicit naive binary sum count is 760, including integer coefficient charges; no target-cell optimized program appears in the inspected format-specific directories or published experiment inventories. Hells-bells contains formats 222,223,224,225,226,227,228,233,234,333,432,532, not this cell.
- The primary catalog paper, https://arxiv.org/html/2606.13408, together with the actual catalog objects already described.
- *Alternative Basis matrix multiplication is fast and stable*, published 26 February 2026, https://link.springer.com/article/10.1007/s00211-026-01531-9, including its live full Table2. Its 3,4,5;47 row gives 298 original linear operations and 238 for the alternative-basis phase. Even before charging input/output basis conversions, 238 exceeds 156; a cheaper kernel cannot be inferred by treating conversions as free.
- The current primary 4×4 rank48 implementation paper, https://arxiv.org/html/2609.12027, and 2026 primary 3×3 papers https://arxiv.org/html/2604.27645, https://arxiv.org/html/2607.28676, https://arxiv.org/abs/2609.32388. These concern different format/rank cells. The latter explicitly gives a 51-addition alternative-basis 3×3 kernel plus 5 conversion additions, 56 in ordinary coordinates. Those conversions are retained in any composition comparison, not erased. Its requested HTML endpoint returned404; the primary abstract endpoint returned200.

No opened primary work or actual public object supplies a rank47, 156-or-less full program for ordered3×4×5. This establishes the stated source-relative novelty comparison; it is not a claim of exhaustive literature coverage.

## Access and receipts

All required binding tables, pages and PR endpoints returned200. Requests used one ordinary GET per URL with the honest user agent `V3R1T4S independent novelty audit (public academic source comparison)`. Sandbox DNS failures did not reach a public server; the same authorized requests were then made with ordinary sandbox escalation. There were no real denial retries, mirror fetches, browser impersonation, credential use, or outward actions.

The two optional denied PDFs in `claim/LITERATURE_ACCESS.md` remain unresolved access gaps: IACR2024/2063.pdf had a real403 at2026-10-14T12:01:02Z; the optional SIAM alternative-basis PDF had a real403 challenge at2026-10-14T13:18:23.764660+00:00 with SHA25652c588c2e38265841bea3da3665a256aa7b70ca1ec48dd4339a2e2c06502a9c4. Neither URL nor an alternate copy was requested. No contents of either denied PDF are asserted here. The accessible primary sources above supply the actual comparison evidence used.

Each of 66 saved retrieval receipts includes URL, UTC, actual HTTP status, response SHA256, response size and headers. Response hashes were mechanically recomputed. There are 65 HTTP200 responses and one optional arXivHTML404. Full receipts are in `panel/novelty-data/receipts.tsv` and beside every downloaded object as `.receipt.json`; primary-source URLs are recorded there without abbreviation. Important receipts:

| Saved source | HTTP | UTC | Response SHA256 |
|---|---|---|---|
| fmm_sota.json | 200 | 2026-10-14T13:38:37.050508+00:00 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 |
| perminov-tree.json | 200 | 2026-10-14T13:38:37.049930+00:00 | 0cb3669d76a7e34604a34d2a204c0bf4e27525ba5348675bea6605d7e7032fab |
| perminov/schemes/results/addition_reduced_ZT/3x4x5_m47_cr161_cn277_ZT_reduced.json | 200 | 2026-10-14T13:39:41.508410+00:00 | d1248a3a32dd03bf5d9216edfdaf6b01be95987d7cefee03f5f9f9645271319a |
| reduced_known.json | 200 | 2026-10-14T13:38:37.050649+00:00 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d |
| lille-3x4x5.html | 200 | 2026-10-14T13:38:38.007291+00:00 | 4719a843d00b97d49c52db2fe20cd431d370869150ac0aa010925e3a4f639e82 |
| catalog-COVERAGE.md | 200 | 2026-10-14T13:38:38.083850+00:00 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 |
| veritas-trophy.md | 200 | 2026-10-14T13:38:38.510011+00:00 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 |
| veritas-open-1.json | 200 | 2026-10-14T13:38:38.515974+00:00 | 41ac8b852be6cb516e63869c7a0359d01e296a9b4be174d96dccbd2ab31e5563 |
| veritas-closed-1.json | 200 | 2026-10-14T13:38:38.930821+00:00 | 5931cf2746947734c307333d7b4cd9296050c4c059fb3a290ffcf0ab7d0b028c |
| veritas-closed-2.json | 200 | 2026-10-14T13:39:44.842883+00:00 | 5c1c7f23821db4c80d81adc8af916389ae22c2689a0abf727a959a68d68bc748 |
| pr24-object.json | 200 | 2026-10-14T13:40:37.105054+00:00 | 197ffad82f4cdd3ea6899fe41fc93c1b7c16917cfa5dba26199fe8143c06292d |

The exact novelty claim passes: the candidate’s full ordered3×4×5 rank47 program costs156, strictly below the established applicable public minimum159. There is no assertion that156 is optimal, that the tensor is new, or that another ordered permutation has no cheaper circuit.

pass: true
