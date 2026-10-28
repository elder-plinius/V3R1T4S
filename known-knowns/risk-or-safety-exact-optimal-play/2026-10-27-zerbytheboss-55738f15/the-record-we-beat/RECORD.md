# The record we extend: OEIS A387261 / A387262 (exact optimal-play win probabilities in "Risk or Safety")

Status source (bank entry risk-or-safety-exact-optimal-play): https://oeis.org/A387261

| what | value | fetched (UTC) | HTTP | sha256 of the fetched page |
|---|---|---|---|---|
| https://oeis.org/A387261 (numerators page) | 15 terms listed, "Table of n, a(n) for n=1..15"; keyword nonn,frac,hard; author Ruediger Jehn, Aug 24 2025; "More terms from Jinyuan Wang, Aug 29 2025" | 2026-10-28T00:36:28Z | 200 | 125834621bd2a3df06eb2406f93ade8ce74bde69569e8daf05501607d445c852 |
| https://oeis.org/A387261/b387261.txt (b-file, numerators) | exactly n = 1..15 (335 bytes) | 2026-10-28T00:36:29Z | 200 | 9685600de66fa0b6bb247b94e49220846d0ce005a4e64d97369e5cf1f38a5e66 |
| https://oeis.org/A387262/b387262.txt (b-file, denominators) | exactly n = 1..15 (339 bytes) | 2026-10-28T00:36:30Z | 200 | 956875288b4c8d37d409ad971a682ce6baef8610f1fc26bf7948c7cf0407d2cc |
| https://oeis.org/A394776/b394776.txt (b-file, strategy table) | 400 terms (points needed up to 20); used as strategy cross-check | 2026-10-28T00:36:31Z | 200 | c6954dcd5485e976fc8fceea604795dd00874d6bf679408f8ed42fc1a57cf252 |
| repository known-knowns (2026-10-15-r-nikhil-8e69676d) | exact terms and certificates for n = 16..30 | 2026-10-28T00:36:32Z | 200 | 8e69676d99d3dc6726098a75c1167f2820f2c3e9c2bd0b82ed98e2dbb8446f24 |

Extracted cell compared against:
The published OEIS table lists terms only up to n = 15:
A387261(15)/A387262(15) = 14364898791782224577113184680141626682 / 27711032758513212360715995025634765625.
The repository known-knowns package extended this through n = 30.
No term for any n >= 31 was previously published or certified.
This run establishes the exact optimal-play values and complete Bellman certificates for every n from 31 through 45.
