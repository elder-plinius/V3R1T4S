# Novelty skeptic report: qubit [[192,2]] upper bound (claim: no [[192,2,64]] code, so at most 63)

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: strictly lower than every source read (live table 65, table-implied bound 64, still 64 with all 47 qubit-code PR claims applied, no PR / trophy-case entry / paper found for [[192,2]]); arXiv refused all 6 requests (HTTP 429), so the literature part rests on fallback sources and is best-effort

Paths below are relative to claim/ unless they start with work/ (my scratch folder next to claim/). All times are what `date -u` printed on this PC; GitHub Date headers on later requests ran about 54 s ahead of it (examples in sections 4 and 5), so true UTC is probably about 54 s later than the quoted PC-clock times.

## 1. Primary status page, fetched once, no retry

- URL: https://codetables.de/QECC.php?q=4&n=192&k=2
- Command (kit form): curl -s -A "V3R1T4S-verexxi" -o work/cell.html -w '%{http_code}' with that URL
- UTC (PC clock): 2026-10-17T05:58:41Z before the request, 2026-10-17T05:58:42Z after; curl exit 0
- HTTP status: 200; 1523 bytes; sha256 20940479cbdff12078de1b0cba4cc0b756a9af457a6aaa441cd741e58415ff76
- Values on the page: "Bounds on [[192,2]]_2", lower bound 37, upper bound 65. Construction shown: "[192,2] Code, Missing Construction". Footer: "Last change: 10.06.2024".
- The page itself notes that for n above 100 the qubit upper bounds are weak and not necessarily monotone in k.
- Byte-identical (cmp) to data/QECC_q4_n192_k2_claimtime.html, which CLAIM.md says was fetched 2026-10-17T05:35:44Z with sha256 20940479cbdff12078de1b0cba4cc0b756a9af457a6aaa441cd741e58415ff76. So the live cell did not move between the claimant's fetch and mine.
- The kit command does not save response headers, so there is no server Last-Modified or Date for this fetch.

## 2. What the "known" value 65 is

- For k = 1, 2, 3 and every n from 101 to 256 (468 cells, from data/qubit_table_full_n1-256.html, whose sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6 matches CLAIM.md) the live upper bound equals floor((n+1)/6) + floor((n+2)/6) + 1 in 426 cells, is lower in 42 cells, and is never higher (0).
- At n = 192 that expression is 65, and the live cells (192,1), (192,2), (192,3) all show 65. This matches the closed form of Rains' 1996 shadow-enumerator paper (its abstract, read on a mirror, says any code of length n can correct at most floor((n+1)/6) errors). So the number being beaten at this cell is a 1996 analytic bound, consistent with the table's own remark that n above 100 is weak. This is my inference from the table data plus that abstract; I did not read the theorem text.

## 3. Is 63 implied by other cells? (propagation rules R1 d(n,k) at most d(n,k-1) for k at least 2; R2 d(n,k) at most d(n+1,k); R3 d(n,k) at most d(n-1,k+1)+1)

- I re-ran the claimant's check/parse_table.py and check/propagate.py (python -I) on data/qubit_table_full_n1-256.html (32896 cells with k at least 1). Live (192,2) = [37, 65]; closure at (192,2) = 64, witness "R3 (191,3)+1". This reproduces check/propagation_check.txt. 63 is below 64, so it is not implied by the live table.
- I then added every qubit-code PR claim in the repo (section 4, 47 cells) as overrides through the same script: closure at (192,2) is still 64 (neighbours after overrides: (193,2) 64, (195,2) 64, (192,1) 65, (191,3) 63).
- Manual cross-check of which PR cells can reach (192,2) at all (k at most 2 with n at least 192, or k = 2+j with n at least 192-j via R3 j times):
  - PR #328 [[195,2]] 65 to 64 gives (192,2) at most 64 (R2/R1 chain)
  - PR #279 [[200,2]] 67 to 65 gives (192,2) at most 65 (R2/R1 chain)
  - PR #280 [[200,5]] 67 to 64 gives (192,2) at most 67 (R3 chain, j=3)
  - PR #304 [[207,2]] 69 to 68 gives (192,2) at most 68 (R2/R1 chain)
  - PR #305 [[213,2]] 71 to 70 gives (192,2) at most 70 (R2/R1 chain)
  - PR #321 [[200,10]] 67 to 62 gives (192,2) at most 70 (R3 chain, j=8)
  - PR #306 [[219,2]] 73 to 72 gives (192,2) at most 72 (R2/R1 chain)
  - PR #307 [[225,2]] 75 to 74 gives (192,2) at most 74 (R2/R1 chain)
  - PR #281 [[230,3]] 77 to 74 gives (192,2) at most 75 (R3 chain, j=1)
  - PR #322 [[215,6]] 73 to 71 gives (192,2) at most 75 (R3 chain, j=4)
  - PR #282 [[230,5]] 77 to 73 gives (192,2) at most 76 (R3 chain, j=3)
  - PR #323 [[230,10]] 77 to 72 gives (192,2) at most 80 (R3 chain, j=8)
  Best implied value is 64 (PR #328, [[195,2]] 65 to 64 through R2), one above the claimed 63. No PR cell touches (192,1) or any (n,1) with n at least 192; the k = 1 claims stop at n = 183.

## 4. Pull requests

Prescribed HTML search, one plain request per page, User-Agent "V3R1T4S-verexxi", until a page lists no pull requests:

| page | URL | UTC (PC clock) | HTTP | bytes | sha256 | PRs listed |
|---|---|---|---|---|---|---|
| 1 | https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit&page=1 | 2026-10-17T05:59:48Z | 200 | 345727 | 5c6574b59c4928a48528ab4e4f1ef60133b0b9b76c7fd7e44afd0e4cafbfa249 | 25 |
| 2 | https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit&page=2 | 2026-10-17T06:00:19Z | 200 | 300265 | acb37dcb3f72fcb4930ec4cf49e4fbf6fc5751346d99b76c1a94dc8b2f64f6b3 | 13 |
| 3 | https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit&page=3 | 2026-10-17T06:00:21Z | 200 | 240316 | f45f236caa59048467477269008e84870b8068bb0e0f91a4f75d7200a1f802b7 | 0 |

- The pages are a React page; the list is in its embedded JSON (currentPage, totalPages, totalCount, openCount, closedCount, results). Page 1 reported totalCount 38 (37 open, 1 closed), totalPages 2; page 2 held the remaining 13; page 3 had no results key and no pull links, so reading stopped there. Pages read: 3. Pull requests read: 38 (distinct numbers 38).
- All 38 titles have the form "[claim] codetables-qubit-upper-bounds-n101-256: [[n,k]] upper bound lowered from A to B". Cells claimed (PR number, cell, A to B, state):
  - #257 [[132,1]] 45 to 43; #258 [[139,1]] 47 to 45; #259 [[145,1]] 49 to 47
  - #260 [[150,1]] 51 to 49 (closed, not merged); #261 [[152,1]] 51 to 49; #262 [[154,1]] 52 to 50
  - #266 [[158,1]] 53 to 51; #267 [[164,1]] 55 to 53; #269 [[105,4]] 35 to 34
  - #270 [[133,2]] 45 to 43; #271 [[140,2]] 47 to 45; #272 [[142,2]] 48 to 46
  - #273 [[146,2]] 49 to 47; #274 [[148,2]] 50 to 48; #275 [[159,2]] 53 to 51
  - #276 [[165,2]] 55 to 53; #277 [[177,1]] 59 to 57; #278 [[183,1]] 61 to 59
  - #279 [[200,2]] 67 to 65; #280 [[200,5]] 67 to 64; #281 [[230,3]] 77 to 74
  - #282 [[230,5]] 77 to 73; #296 [[110,2]] 37 to 36; #297 [[120,2]] 40 to 39
  - #298 [[122,1]] 41 to 40; #299 [[123,2]] 41 to 40; #300 [[127,2]] 42 to 41
  - #301 [[129,2]] 43 to 42; #302 [[135,1]] 45 to 44; #303 [[171,1]] 57 to 55
  - #304 [[207,2]] 69 to 68; #305 [[213,2]] 71 to 70; #306 [[219,2]] 73 to 72
  - #307 [[225,2]] 75 to 74; #316 [[110,5]] 37 to 35; #317 [[155,6]] 53 to 49
  - #318 [[161,2]] 55 to 52; #319 [[173,2]] 59 to 56
- None of the 38 is [[192,2]]. All were authored by one account (verexxi) from a fork, so they are the claimant's own sister claims, not independent prior art.

Cross-check through the REST API (the HTML had parsed fine, so this was an extra, not a fallback; 4 calls, all HTTP 200): https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=N for N = 1..4.

| N | UTC (PC clock) | GitHub Date header | items | bytes | sha256 |
|---|---|---|---|---|---|
| 1 | 2026-10-17T06:02:53Z | Sat, 17 Oct 2026 06:03:47 GMT | 100 | 1764529 | 194814f44dd3f8b04d18b53017ee1536fcb94aba6e1b8342338f23d70f2fd946 |
| 2 | 2026-10-17T06:02:57Z | Sat, 17 Oct 2026 06:03:51 GMT | 100 | 1968597 | 1d44a649462cdeeef139789891067c558a9d0697b1596b355b5746acc056125e |
| 3 | 2026-10-17T06:03:01Z | Sat, 17 Oct 2026 06:03:55 GMT | 100 | 1822408 | 046f58120b39d976127872073d410a1589e862fba879386e155fc6cb0e10e23b |
| 4 | 2026-10-17T06:03:05Z | Sat, 17 Oct 2026 06:03:59 GMT | 20 | 376328 | a876dde80b566bdeb18891f8c9c902d8a3c932cb7771fdf3a25d4870fb33d5a0 |

- Page 4 held 20 items (fewer than 100), so the list was complete: 320 pull requests, numbers 1 to 328 (89 open, 149 closed unmerged, 82 merged). All 38 HTML results are in it.
- It also holds 47 qubit-code claim PRs in total (46 open, 1 closed): the 38 above plus 9 created after my HTML read: #320 [[185,3]] 63 to 60; #321 [[200,10]] 67 to 62; #322 [[215,6]] 73 to 71; #323 [[230,10]] 77 to 72; #324 [[115,2]] 39 to 38; #325 [[125,4]] 41 to 40; #326 [[135,8]] 43 to 42; #327 [[165,6]] 53 to 52; #328 [[195,2]] 65 to 64.
- No PR title or body among all 320 contains "[[192". The other families in the repo (matrix multiplication, packings, a classical binary-linear-code lower-bound family, and so on) are different problems.
- Last snapshot, 2026-10-17T06:19:58Z PC clock (GitHub Date 06:20:52 GMT): the searches "is:pr codetables-qubit 192" and "is:pr 192" returned only unrelated PRs (#192, #201, #311, #69). PRs filed after that moment are not covered.

## 5. TROPHY_CASE.md and the repo tree on main

- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md : UTC 2026-10-17T06:01:59Z (PC clock), HTTP 200, GitHub Date header "Sat, 17 Oct 2026 06:02:52 GMT" (so the PC clock was 53 s behind), ETag a98e1243d09c1bb2c4bf003da26d6e6ff6d3de91079b5b5250f7ce2769f6b378, Source-Age 124 s (CDN copy), 30936 bytes, 100 lines, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9.
- It equals data/TROPHY_CASE_pinned_9b1d444.md once the pinned copy's CRLF line endings are stripped (pinned file 31036 bytes, sha256 cdfe852481ba85e35ccbc386d64ce88de92a56eb73d1ec3e44cdc9a3b86345ad; both reduce to the same sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 after the CR bytes are removed).
- No line mentions qubit, codetables, stabilizer, quantum, Grassl, shadow, a double-bracket code cell, or the number 192. Its families are degree-diameter graphs, constant-weight codes (the only lines containing "upper bound" are the Delsarte LP bounds for A(n,d,w): summary line 18 and rows 38 to 42), matrix multiplication, the Lehmer bound, VNN-COMP, RobustBench and two cipher commitments.
- https://github.com/elder-plinius/V3R1T4S/tree/main/known-knowns/codetables-qubit-upper-bounds-n101-256 : HTTP 404 on main (GitHub Date 06:14:29 GMT). https://github.com/elder-plinius/V3R1T4S/tree/main/known-knowns : HTTP 200, 18 entries, none a qubit upper-bound family (there is a classical codetables-binary-linear folder). So no qubit result has been merged.

## 6. Literature, last 24 months (2024-10-17 to 2026-10-17)

- arXiv API: 6 requests (the cap), spaced at least 6.5 s apart, User-Agent "V3R1T4S-verexxi", query topics: quantum LP bound; shadow / quantum weight enumerator; stabilizer upper bound minimum distance; additive quaternary; codetables / Grassl; SDP. Local times 06:04:27Z, 06:04:49Z, 06:04:56Z, 06:06:04Z, 06:06:26Z, 06:06:33Z. All six returned HTTP 429 with body "Rate exceeded." arXiv refused, so per the kit I used other sources and say so here. No further arXiv requests were made.
- OpenAlex (4 queries, HTTP 200): the numbers of matches were 287, 69, 749, 1596, but each call returned only the 50 newest (reaching back to 2026-08-26, 2025-04-24, 2026-09-30, 2026-10-05 respectively), 178 distinct works. Four follow-up lookups (to list works citing Rains' shadow-enumerator paper and the CRSS paper) all returned HTTP 429: the free daily budget for this IP was used up. The error message offered a key obtained by sending the owner's email to OpenAlex; I did not do that.
- DataCite (7 queries on abstracts / titles, created between 2024-10-17 and 2026-10-17, HTTP 200): 496 distinct records (arXiv DOIs, Zenodo and others). Result sets were read completely for six of the seven queries (92, 16, 51, 21, 44, 43 matches); the broad title query (1183 matches) was read only for its first 300. Titles and abstracts of the records matching code-related AND bound-related terms (161 records) were screened by eye.
- Zenodo API (4 queries, HTTP 200 after a first attempt rejected with HTTP 400 for page size): 63 distinct records. Crossref (2 queries, HTTP 200): 102 records. Semantic Scholar (5 requests): 4 x HTTP 429, 1 x HTTP 200 with no results. Web search: 8 searches answered, then the session search budget ran out (2 refused). WebFetch: OEIS A058224 returned HTTP 403; a mirror of Rains' paper returned only its abstract.
- Result: no work in any of these sets states an upper bound, or a nonexistence result, for a [[192,2]] qubit stabilizer code, and none tabulates LP / shadow bounds for qubit codes with n above 100. No title or abstract collected from these sources (OpenAlex 178, Crossref 102, Zenodo 63, DataCite 496 records, overlapping) pairs the number 192 with a bound on a [[192,k]] code (the 192 hits were unrelated: a [[192,130,3]] construction, LDPC code lists, non-coding Zenodo posts).
- Closest items, read at abstract level only, and why they do not touch the cell: "SDP bounds on quantum codes: rational certificates" (arXiv 2603.19901, March 2026) improves 18 upper bounds for n-qubit codes with 6 to 19 qubits; "Invariant Theory, Magic State Distillation, and Bounds on Classical Codes" (arXiv 2501.10163) works with linear self-orthogonal GF(4) codes and proves non-existence of extremal [12m, 6m, 4m+2] Hermitian self-dual codes (k = 0, linear only; n = 192 is 12m with m = 16 but the case is d = 66, k = 0, not [[192,2]]); "Check-weight-constrained quantum codes: Bounds and examples" (arXiv 2601.15446) bounds codes under a check-weight limit; "Degeneracy Cannot Violate the Quantum Hamming Bound" (arXiv 2606.15558); "A Quantum Analog of Delsarte's Linear Programming Bounds" (arXiv 2502.14165, thesis); "Linear Programming Bounds on k-Uniform States" (arXiv 2503.02222, k-uniform states of qudit systems). The recent Zenodo records on qubit codes (2026-10-11 and 2026-07-30) are lower-bound constructions for n between 17 and 65.

## 7. Reasoning

- Status: live upper bound 65 (lower 37), confirmed by one fetch, unchanged since the claimant looked. The claim says no [[192,2,64]] code exists, so the bound would be at most 63: lower by 2.
- Not a tie and not implied: the best bound obtainable from other live cells is 64 (R3 from (191,3)), and still 64 after adding all 47 qubit-code PR claims, the strongest nearby one being PR #328 ([[195,2]] to 64). 63 is strictly below all of them.
- Repo: no PR, no TROPHY_CASE.md line and no folder on main covers [[192,2]] or implies at most 63 there.
- Literature: nothing found, with the limits listed below. The old analytic value 65 is what the table shows, so a result of 63 would be an improvement over it.

Limits, stated plainly:
- arXiv could not be searched at all (6 x HTTP 429). The fallback sources are keyword searches with the caps described above; they cannot prove that no paper exists.
- The PR list kept growing during my session (PRs #316 to #328 appeared within minutes); coverage ends at the snapshot times given.
- The closure uses the claimant's copy of the complete table (hash matches CLAIM.md). I did not re-fetch that table, because the kit allows one status fetch; the (192,2) cell itself was re-fetched live and matches.
- Not a correctness review: I ran the claimant's checker once per certificate only as a sanity check (python -I check/check_cert.py on result/cert_192_2_64_sh.json and result/cert_192_2_65_sh.json): both printed "VERIFIED" with exit code 0 (value of 2138 digits, 63+2+60 multipliers). Whether the LP is the right one is for another reviewer.

pass: true
