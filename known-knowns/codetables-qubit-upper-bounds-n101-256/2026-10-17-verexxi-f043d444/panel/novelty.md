# Novelty check: no [[125,4,41]] qubit stabilizer code (claimed upper bound 40 on [[125,4]])

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)

novelty: NOVEL as far as checked: the live codetables.de upper bound for [[125,4]] is 41 (24-41, fetched 2026-10-17T05:26:18Z, HTTP 200), the claimed 40 is strictly below it and below every bound implied by other live cells, no TROPHY_CASE.md row or pull request claims or implies it, and the arXiv searches that returned data (2 of the 6 permitted requests; 4 were throttled) found no bound for this cell.

Scope: novelty only. I read CLAIM.md and REPRODUCE.md and the files they name. I ran the claim's own checker once for context (it prints VERIFIED for result/cert_125_4_41_sh.json); I did not independently validate the LP proof, that is for the correctness panel.

## 1. Status source, fetched once, no retries

- Command: curl -s -A "V3R1T4S-verexxi" -o work/cell.html -w '%{http_code}' "https://codetables.de/QECC.php?q=4&n=125&k=4"
- UTC (date -u) before and after the request: 2026-10-17T05:26:18Z and 2026-10-17T05:26:19Z. curl exit 0. HTTP status 200. 63579 bytes.
- sha256 (sha256sum): 7907ff3b963f3557d2fa6f91d771451aad2666cbfe77e64b50136c843412b3ea
- That hash is identical to the claim-time file data/QECC_q4_n125_k4_claimtime.html (CLAIM.md records the same hash), so the cell page is byte for byte what the claimant saw at 2026-10-17T00:29:19Z. Nothing changed at this cell in the roughly five hours between the two fetches.
- Value read from the page text: "Bounds on [[125,4]] ... lower bound: 24 upper bound: 41".
- Notes printed on the same page: "last modified: 2024-05-08", footer "Last change: 10.06.2024", "Most upper bounds on qubit codes for n up to 100 are based on a MAGMA program by Eric Rains", and "For n above 100, the upper bounds on qubit codes are weak (and not necessarily monotone in k)". The table has not been touched since June 2024, which is before my 24-month literature window.
- So the claimed bound 40 is exactly one below the live 41: a strict improvement, not a tie.

## 2. This repo (github.com/elder-plinius/V3R1T4S), 3 requests in total

1. TROPHY_CASE.md on main: curl of the raw file on the main branch, UTC 2026-10-17T05:28:31Z, HTTP 200, 30936 bytes, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9. The pinned copy in the package (data/TROPHY_CASE_pinned_9b1d444.md, 31036 bytes, sha256 cdfe852481ba85e35ccbc386d64ce88de92a56eb73d1ec3e44cdc9a3b86345ad) differs only by CRLF line endings (100 carriage returns = the 100 extra bytes); after normalising line endings a diff of the two is empty. The file lists 53 rows: 7 degree-diameter, 35 constant-weight codes, 5 matrix multiplication, 1 Lehmer, 2 cipher commitments, 2 VNN-COMP, 1 RobustBench. A case-insensitive grep for quantum, stabili, codetables, qubit, [[, 125,4, n=125, grassl and QECC found 0 matches. There is no quantum-code row at all, so nothing at [[125,4]] and nothing that implies it.
2. Pull requests, page 1: https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit , UTC 2026-10-17T05:29:22Z, HTTP 200, 348281 bytes, sha256 97e96754d050805cd708e278a96c11fd0f05ca3d8ee5ffcb12abce238fb2f786. The embedded JSON says totalCount 34, openCount 33, closedCount 1, totalPages 2 (25 results on this page). The query has no state filter, so it covers open and closed.
3. Pull requests, page 2: https://github.com/elder-plinius/V3R1T4S/pulls?page=2&q=is%3Apr+codetables-qubit , UTC 2026-10-17T05:30:17Z, HTTP 200, 281382 bytes, sha256 0060403e7a77ea29221a74f69dedf2a2421433ae302909c0310d892f36b891c7 (9 results).

All 34 are drafts by the account verexxi, all titled "[claim] codetables-qubit-upper-bounds-n101-256: [[n,k]] upper bound lowered from X to Y" (PR 260 is the closed one). Cells: [[105,4]], [[110,2]], [[120,2]], [[122,1]], [[123,2]], [[127,2]], [[129,2]], [[132,1]], [[133,2]], [[135,1]], [[139,1]], [[140,2]], [[142,2]], [[145,1]], [[146,2]], [[148,2]], [[150,1]] (closed), [[152,1]], [[154,1]], [[158,1]], [[159,2]], [[164,1]], [[165,2]], [[171,1]], [[177,1]], [[183,1]], [[200,2]], [[200,5]], [[207,2]], [[213,2]], [[219,2]], [[225,2]], [[230,3]], [[230,5]]. No PR is at [[125,4]].

Cross-check of the table snapshot: for all 34 PRs the "from" value equals the upper bound in the package's full-table snapshot (0 mismatches). That snapshot (data/qubit_table_full_n1-256.html) has the sha256 CLAIM.md states, 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6, and 33152 cells, which is every (n,k) with 0 at most k at most n at most 256.

## 3. Does any other cell already imply the bound? (own code, work/closure_check.py)

I wrote my own parser and closure rather than using check/parse_table.py and check/propagate.py. Rules: R1 d(n,k) at most d(n,k-1) for k at least 2; R2 d(n,k) at most d(n+1,k); R3 d(n,k) at most d(n-1,k+1)+1; and as an extra, R4 d(n,k) at most d(n-1,k)+1 (Calderbank-Rains-Shor-Sloane Theorem 6d).

- Snapshot cells near the target (lower-upper): (125,4) 24-41 (same as the live page); (125,3) 25-41; (125,2) 25-41; (125,1) 27-41; (126,4) 24-42; (124,5) 24-41; (125,5) 24-41; (124,4) 24-41.
- Closure of the live table at (125,4): 41, equal to the stated value. With R4 added: still 41. This agrees with check/propagation_check.txt.
- Closure of the live table plus all 34 PR claims, assuming every one is correct and including the closed one: still 41 at (125,4), with or without R4. The claims lower the closure of 475 other cells but not this one.
- Smallest bound any single claimed cell implies at (125,4): 41, from PR 300 ([[127,2]] 42 to 41), which only ties the table's 41. Next are 42 ([[129,2]] to 42; [[123,2]] to 40, which costs two R3 steps). All other claimed cells imply 43 or more. (The script labels the two k=5 claims "unreachable" because of a shortcut in its cost formula; by hand they imply 65 and 74 via one R3 step. The full closure above handles them correctly and is unaffected.)
- Side observation: the snapshot is not closed under these rules in 1100 cells (for example (124,5) is stated 41 but its closure is 40, and (123,6) is stated 41 with closure 39). This fits the page's own note that the n above 100 bounds are weak, and it does not matter here because the R3 route into (125,4) from (124,5) gives 40+1 = 41. R3 is only valid for pure codes, so using it can only make my closure stronger than the truth, and it still does not reach 40.

## 4. Literature, last 24 months (submitted 2024-10-17 to 2026-10-17), 6 arXiv requests, each at least 36 s after the previous one

1. export.arxiv.org API, UTC 2026-10-17T05:34:29Z to 05:35:15Z, HTTP 503 (bare "503" page), no data. Abstract terms: linear programming / weight enumerator / shadow enumerator / semidefinite, with quantum code(s) / stabilizer code(s) / quantum error-correcting codes.
2. API, 2026-10-17T05:35:51Z, HTTP 429 body "Rate exceeded.", no data. Abstract: "stabilizer codes" AND "linear programming".
3. API, 2026-10-17T05:37:56Z to 05:38:26Z, HTTP 429, no data. Abstract: quantum AND "linear programming" AND stabilizer.
4. API, 2026-10-17T05:41:15Z to 05:41:46Z, HTTP 429, no data. Same query as 3, after a 150 s wait.
5. arxiv.org advanced search (web, not the API), 2026-10-17T05:44:35Z to 05:44:54Z, HTTP 200, 89423 bytes, sha256 7fbc7cc5b3d5146b3e8e8c98ff413b2fe659fc55c1ee1173cd91486b8d565163. Abstract: "linear programming" quantum stabilizer. 15 results.
6. arxiv.org advanced search (web), 2026-10-17T05:47:20Z to 05:47:32Z, HTTP 200, 150273 bytes, sha256 8748540808b1cf5803039bdcb1c8e2a06176489e5e72b0f992c501bf122f343f. Title: bounds quantum codes (page size 200). 30 results.

The date filter was the date of the most recent version, so it also lists older papers revised in the window and cannot miss a paper first submitted in the window. Requests 5 and 6 together return 42 distinct papers (3 appear in both). I read the abstracts of every hit that touches distance bounds for quantum codes and scanned all abstracts and titles for 125, 256, codetables, "up to length" and [[125.

- 2408.10323, SDP bounds on quantum codes (Munne, Nemec, Huber): semidefinite hierarchy, examples (7,1,4), (8,9,3), (10,5,4) only.
- 2603.19901, SDP bounds on quantum codes: rational certificates (Munne, Huber): "improve upon 18 upper bounds ... n-qubit codes with 6 at most n at most 19". Closest in method (exact rational certificates), but n is at most 19.
- 1602.00413, LP bounds for entanglement-assisted codes (Lai, Ashikhmin): small codes, length up to about 28.
- 2601.19848 and 2601.15446: check-weight-constrained stabilizer codes (LP, n at most 9 / tens to hundreds of qubits but with weight constraints). Not the unconstrained [[125,4]] distance.
- 2604.25790 (mixed-dimensional MacWilliams/shadow, AME states), 2608.10922 and other locally recoverable code papers, 2610.09900 (Delsarte theory for quantum association schemes): not about this cell.
- No abstract or title mentions 125, 256, a table of qubit-code bounds above n = 100, or codetables. No hit gives any upper bound for [[125,4]], so nothing at or below 40.

## 5. Reasoning

- Against the live table the claim is a strict improvement: 41 to 40.
- The new bound is not implied by the table: the closure of the live table at (125,4) is 41, even with the extra rule R4.
- It is not implied by anything in this repo: no TROPHY_CASE.md row concerns quantum codes, no PR is at [[125,4]], and even if all 34 sibling claims are right the closure at (125,4) stays 41. The nearest sibling, [[127,2]] to 41, only ties the table.
- The table's own note says its n above 100 bounds are weak, and the 34 sibling claims (e.g. [[123,2]] and [[122,1]] from 41 to 40) show the same flat region being lowered by 1 by the same kind of LP-with-shadow argument. A one-step improvement at (125,4) is consistent with that, and nothing found in the literature contradicts it.
- A tie is not a record: this is not a tie.

## 6. Limits, stated plainly

- Literature coverage is thinner than intended: only 2 of the 6 permitted arXiv requests returned data (the other 4 were a 503 and three 429s from arXiv). The two that worked cover LP-style abstracts and titles with "bounds" for quantum codes. A bound that appears only in a paper body or appendix, or in a paper with different vocabulary (for example additive codes over GF(4), or a table paper with no "bounds" in the title), would not have been seen. I judge the chance of such prior art as small, but I did not rule it out. A spot check on arXiv by author (Grassl, Rains, Huber, Nemec) before any public post would close this.
- Neighbour cells were evaluated from the package's full-table snapshot (hash verified, 34 independent PR "from" values match it), not re-fetched, because the rule was to fetch the status page once. Only the (125,4) page was fetched live, and it matches the snapshot.
- PR search used the token "codetables-qubit" and I read titles only, not PR bodies. A competing PR with different wording and no mention of codetables and qubit could be missed. I made 3 GitHub requests and no more.
- If a later PR lowers any of (125,1), (125,2), (125,3), (126,4) or (127,2) to 40 or below, this claim would become implied by that one. None exists as of 2026-10-17T05:30:17Z.

pass: true