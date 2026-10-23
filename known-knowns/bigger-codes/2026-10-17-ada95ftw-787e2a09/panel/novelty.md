# Novelty verdict: A(31,10,7) <= 106

context: subagent (fresh executor, saw only claim/A31_10_7/)

novelty: CONFIRMED. 106 is strictly below the live printed upper bound of 109, and I found no published or pending bound at or below 106.

## 1. Live status source (one plain curl request, no retries)
- URL: https://aeb.win.tue.nl/codes/Andw.html
- Fetch time (UTC, `date -u`): 2026-10-17T08:40:43Z. Result: HTTP 200, 127383 bytes.
- sha256 of the live page: 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8. This is byte-identical to claim/A31_10_7/table_snapshot/Andw.html and matches the hash in claim/A31_10_7/table_record.md and REPRODUCE.md.
- Section "Bounds on A(n,10,w)", row n=31, column w=7: printed `62<sup>c</sup>-109`, so lower bound 62 and upper bound **109**. The upper bound carries no source mark. The page says "For n > 28 unmarked upper bounds are from the Johnson bound." The secondary table "Values of A(n,10,7)" also prints 31 -> `62c-109`.
- Mirror cell A(31,10,24): the table prints only w <= 16 for n = 31 (columns w=6..16), so there is no separate printed cell for w=24. By complementation, A(31,10,24) = A(31,10,7), so its live bound is the same 62-109. No mirror cell shows a smaller bound.
- Input cell A(24,10,7): row n=24, column w=7 is printed as the single value `24<sup>c</sup>` (raw HTML `<a href="cwc/d10/i24.7">24</a><sup>c</sup>`), with no range. A single value means the bound is exact. The page uses the same convention elsewhere in the d=10 section: A(21,10,8) is printed `21c`, and the note there says "equality follows from [AVZ] (26)".
- I checked this input independently in Agrell-Vardy-Zeger 2000 (IEEE TIT 46, 2373-2395). The PDF link on Brouwer's page (code.ucsd.edu) timed out (connection failed after 133 s) and I did not retry it. I fetched the Chalmers copy once instead, https://publications.lib.chalmers.se/records/fulltext/local_14986.pdf (2026-10-17T08:44:56Z, HTTP 200). Its Example 2 says: "Take (n,2δ,w) = (24,10,7). Corollary 5 gives b = 1/24 and A(24,10,7) <= 24 ... Since a lower bound of 24 is known [17], we conclude that this bound is in fact tight." So the caveat in CLAIM.md is resolved: A(24,10,7) <= 24 is a proven, published bound.

## 2. Do the table's own current neighbours already give <= 106? No.
- First Johnson part: floor(31/7 * A(30,10,6)). A(30,10,6) is printed `25` (row 30) and `25s` (Values of A(n,10,6)), so the bound is floor(110.71) = 110.
- Second Johnson part: floor(31/24 * A(30,10,7)). A(30,10,7) is printed `48s-85`, so with upper bound 85 the bound is floor(109.79) = 109. This is the printed value.
- Pure Delsarte LP for (31,10,7) (my own exact vertex enumeration, lpcheck.py in this folder): 775/7 = 110.71. So the plain LP does not beat 109 either.
- Delsarte plus a_7 <= A(24,10,7) = 24 gives exactly 2015/19 = 106.05, matching the certificate value in claim/A31_10_7/cert_A31_10_7.json. With a_7 <= 25 it gives 108.77, and with a_7 <= 26 it gives 110.71, matching the sensitivity note in CLAIM.md.
- As a side check I ran `python3 verify.py cert_A31_10_7.json` in claim/A31_10_7/. It printed the self-test OK line, all three column sums equal to 1, and "VERIFIED bound 106".

## 3. Literature (each URL fetched once)
- Polak 2018, arXiv:1703.05171 (https://arxiv.org/pdf/1703.05171, HTTP 200, fetched about 2026-10-17T08:41Z). This is the concluding-remarks table "improved upper bounds for n in the range 29 <= n <= 32 and d >= 10". I checked it line by line. Its d=10 rows are only (31,10,8) 322, (32,10,8) 402, (29..32,10,9..16). **There is no n=31, d=10, w=7 entry**, and no w=7 row at all for d=10. Polak says his A3 bound "is in almost all cases equal to the Schrijver bound".
- Kim-Toan 2012, arXiv:1212.3467 (HTTP 200). Table II (new bounds on A(n,d,w)) has d=10 entries only for n = 23..28. There is nothing for n = 31.
- Kang-Kim-Toan 2011, arXiv:1108.5104 (HTTP 200). There is no n=31, d=10 entry.
- Schrijver 2005: the cwi.nl PDF linked from the page timed out (60 s) and I did not retry. According to the live page, Schrijver's sharper bounds apply to the n <= 28 tables. Polak's 29 <= n <= 32 SDP table, which matches Schrijver in almost all cases, has no improvement for this cell.
- Agrell-Vardy-Zeger 2000 (Chalmers copy, above): its tables cover n <= 28. It supplies only the input bound A(24,10,7) <= 24.
- Echols, arXiv:2608.13906 (HTTP 200): a lower-bound paper (seeded tabu search, 124 new constructions). It has no upper bounds and does not mention A(31,10,7).
- Lysenstoen, arXiv:2607.19550 (HTTP 200): a lower-bound paper. It mentions upper bounds only as values quoted from the live table, and nothing for (31,10,7).
- Newer: arXiv:2609.35051 (Yang et al., Sept 2026, cited on the live page; WebFetch of the abs page) is about kissing-number constructions. It contains only lower bounds and no constant-weight upper bounds.
- Two web searches ("A(31,10,7) constant weight code upper bound 2026"; "arXiv 2026 new upper bounds binary constant-weight codes ... n=31 d=10") found no paper that gives an upper bound for A(31,10,7) below 109.
- An arXiv API listing query (export.arxiv.org) timed out after 60 s. I did not retry it, so arXiv recency coverage rests on the two web searches and the live page's own references list. That list cites every 2026 source (E, L, Bo, Dz, Pl, San, YZW, ...) and none of them gives an upper bound for this cell.

## 4. Repository https://github.com/elder-plinius/V3R1T4S (read-only, one request each, 2026-10-17T08:43:04Z)
- TROPHY_CASE.md (raw.githubusercontent.com, HTTP 200, 100 lines). It lists 35 constant-weight rows: 30 codes plus 5 Delsarte LP bounds, for A(31,12,10), A(31,12,11), A(32,12,10), A(32,12,15) and A(32,12,16). There is **no A(31,10,7) or A(31,10,24) entry**.
- Open PRs (api.github.com pulls?state=open&per_page=100, HTTP 200): 93 open PRs (#9..#332), so the full list fit on one page. A regex scan of all titles and bodies for constant-weight, Andw, A(n,10,..), 31,10,7 and 31,10,24 found **no open PR about any constant-weight cell**, so nothing claims A(31,10,7).

## Conclusion
- Live printed upper bound: 109 (Johnson), for both A(31,10,7) and its mirror A(31,10,24). Claimed bound: 106. That is strictly below by 3, so this is not a tie.
- No neighbour-derived Johnson bound, no published LP/SDP table (AVZ, KKT, KT, Polak), no 2026 paper, no trophy-case entry and no open PR gives a value <= 106 for this cell.
- The one external input, A(24,10,7) <= 24, is a proven published bound (AVZ 2000, Example 2) and is printed as an exact value in the live table.
- Limits: the Schrijver 2005 PDF and the arXiv API listing could not be read because both timed out and I did not retry. Polak's 29 <= n <= 32 table and the live page's reference list cover that gap.

pass: true
