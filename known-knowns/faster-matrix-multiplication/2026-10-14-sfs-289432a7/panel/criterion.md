# CRITERION

context: subagent (fork_turns none; isolated capsule)

PROVED-HERE: The candidate meets the full literal success criterion for `fmm-additive-complexity-records`. It is a deterministic explicit-object claim, not a statistical search-performance or optimality claim.

confirmed_scope: scheme.json gives a standard-coordinate exact integer ternary SLP for (2,4,8) at the live-listed rank 51 using 182 additions/subtractions, below the applicable counts in the freshly checked criterion sources and public rank-equal programs.

## Literal criterion and quantifiers

The binding bank criterion was read directly from `repo/bank/targets.json` and matched the verbatim criterion in `CLAIM.md`. The dimensions have maximum 8; the live `fmm_sota.json` entry is `{"format":[2,4,8],"rank":51,"exponent":2.836213}`. The candidate has 51 nonzero, output-active, distinct rank-one terms. This verifies the required number of products and equality to the listed best rank; it does not assert a tensor-rank lower bound.

The count must be below the minimum over every matching live reduced file, not a selected example, and also below applicable Lille and matmulcatalog counts and public rank-equal programs. An applicable count of 182 or less would defeat the claim. The checks below found no such count. The confirmed scope is source-relative and applies to this single exact schedule.

The success criterion requires an exact object and symbolic verification. It does not require an exhaustive discovery-history replay, a globally minimum addition circuit, or a globally optimal rank proof. `research_method` identifies a finite-dictionary MILP construction. `REPRODUCE.md` discloses that the entire original dictionaries and runtime code hashes were not saved. That limit does not change the reproducibility of the immutable schedule or establish an exclusion over other circuits. No chance or statistical-performance assertion is passed; random null controls are not needed for the full exact certificate.

## Exact object and gate convention

Before reading `verify.py`, I wrote an independent integer-vector expansion checker. Its candidate output is saved in `../panel/criterion-code/exact-output.jsonl` and the explicit binary expansion in `../panel/criterion-code/literal-binary-program.txt`.

`scheme.json` SHA-256: `289432a72c0f86a04925e6475d31d4ff86d92a65fb8d57f4b57f918c3866d654`.

The indexing is `A[i,j] = a[i*4+j]`, `B[j,l] = b[j*8+l]`, and `C[i,l] = c[l*2+i]`. Every one of the 4096 bilinear coefficients equals the standard matrix-product tensor over the integers. There are zero tensor mismatches. The left, right and output schedules cost 37, 68 and 77 binary additions/subtractions, respectively, totaling 182. The independently expanded naive count is 354. The supplied verifier was read only after the independent check and separately returned the same values.

Every sparse scheduled coefficient is literally +1 or -1. Every reference points to an already available quantity. Each k-term assignment expands into k-1 binary gates, with unary signs free. All 51 products are present, nonzero and used by the output map. The three maps occupy distinct input spaces; no A-form is reused as a B-form or as an output form. All input preparation and all output reconstruction are charged. There is no hidden basis conversion, multiplication by 2, division, or scalar multiplication other than free signs.

All expanded U, V and rank-one W factor coefficients are in {-1,0,1}. Some expanded W intermediate sums contain -2 or 2. These are legitimate results of already charged binary gates, not uncharged scalar-2 operations. Banning them would strengthen the bank definition. A separate literal scalar-2 mutation is rejected. A forward-reference mutation and a tensor-sign corruption are also rejected with completed semantic checks; the valid intermediate-2 candidate is accepted. The captured control output is `../panel/criterion-code/gate-audit-output.jsonl`.

## Fresh mandatory comparisons

All fetched source bytes, exact URLs, UTC timestamps, HTTP statuses and SHA-256 hashes are retained in `../panel/criterion-code/sources/`; their manifest is `../panel/criterion-code/source-summary.txt`. The required comparisons were fetched independently in this context. The successful fetch interval was 2026-10-14T13:30:13.849397+00:00 through 2026-10-14T13:41:43.610603+00:00; all 56 successful source requests returned HTTP 200. Initial sandbox DNS failures were retried only with normal approved network access, before any remote response. No actual access denial was retried.

| Comparison | Fresh observation and independent recount |
|---|---|
| [Sedoglavic rank table](https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json) | Rank 51; fetched 2026-10-14T13:30:13.849397+00:00; SHA-256 `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1`. |
| [Perminov complete tree](https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1) | The response is untruncated. All matching paths were inspected. Exactly one matching rank-51 file is in `addition_reduced_ZT`: `2x4x8_m51_cr188_cn354_ZT_reduced.json`. |
| [Actual reduced program](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x4x8_m51_cr188_cn354_ZT_reduced.json) | Independent full tensor check and literal recount: 38+72+78 = 188; naive 354. Its live bytes equal the copied reference bytes; SHA-256 `b68445935df00311217280a30d628395594619584691d8264723045b2b62131a`. |
| [reduced_known.json](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json), [README](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md), [CHANGELOG](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md) | No lower matching addition count. `reduced_known.json` has no `2x4x8-51` entry; README lists rank 51. The reduced-format definition agrees with the independent counter. |
| [Lille format page](https://fmm.univ-lille.fr/2x4x8.html) | Rank 51, AlphaEvolve citation, no separate cited best-complexity variant on this page; fetched 2026-10-14T13:30:15.378876+00:00; SHA-256 `dfb8035a9fb6c0ffa4f52f6edcf5c4626a5864d332ce4fe87349f319d62fa805`. The linked raw evaluation was actually fetched, parsed independently, checked against all tensor coefficients and recounted to 72+165+117 = 354. |
| [matmulcatalog COVERAGE](https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md) | The matching row lists rank 51 and +354 additions. The untruncated live tree has six matching objects. Every object was fetched; the rank-51 reduced program recounts to 188, AlphaEvolve's embedded SLP to 193 (41+72+80), and Perminov-ZT's embedded SLP to 221 (23+104+94), with only free scalar -1. Their factors and schedules were verified exactly. |
| Other matching catalog objects | The ternary serendipitous base has naive count 408 and no published SLP count. The integer base has expanded coefficients from -4 through 5 and no published lower SLP count; it is not a ternary factor class. The constructed HK71 program has 52 products and naive count 272, so fails this target's fixed-rank requirement. |

The candidate is strictly below the minimum live reduced count 188, and below each applicable actual catalog program, Lille evaluation and COVERAGE value. The result is a full criterion win for one format, not enumerated partial wins p1, p2 or p3.

## Public claims and recent primary literature

The [live trophy case](https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md) was fetched and inspected. Its matrix-multiplication entries concern different, larger formats and contain no matching additive-count result.

The complete [open PR inventory](https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=1) contains 7 entries. The complete recent closed inventory contains 115 entries across two 100-entry pages; its second page contains 15, establishing pagination completion. Zero closed entries have a non-null `merged_at`. Titles and bodies were screened for matching format and FMM/addition claims. The relevant [closed PR 26](https://github.com/elder-plinius/V3R1T4S/pull/26) reports 187 additions. Its public object at frozen head `aeff32d18580941757bbf8df0978c967902dea8c` was fetched, not merely taken from the title, and independently verified to use 38+71+78 = 187 additions with all 4096 tensor coefficients exact. Object SHA-256: `90d66ebee7ee850df3b63def31ba158745a7eb6c74b3a38d651aebf514bdf388`. Its comments endpoint returns an empty list. The candidate is strictly below this public rank-equal object too. No prior local run or other panel verdict was consulted.

Fresh literature searches used exact-shape/addition queries and broader current matrix-multiplication/additive-complexity and alternative-basis queries. The following primary sources were actually opened:

- [Perminov, parallel additive-complexity exploration](https://arxiv.org/html/2512.13365): the full HTML table gives (2,4,8), rank 51, naive 354 and best reduced 188. It also explains separate input/output basis-conversion costs and CSE conventions.
- [Perminov, March 2026 framework](https://arxiv.org/abs/2603.02398) and [June 2026 serendipitous product results](https://arxiv.org/abs/2606.02480): the current public schemes used for these papers are included in the freshly checked repository inventory; neither abstract publishes a lower matching additive count.
- [matmulcatalog primary paper](https://arxiv.org/abs/2606.13408): it describes axis permutations, concatenation, projection and shared/serendipitous compositions. The actual matching generated objects and schedules were checked as above.
- [AlphaEvolve primary paper](https://arxiv.org/abs/2506.13131): this is Lille's cited source; the relevant evaluation was checked directly through Lille and the catalog's complete program.
- [Sun's rank-23 3x3 result](https://arxiv.org/abs/2601.05272), [Karunaratne et al., 55 additions](https://arxiv.org/abs/2607.28676), and [Stapleton-Perminov alternative-basis kernel](https://arxiv.org/abs/2609.32388): these concern 3x3 rank 23, not (2,4,8) rank 51. The last source explicitly charges five conversion additions on top of its 51-addition kernel, giving 56 in ordinary coordinates. Its kernel count cannot be compared directly to a full standard-coordinate product.

The optional IACR and SIAM PDF denials recorded in `LITERATURE_ACCESS.md` remain access gaps. I did not request either denied PDF, retry its access class, use a mirror, or obtain an alternate copy. No comparison or proof here depends on unread blocked content; every mandatory binding table and its applicable program was available honestly.

## Shared compositions and map conversion

An independent dynamic recurrence checked ordinary recursive axis splits and Kronecker factorizations using the fresh rank table. Its minimum proper composed rank is 52, with zero rank-51 ordinary compositions. Sharing A-side additions between two calls changes addition cost but does not by itself remove a bilinear product.

That ordinary test alone is insufficient because shared-factor/grid-bud fusion can remove products. I therefore fetched 22 non-F2, noncommutative public divisor-base objects for rank-7 2x2x2, rank-14 2x2x4 and rank-26 2x4x4. For 90 applicable axis orientations, an independent exact block-partition dynamic program considered every single-factor subset and complete two-axis class grid present in the supplied tensors and priced the enlarged blocks against the fresh rank oracle. The minimum shared composed rank is 52; zero checked compositions have rank 51 or less. The result and explicit tested partitions are saved in `../panel/criterion-code/shared-rank-results.json`. This is a check of these explicit public bases and constructors, not an exclusion over all tensor orbits or all possible compositions.

The candidate's literal maps contain all conversions to ordinary coordinates. The W intermediates are solely linear combinations of already computed products. No factor-map mixing or free nonunit scalar is hidden in the count. The exact check and the strict comparisons satisfy the actual bank definition without adding a cancellation-free requirement.

## Reproduction

From the run folder:

```sh
python3 panel/criterion-code/check_exact.py claim/scheme.json panel/criterion-code/sources/reference-188.json panel/criterion-code/sources/pr26-object.json
python3 panel/criterion-code/audit_gates.py
python3 panel/criterion-code/check_lille.py
python3 panel/criterion-code/check_catalog.py panel/criterion-code/sources/catalog-reference.json panel/criterion-code/sources/catalog-alphaevolve.json panel/criterion-code/sources/catalog-zt.json panel/criterion-code/sources/catalog-serbase-zt.json panel/criterion-code/sources/catalog-serbase-z.json panel/criterion-code/sources/catalog-hk71.json
python3 panel/criterion-code/check_compositions.py
python3 panel/criterion-code/check_shared_ranks.py
```

pass: true
