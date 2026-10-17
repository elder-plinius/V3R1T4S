# Novelty skeptic report, claim q180-2: no [[180,2,59]] qubit stabilizer code (upper bound at most 58)
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: CONFIRMED against everything found. The claimed bound 58 is strictly below the live cell (61), the live-table propagation closure (60), the closure including all 47 pending claim PRs (59, via PR 278 on [[183,1]]), the Rains closed form (61) and TROPHY_CASE.md (no qubit row); the literature check used fallback sources because my arXiv requests were all lost to a redirect, see section 4.

## 1. Status page, fetched once, no retry
- URL: https://codetables.de/QECC.php?q=4&n=180&k=2
- Command: curl -s -A "V3R1T4S-verexxi" -o work/cell.html -w '%{http_code}' on that URL (one request).
- Time (local clock, date -u): start 2026-10-17T05:59:11Z, end 2026-10-17T05:59:12Z. curl exit code 0. HTTP status 200. Size 1523 bytes.
- sha256 of work/cell.html: dbf9ce06dfaacb2c3998b0301e0d23f529bc9ab66be3859a613708df7d15f7df
- Values on the page: heading Bounds on [[180,2]]; lower bound 35; upper bound 61. Footer says Last change: 10.06.2024. The page notes say the upper bounds for n above 100 are weak and not necessarily monotone in k.
- The sha256 is identical to claim/data/QECC_q4_n180_k2_claimtime.html (captured 2026-10-17T05:34:27Z according to CLAIM.md), so the cell page is byte-identical to what the claimant saw.
- claim/data/qubit_table_full_n1-256.html has the sha256 stated in CLAIM.md (26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6) and its (180,2) entry parses to [35, 61], consistent with the live page. I did not re-fetch the complete table (one status fetch only).

## 2. Pull requests
HTML search pages (plain requests, User-Agent V3R1T4S-verexxi), URL pattern https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit&page=N:
- page 1: local 2026-10-17T05:59:25Z, HTTP 200, 347076 bytes, sha256 5fb91612273f09421a6aa79d708eb7c6176388158543fa8dbbfca9cf80823b38. Parsed from the embedded JSON: 25 PRs (PR 317 down to PR 272); page metadata said totalPages 2, totalCount 36 (35 open, 1 closed).
- page 2: local 2026-10-17T06:00:02Z, HTTP 200, 300265 bytes, sha256 9328621c885d92a970deb87bb18a2064b0b26b2016f2068a4654ae85f7c41b30. 13 PRs (PR 273 down to PR 257); metadata totalCount 38 (37 open, 1 closed).
- page 3: local 2026-10-17T06:00:06Z, HTTP 200, 240312 bytes, sha256 c0c5a6e1d6bac839a5ba3d8b035abaaa1f507597a3ad9300ed32d1be6d404a70. The payload has no results (currentPage 3, totalPages 2, totalCount 38): the page lists no pull requests, so the HTML list ends.
- The count moved from 36 to 38 between page 1 and page 2 (PR 318 and PR 319 were created in between, so PR 273 and PR 272 appear on both pages). The HTML read was therefore not one consistent snapshot, so I also read the REST API (allowed fallback, 2 of the 4 permitted calls used):
  - REST call 1: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1 at local 2026-10-17T06:00:47Z (response Date header: Sat, 17 Oct 2026 06:01:41 GMT), HTTP 200, 100 PRs numbered 214 to 319, Link header shows 4 pages in all; 38 codetables-qubit PRs (PR 257 to PR 319).
  - REST call 2 (final re-read just before writing): same URL at local 2026-10-17T06:09:01Z (Date header: Sat, 17 Oct 2026 06:09:55 GMT), HTTP 200, 100 PRs numbered 223 to 328; 47 codetables-qubit PRs (PR 257 to PR 328): 46 open, 1 closed (PR 260, closed 2026-10-17T01:01:52Z, merged_at empty), 0 merged. New since call 1: PR 320 to PR 328. All 47 are draft PRs by the account verexxi.
  - My local clock runs about 54 s behind GitHub's Date headers (06:00:47Z local vs 06:01:41 GMT; 06:03:01Z vs 06:03:54 GMT; 06:09:01Z vs 06:09:55 GMT). Times written in this report are the local readings unless marked as Date header.
- Read in total: 3 HTML pages (25 + 13 + 0 rows, 36 distinct PRs) and 2 REST pages (100 PRs each). The union is 47 distinct codetables-qubit PRs. REST pages 2 to 4 were not needed: they hold PRs numbered below 223, and the text search over all PRs found nothing below PR 257.
- Cells claimed in those 47 PR titles (PR number, state, cell, live upper bound to claimed upper bound). Every 'lowered from' value equals the upper bound in the claim's copy of the live table (0 mismatches):
  - PR 328 open [[195,2]] 65 to 64
  - PR 327 open [[165,6]] 53 to 52
  - PR 326 open [[135,8]] 43 to 42
  - PR 325 open [[125,4]] 41 to 40
  - PR 324 open [[115,2]] 39 to 38
  - PR 323 open [[230,10]] 77 to 72
  - PR 322 open [[215,6]] 73 to 71
  - PR 321 open [[200,10]] 67 to 62
  - PR 320 open [[185,3]] 63 to 60
  - PR 319 open [[173,2]] 59 to 56
  - PR 318 open [[161,2]] 55 to 52
  - PR 317 open [[155,6]] 53 to 49
  - PR 316 open [[110,5]] 37 to 35
  - PR 307 open [[225,2]] 75 to 74
  - PR 306 open [[219,2]] 73 to 72
  - PR 305 open [[213,2]] 71 to 70
  - PR 304 open [[207,2]] 69 to 68
  - PR 303 open [[171,1]] 57 to 55
  - PR 302 open [[135,1]] 45 to 44
  - PR 301 open [[129,2]] 43 to 42
  - PR 300 open [[127,2]] 42 to 41
  - PR 299 open [[123,2]] 41 to 40
  - PR 298 open [[122,1]] 41 to 40
  - PR 297 open [[120,2]] 40 to 39
  - PR 296 open [[110,2]] 37 to 36
  - PR 282 open [[230,5]] 77 to 73
  - PR 281 open [[230,3]] 77 to 74
  - PR 280 open [[200,5]] 67 to 64
  - PR 279 open [[200,2]] 67 to 65
  - PR 278 open [[183,1]] 61 to 59
  - PR 277 open [[177,1]] 59 to 57
  - PR 276 open [[165,2]] 55 to 53
  - PR 275 open [[159,2]] 53 to 51
  - PR 274 open [[148,2]] 50 to 48
  - PR 273 open [[146,2]] 49 to 47
  - PR 272 open [[142,2]] 48 to 46
  - PR 271 open [[140,2]] 47 to 45
  - PR 270 open [[133,2]] 45 to 43
  - PR 269 open [[105,4]] 35 to 34
  - PR 267 open [[164,1]] 55 to 53
  - PR 266 open [[158,1]] 53 to 51
  - PR 262 open [[154,1]] 52 to 50
  - PR 261 open [[152,1]] 51 to 49
  - PR 260 closed [[150,1]] 51 to 49
  - PR 259 open [[145,1]] 49 to 47
  - PR 258 open [[139,1]] 47 to 45
  - PR 257 open [[132,1]] 45 to 43
- No PR names [[180,2]] or any [[180,k]] cell. Cells with n from 170 to 195: PR 328 [[195,2]] 65 to 64; PR 320 [[185,3]] 63 to 60; PR 319 [[173,2]] 59 to 56; PR 303 [[171,1]] 57 to 55; PR 278 [[183,1]] 61 to 59; PR 277 [[177,1]] 59 to 57.
- Implication check with the three rules of the criterion (R1 d(n,k) at most d(n,k-1) for k at least 2; R2 d(n,k) at most d(n+1,k); R3 d(n,k) at most d(n-1,k+1)+1), computed two ways: claim/check/propagate.py run on the claim's table copy, and my own independent shortest-path implementation (work/closure_indep.py); the two agree on every one of the 32896 cells in every scenario.
  - live table only: closure at (180,2) is 60 (live cell 61). Witness: five R3 steps down from [[175,7]], live bound 55.
  - live table plus all 47 PR claims applied as overrides: closure at (180,2) is 59 (same value counting only the open PRs: 59). Witness: R1 (180,2) from (180,1), R2 (180,1) from (181,1), R2 (181,1) from (182,1), R2 (182,1) from (183,1), where PR 278 claims [[183,1]] at most 59.
  - Adding the further published rule d(n,k) at most d(n-1,k)+1 (my implementation only) changes neither number (60 and 59).
  - So the best bound already implied by live cells plus pending PRs is 59. The claimed 58 is one below it: not implied, not a tie.

## 3. TROPHY_CASE.md and the repository
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md fetched at local 2026-10-17T06:03:01Z (Date header 06:03:54 GMT), HTTP 200, 30936 bytes, 100 lines, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9. git ls-remote gives main at 7dd4480512cc47fe0f897164844432a2738fe649.
- The pinned copy claim/data/TROPHY_CASE_pinned_9b1d444.md (sha256 cdfe852481ba85e35ccbc386d64ce88de92a56eb73d1ec3e44cdc9a3b86345ad) differs only by CRLF line endings (100 carriage returns); with them removed both files hash to 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9.
- Searching it for codetables, qubit, stabilizer, quantum, [[, QECC, Grassl, upper bound and 180: no row concerns qubit codes or codetables-qubit. The only matches were matrix-multiplication and constant-weight-code (Delsarte LP) rows.
- Repository tree at that main commit (blobless shallow clone into work/repo_tree, 2712 files): known-knowns contains codetables-binary-linear (a different target) and no qubit folder; the bank entry known-unknowns/physics/codetables-qubit-upper-bounds-n101-256.md is present. It says (open as of 2026-10-15) that the full quantum LP with shadow constraints appears not to have been run above n = 100, and lists as a trap that propagation-implied improvements are not new bounds.

## 4. Literature, last 24 months (from 2024-10-17)
- arXiv API: I made 6 requests (local 06:03:40Z, 06:03:47Z, 06:03:54Z, 06:04:01Z, 06:04:09Z, 06:04:16Z, about 7 s apart). Every one returned HTTP 301 with an empty body, because I used the http endpoint and did not follow the redirect to https. That was my error, not an arXiv refusal. It used up the 6-request cap, so I made no seventh request. arXiv was therefore not searched, and the fallback below was used instead.
- OpenAlex works search with from_publication_date 2024-10-17 (title and abstract screened by keyword and by hand): first batch of 6 queries all HTTP 200 (06:04:38Z to 06:04:47Z), 109 unique works; second batch 3 of 6 queries HTTP 200 (06:08:08Z to 06:08:11Z), 38 further unique works. The remaining 3 queries (optimal qubit stabilizer codes with small k; quantum MacWilliams LP nonexistence; additive GF(4) codes shadow) returned HTTP 429 at 06:08:13Z and again on retries at 06:08:49Z to 06:08:57Z and 06:11:59Z to 06:12:10Z, so they produced nothing. One OpenAlex lookup of nine arXiv IDs that web search surfaced: HTTP 200 at 06:07:42Z.
- Semantic Scholar API: 3 queries at 06:12:15Z, 06:12:20Z, 06:12:25Z, all HTTP 429, no data.
- WebSearch: 4 searches (the exact cell phrase; the SDP rational-certificate paper; Rains shadow bound formula; recent upper-bound table work).
- About 147 distinct works were screened. Nothing gives an upper bound for [[180,2]], a table of LP or shadow bounds for qubit codes above n = 100, or anything implying a bound at or below 58. The nearest items, and why they do not matter:
  - Angles Munne and Huber, arXiv:2603.19901 (2026-03-20), SDP rational certificates: improves 18 upper bounds on the size of n-qubit codes for n from 6 to 19 only. arXiv:2408.10323 (2024-08-19, before the window): the SDP hierarchy, small n.
  - arXiv:2502.14165 (2025-02-20, thesis) and arXiv:2610.09900 (Quantizing Delsarte Theory, 2026-10-07): general quantum Delsarte/LP theory, no qubit-code table in the abstracts.
  - arXiv:2501.10163 (2025-01-17): shows no extremal Hermitian self-dual GF(4) codes with parameters [12m,6m,4m+2] exist (length 180 is m = 15). That is the k = 0 self-dual case, which uses a different distance notion; none of the three listed propagation rules carries it to k = 2.
  - arXiv:2601.19848 (January 2026): check-weight-constrained codes, exact LP results only for n at most 9; arXiv:2601.15446 is on the same theme. Entropy 2025 (doi 10.3390/e27090940): Monte Carlo upper bound on the distance of a given code, not a nonexistence bound. arXiv:2604.15307: witnesses for specific LDPC codes (title-level screening only).
  - Rains, Quantum shadow enumerators, quant-ph/9611001 (1996, outside the window): per the web-search summary, a code of length n corrects at most floor((n+1)/6) errors, i.e. d at most 2*floor((n+1)/6)+1. Python printed 61 for n = 180, which equals the live table value. So the best published closed form I could identify for [[180,2]] is 61, and the claim improves it to 58 by an LP computation.

## 5. Reasoning and limits
- Comparators: live cell 61; live-table propagation closure 60; closure with every pending PR claim 59; Rains closed form 61; TROPHY_CASE.md nothing. The claim (at most 58) is strictly below each, and lowers the live bound by 3, so the bank criterion of lowering the live bound by at least 1 without being implied by other live cells is met on novelty grounds. It is not a tie with any item found.
- I did not run the certificate checker or judge the proof; that is outside this brief (REPRODUCE.md covers it).
- Limits: the arXiv search was lost to my own redirect mistake and replaced by OpenAlex and web search, which were partly rate limited, so the literature result is no hit found, not proof of absence. The 47 PRs are unmerged drafts that I counted as known anyway, which is the conservative direction.
- Time sensitivity: the same account files bursts of claim PRs (roughly one every 6 s, in the creation times returned by the API) including k = 1 cells near n = 180. A claim of 58 or lower on [[180,1]], [[181,1]], [[182,1]], [[183,1]], [[181,2]], [[182,2]] or [[183,2]] would imply this bound through R1 and R2 and turn it into a tie. None existed at the 06:09:55 GMT re-read.
pass: true
