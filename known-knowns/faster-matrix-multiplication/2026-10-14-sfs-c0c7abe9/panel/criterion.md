# CRITERION skeptic

context: fresh isolated subagent
role: CRITERION
written_utc: 2026-10-14T15:19:13.484901+00:00

confirmed_scope: The immutable ternary straight-line program in claim/scheme.json (SHA256 c0c7abe9136e5f773d01c5c276cb1f6c3f565afab183499fdda63ac67947e02e) computes ordinary ordered (5,5,5) matrix multiplication exactly over Z with the live listed rank of 93 active products and 354 binary additions/subtractions, strictly below the applicable live 383-addition Perminov reference, the 846-addition matmulcatalog coverage value, and the independently verified 378-addition matching public PR circuit.

## Literal criterion

Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format <n,m,p> with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

## Independent exact verification

PROVED-HERE. I first established the coordinates from the live primary `src/schemes/scheme.py`, its `naive` constructor (lines 35–49): A[i,k] is i*m+k, B[k,j] is k*p+j, and C[i,j] is j*n+i. This was done before writing `criterion-code/exact.py` and before inspecting `claim/verify.py`. No coordinate permutation was fitted to the candidate.

The independent checker expands every appended fresh variable over integer base vectors and constructs the complete bilinear tensor. It verifies all 15625 coefficients, from 625 input basis pairs with every output. Its known-positive control is ordinary naive 2x2x2 multiplication; a one-factor sign mutation is rejected. There are exactly 93 active nonzero products. This verifies the full product over Z, rather than a sample or a test modulo 2.

The literal gate count is 93 + 96 + 165 = 354. All fresh definitions have two terms and every final definition is a one-term signed alias. Every reference is backward and every literal coefficient is ±1. All expanded final U, V and W factors have coefficients in {-1,0,1}. Input intermediate magnitudes are at most 1; four paid output additions produce intermediate magnitude 2. These intermediates are permitted computed sums, not hidden scalar multiplications. The final factors remain ternary. The expanded naive factor count is 843, agreeing with the metadata. The independent expanded-factor SHA256 is `391cdd4d2a39c5317f82d7b38151a1bd79bc8d4800fef07a7dc26e5e604e7531`.

Only after this check was saved did I inspect and run the supplied verifier. Its observed output was `{"valid": true, "format": [5, 5, 5], "rank": 93, "addition_counts": {"u": 93, "v": 96, "w": 165}, "additions": 354, "identities_verified": 15625}`. It agrees, but the independent checker also checks the expanded coefficient class and active products.

## Binding comparisons and the coefficient-class quantifier

KNOWN, re-fetched live. `fmm_sota.json` lists format [5,5,5], rank 93. The ordered candidate has that same format and rank; no lower rank or reclassification as a rank target is asserted.

The full live Perminov tree is untruncated, with 6,637 entries. All seven matching rank-93 files were downloaded: the AlphaEvolve dense object, the cr383 reduced object, the c843 dense JSON and Maple objects, and three serendipitous-base dense objects. Exact audits verify the applicable dense tensors and literal SLP. The complete Maple file has 93 terms and exactly matches its dense JSON factors. There is exactly one matching addition_reduced_ZT cr file, with independently counted 383 additions (103+105+175). The MINIMUM cr over all matching files is therefore 383. `reduced_known.json` has no 5x5x5-93 cell. README lists rank 93 and supplies no lower additive count; CHANGELOG contains no lower matching entry. The claim's 354 is strictly below 383 by 29.

The live Lille page cites Moosbauer and Poole's February 2025 paper and links its actual tensor and evaluation scheme. I fetched and parsed both, rather than inferring the count from rank or a catalogue summary. The tensor is exact at rank 93 but its final coefficient alphabet includes ±2. The raw program is exact and has 434 binary additions (122+122+190), with six explicit scalar-2 operations. It is outside the candidate's final ternary coefficient class. The criterion's same-coefficient-class exception therefore applies. No separate lower ternary complexity variant is linked on the fetched per-format page. The actual fetched ternary objects remain the applicable comparisons.

The live matmulcatalog tree is untruncated, with 14,194 entries. All nine matching rank-93 objects were downloaded, including all three bud-bases objects, both Kauers objects, AlphaEvolve, both Perminov imports, and the Waksman constructed object. The eight bilinear objects were independently expanded and checked; their literal costs are 1098, 885, 1247, 846, 1080, 1039, 843 and 383. The reduced import is genuinely 383 even though its `additions` summary is 843; neither metadata nor COVERAGE is treated as an optimized SLP. Waksman's object is a mixed-input non-bilinear construction over Q with nonunit scalars, outside the candidate class; its advertised 396 also does not beat 354. COVERAGE lists +846 for the target cell. The candidate is below that value and every applicable actual fetched SLP.

## Public results and non-subsumption

KNOWN, re-fetched live. The current Trophy Case contains no additive rank-93 5x5x5 entry. The GitHub PR list was read with `state=all`, 100 per page, and followed to its final page using the server's Link header. The two pages contain 125 PRs: 10 open, 115 closed, and no merged entries. Closed PRs remain public mathematical comparisons. The matching PR21 is closed and its actual immutable object was fetched from the files listing; that listing has 21 files and no next-page link. Its SHA256 is `118237670d742163d9f8caa3fd4e5c6a850fe9570fbb39ce3f32906b427c2a4a`. It independently verifies at 93 active products and 378 additions (100+103+175), so 354 improves it by 24. No PR status or another panel verdict was used as proof.

PROVED-HERE for the finite downloaded circuit set. `criterion-code/public_audit.py` reverses each actual binary circuit to form its adjoint, treating the first accumulator, aliases and sign changes as free. The elementary map y=x0+x1 costs one addition; its transpose produces two aliases and costs zero. All six geometric ordered transformations of every applicable fetched rank-93 SLP were reconstructed and checked against the ordinary product tensor. Their minimum total is 378. Their independent per-stage minima are 100,100,168, summing to 368. Thus even a compatible arbitrary mix of these already-published circuit stages cannot have cost at most 354, regardless of product alignment. A separate finite common-factor-filtered exact stage-mixing check finds 119 compatible combinations with minimum 378. This is not an exclusion of all product gauges, new shared reductions, or all possible linear programs.

The candidate's expanded U,V,W factors exactly equal the public c843/cr383 Perminov factors. The claimed improvement is in its explicit evaluation program, not a newly discovered tensor decomposition. Equal tensor factors do not subsume a shorter additive SLP.

PROVED-HERE for the stated finite elementary construction family. `criterion-code/compose.py` independently checked the fetched small-format objects and constructed all six ordered orientations using actual adjoint circuits. Its library contains 125 ordered primitive formats, using the best rank/cost among those fetched circuits or explicit ordinary naive programs. It enumerates all 4,095 nontrivial positive ordered partition grids of 5 along the three axes. The minimum rank within this finite grid family is 98 and no grid has rank 93. Actual shared-gate ordinary programs were built and fully checked: 2+3 one-axis splits attain rank 98 with 373 or 374 additions; the 2+3 split on all axes attains rank 108 with 270 additions; the 4+1 boundary split attains rank 101 with 319 additions. Their cheaper additive counts do not meet the required rank. Sharing was counted from actual hash-consed binary gates, not multiplied catalogue counts. Target dimension 5 admits only 1×5 or 5×1 tensor-axis factorizations; ordinary dimension-one constructions do not yield rank 93. A separate finite recursive one-axis split rank calculation using the live rank table also has minimum 98 at the target; it is rank-only corroboration and supplies no inferred addition counts. No global exclusion is claimed for absorption, restricting larger circuits, padding-and-cancellation, alternative bases or constructions outside this explicit family.

## Bounded recent primary-literature review

KNOWN, inspected as source data. The review window is 2024-10-14 through the current 2026-10-14 UTC fetch date. Primary searches used English, Russian, French and Chinese terms for additive complexity and matrix multiplication. Full accessible primary pages inspected include Moosbauer–Poole (2502.04514), Dumas–Pernet–Sedoglavic (2506.19405), Schwartz–Zwecher (2508.01748), Perminov's ternary and additive-reduction papers (2511.20317, 2512.13365, 2512.21980, 2606.02480), Sun's ordinary 56-addition 3x3 paper (2604.27645), Kauers–Moosbauer–Wood's structured decompositions (2602.11041), Karunaratne–Idamekorala's ordinary 55-addition 3x3 paper (2607.28676), and Dumitriu et al.'s approximate-multiplication paper (2610.13905). Perminov's additive-reduction table explicitly lists target rank 93 and 383 additions. The newer ordinary 3x3 counts do not directly solve the rank-93 5x5x5 cell; the finite block-rank comparison already fails at rank 98 independently of their additive savings. Approximate/alternative-basis kernel costs were not substituted for a complete exact ordinary-coordinate SLP.

Stapleton–Perminov's 2609.32388 primary abstract is accessible and explicitly distinguishes its 51-addition alternative-basis kernel from 56 ordinary-coordinate additions. Its HTML URL returned 404; the linked certificate-tree URL also returned 404, and no certificate contents are asserted. Russian primary search results identified Sergeev's 2025 additive-complexity lower-bound paper over GF(2), with a Russian abstract and primary bibliographic record; two distinct direct Math-Net URLs timed out without an HTTP response. This is a limited non-English/full-text coverage gap, not a claimed exhaustive literature search or an inaccessible binding comparison table.

The three actual prior PDF denials recorded in `claim/LITERATURE_ACCESS.md` were respected: eprint 2024/2063, the stated SIAM PDF URL, and eprint 2026/849 were never requested, mirrored, retried, or bypassed. No denied contents are asserted. Optional coverage limits survive this pass; no claim of first-ever publication, complete global literature coverage or global additive optimality follows.

## Scope, nulls and replay limits

This is one immutable exact object and one table cell, with no statistical language claim or exhaustive discovery-search claim. A 400-control statistical null is not a missing requirement for its deterministic coefficient identity; the checker instead has independently constructed positive and negative controls and verifies every identity. Search-history replay is not inferred from a frozen circuit: the admitted missing original dictionaries and runtime code hashes prevent exact replay of the complete discovery. This report confirms only the object and the stated current comparisons. It does not change the candidate, criterion, publication status, schedule, research priority, paid-work settings or any other panel file.

All source content was treated as data. DNS failures in the sandbox occurred before HTTP; ordinary network escalation was used without access-control evasion. Binding GETs were successful once per URL; no 401,403,429,503 or challenge was bypassed. Every request's URL, UTC, observed HTTP status, body hash and size is in `criterion-code/source-manifest.json`, with full local bodies and receipts in `criterion-code/sources/`. The DNS-only failures are preserved separately.

## Core live-source receipts

| Source | UTC | HTTP | SHA256 | URL |
|---|---|---|---|---|
| rank | 2026-10-14T15:03:54.038388+00:00 | 200 | `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1` | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json |
| perminov-tree | 2026-10-14T15:02:21.235245+00:00 | 200 | `0cb3669d76a7e34604a34d2a204c0bf4e27525ba5348675bea6605d7e7032fab` | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 |
| perminov-obj-1 | 2026-10-14T15:05:01.057961+00:00 | 200 | `808285b8fb393d2e950ecff4ffe9881a209b6d3eff0d787e34d801a3f22293da` | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/f0efd4f67f6ff09bf0418af75c2a209c8cf814b3/schemes/results/addition_reduced_ZT/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json |
| reduced-known | 2026-10-14T15:03:54.038932+00:00 | 200 | `ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d` | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json |
| perminov-readme | 2026-10-14T15:03:54.039595+00:00 | 200 | `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341` | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md |
| perminov-changelog | 2026-10-14T15:03:54.039829+00:00 | 200 | `07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175` | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md |
| lille | 2026-10-14T15:03:54.430194+00:00 | 200 | `3daec22adb7e0efa20ebc2f2e9847b32951da7c57dc0980fbd00bc476645b593` | https://fmm.univ-lille.fr/5x5x5.html |
| lille-raw | 2026-10-14T15:05:02.628456+00:00 | 200 | `84beff33b19182b1adc3e99ba9c57b739c1d57efca43fd001f7d84eadbb29e22` | https://fmm.univ-lille.fr/5x5x5_raw.mpl.bz2 |
| lille-tensor | 2026-10-14T15:05:02.647858+00:00 | 200 | `087fcb6c29dbfc3d376536e0a86a316b6f710c7e83ac988db264267a74ca328e` | https://fmm.univ-lille.fr/5x5x5_tensor.mpl.bz2 |
| catalog-coverage | 2026-10-14T15:03:54.450990+00:00 | 200 | `c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7` | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md |
| catalog-tree | 2026-10-14T15:03:54.459830+00:00 | 200 | `8ce439a454388156fe1032180eb64f86f73140d43d6d38a7882d87944902a82d` | https://api.github.com/repos/solven-eu/matmulcatalog/git/trees/master?recursive=1 |
| trophy | 2026-10-14T15:03:54.545226+00:00 | 200 | `b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412` | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md |
| pr-page-1 | 2026-10-14T15:03:54.919996+00:00 | 200 | `a123b6ebf330afdb94b2b46b941869cd6160c0e5ed4bf5e6a09c5107268aebca` | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1 |
| pr-page-2 | 2026-10-14T15:05:02.682278+00:00 | 200 | `e7c3ae1140ee9ad8213e9c12be1232203541ddcacf7e94e22cdc58c71d554fab` | https://api.github.com/repositories/1011751194/pulls?state=all&per_page=100&page=2 |
| pr21-files | 2026-10-14T15:06:32.820046+00:00 | 200 | `f9fd4e0861b461d51486c56d2a2fa476d32cfde6088452639f11e03ada0f6331` | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/21/files?per_page=100&page=1 |
| pr21-circuit | 2026-10-14T15:07:03.051165+00:00 | 200 | `118237670d742163d9f8caa3fd4e5c6a850fe9570fbb39ce3f32906b427c2a4a` | https://github.com/elder-plinius/V3R1T4S/raw/8349fb0300c2b11cafbc950fa9b4a8740c6c8460/known-knowns%2Ffaster-matrix-multiplication%2F2026-10-14-anonymous-c6d1e0ab-11823767%2Fobject%2F5x5x5_m93_cr378_fv157_cn844_ZT_reduced.json |

## Reproduction

From the run directory:

```sh
python3 panel/criterion-code/exact.py claim/scheme.json panel/criterion-code/exact-result.json
python3 panel/criterion-code/public_audit.py
python3 panel/criterion-code/compose.py
```

These scripts use only the candidate and this skeptic's fetched public sources; they do not read other panels or the discovery workspace. Saved source receipts are reused for local replay, with no new GETs implied. The immutable frozen candidate and exactness/count/class checks pass; all successfully fetched applicable current comparisons are strictly higher; no subsuming circuit was found in the precisely stated public and construction checks.

pass: true
