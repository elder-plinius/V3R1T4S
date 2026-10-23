# CRITERION skeptic

context: fresh isolated subagent; only this run's claim package, pinned AGENTS.md and kit RULES/POLICY/LESSONS/RUN steps 6–7, and independently fetched public primary sources were used; no other local panels, runs, attempts, charter, prior verdicts, or parent reasoning were read.

review_utc: 2026-10-14T16:26:08.588599+00:00

confirmed_scope: scheme.json (sha256 61917376617f1db0a75f5e9f5efd8bbd748713896418760b469126ea042ae5ee) is an exact integer ternary straight-line program for the ordered format (4, 5, 8) at the live listed rank 118, using 486 binary additions/subtractions, strictly below the applicable published counts examined in this audit, including Perminov's 513 and the immutable public PR 15 object's 507.

## Binding criterion, verbatim

Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format <n,m,p> with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

## Literal decision

PROVED-HERE: The immutable submitted object meets the exact-object, ordered-coordinate, coefficient-class, listed-rank, and strict applicable-count conditions within the sources and transformations enumerated below. It is one circuit and one ordered format. This is an explicit constructive certificate comparison; no probabilistic score, statistical significance, global search completion, priority, global optimum, new multiplicative-rank result, or exact replay of the complete discovery history is being confirmed. The optional inaccessible literature remains a limitation to broader literature coverage.

## Independent exact checker

Before inspecting or running supplied verify.py, I wrote `criterion-code/check_integer.py`. It constructs the linear factors over integer coefficient vectors and expands the full tensor, independently fixing A[i,k]=i*5+k, B[k,j]=k*8+j, C[i,j]=j*4+i. A classical positive calibration and sign, forward-reference, and nonunit-literal negative mutations run in the saved checker. Primary ordering is also independently explicit in the live Perminov README and matmulcatalog SchemeIO; no fitted coordinate permutation was used to validate the submitted object.

The saved `integer-result.json` reports 25600 exact tensor coefficients, 160 target monomials, 118 active nonzero products, costs [101, 159, 226] totaling 486, and expanded direct cost 1521. All final U/V/W coefficients are -1, 0, or 1; all literal program coefficients are ±1 and references point backwards. Each fresh row is a charged binary operation. Maximum intermediate magnitudes are [1, 1, 2]: the output-stage 2 is created by paid additions and is not a free nonunit scalar. Aliases and negations are free. The original checker hash remains `1a037a4ecd7d4b95ec2f81544b3a0683b1790e59314a6fd6b7f8ba1782035f94`; supplied verify.py subsequently agreed on the complete coefficient and charged-gate counts. An exact finite certificate comparison does not use a null-model score; no statistical search claim is accepted from the provenance label.

## Live binding-source evidence

Each HTTP result below is an observed honest one-time GET. Full response metadata and bytes are retained under `criterion-code/sources/`; `sources/manifest.tsv` records URL, UTC, HTTP status, SHA256 and byte count for every successful or failed HTTP read. The initial sandbox DNS failure made no HTTP request; the ordinary permitted network escalation then succeeded. There was no HTTP-block retry, challenge bypass, mirror fetch, login, or outward action.

| Primary source / saved response | Independently observed finding | UTC request time | HTTP | Response SHA256 |
|---|---|---|---|---|
| [fmm_sota.json](https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json) | ordered [4,5,8] rank 118 | 2026-10-14T16:07:11.163259+00:00 | 200 | `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1` |
| [perminov-tree.json](https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/f0efd4f67f6ff09bf0418af75c2a209c8cf814b3?recursive=1) | complete tree; only matching reduced file cr513 | 2026-10-14T16:07:53.422532+00:00 | 200 | `0cb3669d76a7e34604a34d2a204c0bf4e27525ba5348675bea6605d7e7032fab` |
| [perminov-4x5x8_m118_cr513_fv249_cn1521_ZT_reduced.json](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/f0efd4f67f6ff09bf0418af75c2a209c8cf814b3/schemes/results/addition_reduced_ZT/4x5x8_m118_cr513_fv249_cn1521_ZT_reduced.json) | actual exact ternary SLP: 111 + 166 + 236 = 513 | 2026-10-14T16:09:15.390321+00:00 | 200 | `7a273fbb34339b6123e5e9253fb088af12c8f11362e46cfe0789b2c3bd9e3860` |
| [perminov-reduced_known.json](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/f0efd4f67f6ff09bf0418af75c2a209c8cf814b3/schemes/reduced_known.json) | 4x5x8-118 absent | 2026-10-14T16:07:54.002282+00:00 | 200 | `ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d` |
| [perminov-README.md](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/f0efd4f67f6ff09bf0418af75c2a209c8cf814b3/README.md) | rank118; defines ordinary U/V and transposed C factor ordering | 2026-10-14T16:07:54.344376+00:00 | 200 | `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341` |
| [perminov-CHANGELOG.md](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/f0efd4f67f6ff09bf0418af75c2a209c8cf814b3/CHANGELOG.md) | no lower applicable 4x5x8 rank118 addition count | 2026-10-14T16:07:54.392334+00:00 | 200 | `07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175` |
| [lille-4x5x8.html](https://fmm.univ-lille.fr/4x5x8.html) | headline rank118; no distinct matching complexity variant | 2026-10-14T16:07:10.461245+00:00 | 200 | `11e5204283178c8e5cc37ed61832e7d3d5da95e0faab8cf4c67fdae1b5399c80` |
| [lille-tensor.bz2](https://fmm.univ-lille.fr/4x5x8_tensor.mpl.bz2) | actual exact ternary rank118; direct cost1521 | 2026-10-14T16:23:25.682618+00:00 | 200 | `9ad56f55680b83d16369e3b64d65522d29943d3483f3b91c5e27180743215610` |
| [lille-raw.bz2](https://fmm.univ-lille.fr/4x5x8_raw.mpl.bz2) | actual exact ternary rank122 and cost419; different rank | 2026-10-14T16:07:54.998174+00:00 | 200 | `33eed9c31feb72878e61cd8a332dc0d631fbfba43406758611b312399c61beb5` |
| [catalog-COVERAGE.md](https://raw.githubusercontent.com/solven-eu/matmulcatalog/4d33faff2ef7d103533e899593639927b9fbaa0a/generated/COVERAGE.md) | matching table cell rank118, adds +1521 | 2026-10-14T16:07:54.411046+00:00 | 200 | `c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7` |
| [catalog-4x5x8-r118-perminov_c1463_ZT-78651f4.json](https://raw.githubusercontent.com/solven-eu/matmulcatalog/4d33faff2ef7d103533e899593639927b9fbaa0a/src/main/resources/schemes/known/section8/4x5x8-r118-perminov_c1463_ZT-78651f4.json) | actual exact integer SLP: 110 + 163 + 235 = 508 | 2026-10-14T16:09:15.694818+00:00 | 200 | `3f1ebe2b84a456d40e90b67e359a50b4ff195d149d984f52b446697b4c3c3460` |
| [pr15-object.json](https://raw.githubusercontent.com/calgulbenkian/V3R1T4S/9f58a7cc51089f081d56a828f26cfe16af455b49/known-knowns/faster-matrix-multiplication/2026-10-14-anonymous-c6d1e0ab-8457e021/object/4x5x8_m118_cr507_fv250_cn1521_ZT_reduced.json) | actual exact integer SLP: 109 + 162 + 236 = 507 | 2026-10-14T16:10:41.605975+00:00 | 200 | `8457e021243c258cc047506d85372ef177054c9f8473261a27b211f1f3a419ec` |

The live Perminov branch resolves to `f0efd4f67f6ff09bf0418af75c2a209c8cf814b3`. Its complete recursive tree has 6637 entries and `truncated: false`; every ordered/permuted-format matching path was enumerated before selecting the minimum cr. There is one rank118 ternary reduced matching file, cr513. Other matching JSONs and Mathematica `.m` factor encodings were read and exactly checked, including duplicate paths identified by immutable blob hashes. The `.m` factors match their JSON factor matrices exactly. `reduced_known.json` has no matching entry and README/CHANGELOG supply no lower applicable count.

Matmulcatalog's current branch is `4d33faff2ef7d103533e899593639927b9fbaa0a`; its complete tree has 14194 entries and `truncated: false`. Actual matching materialized SLPs cost 539 and 508. Every `*` operation in these SLPs is multiplication by -1, so its free treatment is independently legitimate. Its reduced import costs 513; the bud-base rank118 factor object gives direct cost1542, and the equivalent Kauers 8x4x5 rank118 factor object gives an actual returned ordered cost1443. All these tensor objects were checked exactly. The catalogue's +1521 table cell alone is therefore not the complete comparison bar.

Lille's actual tensor download is ternary, exact, rank118, with direct cost1521, agreeing with the corresponding Perminov tensor. Its linked raw Maple evaluation program was separately parsed as data and checked exactly: it has rank122 and 419 additions, despite the per-format page headline118. That lower cost is excluded only because the binding comparison fixes rank118; it is explicitly retained as contrary evidence against any broader minimum-additions claim.

## Transposes and compatible stage mixing

`audit_sources.py` implements actual reverse accumulation of linear circuits; each first incoming adjoint is a free alias and additional accumulation is charged. Its independent calibration transposes y=x0+x1 from one charged operation into two free aliases with cost0. For each matching public circuit all six format permutations were tensor-checked, then transposed/reindexed back to the ordered (4,5,8) target before comparison. No cost from a different orientation was used as the target cost. The source audit records every stage and returned cost.

`mix_stages.py` also compares individual factor systems up to product permutation and product signs, aligns the actual donor stage to the carrier factors, and verifies the synthesized mixed tensor. This allows compatible stage replacement even when complete donor and carrier tensors differ. The minimum across those public mixtures is 507; the candidate is strictly smaller by 21. Merely combining unrelated stage minima is never used.

## Shared compositions and bounded restrictions

`compositions.py` shares actual input linear gates across repeated blocks and reconstructs the output accumulations. All example tensors were independently checked. Its column split and tensor implementation have rank122 and cost411, inner 4+1 split rank128 and cost409, and shared 2-by-(2+2+1)-by-4 Strassen grid rank144 and cost224. These are genuine lower-addition computations, but they do not have the required rank118. The enumerated family has 769 nontrivial integer grid partitions and 22 nontrivial exact tensor factorizations, using the current public catalogue leaf ranks with classical rank when a dimension is1. Their minimum rank is 122. This is a source-relative exclusion of this named ordinary-composition family only; it is not a global lower bound on matrix-multiplication rank or all public derivations.

`restrictions.py` evaluates 215 coordinate-subset restrictions from eight explicitly downloaded nearby larger public reduced circuits: 4x5x9, 4x5x10, 4x6x8, 4x7x8, 5x5x8, 4x6x9, 5x6x8, 5x5x9. It removes zero coordinates/products, shares identical binary gates, trims dead computation, and checks each resulting full ordered tensor. Retained ranks range from 124 to 163; none has rank118. `restrictions-result.json` gives every coordinate set, rank and cost. This bounded result does not assert that all restrictions, basis changes, flips, or larger public circuits have been exhausted.

## Public claims and literature

The live all-state V3R1T4S PR list was followed through both pages and the last page has no next link: 140 PRs, 25 open, 115 closed, 0 merged. All titles and bodies were screened for the target and equivalent formats, not just the open page. Closed PR15 is a matching 507-addition claim. Its complete immutable head tree and actual object bytes were read from commit `9f58a7cc51089f081d56a828f26cfe16af455b49` and checked, rather than accepting its prose count. The live TROPHY_CASE has no corresponding ordered rank118 additive object; its listed matrix-multiplication trophies are larger rational rank results.

The recent-literature audit used primary arXiv texts/metadata and cited author artifact repositories, with English, Russian, French and Chinese query variants. [Perminov's additive-complexity paper](https://arxiv.org/html/2512.13365) explicitly tabulates the matching rank118 tensor at513; [ternary meta-flip work](https://arxiv.org/html/2511.20317) and [the later expanded format catalogue](https://arxiv.org/html/2606.02480) lead to the current primary repository checked above. The published [56-addition](https://arxiv.org/html/2604.27645) and [55-addition](https://arxiv.org/html/2607.28676) results concern 3x3x3 rank23. [The September alternative-basis paper](https://arxiv.org/abs/2609.32388) states51 kernel additions plus5 conversions, totaling56 in ordinary coordinates. [The October APA paper](https://arxiv.org/html/2610.13905) concerns approximate/border-rank methods and alternative bases; no matching exact integer ordered rank118 certificate below486 was found in the examined material. The Greedy-Potential author repository's initial recursive tree was marked truncated, so it was not treated as an absence proof; its root and relevant algorithm roots were read separately. Primary/non-English searches yielded no additional applicable lower ordered-count object in the examined results. This is a bounded literature search, not a universal completeness or priority claim.

The three optional denied PDF URLs documented in claim/LITERATURE_ACCESS.md were not requested again or obtained through another copy. Those full-text gaps remain open. The only new unsuccessful HTTP source read was a404 for an unavailable arXiv HTML rendering; the ordinary public abstract page for that distinct paper returned200. No required binding table/status source is blocked.

## Rerun

From the run folder, use Python3 with the standard library:

```
python3 panel/criterion-code/check_integer.py claim/scheme.json
python3 panel/criterion-code/audit_sources.py
python3 panel/criterion-code/mix_stages.py
python3 panel/criterion-code/parse_lille.py
python3 panel/criterion-code/parse_factor_files.py
python3 panel/criterion-code/compositions.py
python3 panel/criterion-code/restrictions.py
```

These commands check the saved immutable source bytes; they do not refetch blocked or unblocked sources. The parent's honesty gate remains responsible for kit/check_run.py and any final run status. No claim/object/criterion was edited, and nothing was published.

pass: true
