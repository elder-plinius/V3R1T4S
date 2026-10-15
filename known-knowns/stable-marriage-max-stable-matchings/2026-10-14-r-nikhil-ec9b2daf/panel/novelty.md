# Novelty skeptic: stable-marriage-max-stable-matchings, n = 13, claimed 7698

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Instruction: fetch the status source once, honestly; search the last 24 months of literature (2024-10-15 to 2026-10-15), the repository's TROPHY_CASE.md and its open pull requests; pass only if 7698 strictly beats every known order-13 value (a tie is not a record).

Object judged: instance_n13.prefs, sha256 ec9b2daf4bafd04fb7118987cc88ae424471d1bb49f6e3632fb0367c9e3acc69. This equals the object sha256 stated in CLAIM.md.
Scope: novelty only. This skeptic did not recount 7698; the verdict assumes the count is correct and judges only the comparison.

Fetch method: curl, one plain request per URL, User-Agent "V3R1T4S-panel/1.0 (verification agent; one honest request)", `-w '%{http_code}'`, no cookies, no retries, `date -u` recorded immediately before each request. The arXiv API request was the first network request and the only arXiv request. No request returned 401/403/429/503 or a challenge page. Saved copies are in ../panel/scratch_novelty/ (relative to the claim folder).

## Fetches (UTC time is the time recorded just before the request)

1. arXiv API, the only arXiv request, made first
   - URL: https://export.arxiv.org/api/query?search_query=abs:%22stable%20matchings%22%20AND%20abs:%22maximum%20number%22&sortBy=submittedDate&sortOrder=descending&max_results=30
   - time: 2026-10-15T03:33:07Z; HTTP 200; sha256 0e2dcfc73980000e29b6bb66e941a2bc44b6d277ce3fc8237e8f9a8390e07a03
   - value: `totalResults` 6. Only one entry falls in the last 24 months: arXiv:2601.14195 (v1 2026-01-20, v2 2026-09-02), "A Minimax Perspective on Almost-Stable Matchings". It is about minimising blocking pairs, does not count stable matchings and gives no order-13 value. The other five are from 2017-2019: 1711.01032 (asymptotic upper bound f(n) <= c^n, no order-13 value), plus 1910.07159, 1905.06626, 1805.09887 and 1804.09156, which are unrelated. **No order-13 value found.**
   - limitation: the query was fixed by the protocol. It only finds abstracts that contain both "stable matchings" and "maximum number".

2. Status source: OEIS A357271 instance file (Ong, Ang, Ho, Eilers, Marks, Buzi)
   - URL: https://oeis.org/A357271/a357271_1.txt
   - time: 2026-10-15T03:33:20Z; HTTP 200; response header `last-modified: Fri, 16 May 2025 17:50:14 GMT`; 11018 bytes
   - quoted lb(13) line: `lb(13)=7123 (previously 6720)`
   - order-13 block header in the file: `/*  order 13 example with 7123 SM`
   - sha256 95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47. This is **EQUAL** to the sha256 that CLAIM.md states for a357271_1.txt (claimant fetch 2026-10-14T15:18:18Z). The fetched copy is also byte-identical to the claim folder's a357271_1.txt, so the file has not changed since the claimant fetched it.

3. Status source: OEIS A357271 entry (internal text format)
   - URL: https://oeis.org/search?q=id:A357271&fmt=text
   - time: 2026-10-15T03:33:32Z; HTTP 200
   - data line (offset `%O A357271 1,2`): `%S A357271 1,2,3,10,16,48,71,268,330,1000,1231,6472,6720,20176,25011,195472,`. The 13th term is a(13) = **6720** (Thurber 2002 compositions).
   - revision line: `%I A357271 #23 May 26 2025 15:56:20`
   - comment: `%C A357271 Improved lower bounds for n=7, 9, 11, 13, 15 are shown in linked Ong et al. (2025) file.`
   - sha256 fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143. CLAIM.md states no sha256 for this file, but the fetched copy is byte-identical to the claim folder's A357271.txt.

4. Related OEIS entries (one request each)
   - URL: https://oeis.org/search?q=id:A371810&fmt=text. Time 2026-10-15T03:33:43Z; HTTP 200; `%I A371810 #15 May 17 2025 19:22:52`. Data (offset 1): `%S A371810 1,2,3,10,12,32,54,268,288,656,1044,4360,5472,15632,26424,195472,`, so a(13) = **5472**. sha256 fb71c17c72ac94a4b56bc61fde7ff1faecb0c275117da713a8e4b0ea60cefa06 (CLAIM.md gives no hash to compare).
   - URL: https://oeis.org/search?q=id:A069156&fmt=text. Time 2026-10-15T03:33:43Z; HTTP 200; `%I A069156 #6 Aug 09 2019 12:31:00`. Data (offset 1): `%S A069156 1,2,3,10,16,48,71,268,330,1000,1231,4360,5560,19724,25011,195472,`, so a(13) = **5560**. sha256 a0b564cfb51317f995f0719e2cbd6feb54bc76e38239c7b2d1427240220f8a61 (CLAIM.md gives no hash to compare).

5. Zenodo API (one request)
   - URL: https://zenodo.org/api/records?q=%22maximum%20number%20of%20stable%20matchings%22&size=20&sort=mostrecent
   - time: 2026-10-15T03:33:56Z; HTTP 200; sha256 0a667f53edafc3ecb648df249b2bf1498833f95fb7c62420c7aaa36f57244d0d
   - value: hits.total 1. The hit is doi 10.5281/zenodo.23329599 (publication_date 2026-10-13), "A computer-assisted proof that the maximum number of stable matchings of order seven is 85". It is an order-7 result (f(7)=85). Its description contains no order-13 value. **No order-13 value found.**

6. Open pull requests of the public repository (one request)
   - URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   - time: 2026-10-15T03:33:58Z; HTTP 200; sha256 7521bc02d2793301aaaa0d3209fdab11e79b0dd14e61892abefb07f02323ecc9
   - value: 30 open PRs on a single page (no `Link` header, so the list is complete). Two are stable-marriage PRs, both from this same workspace and both expected:
     - #144 "[claim] stable-marriage-max-stable-matchings: order-15 instance with 27510 stable matchings (beats 27059)"
     - #147 "[claim] stable-marriage-max-stable-matchings: order-18 instance with 530528 stable matchings (OEIS A357271 lists 456300)"
   - Neither PR states an order-13 value. Both mention n = 13 only in the list "n = 7, 9, 11, 13, 15" of orders covered by the Ong et al. file. #147 also says its cross-check reproduced "the published n = 7, 9, 11, 13, 15 values". No open PR title or body contains "7123" or "7698". **No order-13 value found.**

## Web searches (2; judged from the result listings only, no result page was opened)
- `"maximum number of stable matchings" order 13 new lower bound 2026`. Results: arXiv 2505.24637 "Note on the size of a stable matching" (about the size of a stable matching, not the count), arXiv 1711.01032 (upper bound c^n), a University of Washington thesis "Pairing Things Off: Counting Stable Matchings, Finding Your Ride, and Designing Tournaments", talks and papers on "at most 4.47^n" and "at most 3.55^n" stable matchings (upper bounds), and a DIMACS seminar page. None shows an order-13 value.
- `stable marriage instance "7123" OR "7698" stable matchings n=13 A357271`. Results: physics reviews and statistics papers (2103.11458, cond-mat/0007321, cond-mat/0509221), Thurber 2002 (core.ac.uk), math/0411028, MaRDI Q1821125, 1707.01540 and seminar pages. No result shows 7123 or 7698 in a stable-marriage context or any order-13 value.

## TROPHY_CASE.md
- Read from the local checkout (../../../repo/TROPHY_CASE.md relative to the claim folder; 100 lines; sha256 b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412).
- It has no stable-marriage or stable-matching entry and contains neither 7123 nor 7698. The only hits for "stable" and "matching" are unrelated: a RobustBench row ("stable across our CPU/MPS settings") and a degree-diameter row ("spread-matching surgery").

## Decision for order 13

| source | order-13 value | 7698 compared |
|---|---|---|
| a357271_1.txt lb(13), Ong et al. (2025): the best known value, per the A357271 comment | 7123 | +575 (+8.07 %), strictly greater |
| A357271 data line a(13) (Thurber 2002 compositions) | 6720 | strictly greater |
| A069156 a(13) | 5560 | strictly greater |
| A371810 a(13) | 5472 | strictly greater |
| arXiv (last 24 months), Zenodo, open PRs, TROPHY_CASE.md, web searches | none found | n/a |

The status source shows that the best known order-13 value is 7123, which is below 7698. Nothing newer that I found contradicts this, and 7698 is not a tie.

Caveats:
- There is newer work for order 7 (Zenodo, 2026-10-13: f(7)=85, above lb(7)=81 in the OEIS file). So the OEIS file is not the latest result for every order. No source found gives an order-13 value derived from that work, and this skeptic computed none.
- Novelty only: if the count 7698 turns out to be wrong, this verdict does not stand.
- 7698 would be a new lower bound for f(13), not a proof of the maximum.

novelty: RECORD (7698 strictly beats the best known order-13 value 7123)
pass: true
