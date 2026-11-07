# The record we compared against: OEIS A316471

Status source for this cell: https://oeis.org/A316471 (bank target oeis-keyword-more-new-terms, status_source
https://oeis.org/search?q=keyword:more).

## Extracted cell
| quantity | OEIS value | this package |
|---|---|---|
| A316471(21) | absent: DATA 1,1,1,2,3,6,11,21,43,89,185,391,840,1822,3975,8727,19280,42841,95661,214490 (n = 1..20, offset 1,4), %K nonn,more; b-file (synthesized from the entry) ends "20 214490"; history newest revision #6 (Susanna Cuyler, Jul 05 2018, approved), no pending draft; value searches "482706" and "214490,482706": no results | 482706 |

## Claim-time fetches (one plain curl GET each, no cookies, no retries)
| when (UTC) | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|
| 2026-11-03T20:00:13Z | https://oeis.org/A316471 | 200 | e42ef5273663792f83b2c6a89726bf9cb1c15e3a8d507732dd1d55eede63876c |
| 2026-11-03T20:00:14Z | https://oeis.org/search?q=keyword:more | 200 | 51649b3a679f59ae82e9be46513b058d34f25d60c4b81d3ade7d32e605d71fbd |
| 2026-11-03T20:00:14Z | https://oeis.org/search?q=id:A316471&fmt=text | 200 | b425e36d75f6f8f075d40e40597e572b05e5bd77d77c3c405074d7292f075a87 |
| 2026-11-03T20:00:14Z | https://oeis.org/A316471/b316471.txt | 200 | da35dd33b0431ceb71f73d6b1ad7ab3efad7dccb999314daf2deeb205227c4f5 |
| 2026-11-03T20:00:14Z | https://oeis.org/history?seq=A316471 | 200 | f2f1fd723dbc984035d20f494e2e132399dd3e1d1a9672dfdc8c5663f206f452 |
| 2026-11-03T20:00:15Z | https://oeis.org/search?q=42841,95661,214490&fmt=text | 200 | a6ecd4ad45594a748c1644c2cb4ea9b2380820e317292895c8d7be95c7e6a8d5 |
| 2026-11-03T20:03:03Z | https://oeis.org/search?q=482706&fmt=text | 200 | 2587c2336704d3a3d81f88fde3b1654dbda23ff33e58cf13150c0d1a16540bc4 |
| 2026-11-03T20:03:04Z | https://oeis.org/search?q=214490,482706&fmt=text | 200 | 8a2d3f20a02f6239d9813e01286e40adc7738602bcbabfba258d5918fe093edb |
| 2026-11-03T20:03:05Z | https://oeis.org/search?q=482706,1090033&fmt=text | 200 | fec7636cfb6d7a1f94d6835262eb71fa28b0f820da94692a71fd462ee9720d3b |
| 2026-11-03T20:03:06Z | https://oeis.org/search?q=id:A316471&fmt=text | 200 | b425e36d75f6f8f075d40e40597e572b05e5bd77d77c3c405074d7292f075a87 |
| 2026-11-03T20:03:08Z | https://oeis.org/A316471/b316471.txt | 200 | da35dd33b0431ceb71f73d6b1ad7ab3efad7dccb999314daf2deeb205227c4f5 |
| 2026-11-03T20:03:09Z | https://oeis.org/history?seq=A316471 | 200 | 0b92ef78281f7e352353b15f90a94a4e7776b124ef3df28198ed3ed263dda544 |

## Panel re-fetches (novelty and criterion skeptics, about 2026-11-03T21:17Z; as recorded in panel/novelty.md and panel/criterion.md)
| URL | HTTP | result |
|---|---|---|
| https://oeis.org/search?q=id:A316471&fmt=text and /internal | 200 | %K nonn,more; DATA ends 214490 (n = 20); "482706" 0 hits (sha256 b425e36d..., same as claim time) |
| https://oeis.org/A316471/b316471.txt | 200 | last line "20 214490" (sha256 da35dd33..., same as claim time) |
| https://oeis.org/history?seq=A316471 | 200 | newest #6, approved; no pending draft; "482706" 0 hits |
| https://oeis.org/search?q=482706 and q=214490,482706 | 200 | no results |

## Gate re-fetch (one plain curl GET each, User-Agent naming V3R1T4S research)
| when (UTC) | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|
| 2026-11-03T21:29:31Z | https://oeis.org/search?q=id:A316471&fmt=text | 200 | b425e36d75f6f8f075d40e40597e572b05e5bd77d77c3c405074d7292f075a87 |
| 2026-11-03T21:29:32Z | https://oeis.org/A316471/b316471.txt | 200 | da35dd33b0431ceb71f73d6b1ad7ab3efad7dccb999314daf2deeb205227c4f5 |
| 2026-11-03T21:29:33Z | https://oeis.org/history?seq=A316471 | 200 | 403a5aa12f521ec8d8ec99f1c7332cc114a33a522922f8e15eb17473f67e07eb |
| 2026-11-03T21:29:34Z | https://oeis.org/search?q=214490,482706&fmt=text | 200 | 8a2d3f20a02f6239d9813e01286e40adc7738602bcbabfba258d5918fe093edb |
| 2026-11-03T21:29:35Z | https://oeis.org/search?q=482706&fmt=text | 200 | 2587c2336704d3a3d81f88fde3b1654dbda23ff33e58cf13150c0d1a16540bc4 |

Result: %I #6 Jul 05 2018, %K nonn,more, %O 1,4, DATA still ends a(20) = 214490; entry text and b-file byte-identical
to claim time; history newest #6 approved, no draft; "482706" 0 hits in entry text, b-file and history; both value
searches "No results.".

Response headers were not recorded for these fetches. The pages themselves are not shipped (third-party content).
