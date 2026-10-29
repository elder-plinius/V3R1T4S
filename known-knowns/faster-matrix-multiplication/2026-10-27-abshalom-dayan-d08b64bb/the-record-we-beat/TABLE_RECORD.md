# Table record (the scout's record and the pre-panel re-fetch)

Every fetch was one plain GET with curl and the User-Agent "V3R1T4S-run (curl)", no cookies, no retries. Times are
UTC from `date -u`; sha256 of the saved body. 

| source | first fetch | pre-panel re-fetch | value for sorted <12,13,13> |
|---|---|---|---|
| https://fmm.univ-lille.fr/ (catalogue index; the bank's status_source) | 2026-10-27T22:02:04Z, HTTP 200, sha256 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | (not re-fetched; per-format page below) | row id="12x13x13": "&lang;12&times;13&times;13:1274&rang;", fast_tensor_rank 1274 |
| https://fmm.univ-lille.fr/12x13x13.html | 2026-10-27T22:01:18Z, HTTP 200, sha256 1f1af49d3da24b39a47937f12e81d97936eb70307fce3dc249d2a75fd5a3b5c8 | 2026-10-27T22:05:33Z, HTTP 200, sha256 1f1af49d3da24b39a47937f12e81d97936eb70307fce3dc249d2a75fd5a3b5c8 | "&lang;12&times;13&times;13:1274&rang;"; the only number 1200..1310 in the page is 1274 |
| https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-27T22:01:17Z, HTTP 200, sha256 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | 2026-10-27T22:05:33Z, HTTP 200, sha256 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | {"format": [12, 13, 13], "rank": 1274}; createdAt 2026-10-19T20:46:33; no other entry for a permutation |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 2026-10-27T22:01:18Z, HTTP 200, sha256 e71786dda6669d49fb1af448046cd294d7246977ba5372eeab5f536bf58dcbe4 | 2026-10-27T22:05:33Z, HTTP 200, sha256 e71786dda6669d49fb1af448046cd294d7246977ba5372eeab5f536bf58dcbe4 | row "`12x13x13` \|  1298 (?) \|  1298 (?) \|  1274 \|  2.816848164": ZT 1298, Z 1298, Q 1274; minimum 1274 |
| https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/SHA256SUMS | 2026-10-27T22:01:19Z, HTTP 200, sha256 de848328881cf69cbe2a8d8309e04d94826cf1431b5b39e81db63f95af58a3fd | 2026-10-27T22:05:33Z, HTTP 200, sha256 de848328881cf69cbe2a8d8309e04d94826cf1431b5b39e81db63f95af58a3fd | no 12x13x13 (or 13x12x13, 13x13x12) file |
| https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-27T22:01:19Z, HTTP 200, sha256 f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | 2026-10-27T22:05:33Z, HTTP 200, sha256 f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | 39 paths, truncated false, none for this format |

The minimum over the four sources the criterion names is 1274; the claimed rank 1270 is 4 below it.

Other sources checked for the same cell:
- This repository: TROPHY_CASE.md (https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md,
  2026-10-27T22:01:19Z, HTTP 200, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113): no <12,13,13> entry; nothing merged for this format.
- Pull requests of this repository, all states (GitHub search API, one request per spelling, 2026-10-27T22:01:20Z
  to 22:01:38Z, all HTTP 200): 12x13x13 (0 results), 13x12x13 (0), 13x13x12 (0), "12,13,13" (0), "12 13 13" (5),
  "12, 13, 13" (4), 1270 (1: a Ramsey claim where 1270 is part of a sha256 prefix), fmm-catalogue-small-format-rank
  (47). No title or body names (12,13,13) or a permutation, and none names rank 1270 for it. A repeat at 22:05Z got
  HTTP 200 and 0 results for 12x13x13 and 13x12x13, then HTTP 403 (search rate limit) and was stopped, not retried.
- LITA repository tree (https://api.github.com/repos/khoruzhii/lita/git/trees/HEAD?recursive=1,
  2026-10-27T22:03:43Z, HTTP 200, sha256 d923a68888fc427aa8e9d216c6e54d45eb078afb8718ea55ae4990f443b89339): schemes/ holds only cubes N x N x N; no <12,13,13> scheme.
