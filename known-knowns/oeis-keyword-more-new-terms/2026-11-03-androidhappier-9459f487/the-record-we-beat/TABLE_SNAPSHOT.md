# The record we compared against: OEIS A326336

Status source for this cell: https://oeis.org/A326336 (bank target oeis-keyword-more-new-terms, status_source
https://oeis.org/search?q=keyword:more).

## Extracted cell
| quantity | OEIS value | this package |
|---|---|---|
| A326336(11) | absent: DATA 1,1,1,1,2,7,24,100,458,2279,12270 (n = 0..10, offset 0,5), %K nonn,more; b-file (synthesized from the entry) ends "10 12270"; history newest revision #6 (Susanna Cuyler, Jun 28 2019, approved), no pending draft; context value search "12270,70472": no match | 70472 |

## Claim-time fetches (one plain curl GET each, User-Agent naming V3R1T4S research, no cookies, no retries)
| when (UTC) | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|
| 2026-11-03T16:25:19Z | https://oeis.org/A326336 | 200 | 336f4aad5df296e99259d36617ef710bce3653346a5c7e4ed7a3f4cccabff7b5 |
| 2026-11-03T16:25:20Z | https://oeis.org/A326336/b326336.txt | 200 | c1111d16bc01d67edf407e7d6725b23dac3b3581d6838cbb16fe8fec5741e0c0 |
| 2026-11-03T16:25:21Z | https://oeis.org/A326336/internal | 200 | 88e75906c0b3d4c9c03ebbde739a024800766e70e72273ec69501c3818f263a2 |
| 2026-11-03T16:25:22Z | https://oeis.org/history?seq=A326336 | 200 | e899fe7da40bf7887c511d2e68f03605b18fd8c0362082bc09b9c99f21c9a620 |
| 2026-11-03T16:25:23Z | https://oeis.org/search?q=keyword:more | 200 | 1e46e5f10e6b0d2ddd2f3b418ea41908808cc5485908c88c75ad45b4fd314d06 |
| 2026-11-03T16:27:33Z | https://oeis.org/search?q=70472&fmt=text | 200 | 1fa63a84c0003d1c608a6fc454416f1e82c794e313dc4659ab2aaa5b002e6339 |
| 2026-11-03T16:27:35Z | https://oeis.org/search?q=12270%2C70472&fmt=text | 200 | 09f472c5775b68daf1ff739860ab76e379334636137c13c3166d1b6478b6243a |

The bare search "70472" returns only A070472 (a(n) = n^3 mod 7; A-number string match); none records 70472 as a
term of A326336.

## Panel re-fetches (novelty and criterion skeptics, 2026-11-03T20:28:43Z-20:29Z; as recorded in panel/novelty.md and panel/criterion.md)
| URL | HTTP | result |
|---|---|---|
| https://oeis.org/A326336?fmt=text and /internal | 200 | %K nonn,more; %O 0,5; DATA ends 12270 (n = 10); "70472" 0 hits |
| https://oeis.org/A326336/b326336.txt | 200 | last line "10 12270" (sha256 c1111d16..., same as claim time) |
| https://oeis.org/history?seq=A326336 | 200 | newest #6, approved; no pending draft; "70472" 0 hits |
| https://oeis.org/search?q=12270,70472 | 200 | no match |

## Gate re-fetch (one plain curl GET each)
| when (UTC) | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|
| 2026-11-03T20:40:50Z | https://oeis.org/search?q=id:A326336&fmt=text | 200 | c41509d2f024635586f257c056a31118c498ce8e0a53e6d58af8a1cda2a088ed |
| 2026-11-03T20:40:50Z | https://oeis.org/A326336/b326336.txt | 200 | c1111d16bc01d67edf407e7d6725b23dac3b3581d6838cbb16fe8fec5741e0c0 |
| 2026-11-03T20:40:50Z | https://oeis.org/history?seq=A326336 | 200 | 357c0ac6263034263da6be5603057e7d2a7aed10197aa7925bd25388c03d9bf0 |
| 2026-11-03T20:40:50Z | https://oeis.org/search?q=12270,70472&fmt=short | 200 | 985827398e2e57c393a052ec66f60b14c3abff48557a2eee78aa4999becee3b6 |
| 2026-11-03T20:40:50Z | https://oeis.org/search?q=70472&fmt=short | 200 | fbd0d448432833e9b4b49a4fd222d100b91bd8661ac99b086704a64201d78b7c |

Result: %I #6 Jun 28 2019, %K nonn,more, %O 0,5, DATA still ends a(10) = 12270; b-file unchanged; history newest #6
approved, no draft; "70472" 0 hits in entry text, b-file and history; value search 12270,70472 "Sorry, but the terms
do not match anything in the table."; bare search 70472 gives 1 result, A070472, as at claim time.

Response headers were not recorded for these fetches. The pages themselves are not shipped (third-party content).
