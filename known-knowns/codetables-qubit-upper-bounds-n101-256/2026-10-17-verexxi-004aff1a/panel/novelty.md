# Novelty review: claim that no [[135,6,44]] qubit stabilizer code exists (upper bound at most 43)

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: an upper bound of at most 43 on d([[135,6]]) is strictly below the live codetables.de bound 45 (HTTP 200), below the 44 the live table already implies by propagation, and below everything in the 47 claim pull requests, TROPHY_CASE.md on main and the last 24 months of literature I could reach (arXiv refused all 6 requests with HTTP 429; OpenAlex and web search used instead)

Scope: novelty only. I did not audit the soundness of the LP formulation (other panel members do that). For completeness I ran the shipped checker on result/cert_135_6_44_sh.json and result/cert_135_6_45_sh.json; both printed VERIFIED and exited 0.

Clock note: this PC's `date -u` ran about 50 to 54 s behind the servers' own Date headers wherever I captured one (PR page 2: PC 06:00:36Z, server 06:01:26 GMT; complete table: PC 06:08:03Z, server 06:08:57 GMT). I did not capture a header for the cell-page fetch, so its time is the PC clock reading. Times below are PC-clock times unless marked "server".

## 1. Status source, fetched once

- URL: https://codetables.de/QECC.php?q=4&n=135&k=6
- Command: curl -s -A "V3R1T4S-verexxi" -o work/cell.html -w '%{http_code}' on that URL. One request, no retry, curl exit 0.
- Time: 2026-10-17T05:59:14Z (PC clock; start and end in the same second). HTTP status: 200.
- File work/cell.html (my scratch folder): 1523 bytes, sha256 867633fbf0f579b8e5adbf7c26d365ca7b3548951fe1df798c835d7b0b62c6b5.
- Values on the page: "Bounds on [[135,6]]", lower bound 25, upper bound 45. Page footer: "Last change: 10.06.2024".
- cmp shows the file is byte-identical to data/QECC_q4_n135_k6_claimtime.html in the claim package (the claim recorded the same sha256 at 2026-10-17T05:35:22Z). The live bound did not move between claim time and my read.

## 2. Is the new bound already implied by the live table?

- I fetched the complete qubit table once (a different URL from the status page; one request, no retry): https://www.codetables.de/QECC/Tables_color.php?q=4&n0=1&n1=256&k0=0&k1=256 . PC clock 2026-10-17T06:08:03Z to 06:08:36Z, server Date "Sat, 17 Oct 2026 06:08:57 GMT", HTTP 200, 5547032 bytes, sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6.
- cmp shows it is byte-identical to data/qubit_table_full_n1-256.html in the claim package, and that sha256 equals the one written in CLAIM.md. So the claimant's table snapshot is the live table.
- Parsed with the claim's check/parse_table.py (33152 cells, n from 1 to 256): cell (135,6) is 25-45, as on the status page. Neighbours: (135,5) 26-45, (136,6) 26-45, (134,7) 25-43.
- I wrote my own closure routine for the three rules named in the bank entry (d(n,k) at most d(n,k-1) for k at least 2; d(n,k) at most d(n+1,k); d(n,k) at most d(n-1,k+1)+1), k at least 1 only, and a second variant that adds d(n,k) at most d(n-1,k)+1. Live table only: closure at (135,6) is 44 in both variants (for example d(135,6) at most d(134,7)+1 = 44). The claim's own check/propagate.py agrees: check/propagation_check.txt reports 44 for the live table.
- So the best bound the table already implies is 44, not 45. The claimed 43 is strictly lower than both 45 and 44.
- Tie risk: the d = 45 certificate alone would give only 44, which ties the implied value and would not be a record. The claim as written (at most 43) rests on the d = 44 certificate, so it is not a tie.

## 3. Pull requests, every page

Repository elder-plinius/V3R1T4S, search is:pr codetables-qubit. Plain requests, curl -s -L, User-Agent "V3R1T4S-verexxi". The HTML is a React page with the list in embedded JSON, which parsed fine.

- HTML page=1: PC 05:59:36Z, HTTP 200, sha256 2f4c369343f6fa6a873c29c23da80be173377e0f5531859638e260aafb181d14. Lists 25 PRs (#317 down to #272). Header counts: 36 PRs (35 open, 1 closed), 2 pages.
- HTML page=2: PC 06:00:36Z (server Date "Sat, 17 Oct 2026 06:01:26 GMT"), HTTP 200, sha256 4ad49fdca4c4ae1ed8c09927f2364596680c0aae704899abd6ffca1e6c8a1d31. Lists 13 PRs (#273 down to #257). Header counts: 38 PRs (37 open, 1 closed). #273 and #272 repeat from page 1 because two new PRs were opened between my two reads.
- HTML page=3: PC 06:01:06Z (server 06:01:58 GMT), HTTP 200, sha256 b47d46f7d35352e890b840d7143988331f7213d454a17f3a75b973543082df80. It lists no pull requests (no results in the embedded data, no pull links on the page). Header counts 40 PRs, 2 pages. This is the stop condition.
- The list kept growing while I read (36, then 38, then 40), so page boundaries shifted. I therefore took a consistent snapshot through the REST API: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=N for N = 1 to 4 (4 calls, the allowed maximum). PC 06:01:26Z to 06:01:35Z, server Date 06:02:20 to 06:02:29 GMT, HTTP 200 each, page 4 has no next link. sha256: page 1 88bb8a38a11809acfe7d1681ab631c3aa1b5919fd3817673c6619315b3422450, page 2 232fdc7d89f693eef27e7051c8776c7e4b98b238e782311493d56cc67ed6ebfa, page 3 7f549d847a6285c538dda33445dd5ba48df314ef55e83633085e98347eb5e667, page 4 c372e03463d38ff8ff0eb12d34495326948101f674867ab777727fa551492cbf. Result: 100 + 100 + 100 + 16 = 316 PRs in the whole repository (numbers 1 to 324). 43 of them have codetables-qubit-upper-bounds-n101-256 in the title.
- HTML page=1 again, to catch PRs opened after the snapshot: PC 06:08:00Z (server 06:08:54 GMT), HTTP 200, sha256 53fadcd1bd93d69a67ada591d6009108313e1675be7550ad106b0fd0f7015b76. Header counts: 47 PRs (46 open, 1 closed). 4 of its 25 entries were newer than the REST snapshot: #325 [[125,4]] 41 to 40, #326 [[135,8]] 43 to 42, #327 [[165,6]] 53 to 52, #328 [[195,2]] 65 to 64.
- Totals: 47 PRs read (43 from REST plus 4 newer = 47 = the header count at the last read; the only closed one is #260). Requests: 4 HTML pages (1, 2, 3, then 1 again) and 4 REST pages. 47 distinct cells are claimed, one PR each.
- Every PR title has the form "[claim] codetables-qubit-upper-bounds-n101-256: [[n,k]] upper bound lowered from X to Y". Every "from" value equals the live table's upper bound for that cell.
- No PR names [[135,6]]. A scan of title and body of all 316 REST PRs for "[[135,6]]" or "135, 6" finds nothing. The 17 other PRs that mention quantum, qubit, stabilizer, QECC, codetables, MacWilliams or Farkas in title or body belong to other families (classical binary-linear code tables, a market-split benchmark) and concern no qubit cell.
- Implication check: I applied all 47 claimed bounds to the live table as overrides and re-ran the closure. The closure at (135,6) stays 44, in both rule variants. No single claim alone lowers it below 44. The nearest claims: #302 [[135,1]] 45 to 44 (gives at most 44 at (135,6) through d(n,k) at most d(n,k-1), which ties the table-implied 44 and is not at or below 43); #326 [[135,8]] 43 to 42 (higher k, gives nothing for k = 6); #317 [[155,6]] 49 and #327 [[165,6]] 52 (same k, larger n, so only 49 and 52 at (135,6)). The claim's own check/propagate.py with the 43 claims known at the snapshot as overrides also gives 44.

## 4. TROPHY_CASE.md on main

- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md : PC 06:02:35Z (server Date "Sat, 17 Oct 2026 06:03:28 GMT"), HTTP 200, 30936 bytes, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9. Head of main at that time (git ls-remote): 7dd4480512cc47fe0f897164844432a2738fe649.
- Equal to the claim's data/TROPHY_CASE_pinned_9b1d444.md once CRLF line endings are normalised (the pinned file has 100 CRLF endings, sha256 cdfe852481ba85e35ccbc386d64ce88de92a56eb73d1ec3e44cdc9a3b86345ad). 53 numbered rows.
- A keyword search for codetables, qubit, QECC, stabiliz, quantum, "[[" and MacWilliams finds nothing. The only "upper bound" hits are Delsarte LP bounds for constant-weight codes. No qubit-code result and no [[135,6]] entry.

## 5. Literature, last 24 months (2024-10-17 to 2026-10-17)

- arXiv API (export.arxiv.org/api/query, 6 requests at least 6 s apart, submittedDate 202410170000 to 202610172359, topics: stabilizer plus linear programming plus bound; shadow enumerators; SDP plus quantum codes; quantum code tables; nonexistence of quantum codes; additive codes over GF(4) with upper bounds). All six answered HTTP 429 (Too Many Requests), PC 06:04:31Z, 06:04:37Z, 06:04:58Z, 06:05:35Z, 06:05:42Z, 06:06:03Z. No results. No retries; the 6-request allowance is spent. arXiv itself could not be searched.
- Fallback 1, OpenAlex (api.openalex.org/works, from_publication_date 2024-10-17), 6 queries, all HTTP 200, PC 06:06:19Z to 06:06:31Z: stabilizer upper bound with linear programming (750 hits), quantum shadow enumerator bound (444), bounds on minimum distance of additive quantum codes table (1414), SDP bound quantum codes (1086), nonexistence of qubit codes [[n,k,d]] (26), qubit code table upper bounds improved n over 100 Grassl (74). I read the top 25 of each: 132 distinct works, scanned by title and abstract for 135, [[135, codetables, Grassl, code table and 256, and I read the abstracts of the five most relevant ones.
- Fallback 2, web search, 3 queries (the [[135,6]] cell itself; improved qubit upper bounds for lengths 101 to 256 with shadow enumerators and Grassl; nonexistence certificates from the quantum weight-enumerator LP with Rains shadow). What came back: older foundational work (the 1996 quantum shadow enumerator paper, a 1997 upper-bounds paper, older theses and bound papers), a 2023 entanglement-assisted SDP paper, a 2025 Monte Carlo distance paper, and the SDP paper below. Nothing about [[135,6]] or lengths 101 to 256. No timestamps recorded for these.
- Closest hit: arXiv:2603.19901, "SDP bounds on quantum codes: rational certificates" (2026-03-20). Abstract: improves 18 upper bounds on the maximum size of n-qubit codes with 6 up to 19 qubits. It does not reach n = 135. Other related hits (quantum Hamming bound papers of June 2026, MacWilliams identities for intrinsic quantum codes, the mixed-dimensional quantum MacWilliams identity, a Delsarte-type thesis, a Monte Carlo upper bound on the distance of given codes) bound other things. The only title or abstract among the 132 that contains the number 135 is a quantum-optics item, not a code-bound paper.
- A second OpenAlex pass for 2024-06-01 to 2024-10-16 (the table page is stamped 10.06.2024) was refused with HTTP 429 on all 4 queries (PC 06:10:50Z to 06:10:57Z). Not retried. That period is outside the required 24-month window and stays unsearched.

## 6. Reasoning and limits

- Best previously known upper bound at [[135,6]]: the printed table value is 45; propagation inside the live table gives 44; the 47 claim PRs together still give 44. So the record to beat is 44.
- The claim excludes d = 44 and therefore gives at most 43. That is one below 44 and two below the printed 45. Not a tie, and not implied by propagation from any live cell or any claimed cell.
- No PR, no TROPHY_CASE row and no paper found in the last 24 months states an upper bound of 43 or less for [[135,6]].
- Limits: (a) arXiv could not be searched, the fallbacks only see titles and abstracts, so a bound hidden in a paper's tables or full text, or unpublished work by the table maintainer, would not show up; (b) the 2024-06-01 to 2024-10-16 pass was rate limited; (c) the PR list is live (the PR author, handle verexxi, opened PRs in bursts about 6 s apart), so PRs opened after server time 06:08:54 GMT on 2026-10-17 were not seen, and none concerned [[135,6]] up to then; (d) this verdict is about novelty, not about whether the certificate proves what it says.
- Verdict: the result strictly beats every known bound I could find for [[135,6]].

pass: true