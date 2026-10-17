# Novelty review: [[155,3]] qubit stabilizer code, claimed upper bound 50 (target codetables-qubit-upper-bounds-n101-256)

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)

novelty: nothing found that ties or beats it: the live cell bound is 53, the live table's own propagation closure is 52, the best bound implied by all 47 repo pull-request claims taken at face value is 51, and the claimed 50 is strictly below each; no pull request, TROPHY_CASE.md row or paper from the last 24 months gives an upper bound for [[155,3]], but literature coverage is limited because the arXiv API refused (HTTP 429)

## 1. Claim under review

claim/CLAIM.md: no [[155,3,51]] stabilizer code exists, so the minimum distance upper bound of [[155,3]] is at most 50, proved by the Farkas certificate result/cert_155_3_51_sh.json. The claim states the live table value is 53 (lower bound 30).

## 2. Status page, fetched once, no retry

- URL: https://codetables.de/QECC.php?q=4&n=155&k=3
- Command (run once from the review folder): curl -s -A "V3R1T4S-verexxi" -o work/cell.html -w '%{http_code}' on that URL
- Machine clock (date -u): start 2026-10-17T05:58:33Z, end 2026-10-17T05:58:34Z. curl exit code 0.
- HTTP status: 200. Size 1523 bytes.
- sha256 of work/cell.html: ad092d4b904c89212e0de366657e1b97a07d53fd7f0aa4ed045a48ca892fcfba
- Values on the page: "Bounds on [[155,3]]", lower bound 30, upper bound 53. Page footer: Last change 10.06.2024. Page note (inequality sign written out in words here): for n over 100, "the upper bounds on qubit codes are weak (and not necessarily monotone in k)."
- Same sha256 as the claim-time page data/QECC_q4_n155_k3_claimtime.html (recorded in CLAIM.md as fetched 2026-10-17T05:33:30Z), so the cell was unchanged between the claimant's fetch and mine.
- Clock note: the machine clock runs slow. GitHub request-id timestamps of four uncached responses I received over the next minutes were 53 to 54 s ahead of the machine clock. So the codetables fetch was most likely at about 05:59:27Z in server time. I did not capture a Date header for the codetables response itself, so that figure is an estimate; the 05:58:33Z reading is the raw one.

Result: the live upper bound is 53. Success needs a bound below 53 that propagation does not already give.

## 3. Propagation check (own code, not the claimant's)

Rules as in the success criterion: R1 d(n,k) at most d(n,k-1) for k at least 2; R2 d(n,k) at most d(n+1,k); R3 d(n,k) at most d(n-1,k+1) plus 1.
work/my_closure.py parses the complete table snapshot data/qubit_table_full_n1-256.html (sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6, stamped Last change 23.05.2024) and computes the closure itself. I did not re-fetch that table (one-fetch rule), so neighbour cells are as of the claimant's 05:31:50Z snapshot. 33152 cells parsed; (155,3) reads 30 to 53, matching the live page.

- Live table only: closure at (155,3) is 52. Chain: R1 to (155,2), then R3 steps through (154,3), (153,4), (152,5), (151,6) to (150,7), whose live bound is 47; 47 plus 5 is 52. This equals the claimant's check/propagation_check.txt (52).
- Direct neighbours that can bound it: (155,2) = 53, (156,3) = 53, (154,4) = 52 (plus 1 gives 53).
- Live table plus all 47 pull-request claims at face value (same result using open ones only): closure 51. Chain: R1 to (155,2), R1 to (155,1), R3 to (154,2), R1 to (154,1), whose claimed bound is 50 (#262). Single claims that alone bring (155,3) to 51: #262 ([[154,1]] to 50), #275 ([[159,2]] to 51), #266 ([[158,1]] to 51). No claim or combination reaches 50 or below.

## 4. Pull requests

Search: https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit&page=N, one plain request per page, User-Agent V3R1T4S-verexxi. The HTML embeds JSON, so it was parseable.

| page | HTTP | rows listed | page-reported total | machine clock | sha256 of page |
|---|---|---|---|---|---|
| 1 | 200 | 25 (#319 down to #274) | 38 | 05:59:47Z | 250ddc577a8cb6391be77dfc10c9ce4c0fe039c61c000700b59cd87c52367a9f |
| 2 | 200 | 14 (#274 down to #257) | 39 (38 open, 1 closed) | 06:01:09Z | 5ed8f716b4c35ad81f60f01f2f4267ebb478749573399f368b70860949ac5427 |
| 3 | 200 | 0, so paging stopped | 40 (39 open, 1 closed) | 06:01:41Z | 6cc9d2de3e2e4a7cf04b1568f7a9dd2c110ab4fbe861f22ce67c7b7dda797407 |

I read 3 pages, 39 rows, 38 distinct pull requests (#274 appears on pages 1 and 2). The reported total rose 38, 39, 40 while I paged, because the account verexxi was opening new claims every few seconds, so the three pages are not one consistent snapshot. I therefore took two consistent snapshots with the REST API (2 calls of the allowed 4): https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1

- Snapshot 1: HTTP 200, server Date 06:03:01 GMT, 100 pull requests (#222 to #327), 46 with the problem id in the title. sha256 73b6bba1b57926c1a4c790e6e719dab7d2dfaaf92f9c6365c3ced17a8a52002b
- Snapshot 2: HTTP 200, server Date 06:11:53 GMT, 100 pull requests (#223 to #328), 47 with the problem id in the title: 46 open drafts and 1 closed draft (#260), none merged. All 47 are by the account verexxi. sha256 194814f44dd3f8b04d18b53017ee1536fcb94aba6e1b8342338f23d70f2fd946
- The 38 pull requests from the HTML pages are all among the 47; the other 9 are #320 to #328 (opened after my page 1).
- Scan of all 100 titles and bodies in snapshot 2 for codetables, QECC, qubit, stabilizer, quantum, Grassl: 47 hits, every one titled with the problem id; nothing under other titles, nothing from other authors. Older pull requests (REST pages 2 to 4) were not fetched; the HTML search, which covers the whole repository and all states, found nothing before #257.

Cells claimed (47, each as old bound to new bound): [[105,4]] 35 to 34; [[110,2]] 37 to 36; [[110,5]] 37 to 35; [[115,2]] 39 to 38; [[120,2]] 40 to 39; [[122,1]] 41 to 40; [[123,2]] 41 to 40; [[125,4]] 41 to 40; [[127,2]] 42 to 41; [[129,2]] 43 to 42; [[132,1]] 45 to 43; [[133,2]] 45 to 43; [[135,1]] 45 to 44; [[135,8]] 43 to 42; [[139,1]] 47 to 45; [[140,2]] 47 to 45; [[142,2]] 48 to 46; [[145,1]] 49 to 47; [[146,2]] 49 to 47; [[148,2]] 50 to 48; [[150,1]] 51 to 49 (closed, #260); [[152,1]] 51 to 49; [[154,1]] 52 to 50; [[155,6]] 53 to 49; [[158,1]] 53 to 51; [[159,2]] 53 to 51; [[161,2]] 55 to 52; [[164,1]] 55 to 53; [[165,2]] 55 to 53; [[165,6]] 53 to 52; [[171,1]] 57 to 55; [[173,2]] 59 to 56; [[177,1]] 59 to 57; [[183,1]] 61 to 59; [[185,3]] 63 to 60; [[195,2]] 65 to 64; [[200,2]] 67 to 65; [[200,5]] 67 to 64; [[200,10]] 67 to 62; [[207,2]] 69 to 68; [[213,2]] 71 to 70; [[215,6]] 73 to 71; [[219,2]] 73 to 72; [[225,2]] 75 to 74; [[230,3]] 77 to 74; [[230,5]] 77 to 73; [[230,10]] 77 to 72. All old bounds equal the table values in the claim package.

Findings:
- No pull request claims [[155,3]], and no body mentions 155,3. The only title or body mentioning n = 155 is #317 ([[155,6]], 53 to 49); a bound on k = 6 does not bound k = 3 from above under R1 to R3.
- The only k = 3 cells are [[185,3]] (to 60) and [[230,3]] (to 74); by R2 they give (155,3) at most 60 and 74.
- Implication test: no claimed cell equals (155,3), and none implies 50 or lower through R1, R2 or R3 (best implied: 51, section 3).

## 5. TROPHY_CASE.md on main

- URL: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md. HTTP 200, 30936 bytes, server Date 06:03:56 GMT, served from cache (X-Cache HIT, max-age 300). sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9
- Identical to data/TROPHY_CASE_pinned_9b1d444.md once line endings are normalised (the pinned copy has CRLF, 31036 bytes, sha256 cdfe852481ba85e35ccbc386d64ce88de92a56eb73d1ec3e44cdc9a3b86345ad).
- 53 numbered rows in 7 families: constant-weight-codes, degree-diameter, fast-matrix-multiplication, lehmer, robustbench-cifar100, sealed-envelopes/bouchaudy-cipher-machines, vnncomp-2026. No codetables or qubit-code row. The constant-weight rows are classical codes.

## 6. Literature, window 2024-10-17 to 2026-10-17

arXiv refused. Three API requests (machine clock 06:05:17Z, 06:05:23Z, 06:05:30Z, 6 to 7 s apart) all returned HTTP 429 and were not retried. I made 3 further arXiv-host requests through the fetch tool: the author listing for M. Grassl (readable, but the tool's summary was sloppy), the HTML of arXiv 2603.19901 (readable), and the PDF of arXiv 2601.15446 (failed: size limit exceeded). That is 6 arXiv-host requests, the cap. I did not log times for those three; they were in separate turns.

Fallback channels, as the rules allow:
- OpenAlex, filter from_publication_date 2024-10-17. Six queries returned HTTP 200: stabilizer codes upper bound minimum distance linear programming (967 matches, 50 listed); quantum codes linear programming bound shadow enumerator (257, 50); additive quantum codes table of bounds minimum distance codetables (7, 7); semidefinite programming upper bound quantum error-correcting codes (735, 50); nonexistence of qubit stabilizer codes upper bound minimum distance (8, 8); quantum weight enumerator MacWilliams bound new upper bounds qubit codes length 256 (11, 11). 162 distinct works reviewed. Four more queries then got HTTP 429, and one polite retry later got 429 with Retry-After 64034 s (daily credit limit), so OpenAlex stopped there.
- Crossref, filter from-pub-date 2024-10-17. Two queries returned HTTP 200 (5703 and 5904 matches, 60 listed each, 111 distinct works).
- Web search: 4 queries answered (including the exact string "[[155,3" with qubit stabilizer code upper bound); a fifth was refused because the session search budget was used up.
- Mirror fetch of arXiv 2601.15446 via alphaxiv.org (second-hand, not the PDF).

What the searches turned up (titles and abstracts only unless stated):
- arXiv 2603.19901, SDP bounds on quantum codes: rational certificates (2026-03-20): "improve upon 18 upper bounds on the maximum size of n-qubit codes with 6 ≤ n ≤ 19". Confirmed in the fetched HTML. Far from n = 155.
- arXiv 2601.15446, Check-weight-constrained quantum codes: Bounds and examples (Wang, Liu, Li, Kubica, Gu; 21 Jan 2026), as relayed by the mirror: floating-point Gurobi LP; "We therefore chose to only process bounds for n ≤ 100 and extrapolated values beyond 100"; precision problems at large n; its n above 100 entries are code constructions; n = 155 not present. I could not read the PDF itself.
- arXiv 2601.19848, Theory of low-weight quantum codes: LP framework with exact results for n up to 9.
- Linear Programming Bounds on k-Uniform States (2025-03-04): local dimension q up to 9; its "code tables maintained by Grassl" remark concerns q = 4 k-uniform states, not qubit stabilizer codes.
- A Quantum Analog of Delsarte's Linear Programming Bounds (arXiv 2502.14165, thesis), MacWilliams Identities for Intrinsic Quantum Codes (arXiv 2604.16023), mixed-dimensional quantum MacWilliams identity (2026), additive twisted codes (Designs, Codes and Cryptography 2025; constructions, so lower bounds), Monte Carlo upper bound on the distance of a given code (Entropy 2025): none gives an upper bound for [[155,3]] or any qubit cell with n above 100.
- Grassl's arXiv listing (via the fetch tool): newest items concern entanglement-assisted Singleton bounds, the punctured dodecacode, SIC-POVMs and puncturing; no bound table. The qubit table's own stamps are 10.06.2024 (cell page) and 23.05.2024 (full table), consistent with no update in the window.

I found no paper in the window that states any upper bound on d for [[155,3]], at or below 50 or otherwise.

## 7. Reasoning

- The live cell says 53. The claim says no code at d = 51, so at most 50: 3 below the cell, 2 below the live closure (52), and 1 below the best bound the repository's own draft claims would imply (51). That is a strict improvement in every comparison, not a tie.
- The 47 pull requests are unreviewed draft claims from one account; even taking all of them as true they leave (155,3) at 51. Nobody else has a pull request on this target.
- TROPHY_CASE.md has nothing on qubit-code bounds.
- Literature: the closest items are SDP bounds at n up to 19 and an LP paper that stops short of n = 100 because of floating-point limits. That is consistent with the table's own note that its n above 100 bounds are weak, and with the idea that an exact-arithmetic certificate at n = 155 has not been published.

Limits, stated plainly:
1. A negative literature result cannot be proved. The arXiv API refused, OpenAlex hit its credit limit, and web search hit its budget, so coverage is OpenAlex (6 queries), Crossref (2), web search (4) and 3 fetch-tool reads. Work older than 24 months was not searched; the live table is taken as the record of it.
2. I did not audit the certificate's soundness; that belongs to other reviewers. As a sanity step I ran claim/check/check_cert.py on result/cert_155_3_51_sh.json and result/cert_155_3_53_sh.json: both printed VERIFIED (each about 0.4 s, exit code 0).
3. The pull-request queue was moving. My last snapshot is 06:11:53 GMT; a claim opened after it is not covered (none of the 47 seen concerns (155,3)).
4. Neighbour cells come from the claimant's table snapshot, not from a fresh fetch.

pass: true
