# The record we compared against: OEIS A127500 and G. I. Bell's Large Triangular Boards page

Status source (bank target triangular-peg-solitaire-shortest-11-12): https://oeis.org/A127500; also
https://www.gibell.net/pegsolitaire/LargeTriangular/index.html.

## Extracted cell
| source | quantity | published value | this package |
|---|---|---|---|
| OEIS A127500 | a(11) | comment: "The reference calculates a(n) up to n=10 and gives the bounds 19<=a(11)<=28, 21<=a(12)<=29"; DATA 5,9,9,12,13,16,18 (n = 4..10); draft page: no pending edit | a(11) <= 22 |
| Bell, Large Triangular Boards ("Last modified March 4th, 2007") | S(11) | table row "11 \| 66 \| 18 \| \| 19≤S(11)≤28"; shortest known Triangle(11) solution: a4 to a1 in 28 moves; "it is believed that S(11) is 20, 21, or 22" | 22 moves, a2 to j11 |

## Fetches (one plain curl GET each, no cookies, no retries)
| when (UTC) | by | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|---|
| 2026-11-02T17:31:50Z | run scout | https://oeis.org/search?q=id:A127500&fmt=text | 200 | f7bc24078f379a90859cee0fc3a99352fb1242393d54947a79fe289b228e54fe |
| 2026-11-02T17:31:50Z | run scout | https://oeis.org/draft/A127500 | 200 | c7c4c2f4ed7cd6f8b3e1a44da42d664df9df127ff89f991c378142005ae58a4d |
| 2026-11-02T17:31:50Z | run scout | https://www.gibell.net/pegsolitaire/LargeTriangular/index.html | 200 | 96000bb372c61196c24eb943499f6aa83529346ee5ad1439f137e279af9fd7a6 |
| 2026-11-02T17:31:51Z | run scout | https://www.gibell.net/pegsolitaire/tindex.html | 200 | 0aa57a743f9beec483120ecbc67138641b164c5e523082d633e392c53100654d |
| 2026-11-02T18:17:50Z | novelty skeptic | https://oeis.org/A127500 (HTML form) | 200 | not recorded in full (begins 99639c2b; HTML form, so it differs from the text form) |
| 2026-11-02T18:17:51Z | novelty skeptic | https://www.gibell.net/pegsolitaire/LargeTriangular/index.html | 200 | 96000bb372c61196c24eb943499f6aa83529346ee5ad1439f137e279af9fd7a6 |
| 2026-11-02T18:18:33Z | novelty skeptic | https://oeis.org/draft/A127500 | 200 | not recorded (no pending edit mentioning a(11)) |
| 2026-11-02T18:20:55Z | packaging | https://oeis.org/search?q=id:A127500&fmt=text | 200 | f7bc24078f379a90859cee0fc3a99352fb1242393d54947a79fe289b228e54fe |
| 2026-11-02T18:20:55Z | packaging | https://www.gibell.net/pegsolitaire/LargeTriangular/index.html | 200 | 96000bb372c61196c24eb943499f6aa83529346ee5ad1439f137e279af9fd7a6 |

Selected headers at the packaging fetch: OEIS text form `content-type: text/plain; charset=utf-8`,
`content-length: 1490`, `date: Mon, 02 Nov 2026 18:20:55 GMT`; Bell page `content-type: text/html`,
`content-length: 8925`, `last-modified: Fri, 08 Jan 2021 19:10:43 GMT`, `date: Mon, 02 Nov 2026 18:20:56 GMT`.
Both packaging fetches are byte-identical to the scout's snapshots. The pages themselves are not shipped
(third-party content).
