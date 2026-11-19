# The record we compared against: OEIS A357953

Status source for this cell: https://oeis.org/A357953 (the bank target graph-automata-max-period lists A357953(9)
"or a later term" in its success criterion; its own status_source is the sibling entry https://oeis.org/A384209).

## Extracted cell
| quantity | OEIS value | this package |
|---|---|---|
| A357953(10) | absent: DATA is 1,2,2,6,7,18,38,96 (n = 1..8, offset 1), %I A357953 #13 Oct 24 2022 14:14:10; draft page "No pending changes for A357953"; no a(9) either | 624 |

## Fetches (one plain curl GET each, User-Agent naming V3R1T4S, no cookies, no retries)
| when (UTC) | by | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|---|
| 2026-11-03T04:23:02Z | run scout | https://oeis.org/search?q=id:A357953&fmt=text | 200 | e217d9de2d829e26350f85d6766fd128a84dcb49d4458cc6d82f08100244754c |
| 2026-11-03T04:23:02Z | run scout | https://oeis.org/draft/A357953 | 200 | 429575fcb57c5a67f9eaa49cb4b84b9e1bcbaa70d4eeb7d4be9566340df8c459 |
| 2026-11-03T04:23:02Z | run scout | https://oeis.org/search?q=id:A001349&fmt=text (completeness control, A001349(10) = 11716571) | 200 | 4cd8df106a0aca9da302aee37a2247c3d02251a6559a05e11a4ad4e300bf79fb |
| 2026-11-03T11:17:59Z | claim-time re-fetch | https://oeis.org/search?q=id:A357953&fmt=text | 200 | e217d9de2d829e26350f85d6766fd128a84dcb49d4458cc6d82f08100244754c (byte-identical to the scout fetch) |
| 2026-11-03T11:17:59Z | claim-time re-fetch | https://oeis.org/draft/A357953 | 200 | 97589ce9fe2cce6b9716a7f30e41dacbdf715124673c13fb35204f729ce9158a (dynamic page; text still "No pending changes for A357953") |
| 2026-11-03T11:54:38Z | novelty skeptic | https://oeis.org/search?q=id:A357953&fmt=text | 200 | same bytes as the claim-time fetch (sha256 prefix e217d9de2d829e26); DATA still ends a(8) = 96 |
| 2026-11-03T11:54:39Z | novelty skeptic | https://oeis.org/draft/A357953 | 200 | not recorded; text "No pending changes for A357953" |
| 2026-11-03T11:54:39Z / 11:54:47Z | novelty skeptic | https://oeis.org/search?q=1,2,2,6,7,18,38,96,180&fmt=text and ...?q=38,96,180,624 | 200 | not recorded; both "No results." |

Repository check: GitHub issue/PR search "A357953 repo:elder-plinius/V3R1T4S" (claim time 2026-11-03T11:18:00Z and
novelty skeptic 11:54:48Z, HTTP 200): only PR #904 (A384209(10)), which lists A357953 as not claimed.

The honesty gate (2026-11-03T13:29:57Z) did not re-fetch: the claim-time fetch was 2 h 12 min old and the novelty
fetch 1 h 35 min old, both under 6 hours (panel/gate.md). Selected response headers were not recorded. The pages
themselves are not shipped (third-party content).
