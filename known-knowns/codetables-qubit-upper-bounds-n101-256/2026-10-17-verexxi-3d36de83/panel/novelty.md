# Novelty check: [[171,1]] qubit upper bound 57 lowered to at most 55 (target codetables-qubit-upper-bounds-n101-256)

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: NOVEL as of 2026-10-17T00:25Z: the live codetables.de upper bound for [[171,1]] is still 57 (HTTP 200, page hash identical to claim time), TROPHY_CASE.md on main has no qubit row, none of the 22 open PRs on this target covers or implies this cell (closure stays 57 even if all 22 are accepted), and no arXiv paper from the last 24 months bounds it, so a proven bound of 55 strictly beats everything found.

Scope: novelty only. I read CLAIM.md, REPRODUCE.md and the package files in claim/. I did not read the panel/ files of any sibling PR, so the other panelists stay independent.

## 1. Status source (fetched once, no retry)

- Command: `curl -s -A "V3R1T4S-verexxi" -o work/cell.html -w '%{http_code}' 'https://codetables.de/QECC.php?q=4&n=171&k=1'`
- UTC (`date -u`): before 2026-10-17T00:25:03Z, after 2026-10-17T00:25:04Z. HTTP status: 200. Size 1523 bytes.
- sha256 (`sha256sum`): c92ff9802e79dc6a595112491da66a27a8bb2f2fec0d11465d8d55477287c20c
- Value on the page: "Bounds on [[171,1]]_2 ... lower bound: 34, upper bound: 57". Page stamp "Last change: 10.06.2024". The page notes still say: "For n>100, the upper bounds on qubit codes are weak (and not necessarily monotone in k)".
- `diff` against data/QECC_q4_n171_k1_claimtime.html (claimant fetch 2026-10-16T21:01:19Z): identical, same sha256. So the cell did not change in the 3 h 24 min since the claim-time fetch.
- Not re-fetched (one request only): neighbouring cells and the complete table. For propagation I used the claimant's complete-table snapshot, data/qubit_table_full_n1-256.html (claimed fetch 2026-10-16T20:55:59Z). Its sha256 is 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6, which matches CLAIM.md. It carries "Last change: 23.05.2024".

## 2. Propagation (bank criterion: the new bound must not follow from other live cells)

- Re-ran `python -I check/parse_table.py` and `python -I check/propagate.py` on data/qubit_table_full_n1-256.html (outputs in work/parsed.json, work/closure.json). Result: live (171,1) = [34, 57], closure = 57. Neighbours: (172,1) live [34,58], (170,2) live [33,57], (170,1) live [33,57]. Nothing forces 55 or 56.
- Same run with all 22 pending PR claims (section 3) applied as upper-bound overrides (work/pending_overrides.json, 3rd argument of propagate.py): closure at (171,1) is still 57. Cells (172..177,1) fall to 57 via the (177,1) claim, but (171,1) is not lowered. So the claimed 55 is not implied by the live table, nor by the pending PRs.
- Observation from the table data (my own computation, work/parsed.json): the live k=1 upper bound equals 2*floor((n+1)/6)+1 (+1 when (n+1) mod 6 = 5) in 80 of 81 cells with 20 <= n <= 100 and in 142 of 156 cells with n > 100. At n = 171 this formula gives 57, the live value. So 57 looks like a closed-form shadow bound, not an LP result, which fits the bank text ("full quantum LP with shadow ... has not been run above n = 100").

## 3. This repo (github.com/elder-plinius/V3R1T4S)

- Blob-less shallow clone: `git clone --depth 1 --filter=blob:none --no-checkout https://github.com/elder-plinius/V3R1T4S.git` at 2026-10-17T00:25:33Z. main = 8b5ba829baa4711791f2dda18e139ae2bd3beeff, committed 2026-10-16T18:18:58-04:00, subject "bank: ebl-unidentified-fragment-overlaps, three pitfalls from two negative runs (#252)". `git ls-remote` at 2026-10-17T00:37:56Z: main unchanged.
- TROPHY_CASE.md on main (30936 bytes, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9): 0 lines match `codetables|qubit|QECC|stabilizer|\[\[|quantum`. known-knowns/ on main has 18 families (bigger-codes, biggest-graphs, codetables-binary-linear, erdos-699-binomial-gcd, faster-matrix-multiplication, hadamard-maxdet-records, lehmer-past-10-to-the-50, lennard-jones-ccd-doye-table, packomania-hyperspheres-hsp4-hsp6, packomania-scu-spheres-in-cube, qoblib-market-split-and-portfolio, risk-or-safety-exact-optimal-play, robust-forecast-aggregation-bounds, robustbench-cifar100-stronger-attack, stable-marriage-max-stable-matchings, sunflower-free-capacity-lower-bound, thomson-problem-live-tables, vnncomp-2026-unsolved-instances); none is a qubit family. The package's pinned copy data/TROPHY_CASE_pinned_9b1d444.md has no qubit row either.
- Pull requests, open and closed, by git protocol (not the REST API): `git ls-remote ... 'refs/pull/*/head'` at 2026-10-17T00:27:56Z returned 281 PR heads; all fetched blob-less at depth 1 (2026-10-17T00:28:10Z); for each head I listed the tree paths absent from main (work/pr_added_paths.txt). 22 PRs add `known-knowns/codetables-qubit-upper-bounds-n101-256/2026-10-16-verexxi-*`; no other PR has a qubit, QECC, quantum or stabilizer path. The only other path that matched "n171" is PR 92's outbox/2026-10-14-anonymous-c6d1e0ab-fd175df4/object/opt_win_q2_n171_k17_d70.json, a classical binary linear code from the codetables-binary-linear family (q2, k17, d70), not a qubit claim.
- GitHub REST, call 1 of 3: `GET https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100` at 2026-10-17T00:31:10Z, HTTP 200, X-RateLimit-Remaining 56, PRs #184 to #289. All 22 qubit PRs are state open, draft, not merged, author verexxi, created 2026-10-16T20:08Z to 21:33Z. (Calls 2 and 3 not needed.) No PR title or body contains "[[171,"; the only "171" hits are the hash in a directory name (PR 261, "3171be38") and unrelated numbers in other families.
- Cells the 22 open PRs claim (old live bound to new bound, from each INDEX.csv and PR title): (132,1) 45 to 43 #257; (139,1) 47 to 45 #258; (145,1) 49 to 47 #259; (150,1) 51 to 49 #260; (152,1) 51 to 49 #261; (154,1) 52 to 50 #262; (158,1) 53 to 51 #266; (164,1) 55 to 53 #267; (105,4) 35 to 34 #269; (133,2) 45 to 43 #270; (140,2) 47 to 45 #271; (142,2) 48 to 46 #272; (146,2) 49 to 47 #273; (148,2) 50 to 48 #274; (159,2) 53 to 51 #275; (165,2) 55 to 53 #276; (177,1) 59 to 57 #277; (183,1) 61 to 59 #278; (200,2) 67 to 65 #279; (200,5) 67 to 64 #280; (230,3) 77 to 74 #281; (230,5) 77 to 73 #282. No cell (171,1) among them.
- Closest neighbour: (177,1) at most 57 gives U(171,1) <= 57 by d(n,k) <= d(n+1,k). That equals the live 57, so it is a tie with the live table and not a record; the claim's 55 is two below it. These PRs come from the same author and sweep (the #277 package records a table fetch at 2026-10-16T21:01:30Z, 11 s after this claim's 21:01:19Z), so they are sibling cells, not duplicates of this one.

## 4. Literature (arXiv only, last 24 months = submitted 2024-10-16 to 2026-10-17)

Six API requests to `https://export.arxiv.org/api/query` (user agent V3R1T4S-verexxi, max_results 100, sorted by date, one request per query, no retries, each at least 5 s after the previous), all HTTP 200:

| # | UTC | query (all with submittedDate 2024-10-16..2026-10-17) | hits |
|---|---|---|---|
| 1 | 2026-10-17T00:32:58Z | (quantum codes OR stabilizer codes OR quantum error-correcting codes) AND (upper bound OR linear programming OR shadow OR semidefinite) | 50 |
| 2 | 2026-10-17T00:33:21Z | (additive codes OR self-dual additive OR GF(4) OR quaternary) AND quantum AND (bound OR bounds) | 5 |
| 3 | 2026-10-17T00:33:27Z | shadow AND (enumerator OR enumerators) AND quantum | 4 |
| 4 | 2026-10-17T00:33:32Z | au:Grassl AND (quantum OR code OR codes) | 8 |
| 5 | 2026-10-17T00:33:37Z | (codetables OR code tables OR table of OR tables of OR online table) AND quantum AND (bounds OR minimum distance) | 30 |
| 6 | 2026-10-17T00:36:14Z | (stabilizer OR additive OR qubit OR quantum) AND nonexistence phrasing AND (minimum distance OR codes) | 10894 (too broad; first 100 by date were noise) |

(Query 1's first run crashed while printing a non-ASCII title, after the response had been saved to work/arxiv_q1.xml; I read the saved file and did not re-request.)

Closest abstracts read (work/arxiv_q*.xml), none bounds [[171,1]]:
- 2603.19901, Munne and Huber, "SDP bounds on quantum codes: rational certificates": improves 18 upper bounds on n-qubit codes for 6 <= n <= 19. Wrong regime.
- 2503.02222, Ning, Shi and Luo, "Linear Programming Bounds on k-Uniform States": LP and shadow bounds for k-uniform states; says some bounds in Grassl's tables are updated for q = 4 (local dimension 4, small n). Different object and table.
- 2604.25790 (mixed-dimensional MacWilliams and shadow identity), 2502.14165 (quantum Delsarte LP, thesis), 2601.15446 and 2601.19848 (check-weight-constrained LP), 2606.15558 (quantum Hamming bound), 2410.17754 (puncturing, Grassl co-author, constructions), 2601.08008 (punctured dodecacode): none gives qubit-code upper bounds for n > 100.
- No abstract in any of the six result sets mentions 171, 256, or a table of qubit upper bounds above n = 100.

Limit: abstract-level search of arXiv only, as the rules allow. A table inside a paper body, or a non-arXiv source, would not show up. Nothing found points to one.

## 5. Side check (outside the novelty remit)

`python -I check/check_cert.py result/cert_171_1_56_sh.json` and `... cert_171_1_57_sh.json` at 2026-10-17T00:37:11Z (2 s): both print VERIFIED ([[171,1,56]] and [[171,1,57]], shadow=True), exit 0. That is the claimant's own checker; independent validation of the certificate belongs to the reproduce panelist, and my verdict does not rest on it.

## 6. Reasoning

1. The bar is the live table (57 at (171,1)), then this repo, then the last 24 months of literature. The claim is "no [[171,1,56]] exists", i.e. an upper bound of at most 55, two below 57. That is not a tie.
2. The live page is readable (HTTP 200) and reads 57; its hash equals the claim-time hash, so there is no drift.
3. This repo: TROPHY_CASE.md has no qubit row, and no PR, open or closed, claims (171,1). 22 open drafts target the same bank entry on other cells, and none implies a bound below 57 at (171,1), even with all of them accepted.
4. The bank's propagation condition holds: the closure of the live table at (171,1) is 57.
5. Nothing in the 24-month arXiv search bounds this cell; the nearest papers are small-n SDP bounds and k-uniform-state LP bounds.

What would change this verdict: a published or pending bound at (171,1), (172..177,1) or (170,2) that implies 56 or less; or a change to those live cells after the claimant's snapshot (2026-10-16T20:55:59Z) that I did not re-fetch under the one-fetch rule.

pass: true
