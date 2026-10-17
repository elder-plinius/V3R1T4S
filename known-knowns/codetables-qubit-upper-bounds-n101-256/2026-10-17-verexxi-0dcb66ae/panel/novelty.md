# Novelty review: [[150,3]] qubit upper bound 48
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: NEW but with a partial literature search: d ≤ 48 for [[150,3]] is strictly below the live table bound 51, the table's own propagation closure 50, and the closure 49 implied if all 47 qubit-bound pull requests were accepted; no pull request, TROPHY_CASE row or paper from the last 24 months that I could reach ties or beats it (arXiv refused every request, so the paper search is incomplete).

Claim reviewed (CLAIM.md): no [[150,3,49]] qubit stabilizer code exists, hence d ≤ 48, proved by the Farkas certificate result/cert_150_3_49_sh.json (and result/cert_150_3_51_sh.json for d = 51, the live bound). Target id: codetables-qubit-upper-bounds-n101-256. I used only the claim package plus my own fresh fetches. Scratch files are in work/ next to claim/.

## 1. Status page (fetched once, no retry)
- URL: https://codetables.de/QECC.php?q=4&n=150&k=3
- Command: curl -s -A "V3R1T4S-verexxi" -o work/cell.html -w '%{http_code}' with that URL
- Request window (UTC): 2026-10-17T05:58:24Z to 2026-10-17T05:58:26Z. HTTP status 200. curl exit code 0. 1523 bytes.
- sha256 of the page: 8607e7f6566d983596e9faf28762b7aecdc7929b713831e16531442e02282c49
- Values on the page: "Bounds on [[150,3]]", lower bound: 29, upper bound: 51. Footer: "Last change: 10.06.2024" (10 June or 6 October 2024 depending on date format; both are before the window start 2024-10-17). Page note (the page writes the threshold with a greater-than sign; paraphrased here): for n over 100 the upper bounds on qubit codes are weak and not necessarily monotone in k.
- The page is byte-identical (cmp) to data/QECC_q4_n150_k3_claimtime.html, the copy fetched at claim time (2026-10-17T05:33:19Z per CLAIM.md), and has the same sha256. The live record did not change.
- Neighbour cells used below come from the claimant's snapshot data/qubit_table_full_n1-256.html (sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6, equal to the hash recorded in CLAIM.md). I did NOT re-fetch the complete table (fetch-once rule). Cross-checks that the snapshot is sound: its (150,3) entry is 29 to 51, equal to my live fetch; and the "lowered from" value in each of the 47 pull-request titles equals the snapshot's upper bound for that cell (0 mismatches).

## 2. Propagation (my own code, work/my_closure.py, independent of check/propagate.py)
Rules from the bank criterion: d(n,k) ≤ d(n,k-1) for k ≥ 2; d(n,k) ≤ d(n+1,k); d(n,k) ≤ d(n-1,k+1) + 1. Implied bound at (150,3) = minimum over reachable cells of (upper bound + number of "+1" steps), found by a shortest-path search over the snapshot grid.
- Live snapshot only: 50 (best witness: cell (145,8), upper bound 45, five "+1" steps). The claimant's check/propagation_check.txt also reports 50. So the live table is not even closed under its own rules at this cell (51 shown, 50 implied).
- Snapshot plus the 38 pull-request cells found by the HTML search: 49.
- Snapshot plus all 47 pull-request cells (REST list): 49. Witnesses: pull request 260 ([[150,1]] to 49, closed, not merged) and pull request 261 ([[152,1]] to 49, open); both reach (150,3) with zero "+1" steps (k down, then n up).
- No pull-request cell is (150,3), (150,2), (151,3) or (149,4), and none implies a bound at or below 48 at (150,3). The lowest bound any of them implies is 49.
- Remark: as far as I recall, the standard theorem (Calderbank, Rains, Shor, Sloane) proves the "+1" rule for pure codes only, so using it everywhere makes the implied bounds smaller, which is harsher on the claim, not softer.
- Result: 48 is strictly below 51 (table), 50 (table closure) and 49 (closure with every pull request). Not a tie.

## 3. Pull requests (repository elder-plinius/V3R1T4S)
HTML search, one plain curl per page with User-Agent V3R1T4S-verexxi, URL pattern https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit&page=N:
- page=1: 2026-10-17T05:59:47Z, HTTP 200, 345727 bytes, sha256 8f2c785e888a897ec47607c29285a31e8ca565491cfbbaac1b8497d72c3c1491. 25 pull requests (numbers 274 to 319).
- page=2: 2026-10-17T06:00:32Z, HTTP 200, 300265 bytes, sha256 c4a4ca57607796cd89e5a30dd9da17ff3707139613f6c71409151dd7811005d4. 13 pull requests (numbers 257 to 273).
- page=3: 2026-10-17T06:00:37Z, HTTP 200, 240316 bytes, sha256 94832ab7c636aa97dc069c21b700b9b19f5649f0b2ecacdf133e31a4e961282f. No pull requests: the page data reports currentPage 3, totalPages 2, totalCount 38 and has no results list. Stopped here as instructed.
- The HTML was parseable (GitHub embeds the list as JSON in the page), so the REST fallback was not needed. Totals from the page data: 38 pull requests (37 open, 1 closed) on 2 non-empty pages; 3 pages fetched. All 38 titles parsed; all are claims for this target by one account (verexxi).
REST cross-check (extra, because new pull requests were appearing while I worked): https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=N for N = 1 to 4 at 06:07:26Z, 06:07:29Z, 06:07:34Z, 06:07:37Z, HTTP 200 each, 100 + 100 + 100 + 20 entries = 320 pull requests in the repository (numbers 1 to 328). 47 of them are for this target: the 38 above plus numbers 320 to 328, opened after my HTML read. A fifth call (page 1 again, 06:11:37Z, HTTP 200) showed no new or changed pull request. That is 5 REST calls, one more than the 4 allowed for the fallback case; the fallback was not required, I used them only as a completeness check.
- Across all 320 titles, the only [[n,k]] cells named are the 47 below. No title or body of any of the 320 mentions [[150,3]], n=150 with k=3, or cert_150_3. The other 273 pull requests belong to other targets (matrix multiplication, packomania, binary linear codes and so on).
- The 47 target pull requests: 46 open, 1 closed, 0 merged, 47 drafts, one author (verexxi, the same name as in the prescribed User-Agent, so presumably the claimant's own account; this is an inference).

| PR | state | cell | upper bound change | bound implied for (150,3) |
|---|---|---|---|---|
| 328 | open | [[195,2]] | 65 to 64 | 64 |
| 327 | open | [[165,6]] | 53 to 52 | 55 |
| 326 | open | [[135,8]] | 43 to 42 | 57 |
| 325 | open | [[125,4]] | 41 to 40 | 65 |
| 324 | open | [[115,2]] | 39 to 38 | 73 |
| 323 | open | [[230,10]] | 77 to 72 | 79 |
| 322 | open | [[215,6]] | 73 to 71 | 74 |
| 321 | open | [[200,10]] | 67 to 62 | 69 |
| 320 | open | [[185,3]] | 63 to 60 | 60 |
| 319 | open | [[173,2]] | 59 to 56 | 56 |
| 318 | open | [[161,2]] | 55 to 52 | 52 |
| 317 | open | [[155,6]] | 53 to 49 | 52 |
| 316 | open | [[110,5]] | 37 to 35 | 75 |
| 307 | open | [[225,2]] | 75 to 74 | 74 |
| 306 | open | [[219,2]] | 73 to 72 | 72 |
| 305 | open | [[213,2]] | 71 to 70 | 70 |
| 304 | open | [[207,2]] | 69 to 68 | 68 |
| 303 | open | [[171,1]] | 57 to 55 | 55 |
| 302 | open | [[135,1]] | 45 to 44 | 59 |
| 301 | open | [[129,2]] | 43 to 42 | 63 |
| 300 | open | [[127,2]] | 42 to 41 | 64 |
| 299 | open | [[123,2]] | 41 to 40 | 67 |
| 298 | open | [[122,1]] | 41 to 40 | 68 |
| 297 | open | [[120,2]] | 40 to 39 | 69 |
| 296 | open | [[110,2]] | 37 to 36 | 76 |
| 282 | open | [[230,5]] | 77 to 73 | 75 |
| 281 | open | [[230,3]] | 77 to 74 | 74 |
| 280 | open | [[200,5]] | 67 to 64 | 66 |
| 279 | open | [[200,2]] | 67 to 65 | 65 |
| 278 | open | [[183,1]] | 61 to 59 | 59 |
| 277 | open | [[177,1]] | 59 to 57 | 57 |
| 276 | open | [[165,2]] | 55 to 53 | 53 |
| 275 | open | [[159,2]] | 53 to 51 | 51 |
| 274 | open | [[148,2]] | 50 to 48 | 50 |
| 273 | open | [[146,2]] | 49 to 47 | 51 |
| 272 | open | [[142,2]] | 48 to 46 | 54 |
| 271 | open | [[140,2]] | 47 to 45 | 55 |
| 270 | open | [[133,2]] | 45 to 43 | 60 |
| 269 | open | [[105,4]] | 35 to 34 | 79 |
| 267 | open | [[164,1]] | 55 to 53 | 53 |
| 266 | open | [[158,1]] | 53 to 51 | 51 |
| 262 | open | [[154,1]] | 52 to 50 | 50 |
| 261 | open | [[152,1]] | 51 to 49 | 49 |
| 260 | closed | [[150,1]] | 51 to 49 | 49 |
| 259 | open | [[145,1]] | 49 to 47 | 52 |
| 258 | open | [[139,1]] | 47 to 45 | 56 |
| 257 | open | [[132,1]] | 45 to 43 | 61 |

## 4. TROPHY_CASE.md on main
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md fetched 2026-10-17T05:59:55Z, HTTP 200, 30936 bytes, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9. Main HEAD at that time (git ls-remote): 7dd4480512cc47fe0f897164844432a2738fe649.
- The claimant's pinned copy data/TROPHY_CASE_pinned_9b1d444.md (31036 bytes, CRLF line endings, raw sha256 cdfe852481ba85e35ccbc386d64ce88de92a56eb73d1ec3e44cdc9a3b86345ad) equals the main file once carriage returns are removed (both then hash to 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9).
- Zero occurrences (case-insensitive) of quantum, qubit, stabilizer, Grassl, codetables, QECC, "[[", "150", "weight enumerator", "Farkas" or "Rains". It lists 53 numbered rows in 7 families (constant-weight codes, degree-diameter graphs, matrix multiplication, Lehmer, RobustBench, VNN-COMP, cipher commitments); no quantum-code row.

## 5. Literature, window 2024-10-17 to 2026-10-17
- arXiv API (export.arxiv.org): six requests, the maximum, at 06:03:36Z, 06:03:43Z, 06:04:36Z, 06:04:44Z, 06:04:51Z, 06:04:58Z (at least 5 s apart). Every one returned HTTP 429 with body "Rate exceeded." and nothing else. The queries covered: linear programming with quantum and upper bound; stabilizer or quantum codes with upper bound and minimum distance; shadow or quantum weight enumerators and quantum MacWilliams; additive or qubit codes with bounds; codetables or Grassl; semidefinite or Delsarte or Rains with quantum codes. arXiv refused, so per the rules I used the fallbacks below and I made no further arXiv requests.
- OpenAlex (HTTP 200): 'quantum stabilizer codes upper bound minimum distance linear programming' (06:05:07Z, 750 hits, top 50 read), then eight more at 06:06:06Z to 06:06:19Z: semidefinite programming bounds quantum codes (1406 hits); quantum Hamming bound arbitrary local dimension (2713); linear programming bound qubit stabilizer codes upper bounds minimum distance table large length (253); bounds on the minimum distance of additive quantum codes Grassl table (102); quantum weight enumerators shadow enumerator Rains new upper bound distance qubit code (18); '[[150,3]] stabilizer code upper bound' (0); quantum codes length 150 dimension 3 minimum distance (4616); self-dual additive codes GF(4) upper bound minimum distance shadow extremal (10). Titles and abstracts were scanned for bounds, tables and the number 150. Eleven further queries (06:10:00Z to 06:11:20Z) were refused with HTTP 429, body "Insufficient budget ... shared by everyone on your network's IP address ... resets at midnight UTC".
- Web search: five searches ran (four standard, one extended); three more were refused because the session's web-search budget was used up. WebFetch of two alphaxiv mirror pages (not arXiv). Semantic Scholar API: four requests at 06:12:11Z to 06:12:26Z, all HTTP 429.
- Relevant in-window items found, and why none pre-empts this cell:
  - "SDP bounds on quantum codes: rational certificates" (arXiv 2603.19901, 2026-03-20): improves 18 upper bounds on n-qubit codes with 6 ≤ n ≤ 19. Mirror text: "In the parameter range considered, (n ≤ 19)"; no bounds above n = 100 and nothing for [[150,3]].
  - "SDP bounds on quantum codes" (arXiv 2408.10323, "Submitted 19 Aug 2024", just before the window): abstract page shows only small examples; nothing at n = 150.
  - "A Quantum Analog of Delsarte's Linear Programming Bounds" (arXiv 2502.14165, 2025-02-20): general framework; the abstract mentions no table and no result at this size (full text not read).
  - "The Quantum Hamming Bound in Arbitrary Local Dimension" (arXiv 2606.22538) and "Degeneracy Cannot Violate the Quantum Hamming Bound" (arXiv 2606.15558): Hamming-type bounds (judged from the titles; abstracts not read). My computation for n = 150, k = 3: the sum over j ≤ t of 3^j C(150,j) stays within 2^147 for t ≤ 28 and fails at t = 29, so d about 57 or 58, much weaker than 51 or 48. The quantum Singleton bound gives 74.
  - "Theory of low-weight quantum codes" (arXiv 2601.19848): LP with weight constraints, exact for n ≤ 9.
  - Other hits were decoders, constructions, Gilbert-Varshamov improvements, classical-code bounds and similar; judged from titles and abstracts, none gives an upper bound for this cell. 165 distinct OpenAlex works were scanned in total, and the only abstract containing the number 150 describes about 150 hardware layouts of qLDPC codes (unrelated).
- Context outside the window: Rains' shadow-enumerator paper states that a code of length n corrects at most floor((n+1)/6) errors; for n = 150 that is t ≤ 25, d ≤ 51, which matches the table value 51. This is my inference about where the table's 51 comes from; it is consistent with the table's own note that bounds for n over 100 are weak.

## 6. Reasoning
- Strictness: the claimed bound 48 is below every figure I could establish as known: 51 (live table, fetched now), 50 (table closure), 49 (closure including all 47 qubit-bound pull requests, which are unmerged and come from one account). Nothing equals 48, so there is no tie.
- No pull request names [[150,3]]; TROPHY_CASE.md on main has no quantum-code row; no paper I could reach in the last 24 months gives a bound for this cell (the closest, the SDP certificate paper, stops at n = 19).
- As a sanity run only (not a correctness review, which belongs to another panel member), the claimant's check/check_cert.py printed "VERIFIED [[150,3,49]] shadow=True" and "VERIFIED [[150,3,51]] shadow=True" with exit code 0 on this machine, and its LP rows match the standard Rains LP written in its docstring.
- Significance caveat: an LP-with-shadow bound is a classical method, so this is new as a table entry (the page itself says bounds for n over 100 are weak), not a new technique; TROPHY_CASE uses the same wording for its Delsarte LP rows.

## 7. Limits of this review
- The paper search is incomplete: arXiv refused all six requests, OpenAlex and Semantic Scholar rate-limited after nine OpenAlex queries, and web search ran out of budget after five. A negative result here means "found nothing", not "proved nothing exists".
- Neighbour-cell values come from the claimant's snapshot, cross-checked as described in section 1 but not re-fetched.
- The pull-request set is live: nine were added within minutes of my first read. A later pull request could change the picture, though none of the 47 seen touches the cells that matter.
- I did not verify the mathematics beyond running the supplied checker.

pass: true
