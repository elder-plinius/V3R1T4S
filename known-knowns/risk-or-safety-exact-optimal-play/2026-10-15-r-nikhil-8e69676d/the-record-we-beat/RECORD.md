# The record we extend: OEIS A387261 / A387262 (exact optimal-play win probabilities in "Risk or Safety")

Status source (bank entry risk-or-safety-exact-optimal-play): https://oeis.org/A387261

| what | value | fetched (UTC) | HTTP | sha256 of the fetched page |
|---|---|---|---|---|
| https://oeis.org/A387261 (numerators page) | 15 terms listed, "Table of n, a(n) for n=1..15"; keyword nonn,frac,hard; author Ruediger Jehn, Aug 24 2025; "More terms from Jinyuan Wang, Aug 29 2025"; site-wide footer "Last modified October 14 23:12 EDT 2026. Contains 400303 sequences." (the entry itself was last revised earlier: the panel's fetch of 2026-10-15T09:10:19Z recorded the HTTP header last-modified: Fri, 10 Apr 2026 08:20:21 GMT) | 2026-10-15T03:16:19Z | 200 | ee9627615472d519e2b11b6985b2ecbaa157b5663f58da45f7ba470a0fb44383 |
| https://oeis.org/A387261/b387261.txt (b-file, numerators) | exactly n = 1..15 (335 bytes) | 2026-10-15T03:16:20Z | 200 | 9685600de66fa0b6bb247b94e49220846d0ce005a4e64d97369e5cf1f38a5e66 |
| https://oeis.org/A387262 (denominators page) | 15 terms, same provenance and footer | 2026-10-15T03:16:21Z | 200 | 33e9dacb635392c25ce302a613f7e09a5f2b15424b2b754cbf2475046d1cf74f |
| https://oeis.org/A387262/b387262.txt (b-file, denominators) | exactly n = 1..15 (339 bytes) | 2026-10-15T03:16:21Z | 200 | 956875288b4c8d37d409ad971a682ce6baef8610f1fc26bf7948c7cf0407d2cc |
| https://oeis.org/A394776 (optimal strategy table) and its b-file (400 terms, points needed up to 20) | used only as a cross-check of the derived toss counts (0 mismatches) | 2026-10-15T03:16:22Z / 23Z | 200 / 200 | cc836252aafc92190c9169db1b39416008ea0d66d7c43a261051c3dfb4d49aea / c6954dcd5485e976fc8fceea604795dd00874d6bf679408f8ed42fc1a57cf252 |
| https://arxiv.org/abs/2603.01002 (Jehn, "Optimal strategy in the game Risk or Safety", v1, 1 Mar 2026) | defines the game and the equations; states the exact probabilities are in OEIS "for n up to 15" | 2026-10-15T03:16:24Z | 200 | 94f1894d081e049a9d36f4cd653f4767050316bc7b2e33bcfdb7e7680333fc0b |

Extracted cell compared against: the last published term is n = 15,
A387261(15)/A387262(15) = 14364898791782224577113184680141626682 / 27711032758513212360715995025634765625.
No term for any n >= 16 is published there. The 15 published terms (transcribed from the two b-files above, same bytes)
are in verify-it-yourself/published_terms/ and are reproduced exactly by the calibration certificates.

Fetch method: one plain GET per page with curl and the User-Agent "V3R1T4S/1.0 (research run; +https://github.com/elder-plinius/V3R1T4S)", no retries. The pages themselves are not included here.
