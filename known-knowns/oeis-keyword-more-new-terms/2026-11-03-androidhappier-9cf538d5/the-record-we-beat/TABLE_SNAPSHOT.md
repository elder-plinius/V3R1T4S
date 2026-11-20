# The record we compared against: OEIS A325786

Status source for this cell: https://oeis.org/A325786 (bank target oeis-keyword-more-new-terms, status_source
https://oeis.org/search?q=keyword:more).

## Extracted cell
| quantity | OEIS value | this package |
|---|---|---|
| A325786(21) | absent: DATA 1,1,2,2,4,7,12,19,41,71,141,255,509,924,1882,3395,6838,12715,25233,47049 (n = 1..20, offset 1,3), %K nonn,more; b-file (synthesized from the entry) ends "20 47049"; history newest revision #6 (Susanna Cuyler, May 22 2019, approved), no pending draft; context value searches "25233,47049,93725" and "47049,93725": no match | 93725 |

## Claim-time fetches (one plain curl GET each, User-Agent naming V3R1T4S research, no cookies, no retries)
| when (UTC) | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|
| 2026-11-03T16:41:07Z | https://oeis.org/A325786 | 200 | 0838b3e1a896781ffca7d9acfebfed979a980507771659f2d96f573f27cd452a |
| 2026-11-03T16:41:08Z | https://oeis.org/A325786/b325786.txt | 200 | 377da0f78ea5b996e8dddef912b383a2a7582ec240c1234c29b2a17eb03f3ba8 |
| 2026-11-03T16:41:10Z | https://oeis.org/A325786/internal | 200 | d699c485df4867c09f40ca46018814339d246b3e152b78a49e711f2507c3aec8 |
| 2026-11-03T16:41:11Z | https://oeis.org/history?seq=A325786 | 200 | 4dd3c14977e2fcd9c380ad812ee9aece762cf5434edfbba748f4c62911261664 |
| 2026-11-03T16:41:12Z | https://oeis.org/search?q=keyword:more | 200 | 5b1566fbd2cf75c98a2c24345abf44c9b543ea4e819e5859aa1f89ad419f8cbc |
| 2026-11-03T16:45:13Z | https://oeis.org/search?q=25233,47049,93725&fmt=short | 200 | 197ec9d1a334e4f008d3f13c6caedd16ad0395ce86b299ab96674270f1cd18ae |
| 2026-11-03T16:45:15Z | https://oeis.org/search?q=93725&fmt=short | 200 | 4d6f98f33adb1835efd546d5fb91dec92cc4d20de996d84cdc56d230f3ad9e27 |

The bare search "93725" returns A332835 (an unrelated sequence that has 93725 as its own a(21)) and A093725 (A-number
string match); neither records 93725 as a term of A325786.

## Panel re-fetches (novelty and criterion skeptics, about 2026-11-03T18:08Z-18:10Z; hashes as recorded in panel/novelty.md, abbreviated there)
| URL | HTTP | result |
|---|---|---|
| https://oeis.org/A325786 and /internal | 200 | %K nonn,more; DATA ends 47049 (n = 20); "93725" 0 hits |
| https://oeis.org/A325786/b325786.txt | 200 | last line "20 47049" (sha256 377da0f7..., same as claim time) |
| https://oeis.org/history?seq=A325786 | 200 | newest #6, approved; no pending draft; "93725" 0 hits |
| https://oeis.org/search?q=25233,47049,93725 | 200 | "Sorry, but the terms do not match anything in the table." |

## Gate re-fetch (one plain curl GET each)
| when (UTC) | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|
| 2026-11-03T18:11:27Z | https://oeis.org/search?q=id:A325786&fmt=text | 200 | 23b2ca2c4e2eebb6f9af01f2b217c1e74766b5b113b421031c07db9acd4d0b3a |
| 2026-11-03T18:11:27Z | https://oeis.org/A325786/b325786.txt | 200 | 377da0f78ea5b996e8dddef912b383a2a7582ec240c1234c29b2a17eb03f3ba8 |
| 2026-11-03T18:11:27Z | https://oeis.org/history?seq=A325786 | 200 | 103297d4dc76340d1eca19017d4d174350ac2ed70fe6900585a70bc27816568a |
| 2026-11-03T18:11:27Z | https://oeis.org/search?q=47049,93725&fmt=short | 200 | 4140317dcbc069d115d8372ae6b02cff0ab287ef60fb3b57da74abe29de6f88d |

Result: %K nonn,more, %O 1,3, DATA still ends a(20) = 47049; b-file unchanged; history newest #6 approved, no draft;
"93725" 0 hits in entry text, b-file and history; value search 47049,93725 "Sorry, but the terms do not match
anything in the table." (The history page hash differs between fetches; the page is rendered dynamically, and its
revision list is unchanged.)

Response headers were not recorded for these fetches. The pages themselves are not shipped (third-party content).
