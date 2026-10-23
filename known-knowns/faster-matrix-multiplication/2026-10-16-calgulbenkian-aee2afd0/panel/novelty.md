# Novelty check: 4x5x6 rank 90, 348 reduced additions

context: Claude Code subagent (Opus 5.5), fresh context

Claim folder read: the claim record, INDEX.csv, the table record, object file name. All four hashes match the claim folder's hash list (claim record 58e37e5b..., INDEX.csv 6ef062b3..., object/4x5x6_m90_cr348_ZT_reduced.json aee2afd0..., table record 5d94e361...). The claim record is not shipped; the-record-we-beat/README.md holds the table record's content.

Every fetch below was one plain curl request, User-Agent 'V3R1T4S-research (honest client; curl)', no retries. Saved copies of the pages are not shipped in this package.

## Primary sources

| Source | URL | UTC fetch | HTTP | sha256 | Value read |
|---|---|---|---|---|---|
| Perminov tree | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-15T23:53:59Z | 200 | 71f2669d17d3636d92243b24d8b7a155ec9d9de472476a31c1a6db6d7ad2a610 | truncated=false. addition_reduced_ZT files for 4x5x6 (and every permutation of 4,5,6): exactly one, 4x5x6_m90_cr380_fv180_cn1023_ZT_reduced.json. Minimum cr = 380. Also naive_addition_reduced_ZT/4x5x6_m90_c998_ZT.json (naive c998, a different convention, not comparable). |
| reduced_known.json | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json | 2026-10-15T23:54:00Z | 200 | ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d | No 4x5x6-90 key. Only "4x5x6-93": Z 542, Z2 465, which is rank 93, a different rank, so it does not compare (and is higher anyway). |
| README.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-15T23:54:00Z | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 | 4x5x6 appears only in rank tables (line "4x5x6 ... 90 ... Z" and "90 (?) 90 90 2.819728939"). No addition count for 4x5x6. |
| CHANGELOG.md | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-15T23:54:00Z | 200 | 07fbb3249d1213b95d9a9c3069d208c0c3b4390a6b87c71325af64a2d56cd175 | No occurrence of 4x5x6. "Reduced additions improvement" entries cover other formats only. |
| Lille 4x5x6 page | https://fmm.univ-lille.fr/4x5x6.html | 2026-10-15T23:54:00Z | 200 | 6c1e64c4e736b598ff8dcffb5bc983aa825561ebadc18701de1a98b5bbda72e2 | Rank 90 ("4x5x6:90"). Cited work: "Manuel Kauers and Issaac Wood. Consequences of the Moosbauer-Poole algorithms. Technical Report 2505.05896, arXiv, May 2025." No Commentaries section, no complexity variant, no addition or operation count on the page. |
| matmulcatalog COVERAGE.md | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T23:54:01Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | Row 4,5,6: "✓ 90 Alphaevolve [Z→F₂] / ✓ 90 Alphaevolve ... adds +775". The legend says "+N adds is the addition count (nz(U)+nz(V)+nz(W) − 2r − n·p)". That is a naive count with no common-subexpression elimination, so it does not compare with a reduced count. Either way, 775 is above 348. |
| fmm_sota.json | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T23:54:01Z | 200 | d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1 | createdAt 2026-10-09T11:45:48. Entry {"format": [4, 5, 6], "rank": 90, "exponent": 2.819729}. Rank 90 is the best known rank, so the scheme is eligible. |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T23:54:02Z | 200 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 | No 4x5x6 entry and no addition-count entry. The fast-matrix-multiplication rows are rank records for formats 13 to 16. |
| V3R1T4S open PRs | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T23:54:02Z | 200 | 12473dc228f9f201566453a3e87b1d4ed24a37bf8eca1240f665a443a7148a2e | 16 open PRs (190-201, 153, 154, 30, 9). I read every title and body. None names fmm-additive-complexity-records or 4x5x6, and none gives an addition count. The only FMM claim is #197 (13,15,15 rank 1762 over Q, a rank target). |
| V3R1T4S known-knowns FMM | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/faster-matrix-multiplication | 2026-10-15T23:54:03Z | 200 | 4f0ffb2c424246006d34fc0ca873263e007bdc80240f69061ccbbdbc3f6511b4 | 21 package directories with opaque names; see the next two rows for what they contain. |
| V3R1T4S known-knowns INDEX.csv | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 2026-10-15T23:55:04Z | 200 | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | Rank records only (14x15x15, 13x14x14, ...). No 4x5x6. |
| V3R1T4S repo tree | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | 2026-10-15T23:55:04Z | 200 | f63c3cc8f48202557b7290f117f14aefdebe4f42ed79cf2448cb318d24b229db | truncated=false. I fetched this once to name the objects in the merged packages. The addition-count packages merged 2026-10-15 cover 4x6x6 (cr373), 5x7x7 (cr699), 6x6x7 (cr695), 6x8x8 (cr993), 4x6x8 (cr476), 6x6x6 (cr588), 5x6x7 (cr582), 4x6x7 (cr469), 6x6x8 (cr719), 5x5x8 (cr556) and 5x6x6 (cr502), plus one 5x5x5 (cr358). No file anywhere in the repo names 4x5x6 or any permutation of it. No merged package covers this format. |

Primary-source hashes for the tree, reduced_known.json, README, CHANGELOG, the Lille page, COVERAGE.md and fmm_sota.json are identical to those in the author's record (the-record-we-beat/README.md). The sources have not changed since the author's fetches.

## Literature (last 24 months)

arXiv export API, four queries in all. The first id_list request went to http:// and got a 301 with an empty body, so I sent that one query to its https:// target once. That is a redirect, not a retry after a block.

| Query | URL | UTC | HTTP | sha256 |
|---|---|---|---|---|
| q1 id_list (named papers) | https://export.arxiv.org/api/query?id_list=2512.21980,2512.13365,2604.27645,2607.28676,2609.32388,2609.06588,2505.05896,2601.05272&max_results=10 | 2026-10-15T23:55:30Z | 200 | 1d9e48daa1363b400de551ab312fd8929536db2c4b2054dcf7d2887717feabe6 |
| q2 abstract has "matrix multiplication" and additions or additive complexity | https://export.arxiv.org/api/query?search_query=abs:%22matrix%20multiplication%22%20AND%20(abs:additions%20OR%20abs:%22additive%20complexity%22)&sortBy=submittedDate&sortOrder=descending&max_results=60 | 2026-10-15T23:55:39Z | 200 | 8302f1b7aa274574e7e73bb858ccd7626fdc9ec864e43b3d90ff61d7b2d379a7 |
| q3 straight-line, CSE or arithmetic complexity | https://export.arxiv.org/api/query?search_query=abs:%22matrix%20multiplication%22%20AND%20(abs:%22straight-line%22%20OR%20abs:%22common%20subexpression%22%20OR%20abs:%22arithmetic%20complexity%22)&sortBy=submittedDate&sortOrder=descending&max_results=60 | 2026-10-15T23:55:39Z | 200 | 976191ef9ef202227f132beb0a488bb5ea2f99008f26d21aa02c59c874ee5e11 |
| q4 Martensson, Stankovski Wagner, "number of the beast", or 4x5x6 | https://export.arxiv.org/api/query?search_query=au:Martensson%20OR%20au:%22Stankovski%20Wagner%22%20OR%20ti:%22number%20of%20the%20beast%22%20OR%20abs:%224x5x6%22%20OR%20abs:%224%20x%205%20x%206%22&sortBy=submittedDate&sortOrder=descending&max_results=40 | 2026-10-15T23:56:43Z | 200 | b4841acd24ba2c186fad798f53268beca994c986a426c229f996d5fa6759772b |

Across the four queries, the only addition-count papers in the window are the ones listed below. No result names 4x5x6. The arXiv results also include no copy of the Martensson-Wagner paper. Two web searches ('"4x5x6" matrix multiplication additions rank 90 addition count' and the 2026/849 title) found no 4x5x6 addition count either.

### Perminov, arXiv:2512.13365 (Parallel Heuristic Exploration for Additive Complexity Reduction)
- PDF https://arxiv.org/pdf/2512.13365, 2026-10-15T23:55:41Z, HTTP 200, sha256 82aff81bf22f80c13cf559f1c42ada3fecda51fb4efc773c3e7ee1ae5b135c27.
- It gives a count for 4x5x6. Table 1 ("Schemes with optimal rank achieving new SOTA addition counts") has the row "4×5×6 90 1023 401 393 386 380". The columns are Naive 1023, GV 401, GP-5 393, GP-40 386 and Proposed 380.
- That count is comparable: same rank, ternary coefficients, no basis change. The paper evaluates "fast matrix multiplication algorithms with ternary coefficients {−1, 0, 1}", and this is the convention of his repository. The best value in the paper is 380. The 386 is Martensson-Wagner's Greedy-Potential tool (fmm_add_reduction), as run by Perminov on this scheme. 348 is below both.
- Table 6 ("Component-wise addition counts for schemes improvable by approaches result combination") lists only 4×7×8, 4×8×8, 5×7×8, 6×6×10, 7×7×7, 7×8×8 and 8×8×8. 4x5x6 is not among them.

### Perminov, arXiv:2512.21980 (A 58-Addition, Rank-23 Scheme for General 3x3)
- Read from q1. Covers 3x3x3 only: "achieving a rank-23 scheme with only 58 scalar additions". No count for 4x5x6.

### Martensson and Wagner, IACR ePrint 2026/849 (On Why and How to Minimize the Arithmetic Complexity of Fast Matrix Multiplication Algorithms)
- Abstract page https://eprint.iacr.org/2026/849, 2026-10-15T23:55:40Z, HTTP 200, sha256 04336b1693be1d37c7ec56b326db67eecdf74dcd1d6171f645a4a49210fdd26b. Received 2026-04-30, approved 2026-05-05.
- PDF https://eprint.iacr.org/2026/849.pdf, 2026-10-15T23:55:40Z, HTTP 403, a Cloudflare "Just a moment..." challenge (sha256 of the challenge page 7df8d0a46e996cab1500040cea8c33249ec2b1ef4aeeff19dcf678ea6fa7b1dc). Not retried.
- Authors' repository tree https://api.github.com/repos/werekorren/fmm_add_reduction/git/trees/main?recursive=1, 2026-10-15T23:55:40Z, HTTP 403 ("API rate limit exceeded"), sha256 3209519d06deb9f4f950810899ddc6fafba9bcfb3fb8cad8b5e1b30459ace147. Not retried.
- I then fetched the repository README once at a different URL, https://raw.githubusercontent.com/werekorren/fmm_add_reduction/main/README.md (2026-10-15T23:56:43Z, HTTP 200, sha256 37b319e0a3cb960cb612d56e1b53ac61bdfcdd673a0cd9ebafd9599cc055e842). It describes the tool and links the ACDA25 paper. It lists no per-format counts.
- The method has no basis change, so its counts would be comparable. The abstract says "We present improved methods for optimizing the number of additions in Strassen-type matrix multiplication schemes for larger matrix sizes, and without any change of basis."
- 4x5x6 is inside the paper's range of formats. The abstract says it optimizes "schemes with dimensions up to (n, m, k) = (5, 7, 10)", and 4 ≤ 5, 5 ≤ 7, 6 ≤ 10. The abstract does not say whether a rank-90 scheme for 4x5x6 is in the paper's sets, and it states no count. With the PDF blocked, I could not decide whether the paper holds a rank-90 count for 4x5x6.
- Predecessor, ePrint 2024/2063 ("The Number of the Beast ... up to 666", ACDA25): https://eprint.iacr.org/2024/2063, 2026-10-15T23:56:44Z, HTTP 200, sha256 dafa562b4f1ff2dd5beac64491d2cdb5cffc9877bc93edf087215977a55bb133. Received and approved 2024-12-23. Its reference set is "another reference set of algorithms due to Moosbauer and Kauers". It predates the first rank-90 scheme for 4x5x6 (Kauers-Wood and AlphaEvolve, May 2025), so any 4x5x6 count in it is not at rank 90. Perminov's reduced_known.json "4x5x6-93" entry is consistent with that.

### Sun, arXiv:2604.27645
- Read from q1. 3x3 only: "a rank-23 algorithm for general 3×3 matrix multiplication that uses 56 additions/subtractions". No count for 4x5x6.

### Karunaratne and Idamekorala, arXiv:2607.28676
- Read from q1. 3x3 only: "We give a 55-addition realization of rank-23 multiplication of two arbitrary 3×3 matrices." No count for 4x5x6.

### Stapleton and Perminov, arXiv:2609.32388
- Read from q1. 3x3 only, and the 51 is counted after a basis change, so it does not compare: "a rank-23 algorithm for 3×3 matrix multiplication using 51 additions and subtractions in alternative bases. The input and output conversions require five further additions". No count for 4x5x6.

### Nielsen, arXiv:2609.06588
- Read from q1. 3x3 only, with a basis change, so it does not compare: "using 52 additions or subtractions, together with a Karstadt-Schwartz-style basis change". No count for 4x5x6.

### Martensson, Stankovski Wagner and Stapleton, arXiv:2601.05272
- Read from q1. 3x3 only: "finding an algorithm requiring only 59 additions, still without a basis change". No count for 4x5x6.

### Kauers and Wood, arXiv:2505.05896 (the work the Lille page cites)
- PDF https://arxiv.org/pdf/2505.05896, 2026-10-15T23:57:17Z, HTTP 200, sha256 ac525dea1ef0277e7a329c1dab3906e74dfcc5286d2174cde479b1491c204b7b.
- It gives ranks only. Its table row is "(4, 5, 6) 120 93 90", and the text states no addition or operation count.

### fmm_add_reduction (Stankovski Wagner and others)
- The tree is blocked (above). The README gives no per-format counts. This tool's count for this exact scheme is known from Perminov's Table 1: GP-40 gives 386, above 348.

## Comparison

- Comparable counts read for 4x5x6 at rank 90 under the reduced, ternary, no-basis-change convention: 380 (Perminov's live repository and arXiv:2512.13365 Table 1) and 386 (GP-40 / fmm_add_reduction in the same table). The minimum is 380.
- Lille page: no count. COVERAGE.md: 775, a naive count that does not compare (and is higher). reduced_known.json: rank 93 only, which does not compare. No open PR, trophy entry or merged known-knowns package covers this format.
- 348 is below 380 by 32. That is a strict improvement, not a tie.

unresolved: IACR ePrint 2026/849 PDF (HTTP 403 Cloudflare challenge) and the werekorren/fmm_add_reduction repository tree (HTTP 403 rate limit). 4x5x6 is inside that paper's stated range "up to (n, m, k) = (5, 7, 10)" and its counts would be comparable (no basis change). The paper could plausibly hold a count for 4x5x6, but nothing I could read shows that it covers this format at rank 90 or states any count for it. Neither Perminov's live repository, which is the bank's status source, nor any later source I read records a lower count. A reader with PDF access should check that paper's tables for a 4x5x6 rank-90 entry below 348.

## Verdicts

- Full criterion: PASS, conditional on the unresolved item above. 348 is strictly below every comparable count I could read: Perminov's live minimum of 380, nothing on the Lille page, matmulcatalog's naive 775 (not comparable), and no V3R1T4S record, PR or package. No unread source is known to cover this format at rank 90.
- Partial win p1, as defined for this panel (strictly fewer than Perminov's live count, same convention): PASS. 348 is below 380 under the reduced convention, and the bar is his repository alone, so the unresolved item does not affect this verdict. Note: the bank's enumerated p1 text is written for a rank-23 SLP for 3x3x3. Read literally, that p1 does not apply to this claim. This claim is a full-criterion claim for 4x5x6.

pass: true
