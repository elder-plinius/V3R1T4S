# Novelty skeptic verdict: stable-marriage-max-stable-matchings, n = 18, claimed count 530528

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Question: does 530528 strictly beat every known order-18 value? (A tie would not count as a record.)
Client for every fetch: curl, User-Agent "V3R1T4S-panel/1.0 (verification agent; one honest request)", one request per URL, no retries, no redirects followed, no cookies. `date -u` was recorded before each fetch.
Scratch copies are under ../panel/scratch_novelty2/ (relative to the claim folder).

## 1. Status source: OEIS A357271 entry (primary table)
- URL: https://oeis.org/search?q=id:A357271&fmt=text
- UTC time: 2026-10-14T22:15:52Z (server Date header 22:15:53 GMT). HTTP code: 200. No challenge page.
- Data line (quoted):
  `%S A357271 1,2,3,10,16,48,71,268,330,1000,1231,6472,6720,20176,25011,195472,`
  `%T A357271 200832,456300,637336,3419680,3506880,11221136,15481956,126112960,`
  `%U A357271 127885440,262860800,384418176,2000043808`
  The offset is `%O A357271 1,2`, so the 18th term is **a(18) = 456300**. This matches the bar in CLAIM.md.
- Revision line: `%I A357271 #23 May 26 2025 15:56:20`
- "Improved lower bounds" comment: `%C A357271 Improved lower bounds for n=7, 9, 11, 13, 15 are shown in linked Ong et al. (2025) file.`
- Saved as ../panel/scratch_novelty2/dl_oeis_entry/A357271.txt (2078 bytes).
  sha256 `fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143`. This **equals** the sha256 stated in CLAIM.md, and the file is byte-identical to A357271.txt in the claim folder.

## 2. Status source: instance file (Ong et al. 2025)
- URL: https://oeis.org/A357271/a357271_1.txt
- UTC time: 2026-10-14T22:15:53Z (server Date 22:15:54 GMT; Last-Modified Fri, 16 May 2025 17:50:14 GMT). HTTP code: 200.
- Orders improved (quoted): `lb(7)=81 (previously 71)`, `lb(9)=365 (previously 330)`, `lb(11)=1690 (previously 1231)`, `lb(13)=7123 (previously 6720)`, `lb(15)=27059 (previously 25011, or 26424 shown in A371810)`.
  The file improves **only n = 7, 9, 11, 13, 15**, as the claim says. Its example blocks are for orders 7, 9, 11, 13 and 15. It contains no n = 18 value and does not mention 456300 or 530528.
- sha256 `95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47` (11018 bytes).
  CLAIM.md does not state a sha256 for this file. The fetched copy is byte-identical to a357271_1.txt in the claim folder.
- The claimed object instance_n18.prefs has sha256 `12429e3eb7c67d315bddabe7ac71edc070cfbaae1760c67f66b8d2fa1e61b488`, which equals the "object sha256" in CLAIM.md.

## 3. Other OEIS sequences with order-18 counts (one request each)
I checked these because the instance file cites A371810 as having held a better n = 15 value than the A357271 data line.

| URL | UTC time | HTTP | value read |
|---|---|---|---|
| https://oeis.org/search?q=id:A371810&fmt=text | 2026-10-14T22:17:02Z | 200 | a(18) = **423104** (pseudo-Latin counts). Revision `#15 May 17 2025`. |
| https://oeis.org/search?q=id:A069124&fmt=text | 2026-10-14T22:17:23Z | 200 | a(18) = **423104** (Thurber Table 1, pseudo-Latin). Revision `#38 May 17 2025`. |
| https://oeis.org/search?q=id:A069194&fmt=text | 2026-10-14T22:17:23Z | 200 | Unrelated sequence: `a(n) = Sum_{d\|n} (n/d)*phi(n)/phi(d)`. It has no stable-matching data. |
| https://oeis.org/search?q=id:A357269&fmt=text | 2026-10-14T22:19:10Z | 200 | Exact maxima only: `1,2,3,10,16` (n <= 5). Nothing for n = 18. |

All of these order-18 values are below both 456300 and 530528.

## 4. Literature of the last 24 months (2024-10-15 to 2026-10-14)
- **arXiv API (the only arXiv request made):** https://export.arxiv.org/api/query?search_query=abs:%22stable%20matchings%22%20AND%20abs:%22maximum%20number%22&sortBy=submittedDate&sortOrder=descending&max_results=30
  - UTC 2026-10-14T22:17:03Z, HTTP 200, totalResults 6.
  - Only one result falls inside the window: 2601.14195 (2026-01-20), "A Minimax Perspective on Almost-Stable Matchings". It is unrelated.
  - The other five are from 2017-2019, including 1711.01032, an upper-bound paper.
  - No result claims an order-18 value.
- **Zenodo API:** https://zenodo.org/api/records?q=%22maximum%20number%20of%20stable%20matchings%22&size=20&sort=mostrecent
  - UTC 2026-10-14T22:17:04Z, HTTP 200, total 1.
  - The one hit is 10.5281/zenodo.23329599 (2026-10-13), Jo, "A computer-assisted proof that the maximum number of stable matchings of order seven is 85". It covers order 7 only.
  - No order-18 value.
- **Web searches (2, run at 2026-10-14T22:18:06Z):**
  - Queries: "maximum number of stable matchings new lower bound order 18 stable marriage instance" and "\"stable matchings\" \"lower bound\" A357271 OR \"Thurber\" improved instances 2025 2026".
  - Neither search found any order-18 construction or value.
  - Results were Thurber 2002, Karlin-Oveis Gharan-Weber (1711.01032), Palmer-Palvolgyi (2011.00915), A005154, background reviews, and a University of Washington thesis title.
  - arXiv 2609.17418 appeared ("A Quadratic Lower Bound for the Shield Number of the Stable Marriage Problem ..."). It is about a different quantity, and I did not fetch it.
  - One hit, https://digitalcommons.biola.edu/faculty-articles/640, was fetched once at 2026-10-14T22:19:08Z.
    - It returned **HTTP 301** to a generic library archives page. Under the one-request rule the redirect was not followed.
    - This is not a 401/403/429/503 or a challenge page, but its content could not be read. The search result showed no title or snippet.
    - My unconfirmed guess is Thurber's 2002 paper, since Thurber was at Biola. No order-18 value was seen from it.

## 5. Repository records
- **TROPHY_CASE.md** (the repo's local copy, read at 2026-10-14T22:17:54Z, sha256 `b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412`):
  - It has no stable-marriage or stable-matching entry.
  - The only matches for "stable" or "matching" are unrelated: a RobustBench row ("stable across our CPU/MPS settings") and a degree-diameter row ("spread-matching surgery").
- **Open pull requests:** https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
  - UTC 2026-10-14T22:17:06Z, HTTP 200, 28 open PRs.
  - Exactly one is a stable-marriage entry: #144, "[claim] stable-marriage-max-stable-matchings: order-15 instance with 27510 stable matchings (beats 27059)", created 2026-10-14T17:31:38Z.
  - It is an **order-15** result. Its body says "Nothing about any other order n" and gives no order-18 value.
  - No open PR mentions 456300, 530528, "order 18" or "n = 18".

## 6. Decision
- The status source shows the best known order-18 value is a(18) = 456300. Its instance file improves only n = 7, 9, 11, 13 and 15.
- Every other order-18 value I found is lower: A371810 and A069124 both give 423104.
- Nothing in the arXiv request, the Zenodo request, the web searches, TROPHY_CASE.md or the open PRs gives a larger order-18 value or contradicts the bar. The two newest related items are the f(7) = 85 Zenodo deposit and PR #144 at order 15.
- 530528 > 456300, a strict improvement of +74228; it is not a tie.
- The construction is classical (the Irving-Leather doubling of the published order-9 instance with 365 stable matchings). That does not affect novelty, and I found no publication of this order-18 value or of any larger one.
- This verdict covers novelty only. Whether the instance really has 530528 stable matchings is for the other skeptics.

novelty: NEW (530528 strictly exceeds the best known order-18 value 456300; no published order-18 value >= 530528 found)
pass: true
