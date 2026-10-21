# Novelty review: [[190,2]] qubit stabilizer codes, no [[190,2,63]] (upper bound 62)

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)

novelty: PASS - the claimed upper bound 62 for [[190,2]] is strictly below the live codetables.de bound 64 (HTTP 200, read 2026-10-17T05:59:07Z on my local clock) and below the bound 63 implied by propagation from other live cells; no pull request, TROPHY_CASE.md entry or last-24-month literature result at or below 62 was found (arXiv refused every request, so OpenAlex and web search were used).

Scope: novelty only. I did not review whether the linear-programming formulation or the certificate is sound; other panel members do that. I re-ran the supplied checker once as a sanity run (section 6). Files are named relative to claim/ (the claim package) and work/ (my scratch folder).

## 1. Status source, fetched once

- URL: https://codetables.de/QECC.php?q=4&n=190&k=2
- Command (one request, no retry): curl -s -A "V3R1T4S-verexxi" -o work/cell.html -w '%{http_code}' with that URL.
- Time (output of date -u run immediately before and after the request): 2026-10-17T05:59:07Z and 2026-10-17T05:59:08Z.
- HTTP status: 200. Size 1523 bytes. sha256 36d83bf11f5ab16750c67c59692941cb2c0f80013f3e25951e59c63821687798.
- Values found on the page: "Bounds on [[190,2]]" with lower bound 37 and upper bound 64. Page footer: "Last change: 10.06.2024".
- cmp of work/cell.html against claim/data/QECC_q4_n190_k2_claimtime.html reported the files byte-identical, and the sha256 equals the one stated in CLAIM.md. So the cell is unchanged since the claim-time capture (2026-10-17T05:35:32Z per CLAIM.md).
- Clock note: in this session my local clock (date -u) read between 27 and 54 seconds behind the Date header that GitHub returned for requests made at nearly the same moment. Times in this file are quoted exactly as date -u printed them; true times are probably up to a minute later.
- I did not re-fetch the complete table. Neighbour cells below come from claim/data/qubit_table_full_n1-256.html, whose sha256 (26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6) equals the value stated in CLAIM.md. The (190,2) cell itself was verified live as above.

## 2. Propagation check (my own script work/my_propagate.py, written for this review, not the claim's scripts)

Rules used (from the task statement): R1 d(n,k) at most d(n,k-1) for k at least 2; R2 d(n,k) at most d(n+1,k); R3 d(n,k) at most d(n-1,k+1) plus 1. The closure uses cells with k at least 1 (the file holds 33152 cells, n from 1 to 256).

- Table values: (190,1) 37-64; (190,2) 37-64; (191,2) 37-65; (189,3) 36-63; (188,4) 36-63; (186,6) 35-59.
- Closure at (190,2) from the table alone: 63. Witness chain: (190,2) from (189,3) plus 1, (189,3) from (188,4) plus 1, (188,4) from (187,5) plus 1, (187,5) from (186,6) plus 1, and the table has 59 at (186,6); 59 + 4 = 63. So the best bound already implied by other live cells is 63, one below the cell's own 64.
- Adding the further rule d(n,k) at most d(n-1,k) plus 1 does not change the closure (still 63).
- This reproduces the claim's own figure (closure 63, claim/check/propagation_check.txt) with separately written code.
- The claimed bound 62 is therefore strictly below both the cell (64) and the propagated value (63).
- Consequence worth stating: the d = 63 certificate is what makes the claim novel. A proof for d = 64 alone (claim/result/cert_190_2_64_sh.json) would give the bound 63, which equals the propagation closure: a tie, not a record. The headline claim rests on the d = 63 certificate.

## 3. Pull requests

Query: https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit&page=N, plain requests with User-Agent V3R1T4S-verexxi. The page embeds its list as JSON, so the HTML was parseable and the REST fallback was not required for the main read. The list grew while I worked (the same account kept opening claim PRs), so I re-read pages. Times are my local clock:

- page 1, 2026-10-17T05:59:35Z, HTTP 200: totalCount 36, 25 listed, sha256 eacf0ae7a07462a9ddb2f4a6fd688ddafddbc4b745457d518c3f54fcedb08ff2
- page 2, 2026-10-17T06:00:28Z, HTTP 200: totalCount 38, 13 listed, sha256 77ba2e728b14b7fbbb0a13bd78aabdb5f03ab2ca2b50b8346a8dd037e3565420
- page 3, 2026-10-17T06:02:03Z, HTTP 200: totalCount 43, no pull requests listed (the stop condition), sha256 d7d2794d8ae3d1cf644a5d26f97c43ec9f44acb6f5e0e09438c925d4000ba714
- page 1 again, 2026-10-17T06:02:04Z, HTTP 200: totalCount 44, 25 listed, sha256 0b6bdba2a454a56fc1ef643ad06e1726a57e3b254a921771e7563c418326ae3a
- page 2 again, 2026-10-17T06:02:05Z, HTTP 200: totalCount 43, 18 listed, sha256 cd8facc4f19333c6014dbf620d62b64ee7196d1189c43fb6541e04c6fdfbdb8d
- page 1, final re-check, 2026-10-17T06:08:27Z, HTTP 200: totalCount 47 (46 open, 1 closed), 25 listed, sha256 30ed909a00d876f3707b8b76754bbdab3bbced2cce51e3276844be5bbf564dd0. Every number listed was already in the REST snapshot below, and 47 equals the number of matching pull requests in that snapshot, so nothing new had appeared.
- Total: 6 HTML requests over 3 distinct pages (page 1 three times, page 2 twice, page 3 once). Distinct pull requests matching codetables-qubit: 47 (46 open, 1 closed), all opened by the account verexxi, numbers 257 to 328.

Because the HTML list moved between requests, and because a text query can miss a pull request that lacks the phrase, I also read the whole repository through the REST API (4 requests, 2026-10-17T06:02:51Z to 06:02:55Z, all HTTP 200, with 100, 100, 100 and 20 items; sha256 194814f44dd3f8b04d18b53017ee1536fcb94aba6e1b8342338f23d70f2fd946, 1d44a649462cdeeef139789891067c558a9d0697b1596b355b5746acc056125e, 046f58120b39d976127872073d410a1589e862fba879386e155fc6cb0e10e23b, a876dde80b566bdeb18891f8c9c902d8a3c932cb7771fdf3a25d4870fb33d5a0). That gave 320 distinct pull requests of all states (89 open, 149 closed without merge, 82 merged), numbers 1 to 328.

Every cell [[n,k]] found in the 47 matching titles (all titled "[claim] codetables-qubit-upper-bounds-n101-256: [[n,k]] upper bound lowered from A to B"; for the 46 open ones, A equals the live table bound of that cell):
  k=1: [[122,1]] 41 to 40 (#298); [[132,1]] 45 to 43 (#257); [[135,1]] 45 to 44 (#302); [[139,1]] 47 to 45 (#258); [[145,1]] 49 to 47 (#259); [[150,1]] 51 to 49 (#260, closed); [[152,1]] 51 to 49 (#261); [[154,1]] 52 to 50 (#262); [[158,1]] 53 to 51 (#266); [[164,1]] 55 to 53 (#267); [[171,1]] 57 to 55 (#303); [[177,1]] 59 to 57 (#277); [[183,1]] 61 to 59 (#278)
  k=2: [[110,2]] 37 to 36 (#296); [[115,2]] 39 to 38 (#324); [[120,2]] 40 to 39 (#297); [[123,2]] 41 to 40 (#299); [[127,2]] 42 to 41 (#300); [[129,2]] 43 to 42 (#301); [[133,2]] 45 to 43 (#270); [[140,2]] 47 to 45 (#271); [[142,2]] 48 to 46 (#272); [[146,2]] 49 to 47 (#273); [[148,2]] 50 to 48 (#274); [[159,2]] 53 to 51 (#275); [[161,2]] 55 to 52 (#318); [[165,2]] 55 to 53 (#276); [[173,2]] 59 to 56 (#319); [[195,2]] 65 to 64 (#328); [[200,2]] 67 to 65 (#279); [[207,2]] 69 to 68 (#304); [[213,2]] 71 to 70 (#305); [[219,2]] 73 to 72 (#306); [[225,2]] 75 to 74 (#307)
  k=3: [[185,3]] 63 to 60 (#320); [[230,3]] 77 to 74 (#281)
  k=4: [[105,4]] 35 to 34 (#269); [[125,4]] 41 to 40 (#325)
  k=5: [[110,5]] 37 to 35 (#316); [[200,5]] 67 to 64 (#280); [[230,5]] 77 to 73 (#282)
  k=6: [[155,6]] 53 to 49 (#317); [[165,6]] 53 to 52 (#327); [[215,6]] 73 to 71 (#322)
  k=8: [[135,8]] 43 to 42 (#326)
  k=10: [[200,10]] 67 to 62 (#321); [[230,10]] 77 to 72 (#323)

Checks against [[190,2]]:
- No title, branch name or body among all 320 pull requests names [[190,2]]. A search of all titles and branch names for the number 190 found only four unrelated pull requests (constant-weight code A(45,8,7), a spherical-code constant, two packing submissions). A search of all bodies for 190,2 patterns found only an unrelated matrix-multiplication claim.
- No claim at (190,1), at (189,3), or at (n,2) for n from 191 to 194. The nearest k=2 claims above are [[195,2]] 65 to 64 (#328), [[200,2]] 67 to 65 (#279) and [[207,2]] 69 to 68 (#304); by R2 they would give 64, 65 and 68 for (190,2), none at or below 62.
- Longer chains: I re-ran the closure with all 46 open claims applied as if accepted. The closure at (190,2) stays 63 (same witness chain). The best any claim within reach of (190,2) gives is 64.
- All 47 are pending claims by the same account, not published results, and none touches this cell.

## 4. TROPHY_CASE.md on main

- URL: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, fetched 2026-10-17T06:03:43Z, HTTP 200, 30936 bytes, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9.
- Occurrence counts for codetables, qubit, stabilizer, quantum and the string [[190 are all 0. The file lists degree-diameter graphs, constant-weight codes, matrix multiplication, the Lehmer bound, VNN-COMP and RobustBench rows and two cipher commitments.
- It equals claim/data/TROPHY_CASE_pinned_9b1d444.md (sha256 cdfe852481ba85e35ccbc386d64ce88de92a56eb73d1ec3e44cdc9a3b86345ad, 31036 bytes) except for line endings: the pinned copy has 100 carriage returns, the main copy has none, and a diff after removing carriage returns printed nothing.
- So main holds no record for qubit upper bounds.

## 5. Literature search, last 24 months (2024-10-17 to 2026-10-17)

arXiv: refused. Six API requests (export.arxiv.org, date-limited queries on quantum linear-programming bounds, stabilizer-code upper bounds, GF(4) additive codes, weight and shadow enumerators, semidefinite bounds, qubit-code tables), spaced at least 6 seconds apart, local times 06:05:13Z, 06:05:34Z, 06:05:40Z, 06:06:02Z, 06:06:38Z, 06:06:45Z. All six returned HTTP 429 (Too Many Requests). I made no further arXiv API requests and did not retry. Script: work/arxiv_search.py.

OpenAlex (api.openalex.org, filter from 2024-10-17, relevance-ranked, first 25 results each), about 06:07 local: four searches, all answered with results: (A) quantum stabilizer codes upper bound minimum distance linear programming, 750 matches; (B) upper bounds qubit quantum codes table minimum distance length 256, 235; (C) quantum weight enumerator shadow enumerator bound qubit code, 127; (D) additive quaternary codes GF(4) quantum code distance bound, 37. That is 90 distinct works, of which 19 mention both a bound term and a code term. A later pair of OpenAlex requests (06:09:20Z and 06:09:22Z) was refused with HTTP 429 and not retried.

Web search: four calls (one of them expanded by the tool into several searches), including the exact string "[[190,2]] qubit stabilizer code upper bound minimum distance", a query for improved upper bounds for qubit stabilizer codes of length 101 to 256 by linear programming and shadow enumerators, a query for non-existence results at n=190, k=2, d=63, and a query on the puncturing paper below. None returned a result about [[190,2]] or a qubit-code bound table beyond n=100.

Works examined and why they do not reach 62 for [[190,2]]:
- Gundersen, Christensen, Grassl, Popovski, Wisniewski, "Puncturing Quantum Stabilizer Codes", IEEE JSAIT 6, 74-84 (2025), arXiv 2410.17754. I downloaded the author manuscript from the Aalborg repository (HTTP 200, 458801 bytes, sha256 90bae6689969591800809d411f2311584da03cdde7c21c2aaf48b4fa750fb2c2) and read Section IV. Theorem 1 (quantum Griesmer bound): n is at least the sum over i from 0 to k-1 of ceil(d/p^i). For [[190,2]] with p = 2 this reads 190 at least d + ceil(d/2), so d at most 126. The authors call their bound comparatively weak. The paper is mainly about constructions (lower bounds).
- Quantum Hamming bound, proved for every local dimension at least 3 and combined with an existing qubit result (arXiv 2606.22538, June 2026; I also saw arXiv 2606.15558, titled "Degeneracy Cannot Violate the Quantum Hamming Bound", and read only its title). My own computation for [[190,2]]: the largest d with the sum over j up to floor((d-1)/2) of 3^j C(190,j) at most 2^188 is 74. Quantum Singleton gives 95.
- "SDP bounds on quantum codes: rational certificates", arXiv 2603.19901 (March 2026): improves 18 bounds for n-qubit codes with n from 6 to 19. Not n = 190.
- "A Quantum Analog of Delsarte's Linear Programming Bounds", arXiv 2502.14165 (thesis, general quantum metric spaces); "Theory of low-weight quantum codes", arXiv 2601.19848 (linear programs for n at most 9); the mixed-dimensional quantum MacWilliams identity (Physical Review A 2026); intrinsic-code MacWilliams identities (arXiv 2604.16023); Monte Carlo distance upper bounds for given codes (Entropy 2025). None gives a bound table for qubit codes of length 190.
- Classical additive-code Griesmer papers (arXiv 2412.14615; Designs, Codes and Cryptography, November 2024) concern classical additive codes, not stabilizer distance bounds.
- The codetables.de page itself states that for n above 100 the qubit upper bounds are weak and not necessarily monotone in k, and its last change is dated 10.06.2024, which is outside the window.

Limits of this search: keyword search only; arXiv was unreachable, so the newest preprints rest on OpenAlex (which listed items up to 2026-10-05) and web search; I read full text only for the puncturing paper. I found no published bound for [[190,2]] below the table's own 64, other than the value 63 that follows from the table's neighbouring cells (section 2).

## 6. Reasoning

1. Primary record: the live cell says upper bound 64, unchanged since the claim was prepared. The claimed bound is 62.
2. Propagation from other live cells gives 63 at best (my computation agrees with the figure reported in claim/check/propagation_check.txt). 62 is strictly below it.
3. No pull request (47 matching ones, 320 in the repository) and no main-branch trophy entry concerns this cell, and even with every pending claim accepted the propagated bound stays 63.
4. No result in the last 24 months that I could find gives a distance bound for [[190,2]] qubit codes at or below 62; the general Griesmer (126), Hamming (74) and Singleton (95) bounds are far weaker.
5. Sanity run only: python -I check/check_cert.py result/cert_190_2_63_sh.json, run inside claim/, printed VERIFIED for [[190,2,63]] with shadow=True, a value of 2141 digits, every column coefficient at most 0, and 62+2+64 multipliers, and exited 0. This is the claim's own checker, not an independent verification, and soundness is outside this review.
6. Residual risks: (a) a very recent or non-indexed paper could exist that my keyword searches missed, since arXiv could not be queried; (b) the neighbour cells come from the claim-time table capture, not a fresh fetch (the table page states no change since June 2024); (c) the pull-request stream was still active, so a later pull request on this cell could appear after 06:08 local time; (d) the novelty depends on the d = 63 certificate being valid (section 2).

On the evidence above the result strictly beats everything I found, so I pass it on novelty.

pass: true
