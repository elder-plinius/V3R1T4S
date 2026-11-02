# Novelty check: <28,29,29> rank 10739

context: subagent (Claude Opus 5.5, fresh context, given only a copy of claim/)

Claim read: CLAIM.md (rank 10739 over Q, partial win p1; provenance: LITA <29,29,29> rank 11203, schemes/29x29x29_r11203.npz, by exact one-slice restriction(s) each followed by one exact 2-reduction) and the-record-we-beat/RECORD.md (author's comparators). I did not use the author's fetched values; every value below is from my own single GET.

## Fetches (one plain GET each with curl, no retries, no cookies, no custom headers; GitHub API read-only, unauthenticated)

| UTC time | HTTP | URL | sha256 of body | value read |
|---|---|---|---|---|
| 2026-10-25T08:42:07Z | 200 | https://fmm.univ-lille.fr/ | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | row 28x29x29: 11203 (Last-Modified Tue, 20 Oct 2026 08:14:45 GMT; byte-identical to the claim's 2026-10-24T22:35:44Z copy). Square row 29x29x29: 11203 credited to Khoruzhii, Gelß and Pokutta 2026 |
| 2026-10-25T08:42:07Z | 200 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | entry [28,29,29] rank 11203; createdAt 2026-10-19T20:46:33, 5456 entries; no entry containing the format componentwise is below 11203; byte-identical to the claim's copy |
| 2026-10-25T08:42:10Z | 200 | https://fmm.univ-lille.fr/28x29x29.html | 776a6a22fb8ed66a27f91131e545538811ddb6fbf9bdf4ed85458da07ebaf448 | ⟨28×29×29:12152⟩ (page construction text; byte-identical to the claim's copy) |
| 2026-10-25T08:42:54Z | 200 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json | 5c600b98b4bb8f9feed5b4d9ffabf11af34b98f49bf43ae250b81e71f43e000b | best scheme for the format (any order) 11145; external_best_rank 11203 (fmm-lille); nothing at or below 10739; byte-identical to the claim's copy |
| 2026-10-25T08:42:55Z | 200 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | no row for the format (sections stop at max dimension 16) |
| 2026-10-25T08:42:55Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 77203a718e82fec693578d193c9ccbb2332edcf41f086088a8405cd403666c5a | no row; largest dimension 16 |
| 2026-10-25T08:42:55Z | 200 | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/HEAD?recursive=1 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | 39 paths, not truncated; largest dimension 16; nothing for the format |
| 2026-10-25T08:42:56Z | 200 | https://api.github.com/repos/khoruzhii/lita/git/trees/HEAD?recursive=1 | d923a68888fc427aa8e9d216c6e54d45eb078afb8718ea55ae4990f443b89339 | 31 paths: 20 square schemes 13^3..32^3 only, scripts lita.py / lita_odd.py / verify.py, src; no rectangular scheme or table |
| 2026-10-25T08:42:56Z | 200 | https://api.github.com/repos/khoruzhii/lita/commits?per_page=5 | 39509a9b1eecf14c9d38d855460f419a58587cac450b1eea5039c961d9150557 | head 472a79fbc8, 2026-10-07T19:22:13Z (unchanged since the claim's fetch) |
| 2026-10-25T08:42:57Z | 200 | https://raw.githubusercontent.com/khoruzhii/lita/HEAD/README.md | 97df246f15643a7396307765d23432d03bcb5af97a9f8bf92cae85cb428d5b3f | tables list only square ⟨N×N×N⟩ ranks (odd N=29: 11203); no rectangular format; manuscript 'in preparation' |
| 2026-10-25T08:42:57Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 | FMM rows only for <13..15,..> formats; nothing for this format |
| 2026-10-25T08:42:57Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | 7 data rows, all max dimension <= 16; nothing for this format |
| 2026-10-25T08:42:57Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/commits?per_page=3 | 2e2ce4f0129f6e3ff6e630abbc90ce8834fd6fa0f7bdf83dde986abd39efb2bb | main head 1ebdef41c3, 2026-10-24T16:13:09Z |
| 2026-10-25T08:42:58Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1 | 4db10e495c51c8122ee1a9d7c2fd5b93724e3335e684c2ae53265235fbb7d820 | pull-request page (see the pull-request finding below) |
| 2026-10-25T08:42:59Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=2 | 76a5953ee49a263f2921f2f8a6c3ca56298f6133ff8d3b1a268515c969acffc3 | pull-request page (see the pull-request finding below) |
| 2026-10-25T08:42:59Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=3 | 855dc99d87975ec630178f06810b5ea6207b077b131fd2fecb41d66b2a7450da | pull-request page (see the pull-request finding below) |
| 2026-10-25T08:43:00Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=4 | daa21d7fd9bd5569861d40c4beba8a72b889c4c93e2af99df3276ed65312f2ac | pull-request page (see the pull-request finding below) |
| 2026-10-25T08:43:01Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=5 | 578f1c04889b3fe2fe0bd24803a0c143b90d00e5ad60b7211d21673f7d76b746 | pull-request page (see the pull-request finding below) |
| 2026-10-25T08:43:02Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=6 | 601d4e97605a78e211bd8f8618d4b31c9fcc4a5ed5b9f946016714d80befa1c8 | pull-request page (see the pull-request finding below) |
| 2026-10-25T08:43:03Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=7 | 877421c983aabcca4693c3c2150daf98caf8961e088c63a19611237c7ceb8560 | pull-request page (see the pull-request finding below) |
| 2026-10-25T08:43:03Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=8 | c3c6eab0d05b53c632a41fa8f12723df242db3c11b22c5033bffd9fc1cf2fa12 | pull-request page (see the pull-request finding below) |
| 2026-10-25T08:44:13Z | 301 | http://export.arxiv.org/api/query?search_query=au:Khoruzhii&max_results=50&sortBy=submittedDate&sortOrder=descending | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 301 redirect to the https URL (my http typo, empty body; the https URL was then fetched once, next row) |
| 2026-10-25T08:44:21Z | 200 | https://export.arxiv.org/api/query?search_query=au:Khoruzhii&max_results=50&sortBy=submittedDate&sortOrder=descending | e9c882bd3582722b884ea42aed11b96536bb09488a20f0e36720252b5b73465c | 13 entries (newest 2026-07-02); no LITA manuscript; none gives a rank for this format |
| 2026-10-25T08:44:14Z | 301 | http://export.arxiv.org/api/query?search_query=abs:%22matrix%20multiplication%22%20AND%20abs:rank&max_results=200&sortBy=submittedDate&sortOrder=descending | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 301 redirect to the https URL (my http typo, empty body; the https URL was then fetched once, next row) |
| 2026-10-25T08:44:24Z | 200 | https://export.arxiv.org/api/query?search_query=abs:%22matrix%20multiplication%22%20AND%20abs:rank&max_results=200&sortBy=submittedDate&sortOrder=descending | 55c25086c514b310295aa16078d7b3626bacc249d8ef277cfaf73eca0535b402 | 200 newest entries ('matrix multiplication' AND rank in abstract), 2020-07-31..2026-10-19; no abstract names this format or the ranks above |
| 2026-10-25T08:44:14Z | 301 | http://export.arxiv.org/api/query?search_query=abs:%22trilinear%20aggregation%22&max_results=50&sortBy=submittedDate&sortOrder=descending | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 301 redirect to the https URL (my http typo, empty body; the https URL was then fetched once, next row) |
| 2026-10-25T08:44:28Z | 200 | https://export.arxiv.org/api/query?search_query=abs:%22trilinear%20aggregation%22&max_results=50&sortBy=submittedDate&sortOrder=descending | 8fb12be99b47d52d858560f367ca93eca62f089dce5254f7752133f133636aed | 1 entry (2508.01748, Schwartz-Zwecher); square only |
| 2026-10-25T08:44:14Z | 301 | http://export.arxiv.org/api/query?search_query=abs:%22matrix%20multiplication%22%20AND%20(abs:scheme%20OR%20abs:schemes%20OR%20abs:%22flip%20graph%22)&max_results=200&sortBy=submittedDate&sortOrder=descending | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 301 redirect to the https URL (my http typo, empty body; the https URL was then fetched once, next row) |
| 2026-10-25T08:44:31Z | 200 | https://export.arxiv.org/api/query?search_query=abs:%22matrix%20multiplication%22%20AND%20(abs:scheme%20OR%20abs:schemes%20OR%20abs:%22flip%20graph%22)&max_results=200&sortBy=submittedDate&sortOrder=descending | fdc50144a111a1439f1680a49c038c6b998177d4c58071e03f82732945c2eca3 | 200 newest entries (matrix multiplication AND scheme/schemes/flip graph), 2022-01-27..2026-10-19; no abstract names this format or the ranks above |
| 2026-10-25T08:45:25Z | 200 | https://arxiv.org/html/2508.01748v1 | b54a99c5359e4a4ee790bffd1d337c8769b311d4b2d2ff3a59be899d9227cd3f | Schwartz-Zwecher: only square ⟨n0,n0,n0⟩ base cases (Tables 1-2); text says generalizing to rectangular is left for future research; none of the ranks above appears |
| 2026-10-25T08:45:26Z | 200 | https://arxiv.org/abs/2606.13408 | 9a31847c8ff48c914c40087b5834ace1549350ae701c6d5fee79c3fe9a0745ec | abstract of 'A catalog of fast matrix multiplication algorithms with exhaustive derivations' (the matmulcatalog paper; snapshot 2026-07-12): its values are those in catalog.json, read above |

Also: web searches (WebSearch, 2026-10-25 ~08:44-08:47Z) for the LITA manuscript, trilinear aggregation rectangular ranks 2026, flip-graph rectangular formats, AlphaEvolve follow-ups and 17..32 format catalogues; WebFetch of https://arxiv.org/abs/2508.01748 (v1 only, 3 Aug 2025). No hit gives a rank for this format.

## Pull requests of elder-plinius/V3R1T4S

705 pull requests (#1..#729; 357 open, 198 closed, 150 merged) scanned (title and body) for the format in every axis order and notation (x, ×, comma) and for the numbers in the table below. Result: no pull request names this format. Number coincidences only: #561 (sorting network) contains 4230, #23 (additive complexity <3,5,5>) contains 5625, #695 (selection bank) matches a '28, 29, 29' bound list; none is about FMM at this format. No FMM pull request names any format with a dimension >= 20; the largest are the sibling 19-family claims #708 <18,19,19> 3424 and #714 <18,18,19> 3225. TROPHY_CASE.md and INDEX.csv have nothing for this format.

## Best known value

- p1 bar (live fmm_sota.json and live Lille per-format page, plus the Lille index): fmm_sota.json 11203, Lille index 11203, Lille per-format page 12152; bar = 11203.
- Lowest value anywhere I found: **11145**, matmulcatalog docs/catalog.json (rows 11145, 11442, 11826, 11862, 12005, 12234); fmm_sota.json and Lille index 11203 (Proj([[29, 0], [0]],⟨29×29×29:11203⟩)).
- Formats containing <28,29,29> componentwise (restriction gives the cell at no higher rank): the lowest in fmm_sota.json is the cell itself (11203); LITA's <29,29,29> 11203 is above 10739.
- LITA (github.com/khoruzhii/lita at 472a79fbc8): published schemes and README tables are square only; no rectangular format is listed, so nothing at or below 10739 for this format.
- Perminov ranks.md, MerlijnW70/fmm-schemes, matmulcatalog COVERAGE.md: no row (all stop at dimension 16).

## Literature (last 24 months)

arXiv API queries above (author Khoruzhii; 'matrix multiplication' + rank; 'trilinear aggregation'; matrix multiplication + scheme/flip graph). Read in full: Schwartz-Zwecher 2508.01748 HTML (square trilinear-aggregation base cases only; rectangular left as future work). Abstracts read (from the arXiv API results and web search): Kauers-Wood 2510.19787 meta flip graph (about thirty small formats), Kauers-Wood 2505.05896 Moosbauer-Poole consequences (small rectangular formats), Perminov 2603.02398 and 2606.02480 (formats up to 16x16x16), Khoruzhii et al. 2511.10786 (structured n<=5), 2606.13408 matmulcatalog paper (its values are catalog.json, checked above); AlphaEvolve follow-ups found by web search concern small formats or the exponent omega only. The LITA manuscript is not on arXiv (README: in preparation). None lists this format at or below the claimed rank.

## Composition clause

The listed constructions for this format are Proj(LITA ⟨29³⟩) = 11203 (index) and the per-format page's 12152. The claimed 10739 equals none of them and is not a plain composition, padding or projection of a listed scheme: a plain coordinate projection of LITA gives 11203 (Lille) or the matmulcatalog projection values, all above 10739; the extra drop comes from a non-coordinate slice (e* direction) plus an exact 2-reduction (how-we-built-it/COMMANDS.md). This is a derivation from LITA's public scheme and must credit it, but its rank is not already listed.

## Verdict

r = 10739 is strictly below every known value I found: margin 464 against the p1 bar (11203, fmm_sota.json and Lille), and 406 against the lowest value anywhere (11145). Not a tie, not a listed composition. All primary pages returned HTTP 200 with no block; the Lille index, fmm_sota.json and the per-format page are byte-identical to the author's 2026-10-24 copies, so the tables did not move between claim and check. Residual risk: the LITA authors' unpublished manuscript could contain rectangular ranks; nothing public does as of this check. Novelty only; correctness of the scheme is for the other skeptics.

novelty: PASS

pass: true
