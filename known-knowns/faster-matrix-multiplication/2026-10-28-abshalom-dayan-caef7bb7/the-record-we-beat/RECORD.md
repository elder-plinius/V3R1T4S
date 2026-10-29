# The record we beat

Snapshot of the four sources the criterion names, for the sorted format (13,14,15), plus this repository's merged
records and pull requests, from the pre-packaging fetch. One plain GET per URL (curl, User-Agent "V3R1T4S-run
(curl)"), no cookies, no retries. The pages themselves are not shipped; fetch_log.txt lists the fetches (time, HTTP
status, URL, saved name, sha256, bytes) and headers/ holds selected response headers.

| source | cell | value | URL | fetched (UTC), HTTP, sha256 |
|---|---|---|---|---|
| fmm_sota.json (createdAt 2026-10-19T20:46:33) | [13, 14, 15] | 1681 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-28T22:28:45Z, 200, 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae |
| Lille per-format page | <13x14x15> | 1681 | https://fmm.univ-lille.fr/13x14x15.html | 2026-10-28T22:28:45Z, 200, d2a562a11c213effc7df98468757cda923925f248fab408ed38c485039851158 |
| Lille catalogue index (status_source) | <13x14x15> | 1681 | https://fmm.univ-lille.fr/ | 2026-10-28T22:03:15Z, 200, 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 |
| Perminov docs/ranks.md | 13x14x15 | ZT 1681 (?), Z 1681 (1714), Q 1681 (1714); min 1681 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 2026-10-28T22:28:46Z, 200, 5f433497fdc4ea056f0d13e5adfdb22b70237ea23170134fe1a3d9637bb5f4bb |
| MerlijnW70/fmm-schemes (git tree, not truncated; SHA256SUMS) | 13x14x15 any orientation | none | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-28T22:28:46Z, 200, f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 |
| this repository, TROPHY_CASE.md | <13,14,15> | row 48: our 1677, superseded by 1645 (pull request #166) | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-28T22:28:46Z, 200, 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 |

Minimum over the four named sources: 1681; merged here: 1645. 1644 is 37 and 1 below them.

Pull requests: all 781 (numbers 1 to 811), every state, read through
https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100 (pages 1-8, 2026-10-28T22:28:50Z to
22:29:18Z, HTTP 200; page 8 has fewer than 100). A regex over every title and body for any ordering of 13, 14, 15 in
the spellings AxBxC, (A, B, C), <A,B,C> and "A B C", and for ranks 1600-1649, finds two claims for this format: #4
(closed, unmerged, 1646) and #166 (merged, 1645). The other hits are other cells or index lists. "1644" occurs only in
#55 (inside a sha256) and #399 (a count, "16448 rows").

The skeptics' own fetches (NOVELTY 2026-10-28T22:16-22:19Z, see panel/novelty.md; CRITERION 22:33Z in the re-run of record, see panel/criterion.md, and 22:23Z in its first run, whose verdict is not shipped) returned the same sha256 for all four sources. TABLE_RECORD.md is the scout's record shown to the panel
(unchanged). The criterion asks for all four sources to be re-fetched immediately before claiming; the last fetch of
all four was by CRITERION at 22:33Z.
