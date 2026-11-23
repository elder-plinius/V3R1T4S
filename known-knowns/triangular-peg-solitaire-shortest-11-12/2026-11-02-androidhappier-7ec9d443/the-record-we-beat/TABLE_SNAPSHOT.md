# The record we compared against: OEIS A127500 and G. I. Bell's triangular peg solitaire pages

Status source (bank target triangular-peg-solitaire-shortest-11-12): https://oeis.org/A127500, and
https://www.gibell.net/pegsolitaire/LargeTriangular/index.html.

## Extracted cell
| source | quantity | published value | this package |
|---|---|---|---|
| OEIS A127500 (%I A127500 #12 Sep 07 2015; DATA 5,9,9,12,13,16,18 for n = 4..10; keywords hard,more,nonn) | a(12) | comment: "gives the bounds 19<=a(11)<=28, 21<=a(12)<=29"; draft page: no pending changes | a(12) <= 25 |
| G. I. Bell, Large Triangular Boards ("Last modified March 4th, 2007") | S(12) | 21 <= S(12) <= 29; shortest known Triangle(12) solution: 29 moves, e11 to a3 | 25 moves, a3 to j12 |
| G. I. Bell, Triangular peg solitaire main page ("Last Modified April 27th, 2025") | Triangle(12) | nothing below 29 | |

## Fetches (one plain curl GET each, no cookies, no retries)
| when (UTC) | by | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|---|
| 2026-11-02T17:31:50Z | run scout | https://oeis.org/search?q=id:A127500&fmt=text | 200 | f7bc24078f379a90859cee0fc3a99352fb1242393d54947a79fe289b228e54fe |
| 2026-11-02T17:31:50Z | run scout | https://oeis.org/draft/A127500 | 200 | c7c4c2f4ed7cd6f8b3e1a44da42d664df9df127ff89f991c378142005ae58a4d |
| 2026-11-02T17:31:50Z | run scout | https://www.gibell.net/pegsolitaire/LargeTriangular/index.html | 200 | 96000bb372c61196c24eb943499f6aa83529346ee5ad1439f137e279af9fd7a6 |
| 2026-11-02T17:31:51Z | run scout | https://www.gibell.net/pegsolitaire/tindex.html | 200 | 0aa57a743f9beec483120ecbc67138641b164c5e523082d633e392c53100654d |
| 2026-11-02T18:19:57Z | novelty skeptic | https://oeis.org/A127500 (HTML page) | 200 | 50ba5e837df3e594556d8d2e6888b4f9af3c8548681737ab90c7345e140a1a6c |
| 2026-11-02T18:19:57Z | novelty skeptic | https://www.gibell.net/pegsolitaire/LargeTriangular/index.html | 200 | 96000bb372c61196c24eb943499f6aa83529346ee5ad1439f137e279af9fd7a6 |

Selected headers were not recorded. The scout fetches were made once in run 2026-11-02-1731 and copied
byte-for-byte into this run. The novelty skeptic's HTML fetch of OEIS has a different hash from the text-format
fetch (different endpoint, same content); Bell's page is byte-identical at both fetches. The pages themselves are
not shipped (third-party content).
