# Novelty review: [[135,8]] qubit stabilizer codes, upper bound 43 lowered to 42 (codetables-qubit-upper-bounds-n101-256)

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: NOVEL as far as checkable: the live codetables.de cell [[135,8]] reads 25-43 (HTTP 200, 2026-10-17T05:26:53Z), the claimed 42 is strictly below it, it is not implied by any live neighbour (closure stays 43) nor by any of the 34 claims in this repo's codetables-qubit pull requests, and TROPHY_CASE.md plus the in-window literature show no result at or below 42 for this cell; caveat: the arXiv API refused all 6 permitted requests (HTTP 429/503), so the literature leg was done through OpenAlex and web search instead.

Scope: only the claim package (claim files are named relative to claim/) plus the sources the instruction names. My scratch files are under work/, next to claim/. Every time, hash, value and HTTP status below was copied from command output in this session. I did not assess the mathematics of the certificate (that is a soundness question, not novelty).

## 1. Status source, fetched once (no retry)

Command: curl -s -A "V3R1T4S-verexxi" -o work/cell.html -w '%{http_code}' 'https://codetables.de/QECC.php?q=4&n=135&k=8'

- UTC from date -u, taken immediately before the request: 2026-10-17T05:26:53Z
- curl exit code 0, HTTP status 200, 1523 bytes
- sha256: 98f7ab4b286f9e163f24a0a4518963451cedc989b13ed0f3d52ad4556ef51f91
- Value on the page ("Bounds on [[135,8]]"): lower bound 25, upper bound 43
- cmp against data/QECC_q4_n135_k8_claimtime.html (fetched by the claimant at 2026-10-17T00:29:55Z according to CLAIM.md): byte-identical, and the hash equals the one CLAIM.md records
- The page itself says that qubit upper bounds for n above 100 are weak and not necessarily monotone in k.

Freshness check of the three direct propagation neighbours, one request each, same command form, 6 seconds apart, all HTTP 200, 1523 bytes each:
- [[135,7]], 2026-10-17T05:32:40Z: lower 25, upper 43, sha256 076b771abfbb2e9b6516ac3f241013496a5235c61127a3ae1fd356cf6ad37e27
- [[136,8]], 2026-10-17T05:32:46Z: lower 25, upper 43, sha256 e26fc8c91ba5aea4083218232ae3cae34c7c53da6943621dc2c60b629800d90f
- [[134,9]], 2026-10-17T05:32:52Z: lower 24, upper 42, sha256 a995d6f5dc09720ada4719896fe5f06ad6073ee6b81c49a15e5df0aa0ed82c01

Result: the live upper bound is 43, so the claimed 42 is a strict improvement by 1 (not a tie).

## 2. Is 42 already implied by other live cells? No.

- The package's complete qubit table, data/qubit_table_full_n1-256.html, has sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6 (equal to CLAIM.md). I re-ran the claim's check/parse_table.py and check/propagate.py on it: 33152 cells parsed, live (135,8) = [25, 43], closure at (135,8) = 43.
- I also wrote my own parser and relaxation (work/my_closure.py, not using the claim's scripts): closure at (135,8) = 43. The three rule inputs are R1 from (135,7) = 43, R2 from (136,8) = 43, R3 from (134,9) plus 1 = 42 + 1 = 43. The live re-reads in section 1 agree with these inputs.
- Side observation: 1075 cells (1072 with n above 100) sit above their own closure, so the table is not closed for n above 100, but (135,8) itself is exactly at its closure.
- Classical bounds computed here with Python: the quantum Hamming bound for [[135,8]] excludes only d of at least 51 (log2 of the sphere sum is 114.15 at t = 21 and 129.56 at t = 25, against n minus k = 127); the quantum Singleton bound gives d at most 64. Neither touches d = 43.
- Direction check: the table has 42 at (135,9) and (134,9). By Rains' monotonicity result (quant-ph/9802070, abstract read) LP feasibility carries down to lower dimension, so LP infeasibility at k = 9 says nothing about k = 8; and R3 from (134,9) gives only 43. So these cells do not imply 42 at (135,8).

## 3. This repo (github.com/elder-plinius/V3R1T4S)

Three requests to GitHub in total (the cap), all HTTP 200:

1. 2026-10-17T05:27:44Z, curl of https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit, 348281 bytes, sha256 5eb99b0f304c03599d0bea653a6f0015ab2bac9405f96a1fa6e307583ddf5705. The embedded page data says totalCount 34, openCount 33, closedCount 1, page 1 of 2, 25 results.
2. 2026-10-17T05:28:45Z, same query with page=2, 281383 bytes, sha256 f72da414a58bcc3842ef3a829bc0d0bdc69834d5bfa710989b9872a54f2ba693, 9 results.
3. 2026-10-17T05:30:40Z, https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, 30936 bytes, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9.

TROPHY_CASE.md on main: 53 rows (constant-weight codes 35, degree-diameter 7, fast matrix multiplication 5, Lehmer 1, RobustBench 1, cipher commitments 2, VNN-COMP 2). A grep for qubit, quantum, stabilizer, codetables, QECC and [[n,k patterns finds nothing. The pinned copy in the package (data/TROPHY_CASE_pinned_9b1d444.md) has CRLF line endings; after stripping carriage returns both files hash to 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9, so main has not moved on that file.

Pull requests: all 34 matches are titled "[claim] codetables-qubit-upper-bounds-n101-256: [[n,k]] upper bound lowered from X to Y", all by one author (verexxi), 33 open drafts and 1 closed (number 260). Numbers 257-262, 266, 267, 269-282 and 296-307. Their cells all have k between 1 and 5 (k = 1: 13 cells, k = 2: 17, k = 3: 1, k = 4: 1, k = 5: 2). None is at [[135,8]], and none is at (135,7), (136,8) or (134,9). In every PR the stated old value equals the table's upper bound in the package's table.

Implication check on those 34 claims, using the bank's three rules: a claim of value v at (n, k) bounds (135,8) by v + max(0, 135 minus n, k minus 8). The smallest result over all 34 claims is 44 (number 302, [[135,1]] from 45 to 44), which is worse than the live 43. Re-running the closure with all 34 claims overlaid on the live table (and again without the closed one) still gives 43 at (135,8). So no claimed cell implies 42 or even ties the claim.

Limit: the PR search is text-based on the string codetables-qubit; a differently-titled PR would not appear, and I made no further GitHub calls because of the 3-call cap.

## 4. Literature, last 24 months (2024-10-17 to 2026-10-17)

arXiv API (export.arxiv.org/api/query with a submittedDate window), 6 requests, at least 5 s apart. All six failed, so they produced no data:
- 2026-10-17T05:33:22Z, stabilizer codes with linear programming / LP bound / shadow: HTTP 429
- 2026-10-17T05:33:38Z, quantum codes with upper bound / nonexistence and minimum distance: HTTP 429
- 2026-10-17T05:33:58Z, quantum weight enumerator / MacWilliams / shadow enumerator: HTTP 429
- 2026-10-17T05:35:51Z, broad combined query, after a 90 s pause: HTTP 429 (body "Rate exceeded.", response Date header 05:37:15 GMT)
- 2026-10-17T05:38:52Z, combined query: HTTP 503
- 2026-10-17T05:47:12Z, narrower combined query after a 210 s pause: HTTP 429

Substitute channels (not the arXiv API):
- OpenAlex works search (api.openalex.org, publication-date filter 2024-10-17 to 2026-10-17), 10 distinct queries on stabilizer-code upper bounds, LP and shadow enumerators, MacWilliams, nonexistence, tables of qubit-code bounds to length 256, additive codes over GF(4), Grassl's table. All HTTP 200 (runs at 05:48, 05:49 and 05:50 UTC; the first run crashed while printing, so its 5 queries were re-run). 194 distinct works. No title or abstract mentions [[135,8]] or n = 135, and no work presents upper bounds or a bound table for qubit stabilizer codes above n = 100.
- 10 web searches and about 10 single-page reads through the web-fetch tool (including arXiv abs/html pages for individual papers, which are separate from the API budget above).
- quantumcodes.info (a database named in a search summary) could not be reached: curl exit 35, HTTP 000 at 2026-10-17T05:52:00Z, and the fetch tool got ECONNRESET. It is a secondary mirror; the specified status source is codetables.de.

Closest in-window items and why they do not bear on this cell:
- arXiv 2603.19901 (2026-03-20), SDP bounds on quantum codes with rational certificates: general (n,K,d) codes, n from 6 to 19 (paper text read).
- arXiv 2601.19848 (2026-01-27), low-weight stabilizer codes, and arXiv 2501.17447 (2025-01-29), small binary stabilizer subsystem codes: n up to 9.
- arXiv 2502.14165 (2025-02-20, thesis on quantum Delsarte LP) and arXiv 2610.09900 (2026-10-07, Quantizing Delsarte Theory): theory, no table near n = 135.
- arXiv 2606.15558 and 2606.22538 (June 2026), Hamming bound for degenerate codes and arbitrary local dimension: as computed in section 2, it does not exclude d = 43 here.
- Zenodo record 10.5281/zenodo.23303034 (2026-10-11), 38 qubit stabilizer codes that improve LOWER bounds in Grassl's table: lengths 17 to 55, so no overlap.
- IEEE JSAIT 2025, Puncturing Quantum Stabilizer Codes: constructions and a Griesmer-type bound for prime-dimension stabilizer codes; the abstract mentions no bound tables for n above 100.
- Foundations (outside the window, define the method rather than this cell): Calderbank-Rains-Shor-Sloane quant-ph/9608006, Rains quant-ph/9611001 (shadow), Rains quant-ph/9802070 (monotonicity).

## 5. Reasoning

- The bank entry's operational test is: the live table bound for the cell is 43, the proof lowers it by at least 1, and the result is not implied by the standard propagation rules applied to other live cells. All three hold on live data (sections 1 and 2).
- "A tie is not a record": nothing known to me sets an upper bound at or below 42 for [[135,8]]. The only equal-valued cells are (135,9) and (134,9), which point the wrong way for R1 and give 43 through R3. No pull request or TROPHY_CASE row touches this cell or implies it (section 3).
- The method (quantum LP with Rains shadow constraints) is thirty years old; the table's own note says its n-above-100 bounds are weak, so a bound at this cell being new as a table entry is plausible and consistent with what I saw.
- For information only: the claim's checker, run on its certificate, printed VERIFIED for [[135,8,43]] with shadow set to True (731-digit value, 42+2+42 multipliers) and exit code 0. That is the claimant's own script, not an independent audit.

## 6. Limits, and what would flip this

- The prescribed arXiv API search could not be completed (6 of 6 requests refused). The substitute search is abstract-level only; a bound that appears only inside a table in a paper body would not be seen.
- The full-table closure used the claimant's table from 2026-10-17T00:27:18Z; I re-read only the cell itself and its three direct neighbours live (unchanged). Far cells were not re-read.
- GitHub was limited to 3 requests; PRs whose titles do not contain codetables-qubit were not searched.
- Verdict would flip to false on any of: a live value at (135,8) or at (135,7), (136,8), (134,9) that makes the closure 42 or lower; a PR or merged row claiming this cell or an implying cell at the same or lower bound; a paper or table giving an upper bound of 42 or lower for [[135,8]]. A re-run of the arXiv search once the API recovers is advisable if the panel requires arXiv-API coverage specifically.

pass: true
