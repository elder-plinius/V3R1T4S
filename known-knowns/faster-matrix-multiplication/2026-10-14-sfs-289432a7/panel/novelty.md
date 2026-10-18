context: subagent (fork_turns none; isolated capsule)

# Independent novelty review

PROVED-HERE: The explicit integer ternary circuit in `claim/scheme.json` has format `(2,4,8)`, rank 51, and 182 binary additions/subtractions. It strictly improves the lowest applicable public circuit found in the required current sources and public claims, which has 187 additions. This verdict concerns that one object and the current-source comparison. It is not a global optimality theorem or an exhaustive-literature claim.

The input was this run's isolated `claim/` capsule. I read the repository's `AGENTS.md`, `kit/RULES.md`, `kit/POLICY.md`, and panel/honesty-gate instructions in `kit/RUN.md`. I did not read this run's attempts, charter, sibling panel reports, other run capsules, or prior local verdicts. External public PR descriptions and their object evidence were comparison data.

## Independent programme comparison

PROVED-HERE: `novelty-data/audit.py` expands every linear stage over the integers, counts each literal binary `+/-`, checks all 4,096 tensor coefficients for this format, and normalizes term permutations and term signs. It also reads the catalog's actual operation lists, verifies that each operation list expands to the stored factors, and accounts for the catalog's row-major output ordering. Multiplication by -1 costs zero. Nonunit scalar operations are not allowed in an applicable ternary SLP.

Run from the run directory:

```sh
python3 panel/novelty-data/audit.py
```

The saved output and detailed records are `novelty-data/audit-output.json` and `novelty-data/audit-results.json`.

| Object or source | Rank | U additions | V additions | W additions | Total | Assessment |
|---|---:|---:|---:|---:|---:|---|
| Candidate `claim/scheme.json` | 51 | 37 | 68 | 77 | 182 | Exact ternary SLP |
| Perminov `2x4x8_m51_cr188_cn354_ZT_reduced.json` | 51 | 38 | 72 | 78 | 188 | Exact public ternary SLP |
| Closed public PR #26 actual object | 51 | 38 | 71 | 78 | 187 | Exact public ternary SLP, current minimum |
| matmulcatalog AlphaEvolve actual `slp` | 51 | 41 | 72 | 80 | 193 | Counted operations, all scalar instructions are unit scalars |
| matmulcatalog Perminov ZT actual `slp` | 51 | 23 | 104 | 94 | 221 | Different decomposition, exact ternary SLP |
| matmulcatalog imported Perminov reduced programme | 51 | 38 | 72 | 78 | 188 | Same reduced programme as upstream |
| Lille cited raw evaluation scheme | 51 | 72 | 165 | 117 | 354 | Exact unshared ternary programme |

KNOWN: Sedoglavic's live `fmm_sota.json` lists format `[2,4,8]` at rank 51. Lille's live per-format page cites AlphaEvolve and links the actual raw evaluation scheme and tensor. The page contains no separately linked complexity variant. I fetched and parsed the raw scheme and tensor rather than treating that absence as an addition-count result. The raw scheme has 354 additions and matches the candidate's underlying rank-one terms up to signs and order.

KNOWN: The current Perminov recursive tree is complete, with `truncated: false` and 6,637 entries. I searched all six dimension permutations. All seven matching format files were fetched, including the unsuffixed Maple tensor that a rank-filename-only filter misses:

```text
schemes/known/alpha_evolve/2x4x8_m51_mod0.json
schemes/known/tensor/2x4x8_tensor.mpl
schemes/results/ZT/2x4x8_m51_ZT.json
schemes/results/ZT/2x4x8_m51_ZT.m
schemes/results/addition_reduced_ZT/2x4x8_m51_cr188_cn354_ZT_reduced.json
schemes/results/serendipitous_base/2x4x8_m51_4f8823917d1632e9d8a0f24c08bc414f7633f115_ZT.json
schemes/results/serendipitous_base/2x4x8_m51_abdcfcb8ce16413df66a1512b9ffef5d662c232b_Z.json
```

PROVED-HERE: The minimum matching reduced-file `cr` is 188, independently counted as 188. The ZT dense variant is 414 additions before sharing, and the ZT serendipitous base is 408. The integer serendipitous base contains nonunit coefficients and supplies no applicable ternary SLP. Its 862 dense summation operations do not include the scalar costs, so that number is not a competing ternary schedule. `reduced_known.json` has no `2x4x8-51` entry. The fetched README and CHANGELOG supply no lower applicable count.

KNOWN: The current matmulcatalog tree is complete, with `truncated: false` and 14,194 entries. All eight matching format/permutation files were fetched. The COVERAGE row's `+354` is the naive total. The actual stored schedules have 193, 221, and 188 additions, as counted above. The additional rank-51 derived files have formats `(2,8,4)` and `(4,8,2)`, with literal totals 362. The remaining constructed file has rank 52. The catalog's unshared integer serendipitous base has the same nonunit-coefficient limitation as upstream.

## Equivalences and compositions

PROVED-HERE: The candidate, Lille raw/Maple objects, AlphaEvolve factors, Perminov's reduced 188 programme, catalog's AlphaEvolve 193 programme, and PR #26's 187 programme normalize to the same rank-one term multiset. The normalized signature is `e1f42e9ea70533ec67e836e6db78f4740a450b3887556df45b60b2f5acbfd444`. This comparison allows product reordering and any sign changes that preserve the tensor term.

PROVED-HERE: I converted the catalog's dimension permutations back to `(2,4,8)`, transposed the appropriate linear maps, and rechecked the full tensor. Componentwise mixing is allowed only within the same normalized term multiset. The public component minima after these conversions are `(38,71,78)`, total 187, for the AlphaEvolve decomposition. The other applicable public term groups have component minima `(23,104,94)`, total 221, and `(79,187,142)`, total 408. Combining the 23-addition U stage of the different Perminov decomposition with AlphaEvolve's V/W stages would not compute the claimed decomposition.

PROVED-HERE: The counter enumerates every one-cut block split on each dimension and every proper dimension-dividing tensor product using the live rank table, with classical rank when a dimension is one. Both families have minimum rank 52 for `(2,4,8)`. No rank-equal 51 composition arises in these families. This is an enumeration of these obvious compositions using the stated public building blocks, not a lower bound on all possible composition methods.

PROVED-HERE: Sharing the left input stage across two column blocks matters. I constructed full explicit programmes from the public `(2,4,4)` rank-26 schedules, shared U once, and checked the complete resulting product. The public 82-addition base yields `18+56+72=146` additions at rank 52. The public 92-addition base yields `21+64+78=163` at rank 52. Both explicit objects are saved as `novelty-data/composition-shared-*.json`. The public `(2,4,7)` rank-45 programme plus a classical final column gives an upper bound of 180 additions at rank 53. These lower addition counts do not satisfy the required rank 51. The alternative-basis rank-7 `(2,2,2)` family likewise gives rank 56 when combined with the remaining classical dimensions, rather than rank 51.

## Current public claims and trophy

KNOWN: I queried the canonical repository `elder-plinius/V3R1T4S`, explicitly with `state=open&per_page=100&page=1`. Each returned `base.repo.full_name` is `elder-plinius/V3R1T4S`. The current response contains 7 open PRs, has no next Link, and an explicit page-2 request is empty. I read the complete returned titles and bodies. No open PR contains an applicable matrix multiplication claim.

KNOWN: I also fetched the complete closed inventory, 100 entries on page 1 and 15 on page 2, with no next Link on page 2 and an empty page 3. There are 39 FMM-related descriptions across the current open/closed inventory. Only PR #26 names this format and rank. It is closed and unmerged. I fetched its changed-file inventory and actual object at immutable commit `aeff32d18580941757bbf8df0978c967902dea8c`, not only its description. The programme SHA256 is `90d66ebee7ee850df3b63def31ba158745a7eb6c74b3a38d651aebf514bdf388`; the independent count and tensor check establish 187 additions. The candidate improves that published circuit by 5 additions.

KNOWN: The freshly fetched TROPHY_CASE has no matching additive-complexity entry. Its matrix multiplication records concern larger rational rank formats and do not supply an applicable 182-or-less schedule. PR snapshots supplied in the claim capsule were not used as the current inventory. Pagination and selection evidence is saved in `novelty-data/pr-inventory-summary.json`.

## Recent primary literature and access gaps

KNOWN: I searched the last 24 months, including exact-format queries, broader additive-complexity and basis-conversion queries, GitHub, Zenodo, and Russian-language search terms. Search terms and the primary-document inventory are in `novelty-data/literature-search.json`. I read the saved primary documents below. No accessible primary document supplied an applicable rank-51 integer ternary circuit with 182 or fewer additions.

- [AlphaEvolve](https://arxiv.org/html/2506.13131) gives the rank-51 result for this format. Its actual decomposition was checked through Lille and the repositories.
- [Parallel heuristic exploration](https://arxiv.org/html/2512.13365) directly tabulates rank 51, naive 354, and reduced counts 197, 191, 190, 188 for `(2,4,8)`. Its best entry is the checked 188 programme.
- [Ternary meta flip graphs](https://arxiv.org/html/2511.20317), [small-format flip-graph framework](https://arxiv.org/html/2603.02398), [meta flip graph with serendipitous product](https://arxiv.org/html/2606.02480), and [catalog with exhaustive derivations](https://arxiv.org/html/2606.13408) provide relevant decomposition/composition context. The applicable repository objects were counted rather than substituting their summaries for SLP evidence.
- [Trilinear aggregation](https://arxiv.org/html/2508.01748) and [alternative basis matrix multiplication is fast and stable](https://link.springer.com/article/10.1007/s00211-026-01531-9) discuss basis conversion and arithmetic costs. A smaller bilinear-phase count alone is not a full standard-input/output schedule. Input and output basis conversions must be included. These accessible papers provide no competing full rank-51 ternary programme for this cell.
- The [60-addition](https://arxiv.org/html/2508.03857), [58-addition](https://arxiv.org/html/2512.21980), and [56-addition](https://arxiv.org/html/2604.27645) papers concern rank-23 `(3,3,3)`. Their tensor reorientation methods are relevant comparison methods, while their programmes have a different format and rank.

KNOWN: The optional IACR PDF `https://eprint.iacr.org/2024/2063.pdf` had already returned a real HTTP 403, as recorded in `claim/LITERATURE_ACCESS.md`. I did not request it, retry it, mirror it, or bypass it. That optional access gap remains. A separate first request for the optional [Alternative bases for new fast matrix multiplication algorithms PDF](https://epubs.siam.org/doi/pdf/10.1137/1.9781611979084.24?download=true) returned a real 403 at `2026-10-14T13:18:23.764660+00:00`. I made no retry, mirror request, or bypass. Its response SHA256 is `52c588c2e38265841bea3da3665a256aa7b70ca1ec48dd4339a2e2c06502a9c4`. These are explicit optional-literature gaps. Every binding table, repository, raw programme, trophy and current PR comparison used for the verdict was accessible.

## Source receipts

KNOWN: Requests used ordinary public GETs and User-Agent `V3R1T4S independent novelty audit`. Sandbox DNS failures made no HTTP contact; I used ordinary approved network execution to make the requests. No actual denial was retried. `novelty-data/source-receipts.json` contains the URL, UTC time, actual status, SHA256, byte count and final URL for all 78 saved responses. Every saved response hash was recomputed successfully. The following receipts anchor the binding comparison; every programme and paper has its own adjacent `.fetch.json` receipt.

| Source file in `novelty-data/` | UTC request time | HTTP | SHA256 |
|---|---|---:|---|
| `fmm_sota.json` | 2026-10-14T13:14:31.512252+00:00 | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 |
| `perminov-tree.json` | 2026-10-14T13:14:31.512843+00:00 | 200 | 0cb3669d76a7e34604a34d2a204c0bf4e27525ba5348675bea6605d7e7032fab |
| `perminov-README.md` | 2026-10-14T13:14:31.513272+00:00 | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 |
| `perminov-CHANGELOG.md` | 2026-10-14T13:14:31.513134+00:00 | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 |
| `perminov-reduced_known.json` | 2026-10-14T13:14:31.701343+00:00 | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d |
| `lille-2x4x8.html` | 2026-10-14T13:14:32.343355+00:00 | 200 | dfb8035a9fb6c0ffa4f52f6edcf5c4626a5864d332ce4fe87349f319d62fa805 |
| `catalog-COVERAGE.md` | 2026-10-14T13:14:31.944969+00:00 | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 |
| `catalog-tree.json` | 2026-10-14T13:14:32.103218+00:00 | 200 | 8ce439a454388156fe1032180eb64f86f73140d43d6d38a7882d87944902a82d |
| `trophy.md` | 2026-10-14T13:14:32.411075+00:00 | 200 | b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412 |
| `pulls-page1.json` | 2026-10-14T13:14:32.777243+00:00 | 200 | c7534e525754c988d2f69dd176478f1b290e7fe1ced387d1a2d6871b07df8e80 |
| `pulls-closed-page1.json` | 2026-10-14T13:18:23.763845+00:00 | 200 | 3944c5cc947795dbe48c066c0f8d14fc71c2f4afff09594323bae75b09604a6a |
| `pulls-closed-page2.json` | 2026-10-14T13:19:16.606726+00:00 | 200 | 9e47f15c05eef435674e9e6167888fc8e4fb540bc661d5f42996abe0d9279f9b |

The full URLs are retained without abbreviation in the manifest. They include the canonical GitHub API repository/state/page query, raw GitHub paths, Lille resources and primary paper URLs. No public action or publication was made.

pass: true
