# Novelty skeptic verdict: order-22 stable marriage instance with 12277568 stable matchings

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

- Role: NOVELTY skeptic. The question is whether 12277568 strictly beats every published order-22 value. The count itself is not re-verified here, so this verdict assumes it is correct.
- Read: CLAIM.md, REPRODUCE.md, A357271.txt, a357271_1.txt and the first lines of instance_n22.prefs. Nothing else in the run folder was opened.
- Object hash: `shasum -a 256 instance_n22.prefs` gives 213b4ac73bfb4218a4295514410d0d53b6a87f48e8f1462d61382579efdd5b37. This equals the object sha256 in CLAIM.md.
- Fetch method: curl with User-Agent "V3R1T4S-panel/1.0 (verification agent; one honest request)". Each URL got one plain request with no redirect following, no cookies and no retries. Every time below is `date -u`, recorded just before the request.

## 1. Status source: OEIS A357271 entry (data line)
- URL: https://oeis.org/search?q=id:A357271&fmt=text
- Time and response: 2026-10-14T22:22:35Z. The server's Date header was Wed, 14 Oct 2026 22:22:36 GMT. HTTP 200, 2078 bytes. This was a real entry page, not a challenge page.
- Revision line: `%I A357271 #23 May 26 2025 15:56:20`
- Data line, quoted:
  `%S A357271 1,2,3,10,16,48,71,268,330,1000,1231,6472,6720,20176,25011,195472,`
  `%T A357271 200832,456300,637336,3419680,3506880,11221136,15481956,126112960,`
  `%U A357271 127885440,262860800,384418176,2000043808`
- 22nd term: the offset is `%O A357271 1,2`, so the 22nd term is **a(22) = 11221136**. A script read terms 20 to 24 as 3419680, 3506880, 11221136, 15481956, 126112960. This matches the claim's a(22) = 11221136.
- "Improved lower bounds" comment, quoted: `%C A357271 Improved lower bounds for n=7, 9, 11, 13, 15 are shown in linked Ong et al. (2025) file.`
- sha256 of the fetched page: fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143. This **equals** the value stated in CLAIM.md, and the page is byte-identical to A357271.txt.
- Saved as ../panel/scratch_novelty2/f1_A357271/page.txt.

## 2. Status source: instance file (Ong et al. 2025)
- URL: https://oeis.org/A357271/a357271_1.txt
- Time and response: 2026-10-14T22:22:49Z. Server Date: Wed, 14 Oct 2026 22:22:50 GMT. Last-Modified: Fri, 16 May 2025 17:50:14 GMT. HTTP 200, 11018 bytes.
- Orders it improves, quoted:
  `lb(7)=81 (previously 71)`
  `lb(9)=365 (previously 330)`
  `lb(11)=1690 (previously 1231)`
  `lb(13)=7123 (previously 6720)`
  `lb(15)=27059 (previously 25011, or 26424 shown in A371810)`
- Instances in the file are for n = 7, 9, 11, 13 and 15 only. No line of the file contains "22", so it gives no order-22 instance or value. This confirms the claim that the file improves only n = 7, 9, 11, 13, 15.
- sha256: 95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47. CLAIM.md states no hash for this file. The value equals the one listed in REPRODUCE.md, and the file is byte-identical to a357271_1.txt.
- Saved as ../panel/scratch_novelty2/f2_a357271_1/file.txt.

## 3. Related OEIS entries (order-22 values)
All three have offset 1.

| entry | URL | UTC (before request) | HTTP | revision line | a(22) | sha256 of page |
|---|---|---|---|---|---|---|
| A371810 | https://oeis.org/search?q=id:A371810&fmt=text | 2026-10-14T22:23:02Z | 200 | #15 May 17 2025 19:22:52 | 8146112 | fb71c17c72ac94a4b56bc61fde7ff1faecb0c275117da713a8e4b0ea60cefa06 |
| A069156 | https://oeis.org/search?q=id:A069156&fmt=text | 2026-10-14T22:23:03Z | 200 | #6 Aug 09 2019 12:31:00 | 11221136 | a0b564cfb51317f995f0719e2cbd6feb54bc76e38239c7b2d1427240220f8a61 |
| A069124 | https://oeis.org/search?q=id:A069124&fmt=text | 2026-10-14T22:23:03Z | 200 | #38 May 17 2025 15:53:53 | 6994784 | 8506285dd93d05bdd0b8a392d8bc2b5de1177f17322334d5083049dc67ed6f2b |

- Every order-22 value here is below 12277568. The largest is 11221136, which is the same as the bar.
- CLAIM.md states no hashes for these pages.
- Saved under ../panel/scratch_novelty2/f3_*/page.txt.

Two extra OEIS checks, one request each:
- **Keyword search.** URL: https://oeis.org/search?q=%22stable+matchings%22&fmt=text. Time 2026-10-14T22:23:48Z, HTTP 200, sha256 41f0f903c82ceddf68b59e1da43d16ef8ecd186accf508697363d85fc05fd54a. The page says "Showing 1-10 of 49", and only that first page was read.
  - Entries with an order-22 term: A357271 (11221136), A069156 (11221136) and A069124 (6994784).
  - A357269 (exact maximum) has 5 terms, `1,2,3,10,16`. A351413 (Latin stable marriage problem) has 7 terms.
  - Nothing exceeds 11221136 at n = 22.
- **Search for the claimed value.** URL: https://oeis.org/search?q=12277568&fmt=text. Time 2026-10-14T22:25:41Z, HTTP 200, sha256 b47f9127fe3ba4f548a1d57cba32c846274c8df1b65ac505b7a369b6d31a47e2.
  - The page says "Showing 1-2 of 2": A221852 and A221850. Both count occupancy arrays and are unrelated to stable matchings.
  - So the claimed value is not already published as a stable-matching count on OEIS, and this is not a tie with an existing OEIS value.

## 4. Literature, last 24 months (2024-10 to 2026-10)
- **arXiv API** (the single arXiv request).
  - URL: https://export.arxiv.org/api/query?search_query=abs:%22stable%20matchings%22%20AND%20abs:%22maximum%20number%22&sortBy=submittedDate&sortOrder=descending&max_results=30
  - Time 2026-10-14T22:23:43Z, HTTP 200, sha256 c623b4c5f6704271121b96fab8e6f74fc0975e59308d30774e2584b145e36905. totalResults: 6.
  - Only one result is within 24 months: 2601.14195, "A Minimax Perspective on Almost-Stable Matchings" (2026-01-20). It is not about record counts.
  - The other five are from 2017 to 2019, including 1711.01032 (Karlin, Oveis Gharan and Weber, upper bound).
  - None of the six gives an order-22 value.
- **Zenodo API.**
  - URL: https://zenodo.org/api/records?q=%22maximum%20number%20of%20stable%20matchings%22&size=20&sort=mostrecent
  - Time 2026-10-14T22:23:44Z, HTTP 200, sha256 0a667f53edafc3ecb648df249b2bf1498833f95fb7c62420c7aaa36f57244d0d. Total: 1.
  - The one record is 10.5281/zenodo.23329599: M. Jo, "A computer-assisted proof that the maximum number of stable matchings of order seven is 85" (2026-10-13).
  - It covers order 7 only. It is newer than the instance file's lb(7)=81, but the record description gives no order-22 value. The manuscript PDF was not downloaded.
- **Web search 1** (search tool, no HTTP code). Time 2026-10-14T22:24:41Z. Query: "maximum number of stable matchings lower bound new record instance order 22 stable marriage 2025 2026".
  - Results: arXiv 1711.01032, arXiv 2011.00915 (Palmer and Palvolgyi, 3.55^n), a University of Washington thesis on counting stable matchings, and the Kyoto repository.
  - No 2025 or 2026 order-22 value.
- **Web search 2** (search tool, no HTTP code). Time 2026-10-14T22:24:51Z. Query: '"stable matchings" A357271 OR "Improved Hill Climbing for the Stable Marriage Problem" lower bounds composition n=22'.
  - Results: arXiv 2201.00645 ("Sequences of the Stable Matching Problem"), a JIS Khovanova paper, OEIS A005154, A344671 and A343698, arXiv 2406.10319 and EGRES TR 02-08.
  - No order-22 value.
- **Not opened:** the Ong et al. IFoRE 2024 poster on JSTOR. Its OEIS-hosted companion file (section 2) lists only n = 7, 9, 11, 13, 15.

## 5. Repository
- **TROPHY_CASE.md** (local copy at ../../../repo/TROPHY_CASE.md): 100 lines, sha256 b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412.
  - It has no stable-marriage or stable-matching entry.
  - The only grep hits are unrelated words: "stable across our CPU/MPS settings" and "spread-matching surgery".
- **Open pull requests.**
  - URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
  - Time 2026-10-14T22:23:45Z, HTTP 200, 28 open PRs, sha256 b6d0ce7be7190977ea5286023d7d713488d929672db085cb47516aabf2e7d1d3.
  - One stable-marriage entry: #144, "[claim] stable-marriage-max-stable-matchings: order-15 instance with 27510 stable matchings (beats 27059)", created 2026-10-14T17:31:38Z. Its body says "Nothing about any other order n; one cell per package."
  - That is an order-15 result, not an order-22 one. No open PR gives any order-22 value.

## 6. Decision
- **Best published order-22 value found:** 11221136. It is A357271 a(22), from Thurber 2002 Appendix C, and A069156 has the same value. The other order-22 values found are 8146112 (A371810) and 6994784 (A069124).
- **Status source:** it shows a(22) = 11221136. Its only newer improvements are at n = 7, 9, 11, 13 and 15.
- **Newer work:** nothing newer gives an order-22 value. Zenodo 2026-10-13 is about order 7, and PR #144 is about order 15.
- **Comparison:** the claimed 12277568 is larger than 11221136 by 1056432 (+9.415 %). That is a strict improvement, not a tie. The value 12277568 does not appear in any OEIS stable-matching sequence.
- **Caveats:**
  - (a) The bar is stale. The published 2025 order-11 block (1690) makes a larger order-22 value derivable by the classical Irving-Leather doubling. As the panel brief says, a classical construction does not affect novelty; only a published larger or equal order-22 value would.
  - (b) Search coverage is limited: one narrow arXiv query, one Zenodo query, two web searches and only the first page of the OEIS keyword search. The JSTOR poster and the Zenodo PDF were not opened.
  - (c) Whether the count is correct is outside this skeptic's remit.

novelty: NEW RECORD for n = 22 (12277568 > 11221136, the best published order-22 value found), provided the count is correct.
pass: true
