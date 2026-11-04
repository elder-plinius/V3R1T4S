# Table record (the scout's record and the pre-panel re-fetch)

Every fetch was one plain GET with curl and the User-Agent "V3R1T4S-run (curl)", no cookies, no retries. Times are
UTC from `date -u`; sha256 of the saved body. The two fetches returned identical bytes for every source.

| source | first fetch | pre-panel re-fetch | value for sorted <13,14,15> |
|---|---|---|---|
| https://fmm.univ-lille.fr/ (catalogue index; the bank's status_source) | 2026-10-28T22:03:15Z, HTTP 200, sha256 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | (per-format page below) | row id="13x14x15": "&lang;13&times;14&times;15:1681&rang;" |
| https://fmm.univ-lille.fr/13x14x15.html | 2026-10-28T22:01:18Z, HTTP 200, sha256 d2a562a11c213effc7df98468757cda923925f248fab408ed38c485039851158 | 2026-10-28T22:08:49Z, HTTP 200, same sha256 | "&lang;13&times;14&times;15:1681&rang;"; the only number 1600..1700 in the page is 1681 |
| https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-28T22:01:18Z, HTTP 200, sha256 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | 2026-10-28T22:08:49Z, HTTP 200, same sha256 | {"format": [13, 14, 15], "rank": 1681}; createdAt 2026-10-19T20:46:33 |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 2026-10-28T22:01:19Z, HTTP 200, sha256 5f433497fdc4ea056f0d13e5adfdb22b70237ea23170134fe1a3d9637bb5f4bb | 2026-10-28T22:08:49Z, HTTP 200, same sha256 | row "`13x14x15` \|  1681 (?)   \| 1681 (1714)  \| 1681 (1714)  \|   2.816136526": minimum 1681 |
| https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/SHA256SUMS | 2026-10-28T22:01:19Z, HTTP 200, sha256 de848328881cf69cbe2a8d8309e04d94826cf1431b5b39e81db63f95af58a3fd | 2026-10-28T22:08:49Z, HTTP 200, same sha256 | no file for any permutation of 13x14x15 |
| https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | 2026-10-28T22:01:19Z, HTTP 200, sha256 f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | 2026-10-28T22:08:50Z, HTTP 200, same sha256 | truncated false, none for this format |

Minimum over the four criterion sources: 1681. Merged here: 1645 (pull request #166). Claimed: 1644.

Other sources checked:
- TROPHY_CASE.md (https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, 2026-10-28T22:01:20Z
  and 22:08:50Z, HTTP 200, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113): row 48 lists
  <13,14,15> 1677, "superseded 2026-10-15 by contributed rank 1645, pull request #166".
- Pull requests, all states (https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1..8,
  one request at a time, 2026-10-28T22:01:23Z-22:01:52Z and 22:08:53Z-22:09:22Z, all HTTP 200, identical bytes): 781
  PRs, numbers 1-811. Every title and body mentioning (13,14,15) in any order and spelling: #4 (closed, unmerged,
  rank 1646), #166 (merged, 1645), #164/#177/#178 (other cells), #743/#747/#749/#751/#809 (the digits appear only in
  index lists). No PR claims rank <= 1644 for this format; "1644" occurs only in #55 (inside a sha256) and #399 (a
  kissing-number count).
- LITA tree (https://api.github.com/repos/khoruzhii/lita/git/trees/HEAD?recursive=1, 2026-10-28T22:06:05Z, HTTP 200,
  sha256 d923a68888fc427aa8e9d216c6e54d45eb078afb8718ea55ae4990f443b89339): only cubes N x N x N; the 15x15x15 file's
  git blob 65821484d954b4aade06cbda624932ba2a481f7b equals `git hash-object rebuild/15x15x15_r1977.npz`.
