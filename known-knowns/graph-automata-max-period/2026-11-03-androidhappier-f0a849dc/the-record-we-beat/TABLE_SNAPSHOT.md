# The record we compared against: OEIS A384209

Status source (bank target graph-automata-max-period): https://oeis.org/A384209.

## Extracted cell
| quantity | OEIS value | this package |
|---|---|---|
| A384209(11) | absent: DATA is 1,1,1,1,2,4,8,14,27 (n = 1..9), %I A384209 #8 May 22 2025, keyword more; no a(10), no a(11); draft page "No pending changes for A384209" | 71 |

## Fetches (one plain curl GET each, User-Agent naming V3R1T4S, no cookies, no retries)
| when (UTC) | by | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|---|
| 2026-11-03T03:24:38Z | run scout | https://oeis.org/search?q=id:A384209&fmt=text | 200 | a2d2fe9c9ff2aab776502142000c0bd3bc4d5b2e120022d1679f0990a8c84247 |
| 2026-11-03T03:24:38Z | run scout | https://oeis.org/draft/A384209 | 200 | d80b0cefa53669100473049c0298231c7f4cfc38f661dc4e27d209483e05b957 |
| 2026-11-03T07:36:52Z | claim time | https://oeis.org/search?q=id:A384209&fmt=text | 200 | a2d2fe9c9ff2aab776502142000c0bd3bc4d5b2e120022d1679f0990a8c84247 |
| 2026-11-03T07:36:52Z | claim time | https://oeis.org/draft/A384209 | 200 | a1c8c3ab7222694b637b5dffdc27061525099436357b4273cb70837b367d9577 |
| 2026-11-03T07:36:57Z | claim time | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+A384209 | 200 | 856667ab8608b2ffede754e710aa3ab7d911f0d599dcc1012b89e4a43d1a033b |
| 2026-11-03T07:53:58Z | novelty skeptic | https://oeis.org/search?q=id:A384209&fmt=text | 200 | a2d2fe9c9ff2aab776502142000c0bd3bc4d5b2e120022d1679f0990a8c84247 |

The text-format page is byte-identical at all three fetches. The draft page is dynamic (its hash changes between
fetches); both copies say "No pending changes". The GitHub search found one item, PR #904 (A384209(10) only).
The honesty gate (2026-11-03T09:56:51Z) made no new fetch: the claim-time and novelty fetches were less than 6 hours
old. Selected headers were not recorded. The pages themselves are not shipped (third-party content).
