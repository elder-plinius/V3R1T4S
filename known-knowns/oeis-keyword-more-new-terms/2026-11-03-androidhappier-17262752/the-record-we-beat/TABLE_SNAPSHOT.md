# The record we compared against: OEIS A326335

Status source for this cell: https://oeis.org/A326335 (bank target oeis-keyword-more-new-terms, status_source
https://oeis.org/search?q=keyword:more).

## Extracted cell
| quantity | OEIS value | this package |
|---|---|---|
| A326335(11) | absent: DATA 1,1,1,1,2,6,21,86,394,1974,10696 (n = 0..10, offset 0,5), %K nonn,more; b-file (synthesized from the entry) ends "10 10696"; history newest revision #6 (Susanna Cuyler, Jun 28 2019, approved), no pending draft; context value search "10696,61987": no match | 61987 |

## Claim-time fetches (one plain curl GET each, User-Agent naming V3R1T4S research, no cookies, no retries)
| when (UTC) | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|
| 2026-11-03T16:25:13Z | https://oeis.org/A326335 | 200 | 66a171d61e402d3b155bf0e64652f906dd393c4dd89ade5660b61127fad6eaee |
| 2026-11-03T16:25:14Z | https://oeis.org/A326335/b326335.txt | 200 | 22e6ca0a969c252d87b19b0b6ec2f24567a3ebcc2f186dfedc62f9989eb987fb |
| 2026-11-03T16:25:15Z | https://oeis.org/A326335/internal | 200 | 38087a77d1c73eb27e97b1f8faa599429c0c3feb556cf9511f4270b7d8b49b57 |
| 2026-11-03T16:25:16Z | https://oeis.org/history?seq=A326335 | 200 | 7d22a1d7dd13393758d3cfe3da0aa8b401f46107ebf329594e07d681749321fe |
| 2026-11-03T16:25:17Z | https://oeis.org/search?q=keyword:more | 200 | 2ff0acc54a932dd8c305265c9503d3ea06bbcad297bd6edd88486f248d5795f5 |
| 2026-11-03T16:27:31Z | https://oeis.org/search?q=61987&fmt=text | 200 | 2062eba1c060afcc3d31ac7ece20743460c48bd862b64e88399f03a589d64422 |
| 2026-11-03T16:27:32Z | https://oeis.org/search?q=10696%2C61987&fmt=text | 200 | 2e27052c3188ad2249652d5e65870da1ad1cb3be9ec542c51b32e16c245422c0 |

The bare search "61987" returns A209399 (an unrelated sequence that has 61987 as one of its own terms), A061987
(A-number string match), A220933, A243426 and A302318; none records 61987 as a term of A326335.

## Panel re-fetches (novelty and criterion skeptics, about 2026-11-03T19:12Z-19:13Z; as recorded in panel/novelty.md and panel/criterion.md)
| URL | HTTP | result |
|---|---|---|
| https://oeis.org/A326335 and /internal | 200 | %K nonn,more; DATA ends 10696 (n = 10); "61987" 0 hits |
| https://oeis.org/A326335/b326335.txt | 200 | last line "10 10696" (sha256 22e6ca0a..., same as claim time) |
| https://oeis.org/history?seq=A326335 | 200 | newest #6, approved; no pending draft; "61987" 0 hits |
| https://oeis.org/search?q=seq:10696,61987 | 200 | no match |

## Gate re-fetch (one plain curl GET each)
| when (UTC) | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|
| 2026-11-03T19:16:29Z | https://oeis.org/search?q=id:A326335&fmt=text | 200 | 13a9a46a27dd80a6a4eca780f83bd00e03b73f6448b4f9e41035f8fbabb477bb |
| 2026-11-03T19:16:29Z | https://oeis.org/A326335/b326335.txt | 200 | 22e6ca0a969c252d87b19b0b6ec2f24567a3ebcc2f186dfedc62f9989eb987fb |
| 2026-11-03T19:16:29Z | https://oeis.org/history?seq=A326335 | 200 | 0c2ebe1e29055d32834c2d719f31d39c5c98ceea40eecc76867302e5c2a0b96e |
| 2026-11-03T19:16:29Z | https://oeis.org/search?q=10696,61987&fmt=short | 200 | 02ceb0695fd680171807a3c49810d6044849988492ebe1bde2d7f264274579bc |
| 2026-11-03T19:16:29Z | https://oeis.org/search?q=61987&fmt=short | 200 | 9057348cf2e5c0d1f9e7d17e8a6c4b94d6f1ff48922fa90b8e6b3474b34624fd |

Result: %K nonn,more, %O 0,5, DATA still ends a(10) = 10696; b-file unchanged; history newest #6 approved, no draft;
"61987" 0 hits in entry text, b-file and history; value search 10696,61987 "Sorry, but the terms do not match
anything in the table."; bare search 61987 gives the same 5 results as at claim time.

Response headers were not recorded for these fetches. The pages themselves are not shipped (third-party content).
