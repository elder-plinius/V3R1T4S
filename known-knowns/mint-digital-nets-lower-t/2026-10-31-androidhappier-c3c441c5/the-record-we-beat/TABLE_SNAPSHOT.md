# The record we compared against: MinT, base 2, (m, s) = (24, 17)

Status source (bank target mint-digital-nets-lower-t): http://mint.sbg.ac.at/query.php?b=2&m=24&s=17&p=smt

## Extracted cell
| quantity (b=2, m=24, s=17) | MinT value | this package |
|---|---|---|
| Constructive and digital t | 13 | 11 |
| Digital (existence) t | 13 (from the cd/ed table; the query page shows no separate entry) | not claimed |
| Lower bound on t | 8 | 11 is at or above it |

Quoted from the query page: "(13, 24, 17)-Net over F2 — Constructive and digital: Digital (13, 24, 17)-net over F2,
using s-reduction based on digital (13, 24, 24)-net over F2, using a shift-net" and "(8, 24, 17)-Net in Base 2 —
Lower bound on t: There is no (7, 24, 17)-net in base 2".

## Fetches (one GET each, no retries, default client)
| when (UTC) | by | URL | result |
|---|---|---|---|
| 2026-10-31T14:58Z (approx.) | run scout | query.php?b=2&m=24&s=17&p=smt (above) | content returned; t=13, lower bound 8; sha256 of the saved rendering below |
| 2026-10-31T14:27Z to 14:33Z | run scout | http://mint.sbg.ac.at/table.php?b=2&col=1&p=smt&mode=cd&opt=bd&minx=1&maxx=30&miny=0&maxy=25 | content returned; cell m=24, s=17 reads "13-8" (constructive digital 13, lower bound 8) |
| 2026-10-31T14:49Z (approx.) | run scout | http://mint.sbg.ac.at/table.php?b=2&col=1&p=smt&mode=cd&opt=ed&minx=1&maxx=30&miny=0&maxy=25 | content returned; cell m=24, s=17 reads 13 (digital existence) |
| 2026-10-31T16:09Z to 16:10Z | novelty skeptic (panel) | query page (above) | HTTP OK, title "MinT - Best Known (t, 24, 17)-Nets in Base 2"; t=13, lower bound 8 |
| 2026-10-31T16:15Z (approx.) | honesty gate | query page (above) | still Constructive and digital t=13, lower bound t=8 |

## sha256 of what was fetched
The pages were read with a web-fetch tool that returns a markdown rendering of the page. It does not expose the
HTTP status code, the response headers or the raw HTML bytes, so no headers can be listed here and the hashes are of
the saved renderings, not of the raw HTML. (Plain-http requests with curl from the run machine were refused by its
local egress proxy with HTTP 500 before reaching MinT, so no raw copy exists.)

| saved rendering | sha256 |
|---|---|
| query page b=2 m=24 s=17 (14:58Z fetch) | 3b72b8111577a59e69bf9c18974f3f06902592bc26fb309797dc5b89430d6a79 |
| table b=2 cd/bd (14:27Z-14:33Z fetch) | a0ba0ef8c58d6b1221b98fcd2d412bb4f977669353af47f48bc3a6b73fa7f6be |
| table b=2 cd/ed, rows m=20..25 excerpt (14:49Z fetch) | e32c747ee1af2c6ea544a8135cc88466617e5c8fa19aaab5b45a046feff9d189 |

The pages themselves are not included (third-party content). Anyone can re-fetch the URLs above.
