# Novelty skeptic verdict: stable-marriage-max-stable-matchings, order 28

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Claim under test (CLAIM.md): instance_n28.prefs has exactly 2497797760 stable matchings; bar 2000043808 = OEIS A357271 a(28).
I checked novelty only, not the count. Every fetch below was made once with curl, User-Agent "V3R1T4S-panel/1.0 (verification agent; one honest request)",
`-w '%{http_code}'`, `date -u` recorded just before it, no retries, no cookies. Every fetch returned HTTP 200. None returned a challenge page.
Saved copies are in ../panel/scratch_novelty/ (relative to the claim folder).

## Fetches (in order)

1. arXiv API (the only arXiv request, made first)
   - URL: https://export.arxiv.org/api/query?search_query=abs:%22stable%20matchings%22%20AND%20abs:%22maximum%20number%22&sortBy=submittedDate&sortOrder=descending&max_results=30
   - time 2026-10-15T08:16:49Z, HTTP 200, sha256 801d0f714ff92aacdcbdaba0ebba707cac1f216785e4ee226be1755657f5521b
   - value: totalResults 6. Only one is from the last 24 months: arXiv:2601.14195v2 (Glitzner, Manlove, "A Minimax Perspective on
     Almost-Stable Matchings", 2026-01-20, updated 2026-09-02). It is about almost-stable matchings and gives no maximum-count value at any order.
     The other five are from 2017 to 2020 (including Karlin, Oveis Gharan and Weber, arXiv:1711.01032, an asymptotic upper bound). None claims an order-28 value.

2. OEIS A357271, internal format (the status source)
   - URL: https://oeis.org/search?q=id:A357271&fmt=text
   - time 2026-10-15T08:17:00Z, HTTP 200, 2078 bytes
   - sha256 fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143. This equals the sha256 stated in CLAIM.md, and the file is byte-identical to A357271.txt.
   - revision line: `%I A357271 #23 May 26 2025 15:56:20`
   - data: 28 terms, offset 1. The 28th (last) term is a(28) = 2000043808 (`%U A357271 127885440,262860800,384418176,2000043808`).
   - comment: `%C A357271 Improved lower bounds for n=7, 9, 11, 13, 15 are shown in linked Ong et al. (2025) file.`

3. OEIS A357271 instance file (Ong et al.)
   - URL: https://oeis.org/A357271/a357271_1.txt
   - time 2026-10-15T08:17:01Z, HTTP 200, 11018 bytes
   - sha256 95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47. CLAIM.md gives no sha256 for this file. It is byte-identical to the claim's a357271_1.txt.
   - value: it improves only n = 7, 9, 11, 13, 15: "lb(7)=81 (previously 71)", "lb(9)=365 (previously 330)", "lb(11)=1690 (previously 1231)",
     "lb(13)=7123 (previously 6720)", "lb(15)=27059 (previously 25011, or 26424 shown in A371810)". It contains instances only for orders 7, 9, 11, 13 and 15, and nothing for n = 28.

4. OEIS A371810
   - URL: https://oeis.org/search?q=id:A371810&fmt=text
   - time 2026-10-15T08:17:01Z, HTTP 200, sha256 fb71c17c72ac94a4b56bc61fde7ff1faecb0c275117da713a8e4b0ea60cefa06
   - value: 25 terms, ending `...,85524160,93450240` (a(25)). There is no order-28 term. Revision `#15 May 17 2025`.

5. OEIS A069156
   - URL: https://oeis.org/search?q=id:A069156&fmt=text
   - time 2026-10-15T08:17:03Z, HTTP 200, sha256 a0b564cfb51317f995f0719e2cbd6feb54bc76e38239c7b2d1427240220f8a61
   - value: a(28) = 1233927520 (29 terms, offset 1; a(29) = 2023228320 is for order 29, which cannot bound order 28).

6. OEIS A069124
   - URL: https://oeis.org/search?q=id:A069124&fmt=text
   - time 2026-10-15T08:17:03Z, HTTP 200, sha256 8506285dd93d05bdd0b8a392d8bc2b5de1177f17322334d5083049dc67ed6f2b
   - value: a(28) = 1073479840 (the last of 28 terms, offset 1).

7. Zenodo API (one request)
   - URL: https://zenodo.org/api/records?q=%22maximum%20number%20of%20stable%20matchings%22&size=20&sort=mostrecent
   - time 2026-10-15T08:17:10Z, HTTP 200, sha256 1ab25469d3413a6feda9139f07e474e3945306312c9ab9ea1660f949a98f9b05
   - value: total 1. The record is M. Jo, "A computer-assisted proof that the maximum number of stable matchings of order seven is 85",
     preprint, 2026-10-13, doi 10.5281/zenodo.23329599 (version R2). This is the source of the order-7 seed named in CLAIM.md. Its description claims
     f(7) = 85 and does not mention order 14, order 28, doubling or products.

8. GitHub open pull requests (one request)
   - URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   - time 2026-10-15T08:17:35Z, HTTP 200, sha256 36b918244c96cc66891a679b915eb6213cb856d95d74903162cb26881cf517ea
   - value: 34 open PRs. The stable-marriage ones are #144 (order 15, 27510), #147 (order 18, 530528), #150 (order 13, 7698) and #151 (order 15, 30362).
     None is an order-28 entry, and no PR title or body mentions order 28, n = 28 or 2497797760. The order-14, 22 and 26 PRs were not among the open PRs.

9. Jo manuscript (one extra request, made to read the newest relevant paper in full)
   - URL: https://zenodo.org/records/23329599/files/F7_MANUSCRIPT.pdf?download=1
   - time 2026-10-15T08:19:56Z, HTTP 200, 0 redirects, 329376 bytes, sha256 bf9dddd87be101687567af81eeca7b468500bee9497b7d3661014dfbcc5ba4f4.
     Its md5 equals the md5 that the Zenodo API lists for this file.
   - value: it covers order 7 only (f(7) = 85, building on the author's f(6) = 48 preprint). It does not mention Irving-Leather doubling,
     Thurber, A357271, order 14 or order 28, and it states no lower bound for any order above 7.

10. OEIS full-text search (one extra request)
   - URL: https://oeis.org/search?q=%22stable+matchings%22&fmt=text
   - time 2026-10-15T08:21:56Z, HTTP 200, sha256 41f0f903c82ceddf68b59e1da43d16ef8ecd186accf508697363d85fc05fd54a
   - value: "Showing 1-10 of 49". Among these 10, the only order-28 stable-matching counts are the three above (A357271 2000043808,
     A069156 1233927520, A069124 1073479840). Terms of 2497797760 or more occur only in A344667 and A344668, which count preference profiles,
     not stable matchings. I did not page past the first 10 results.

Web searches (2): "maximum number of stable matchings lower bound order 28 n=28 stable marriage 2025 2026" and
"\"stable matchings\" Jo 2026 f(7)=85 Irving-Leather doubling lower bound f(14) f(28)". The hits were arXiv 1711.01032, 2011.00915, 2103.11458,
2601.07959 and 2502.06464, the Thurber 2002 record on core.ac.uk, a 2022 UW thesis, LIPIcs ESA 2026 paper 36 and OEIS A005154 (powers of 2 only).
No hit reported an order-28 value.

## Repository records
- TROPHY_CASE.md (read locally, 100 lines): there is no stable-marriage or stable-matching entry and no order-28 value. The only line matching "stable"
  is an unrelated RobustBench row.
- Open PRs: see fetch 8. No order-28 stable-marriage result is pending.

## Judgement
- The best known order-28 value I read from a page is 2000043808 (OEIS A357271 a(28), revision #23 of May 26 2025, whose bytes match the claim's copy).
  The other order-28 values are A069156 1233927520 and A069124 1073479840. The newer improvements (Ong et al. 2025 file, and Jo 2026 at order 7) do not reach order 28.
- None of the arXiv results (last 24 months), the Zenodo results, the Jo 2026 manuscript, the two web searches, TROPHY_CASE.md or the open PRs contains an order-28 value of
  2497797760 or more. The exact number 2497797760 appears in no fetched source, so this is not a tie.
- 2497797760 > 2000043808 strictly, a margin of +497753952 (factor 1.2489). It is novel as an order-28 value. The construction (Irving-Leather doubling of a
  2026 order-7 seed) is classical, which is irrelevant here. Whether the count is correct is for the other skeptics.

novelty: NEW RECORD (strictly above every published order-28 value found)
pass: true
