# The record we compared against: OEIS A364417 (and A364416, the bank's status source)

Status source (bank target benzel-stones-and-bones-next-terms): https://oeis.org/A364416. Cell: https://oeis.org/A364417.

## Extracted cell
| quantity | OEIS value | this package |
|---|---|---|
| A364417(20) = T113(20,37) | absent: DATA and b-file end at a(19) = 20915277691567206 (%I A364417 #26 Apr 25 2024; "a(15)-a(19) from James Propp, Apr 25 2024"); draft page "No pending changes" | 225354012176304818 |
| A364416(20) (control, status source) | 87817595880192684, last term (%I A364416 #20 Apr 26 2024) | reproduced by benzZQ.c |

A364417 DATA as fetched (offset 3, n = 3..19): 3, 18, 142, 1266, 12030, 118650, 1198230, 12296202, 127633590,
1336133730, 14079114270, 149124688482, 1586159072814, 16929780310218, 181227223899942, 1944808008842490,
20915277691567206.

A364416 DATA as fetched (offset 3, n = 3..20): 1, 10, 84, 724, 6516, 60900, 586404, 5777916, 57952212, 589381020,
6060195316, 62863155972, 656765033268, 6902094928308, 72892778268996, 773013952508268, 8226672021670804,
87817595880192684.

The string 225354012176304818 occurs in none of the fetched pages (checked at every fetch below).

## Fetches (one plain curl GET each, no cookies, no retries)
| when (UTC) | by | URL | HTTP | bytes | sha256 of the bytes received |
|---|---|---|---|---|---|
| 2026-11-02T03:17:20Z | run scout | https://oeis.org/search?q=id:A364417&fmt=text | 200 | 1029 | 8b0c55d787cc7a9d9f25ee5f1d615cd753597d1430ab09a8a86f6db07c5537f7 |
| 2026-11-02T03:17:20Z | run scout | https://oeis.org/search?q=id:A364416&fmt=text | 200 | 1029 | c2c41c8ea6debb93043582bf6483f925683f5433a1585fa8f4383ddc1330ea4c |
| 2026-11-02T05:49:16Z | claim | https://oeis.org/search?q=id:A364417&fmt=text | 200 | 1029 | 8b0c55d787cc7a9d9f25ee5f1d615cd753597d1430ab09a8a86f6db07c5537f7 |
| 2026-11-02T05:49:16Z | claim | https://oeis.org/search?q=id:A364416&fmt=text | 200 | 1029 | c2c41c8ea6debb93043582bf6483f925683f5433a1585fa8f4383ddc1330ea4c |
| 2026-11-02T05:49:17Z | claim | https://oeis.org/A364417/b364417.txt | 200 | 265 | 0cd8e248ff06ebaa7c81a15799f6c3e295cb640730f998885756996283f0568e |
| 2026-11-02T05:49:17Z | claim | https://oeis.org/draft/A364417 | 200 | 6133 | 67cd983f39058d2e3c8b516bec45f540c53e00ba742e49205888ad3efc154946 |
| 2026-11-02T06:40:30Z | novelty skeptic (panel) | A364417 text, b-file, draft; https://oeis.org/A364416 | 200 each | | (read, not hashed: a(19) last term, b-file ends n = 19, "No pending changes") |
| 2026-11-02T07:41:24Z | honesty gate | https://oeis.org/search?q=id:A364417&fmt=text | 200 | | 8b0c55d787cc7a9d9f25ee5f1d615cd753597d1430ab09a8a86f6db07c5537f7 (unchanged); b-file ends n = 19; draft "No pending changes" |
| 2026-11-02T07:44:48Z | packaging re-check | https://oeis.org/search?q=id:A364417&fmt=text | 200 | 1029 | 8b0c55d787cc7a9d9f25ee5f1d615cd753597d1430ab09a8a86f6db07c5537f7 |
| 2026-11-02T07:44:48Z | packaging re-check | https://oeis.org/search?q=id:A364416&fmt=text | 200 | 1029 | c2c41c8ea6debb93043582bf6483f925683f5433a1585fa8f4383ddc1330ea4c |
| 2026-11-02T07:44:48Z | packaging re-check | https://oeis.org/A364417/b364417.txt | 200 | 265 | 0cd8e248ff06ebaa7c81a15799f6c3e295cb640730f998885756996283f0568e |
| 2026-11-02T07:44:48Z | packaging re-check | https://oeis.org/draft/A364417 | no response (curl status 000) | | not retried (one-GET rule); the gate's draft check 3 minutes earlier read "No pending changes" |

The text-form records and the b-file were byte-identical at every hashed fetch, from the scout (03:17Z) through
packaging (07:44Z), so the entries did not change during the run.

Selected response headers of the packaging-time fetches (all three identical apart from content type):

    HTTP/2 200
    date: Mon, 02 Nov 2026 07:44:48 GMT
    content-type: text/plain; charset=utf-8     (b-file: text/plain)
    cache-control: private, no-store            (text-form records)
    server: cloudflare

The pages are not included (third-party content). Anyone can re-fetch the URLs above.
