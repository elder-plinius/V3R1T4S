# The record we beat

Snapshot of the four sources the criterion names, for the sorted format (12,13,13), plus this repository's merged
records and pull requests. One plain GET per URL (curl, User-Agent "V3R1T4S-run (curl)"), no cookies, no retries. The
pages themselves are not shipped; fetch_log.txt lists the last fetches (time, HTTP status, URL, saved name, sha256,
bytes) and headers/ holds selected response headers.

| source | cell | value | URL | fetched (UTC), HTTP, sha256 |
|---|---|---|---|---|
| fmm_sota.json (createdAt 2026-10-19T20:46:33) | [12, 13, 13] | 1274 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-27T22:19:24Z, 200, 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae |
| Lille per-format page | <12x13x13> | 1274 | https://fmm.univ-lille.fr/12x13x13.html | 2026-10-27T22:19:24Z, 200, 1f1af49d3da24b39a47937f12e81d97936eb70307fce3dc249d2a75fd5a3b5c8 |
| Lille catalogue index (status_source) | <12x13x13> | 1274 | https://fmm.univ-lille.fr/ | 2026-10-27T22:02:04Z, 200, 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 |
| Perminov docs/ranks.md | 12x13x13 | ZT 1298 (?), Z 1298 (?), Q 1274; min 1274 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 2026-10-27T22:19:24Z, 200, e71786dda6669d49fb1af448046cd294d7246977ba5372eeab5f536bf58dcbe4 |
| MerlijnW70/fmm-schemes (git tree, 39 paths, not truncated) | 12x13x13 any orientation | none | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-27T22:19:25Z, 200, f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 |
| this repository, TROPHY_CASE.md | <12,13,13> | no entry | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-27T22:19:25Z, 200, 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 |

Minimum over the four named sources: 1274. 1270 is 4 below it.

Pull requests: all 761 (numbers 1 to 790, newest created 2026-10-27T19:51:59Z), every state, read through
https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100 (pages 1-8, 2026-10-27T22:19:25Z to
22:19:48Z, HTTP 200; page 9 empty). A regex over every title and body for 12x13x13, 13x12x13, 13x13x12, "12,13,13",
"12 13 13", <12,13,13> and 1270 finds one hit only: #731, a Ramsey claim where "1270" is the end of a sha256 prefix.
Earlier the same day the GitHub search API, under eight spellings, found nothing for this cell either.

The skeptics' own fetches (2026-10-27T22:09-22:11Z NOVELTY, 22:16Z CRITERION) returned the same sha256 for all four
sources; see panel/novelty.md and panel/criterion.md. TABLE_RECORD.md is the scout's record shown to the panel
(unchanged). The criterion asks for all four sources to be re-fetched immediately before claiming; the CRITERION
re-run fetched all four again at 2026-10-28T05:44:19-05:44:20Z (panel/criterion.md, panel/gate.md).
