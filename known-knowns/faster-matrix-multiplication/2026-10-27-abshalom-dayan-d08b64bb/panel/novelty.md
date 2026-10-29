# Novelty skeptic: <12,13,13> rank 1270 over Q

context: subagent (fresh Claude Code Agent context, Opus 5.5, saw only claim/)

Claim under test (claim/CLAIM.md): an explicit scheme for <12,13,13> with 1270 rank-one terms over Q, against a
claimed bar of 1274. Rank is invariant under permuting the format, so every source was checked for 12x13x13,
13x12x13 and 13x13x12 (and the spellings "12,13,13", (12, 13, 13), <12,13,13>, "12 13 13", rank 1270).

Every fetch was one plain GET with curl, User-Agent "V3R1T4S-panel (curl)", no cookies, no retries. Bodies are saved
in the working folder under fetched/. Times are UTC from `date -u` taken just before the request; sha256 is
`shasum -a 256` of the saved body.

## The four criterion sources and the status_source

| URL | UTC time | HTTP | sha256 | value for (12,13,13) |
|---|---|---|---|---|
| https://fmm.univ-lille.fr/ (status_source, catalogue index) | 2026-10-27T22:09:27Z | 200 | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | row id="12x13x13": "&lang;12&times;13&times;13:1274&rang;", rank column 1274, construction 2 x <4,4,6:73> + 12 x <3,3,6:40> + 12 x <3,4,6:54>; no row for 13x12x13 or 13x13x12 (0 occurrences) |
| https://fmm.univ-lille.fr/12x13x13.html | 2026-10-27T22:09:33Z | 200 | 1f1af49d3da24b39a47937f12e81d97936eb70307fce3dc249d2a75fd5a3b5c8 | "&lang;12&times;13&times;13:1274&rang;" (3 times); the only number 1200..1399 in the page is 1274 |
| https://fmm.univ-lille.fr/13x12x13.html | 2026-10-27T22:09:33Z | 404 | 9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e | no page (the catalogue names formats in sorted order only) |
| https://fmm.univ-lille.fr/13x13x12.html | 2026-10-27T22:09:38Z | 404 | 9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e | no page (as above) |
| https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-27T22:09:38Z | 200 | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | {"format": [12, 13, 13], "rank": 1274}; the only entry whose sorted format is (12,13,13); createdAt 2026-10-19T20:46:33 |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 2026-10-27T22:09:39Z | 200 | e71786dda6669d49fb1af448046cd294d7246977ba5372eeab5f536bf58dcbe4 | row `12x13x13`: ZT 1298 (?), Z 1298 (?), Q 1274; minimum 1274; no row for a permutation |
| https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/SHA256SUMS | 2026-10-27T22:09:39Z | 200 | de848328881cf69cbe2a8d8309e04d94826cf1431b5b39e81db63f95af58a3fd | no file for 12x13x13, 13x12x13 or 13x13x12 |
| https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-27T22:11:13Z | 200 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | 39 entries, truncated false, no path for any permutation |

Minimum over the four criterion sources: 1274 (fmm_sota.json 1274, Lille page 1274, Perminov min(ZT, Z, Q) = 1274,
MerlijnW70 none). The hashes of all four sources are identical to those the claim's TABLE_RECORD.md reports for
22:01Z and 22:05Z, so nothing changed between the claim's fetch and this one. 1270 < 1274 (by 4).

## This repository (github.com/elder-plinius/V3R1T4S)

| URL | UTC time | HTTP | sha256 | finding |
|---|---|---|---|---|
| https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-27T22:09:39Z | 200 | 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 | fast matrix multiplication rows cover <15,16,16>, <14,15,15>, <13,14,14>, <14,14,15>, <13,14,15>; nothing for <12,13,13> or a permutation; no 1270 or 1274 |
| https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | 2026-10-27T22:10:00Z | 200 | f3df364663fb1de338700ce286a6e0a80dad7145029339d00cdc285aa80b1677 | 5684 entries, truncated false; 1411 paths under known-knowns/faster-matrix-multiplication (48 subfolders); no path anywhere in the repo matches a 12/13/13 permutation or 1270; merged rank schemes there are 13x13x14 1479, 13x13x15 1578, 13x14x14 1538/1558, 13x14x15 1645/1677, 13x15x15 1762/1763, 11x13x16 1445, 14x14x15 1716, 14x15x15 1842/1843, 14x16x16 2117, 15x16x15 2105, 15x16x16 2176/2180/2196, plus small ZT addition-reduced schemes |
| https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 2026-10-27T22:10:14Z | 200 | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | 8 lines; no 12x13x13 / 13x12x13 / 13x13x12 / 1270 |
| https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1 .. page=8 (8 requests, 22:10:14Z to 22:10:40Z) | 2026-10-27T22:10:14Z (p1) ... 22:10:40Z (p8) | 200 (all 8) | p1 c50684b715186b4bb26042bef081bb9f2d9ec8ce5f1bfb76701b0092836cd77c, p2 6c1fb247807be3711061d6ae5f0e83bee48eb7ea0ad8517fbedea2413d56b95b, p3 f67c6986b774a00ff9ff29db7f93caa7fce4763077d2ac3e99edfd1503385d25, p4 d316afc60c9be4c924234fe6512a575f091f49d4bf6f0719f89c80ecdb44a847, p5 e11a8979d35cf46fe303822d74f76387fba9a003c760d22558d25e6fb02d1f3e, p6 f50b3876c4f7ec0995bcd85269195f0214bb969ac83e5c4975042844f24fc6b7, p7 a1f178fbd9847ed0746d1187f447f5f3833f30a7770b713bdf8a70c78310580a, p8 1a216d7c363aaa687cfd8001b0123c106603a6a4bb0ac4af9f820e46b9366096 | 761 pull requests (#1 to #790; 332 open, 273 closed unmerged, 156 merged). Titles, bodies and branch names scanned with regexes for 12x13x13, 13x12x13, 13x13x12 (x, ×, *), "12,13,13" and permutations, "<12,", "(12, 13", "12 13 13" and permutations, 1270..1273 and 1274. Only hits: #731 (Ramsey claim; "1270" is the tail of a sha256 prefix) and 12x13x16 in #168, #412, #615 (a different format). No open or closed PR names <12,13,13> or a permutation |

## Literature and public repositories (last 24 months)

| URL / query | UTC time | HTTP | sha256 | finding for (12,13,13) |
|---|---|---|---|---|
| https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-27T22:11:05Z | 200 | 3b9e56025720ae01521feeef6f3955aa1c0976737c55677a83ffcd5f118ba0ad | 6957 entries, truncated false; only schemes/known/tensor/12x13x13_tensor.mpl, schemes/results/ZT/12x13x13_m1298_ZT.json and .m (rank 1298) |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | 2026-10-27T22:11:08Z | 200 | 3fe5142019d26f5f191f1a5e35b9a92354bb274aeef22ba2ec550ad1e409ca94 | latest entry 27/10/2026 (addition reductions); no line mentions 12x13x13, a permutation, or 1270..1274 |
| https://api.github.com/repos/khoruzhii/lita/git/trees/HEAD?recursive=1 | 2026-10-27T22:11:11Z | 200 | d923a68888fc427aa8e9d216c6e54d45eb078afb8718ea55ae4990f443b89339 | 31 entries; schemes/ holds only cubes 13x13x13 r1379 up to 32x32x32 r14196; no rectangular scheme |
| https://raw.githubusercontent.com/khoruzhii/lita/HEAD/README.md | 2026-10-27T22:12:15Z | 200 | 97df246f15643a7396307765d23432d03bcb5af97a9f8bf92cae85cb428d5b3f | cube table only (N=13 rank 1379); no rectangular formats |
| https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-27T22:11:16Z | 200 | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | row ⟨12,13,13⟩: F2 1298, R/Q/Z 1298 (Dronperminov-ZT); best 1298 |
| https://api.github.com/search/issues?q=12x13x13 (all of GitHub) | 2026-10-27T22:12:45Z | 200 | 840185ac69ff01c964c2bfead7f7b8a5a7764c3814155124f82ebe285189a90f | total_count 0 |
| https://api.github.com/search/repositories?q=12x13x13 (10 s after the previous search) | 2026-10-27T22:12:55Z | 200 | 08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2 | total_count 0 |

Read with the web tool's default client (no body saved, so no sha256):
- arXiv:2606.02480v2, A. I. Perminov, "Meta Flip Graph meets Serendipitous Product: new Fast Matrix Multiplication
  results" (June 2026): reports 12x12x13 1144, 12x13x14 1370, 12x13x15 1442, 12x13x16 1509 and others; nothing for
  12x13x13 or a permutation.
- arXiv:2603.02398v1, A. I. Perminov, "Fast Matrix Multiplication in Small Formats: ... Open-Source Flip Graph
  Framework" (March 2026): formats up to 16x16x16; nothing for 12x13x13 or a permutation.
- arXiv:2510.19787v1, Kauers and Wood, "Exploring the Meta Flip Graph for Matrix Multiplication" (October 2025):
  formats with n+m+p <= 19 and dimensions up to 8; 12x13x13 is out of scope.
- Web searches for "12x13x13" matrix multiplication scheme rank, for <12,13,13> tensor rank upper bounds 2026, and for
  the LITA authors' paper: no source reports a <12,13,13> rank below 1274.

## Assessment

- Best known value for sorted (12,13,13), in every source found: 1274 over Q (Lille, fmm_sota.json, Perminov Q column,
  all from the Lille composition 2 x <4,4,6:73> + 12 x <3,3,6:40> + 12 x <3,4,6:54>); 1298 over ZT/Z/F2 (Perminov,
  matmulcatalog). Nothing lists 1270 or anything in 1270..1273, for this format or a permutation.
- 1270 is strictly below 1274 (by 4). It is not a tie, and it is not a composition rank already listed (the Lille
  construction column gives 1274).
- Caveats: (1) the claimed object is a restriction of LITA's published 13x13x13 rank-1379 scheme plus 25 absorbed
  terms, the same technique this repository already used for its merged <13,14,14>, <14,15,15> and similar records;
  the technique is not new, the value is. Anyone running it on the LITA cube could have obtained it, but no one has
  published it in the sources checked. (2) This panel member checked novelty only, not whether the scheme is
  correct; that is for the other skeptics. (3) Literature search covers arXiv and GitHub as reachable by web search
  and the API endpoints listed; a private or unindexed result cannot be ruled out.

pass: true
