# Novelty skeptic verdict (V3R1T4S panel): stable marriage, order 14, 24992 stable matchings

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Scope: CLAIM.md and the claim folder's files (only hashed and header-checked here), plus the two extra local documents named in my instruction: an earlier run's text extraction of the Zenodo manuscript (../../2026-10-14-1426/data/zenodo_23329599/F7_MANUSCRIPT.txt) and the repository's TROPHY_CASE.md (../../../repo/TROPHY_CASE.md). All paths here are relative to the claim folder. Fetched copies are in ../panel/scratch_novelty2/.

Claim under test: instance_n14.prefs (order 14) has exactly 24992 stable matchings, strictly more than the best known 20176 for n = 14.
Object sha256 (computed): 2eeddab210507ca8fecf7cb18e88a27245dd861ab7497acfc0d023766cf76965. This equals the value stated in CLAIM.md.
This panel member checks novelty only. I did not count the stable matchings.

## Fetches
Each page got one plain curl request (User-Agent "V3R1T4S-panel/1.0 (verification agent; one honest request)"), with no retries and no cookies. I recorded `date -u` just before each request. There were no blocks or challenge pages.

1. arXiv API. This was the only arXiv request, and I made it first.
   - URL: https://export.arxiv.org/api/query?search_query=abs:%22stable%20matchings%22%20AND%20abs:%22maximum%20number%22&sortBy=submittedDate&sortOrder=descending&max_results=30
   - time 2026-10-15T03:25:47Z, HTTP 200, sha256 0e2dcfc73980000e29b6bb66e941a2bc44b6d277ce3fc8237e8f9a8390e07a03
   - value: `<opensearch:totalResults>6</opensearch:totalResults>`.
   - Only one entry is from the last 24 months (on or after 2024-10-15): 2601.14195v2, F. Glitzner and D. Manlove, "A Minimax Perspective on Almost-Stable Matchings" (published 2026-01-20, updated 2026-09-02). It matched on "the maximum number of blocking pairs". It gives no count of stable matchings for any order.
   - The other five (1910.07159, 1905.06626, 1805.09887, 1804.09156, 1711.01032) are older than 24 months.
   - No order-14 value.

2. OEIS A357271 entry (text format). This is the status source.
   - URL: https://oeis.org/search?q=id:A357271&fmt=text
   - time 2026-10-15T03:26:03Z, HTTP 200, sha256 fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143
   - revision line: `%I A357271 #23 May 26 2025 15:56:20`
   - data line: `%S A357271 1,2,3,10,16,48,71,268,330,1000,1231,6472,6720,20176,25011,195472,`
   - The offset line is `%O A357271 1,2`, so the 14th term is a(14) = 20176.
   - comment: `%C A357271 Improved lower bounds for n=7, 9, 11, 13, 15 are shown in linked Ong et al. (2025) file.`
   - The entry also says "a(6), a(8), a(10), a(12), and a(16) are also conjectured to be exact". 14 is not in that list.
   - CLAIM.md gives no sha256 for A357271.txt. The fetched bytes are identical to the claim folder's A357271.txt (same sha256, 2078 bytes).

3. OEIS A357271 instance file (Ong, Ang, Ho, Eilers, Marks, Buzi).
   - URL: https://oeis.org/A357271/a357271_1.txt
   - time 2026-10-15T03:26:14Z, HTTP 200, sha256 95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47
   - This EQUALS the sha256 stated in CLAIM.md, and the file is byte-identical to the claim folder's a357271_1.txt (11018 bytes).
   - The header lists `lb(7)=81 (previously 71)`, `lb(9)=365 (previously 330)`, `lb(11)=1690 (previously 1231)`, `lb(13)=7123 (previously 6720)` and `lb(15)=27059 (previously 25011, or 26424 shown in A371810)`.
   - It has instance blocks only for orders 7 (81 SM), 9 (365), 11 (1690), 13 (7123) and 15 (27059).
   - So it improves only n = 7, 9, 11, 13, 15. It has nothing for n = 14.

4. Related OEIS entries (text format, one request each).
   - A371810
     - URL: https://oeis.org/search?q=id:A371810&fmt=text
     - time 2026-10-15T03:26:28Z, HTTP 200, sha256 fb71c17c72ac94a4b56bc61fde7ff1faecb0c275117da713a8e4b0ea60cefa06
     - revision: `%I A371810 #15 May 17 2025 19:22:52`
     - data: `1,2,3,10,12,32,54,268,288,656,1044,4360,5472,15632,26424,...`, offset 1, so a(14) = 15632.
   - A069156
     - URL: https://oeis.org/search?q=id:A069156&fmt=text
     - time 2026-10-15T03:26:34Z, HTTP 200, sha256 a0b564cfb51317f995f0719e2cbd6feb54bc76e38239c7b2d1427240220f8a61
     - revision: `%I A069156 #6 Aug 09 2019 12:31:00`
     - data: `1,2,3,10,16,48,71,268,330,1000,1231,4360,5560,19724,25011,...`, offset 1, so a(14) = 19724.
   - A069124
     - URL: https://oeis.org/search?q=id:A069124&fmt=text
     - time 2026-10-15T03:26:40Z, HTTP 200, sha256 8506285dd93d05bdd0b8a392d8bc2b5de1177f17322334d5083049dc67ed6f2b
     - revision: `%I A069124 #38 May 17 2025 15:53:53`
     - data: `1,2,3,10,12,32,42,268,288,656,924,4360,3816,11336,13536,...`, offset 1, so a(14) = 11336.
   - Side note: a comment in A371810 points to a "verification by Dan Eilers in A069194". The matching Eilers verification comment (May 14 2025, a(7)=42) is in A069124, so this looks like a typo. I did not fetch A069194.

5. Zenodo API (one request).
   - URL: https://zenodo.org/api/records?q=%22maximum%20number%20of%20stable%20matchings%22&size=20&sort=mostrecent
   - time 2026-10-15T03:26:53Z, HTTP 200, sha256 0a667f53edafc3ecb648df249b2bf1498833f95fb7c62420c7aaa36f57244d0d
   - value: 1 hit in total. It is record 23329599 (doi 10.5281/zenodo.23329599, created 2026-10-13, version R2), "A computer-assisted proof that the maximum number of stable matchings of order seven is 85", by Jo, Myunglae. Files: F7_PUBLIC_RELEASE.zip, F7_PUBLIC_RELEASE.zip.sha256, F7_MANUSCRIPT.pdf.
   - The description states f(7)=85. It has no order-14 value and no doubling or product result.
   - Manuscript text: the earlier run's extraction, ../../2026-10-14-1426/data/zenodo_23329599/F7_MANUSCRIPT.txt, sha256 78761edae170d73cc65246ca895f86bc8efe90db87d9680952e736508e99115e. I did not check it against the deposited PDF myself.
     - It proves Theorem 1.1, f(7) = 85, and cites f(6) = 48 from the author's order-six paper.
     - "14" appears only as an equation number "(14)", in "B = (2, 4, 7, 11, 14, 18)", in "A3 ≥ 14" and in table cells.
     - There is no order-14 value. None of "doubl", "lexicograph", "product", 24992, 20176, 14450 (2·85²) or 7225 (85²) appears.
     - It does not cite Thurber, Knuth, OEIS or Ong et al.

6. GitHub open pull requests (one request).
   - URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   - time 2026-10-15T03:28:22Z, HTTP 200, sha256 fff8ee82083b3bb5c102d506a3ea59167183670e8deb79551fcc70751bddf283
   - value: 30 open PRs on a single page (no Link header). Two are stable-marriage PRs:
     - #144 "[claim] stable-marriage-max-stable-matchings: order-15 instance with 27510 stable matchings (beats 27059)"
     - #147 "[claim] stable-marriage-max-stable-matchings: order-18 instance with 530528 stable matchings (OEIS A357271 lists 456300)"
   - Both bodies state "Nothing about any other order n; one cell per package." Neither contains an order-14 value. Order-15 and order-18 results are not order-14 results.
   - Four thomson-problem PRs matched my keyword filter only on the word "rotational". They are unrelated.

## Web searches (2; I saw only titles and snippets and opened no result page)
- 2026-10-15T03:27:52Z, query "maximum number of stable matchings stable marriage new lower bound order 14 instance 2025 2026".
  - Results: asymptotic upper-bound work ("At most 4.47^n stable matchings", "At most 3.55^n stable matchings", arXiv 1711.01032), arXiv 2505.24637 "Note on the size of a stable matching", and Thurber 2002.
  - No order-14 value appeared.
- 2026-10-15T03:28:02Z, query "\"stable matchings\" \"20176\" OR \"24992\" stable marriage order 14 A357271".
  - No result mentions 20176, 24992 or A357271.

## TROPHY_CASE.md
- File: ../../../repo/TROPHY_CASE.md (local repository copy, sha256 b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412, 53 rows).
- It has no stable-marriage or stable-matching entry. Its rows are degree-diameter, constant-weight-codes, lehmer, fast-matrix-multiplication, sealed-envelopes, vnncomp-2026 and robustbench-cifar100.
- The only "stable" in the file is "stable across our CPU/MPS settings" in the RobustBench row.

## Order-14 comparison
| source | order-14 value |
|---|---|
| OEIS A357271 a(14) (status source; its linked file does not cover n = 14) | 20176 |
| OEIS A069156 a(14) | 19724 |
| OEIS A371810 a(14) | 15632 |
| OEIS A069124 a(14) | 11336 |
| arXiv (last 24 months), Zenodo deposit and manuscript, web searches, TROPHY_CASE.md, open PRs | none found |
| claim | 24992 |

24992 - 20176 = +4816. This is a strict improvement, not a tie.

## Limits
- I read only the approved OEIS text. I did not check OEIS pending edits or history.
- Values that were never published are not "known", and I did not compute any. An example is doubling the published order-7 instances with 71 or 81 stable matchings.
- This verdict is about novelty only. Checking the count 24992 itself is left to the other skeptics.

## Verdict
novelty: PASS.
- The status source is OEIS A357271 (revision #23 of May 26 2025, fetched 2026-10-15T03:26:03Z, HTTP 200). It gives a(14) = 20176, and its improvement file covers only n = 7, 9, 11, 13, 15.
- No newer source I found gives an order-14 value at or above 24992.
- So 24992 strictly beats everything known for n = 14.
pass: true
