context: subagent (fork_turns none; isolated claim capsule)
target: fmm-additive-complexity-records
criterion_result: full success criterion, relative to the required live records
claim_level: PROVED-HERE for exact computation and cost; KNOWN for the fetched record comparisons

confirmed_scope: scheme.json exactly computes the full ⟨2,5,6⟩ product over Z with 47 bilinear products and 179 additions/subtractions under Perminov's reduced convention, two fewer than the live applicable 181-addition Perminov record and below the applicable Lille and matmulcatalog counts checked on 2026-10-14.

The claim passes the literal full criterion for this single object and table cell. It does not establish a minimum addition count among all possible programs, a minimum tensor rank, or an exhaustive literature exclusion. The named partial wins do not describe this format or this single-object claim.

## Independence and programs

I read all files in `claim/`, the binding bank entry, `repo/AGENTS.md`, `kit/RULES.md`, `kit/POLICY.md`, `kit/LESSONS.md`, and RUN steps 6–7. I did not read other local run content, sibling panel files, search attempts, or previous reasoning. Public source retrievals were ordinary unauthenticated GETs with a User-Agent identifying V3R1T4S. Their complete bodies and access receipts are in `criterion-code/`. No fetched code was executed.

`criterion-code/check.py` is my independent coefficient-expansion and operation-count checker. It expands each fresh expression into integer coefficients, expands each of the 47 ordered input products into formal A-entry/B-entry monomials, and checks all coefficients of all 12 outputs. It rejects forward references, repeated indices, nonunit instruction scalars, the binary-field flag, missing rows, and a deliberate output-sign corruption. It also emits `criterion-code/candidate-binary-slp.txt`, making the binary implementation of each multi-term form explicit.

`criterion-code/check_tables.py` parses the actual Lille Maple evaluation text as data and checks the catalogue's dense tensors and its actual published SLP instructions. The catalogue's dense W columns use transposed-output order; its SLP output list uses row order. The checker converts those indices explicitly and then verifies the same full integer identities. `criterion-code/check-result.json` and `criterion-code/tables-result.json` contain the measured results.

Reproduce from this run's `panel/` directory:

```sh
python3 criterion-code/check.py
python3 criterion-code/check_tables.py
```

## Literal criterion checks

PROVED-HERE:

- The object is an explicit, finite SLP. The input dimensions are 2×5 and 5×6, and the output is 2×6. The maximum dimension is 6, within the criterion's limit of 8.
- There are exactly 47 nonzero bilinear products. The candidate and the freshly downloaded reference have identical expanded U, V, and W factors, so this is an addition improvement for an existing rank, not a rank improvement.
- Every instruction scalar and every nonzero expanded factor coefficient is +1 or -1. The arithmetic is over Z, not merely modulo 2. The complete expansion verifies 3,600 bilinear coefficient identities. This is a symbolic polynomial identity check, not a sample of integer matrices.
- The total candidate count is 38+65+76 = 179. The freshly fetched reference is 40+65+76 = 181. Every k-term nonempty form costs k−1 binary additions/subtractions; a copy or unary sign costs zero. All fresh assignments and all final forms are included. There are no uncharged input/output basis conversions, nonunit scalar multiplications, or cross-sharing of A and B variables.
- The candidate is strictly better by two additions under the same counter. The candidate's expanded flat tensor still has 332 additions, which illustrates why the reduced convention matters.

KNOWN from the fresh primary sources:

- Sedoglavic's binding `fmm_sota.json` lists format [2,5,6] at rank 47. Equality with the listed rank is established; no assertion that 47 is mathematically optimal is needed.
- Perminov's recursive tree is explicitly untruncated and contains one matching file in `addition_reduced_ZT`, `2x5x6_m47_cr181_fv63_cn332_ZT_reduced.json`. Therefore the minimum matching cr is 181. The downloaded object independently verifies and recounts to 181. The README confirms the fresh-variable format and the meaning of reduced complexity. The CHANGELOG has no 2x5x6 lower-count entry. `reduced_known.json` contains only `2x5x6-48: Z2 227`, which has the wrong rank and domain for this comparison.
- Lille's 2x5x6 page cites AlphaEvolve and links its tensor, LRP, raw evaluation, and symmetry objects. It does not cite a separate best-complexity variant for this cell. Its actual raw evaluation program independently verifies over Z and uses 332 additions, split 75+145+112. Its LRP coefficients are ternary. Thus the coefficient-class exception for a rank attained only with nonternary coefficients is not invoked.
- matmulcatalog's live COVERAGE row lists rank 47 in the applicable integer class and `+332`. The actual AlphaEvolve catalogue SLP independently verifies and recounts to 187 = 42+66+79. Its 39 explicit scalar operations are all multiplication by -1 and are free under the binding convention. The catalogue's imported Perminov reduced object independently recounts to 181. Both actual schedules exceed 179.
- The complete generated catalogue contains six canonical [2,5,6] entries. The other rank-47 flat counts are 783 and 1384 for nonternary integer/rational bud bases, and 334 for an entry derived in the 2x6x5 orientation. Neither the objects nor the generated metadata publish a lower applicable schedule. The rational and nonternary objects were checked with exact fractions and are not silently equated with a ternary unit-scalar SLP.

The rank and addition comparisons use the same format, rank, standard coordinates, exact coefficient domain, and operation convention. 179 is below the smallest applicable reduced count of 181 and below the additional applicable published counts required by the bank.

## Source scope, literature, and duplication

The current V3R1T4S open-PR listing required two pages, with 100 and 22 entries. I followed the first page's actual next link. The terminal page has previous/first links and no next link; all 122 PR numbers are distinct. Neither page's title/body metadata contains this cell. The saved 77-entry capsule snapshot was not treated as complete-current evidence. The live public trophy case has no same-cell addition result.

Perminov's accessible primary paper `arxiv.org/html/2512.13365` directly tabulates this cell at rank 47, with naive count 332 and reduced comparison values 189, 186, 184, and 181. The last value agrees with the downloaded program. AlphaEvolve's primary paper records the improvement from rank 48 to 47. The other opened recent primary papers concern ternary searches, serendipitous constructions, and 3×3 addition improvements. None supplies a lower 2x5x6 rank-47 reduced count in the inspected text. Credits belong to Alexander Novikov and the AlphaEvolve authors for the rank-47 scheme, Andrew Perminov for the public 181-addition program and reduction conventions, Alexandre Sedoglavic for the Lille catalogue, and solven-eu/matmulcatalog for the independent catalogue and published SLP.

`criterion-code/literature-result.json` records the focused search queries and inspected primary-paper excerpts. This source check is bounded and does not prove the absence of every unpublished or inaccessible result.

The optional `https://eprint.iacr.org/2024/2063.pdf` access gap is inherited from `claim/LITERATURE_ACCESS.md`: an actual HTTP403 was recorded there at 2026-10-14T12:01:02Z. I did not request it again, use a mirror or proxy, or bypass the block. I do not claim to know its contents. This is an unresolved optional literature gap, not a blocked binding record table. The full-source-relative bank comparison above is supported independently by accessible binding sources and actual programs. The optional HTML representation for `https://arxiv.org/html/2609.32388` returned HTTP404; its normal primary abstract page returned HTTP200 and identifies a 3×3 alternative-basis kernel rather than this cell. The report does not count its kernel-only additions as a complete ordinary-coordinate multiplication.

## Null-model and scope limits

The claim is an explicit deterministic SLP certificate and an exact operation count. It contains no statistical score, random-success assertion, or exhaustive-search exclusion, so no null model is used to justify this mathematical conclusion. The deliberate corruption is a checker-sensitivity control and is not represented as a 400-control search experiment. Any run-level preregistration or search-control obligations remain with the main session's honesty gate; I did not inspect material outside the capsule to assert they passed.

This panel file judges the literal claim and its required live comparisons. The main session still owns the overall run checker and final status. All source receipts below are from this review, except the expressly inherited optional ePrint gap.

## Access receipts

Each saved `criterion-code/*.fetch.json` gives URL, UTC, observed HTTP status, exact bytes, SHA256, and response headers. No blocked source was retried. Optional HTML HTTP404 is listed explicitly; no binding table was blocked. The records below enumerate all fresh GETs.

| Saved source | Primary URL | Access UTC | HTTP status |
|---|---|---|---|
| `source-status.html` | [source-status.html](https://github.com/dronperminov/FastMatrixMultiplication) | 2026-10-14T12:41:33.206370+00:00 | 200 |
| `rank.json` | [rank.json](https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json) | 2026-10-14T12:41:33.206873+00:00 | 200 |
| `tree.json` | [tree.json](https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1) | 2026-10-14T12:41:33.207067+00:00 | 200 |
| `README.md` | [README.md](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md) | 2026-10-14T12:41:33.207261+00:00 | 200 |
| `CHANGELOG.md` | [CHANGELOG.md](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md) | 2026-10-14T12:41:33.207406+00:00 | 200 |
| `known.json` | [known.json](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json) | 2026-10-14T12:41:33.207659+00:00 | 200 |
| `COVERAGE.md` | [COVERAGE.md](https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md) | 2026-10-14T12:41:33.207831+00:00 | 200 |
| `lille.html` | [lille.html](https://fmm.univ-lille.fr/2x5x6.html) | 2026-10-14T12:41:33.208046+00:00 | 200 |
| `pulls1.json` | [pulls1.json](https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=1) | 2026-10-14T12:41:33.612179+00:00 | 200 |
| `TROPHY_CASE.md` | [TROPHY_CASE.md](https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md) | 2026-10-14T12:41:33.670231+00:00 | 200 |
| `matmul-readme.md` | [matmul-readme.md](https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/README.md) | 2026-10-14T12:41:33.684585+00:00 | 200 |
| `pulls2.json` | [pulls2.json](https://api.github.com/repositories/1011751194/pulls?state=open&per_page=100&page=2) | 2026-10-14T12:43:23.587563+00:00 | 200 |
| `lille-raw.mpl.bz2` | [lille-raw.mpl.bz2](https://fmm.univ-lille.fr/2x5x6_raw.mpl.bz2) | 2026-10-14T12:43:23.588217+00:00 | 200 |
| `lille-lrp.mpl.bz2` | [lille-lrp.mpl.bz2](https://fmm.univ-lille.fr/2x5x6_LRP.mpl.bz2) | 2026-10-14T12:43:23.588441+00:00 | 200 |
| `perminov-reducer-paper.html` | [perminov-reducer-paper.html](https://arxiv.org/html/2512.13365) | 2026-10-14T12:43:23.588694+00:00 | 200 |
| `perminov58.html` | [perminov58.html](https://arxiv.org/html/2512.21980) | 2026-10-14T12:43:23.588966+00:00 | 200 |
| `reference181.json` | [reference181.json](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x5x6_m47_cr181_fv63_cn332_ZT_reduced.json) | 2026-10-14T12:43:23.589216+00:00 | 200 |
| `alphaevolve.html` | [alphaevolve.html](https://arxiv.org/html/2506.13131) | 2026-10-14T12:43:23.589497+00:00 | 200 |
| `sun.html` | [sun.html](https://arxiv.org/html/2601.05272) | 2026-10-14T12:43:23.589666+00:00 | 200 |
| `matmul-tree.json` | [matmul-tree.json](https://api.github.com/repos/solven-eu/matmulcatalog/git/trees/master?recursive=1) | 2026-10-14T12:44:35.600591+00:00 | 200 |
| `new55.html` | [new55.html](https://arxiv.org/html/2607.28676) | 2026-10-14T12:44:35.601141+00:00 | 200 |
| `new51.html` | [new51.html](https://arxiv.org/html/2609.32388) | 2026-10-14T12:44:35.601293+00:00 | 404 |
| `catalog-alpha.json` | [catalog-alpha.json](https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/src/main/resources/schemes/known/section6/2x5x6-r47-alphaevolve-7387644.json) | 2026-10-14T12:45:40.731796+00:00 | 200 |
| `catalog-reduced.json` | [catalog-reduced.json](https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/src/main/resources/schemes/known/section6/2x5x6-r47-perminov_cr181_fv63_cn332_ZT_reduced-413a41d.json) | 2026-10-14T12:45:40.732340+00:00 | 200 |
| `catalog-baseZ.json` | [catalog-baseZ.json](https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/src/main/resources/schemes/bud-bases/section6/2x5x6-r47-perminov_serbase_Z-5962adf.json) | 2026-10-14T12:45:40.732514+00:00 | 200 |
| `catalog-baseQ.json` | [catalog-baseQ.json](https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/src/main/resources/schemes/bud-bases/section6/2x5x6-r47-perminov_serbase_Q-087c8a7.json) | 2026-10-14T12:45:40.732705+00:00 | 200 |
| `catalog.json` | [catalog.json](https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json) | 2026-10-14T12:45:40.732904+00:00 | 200 |
| `new51-abs.html` | [new51-abs.html](https://arxiv.org/abs/2609.32388) | 2026-10-14T12:45:40.733055+00:00 | 200 |
| `serendipitous-paper.html` | [serendipitous-paper.html](https://arxiv.org/html/2606.02480) | 2026-10-14T12:47:55.735301+00:00 | 200 |
| `ternary-meta-paper.html` | [ternary-meta-paper.html](https://arxiv.org/html/2511.20317) | 2026-10-14T12:47:55.735784+00:00 | 200 |

pass: true
