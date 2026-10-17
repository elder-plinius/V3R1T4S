# Novelty review: [[167,2]] qubit stabilizer codes, upper bound at most 54
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: CONFIRMED against every source I could read: the live table says 57 for [[167,2]] (closure of live cells 56, best bound implied by the 47 claim pull requests 55), the claimed 54 is strictly lower than all three, and no pull request, TROPHY_CASE.md entry or 24-month literature hit gives 54 or lower; arXiv refused me (HTTP 429), so literature coverage is OpenAlex plus web search only.

Target: codetables-qubit-upper-bounds-n101-256. Claim under review (claim/CLAIM.md): no [[167,2,55]] qubit stabilizer code exists, so the upper bound is at most 54, against a live table bound of 57. I reviewed novelty only. As a courtesy I re-ran the claimant's checker (section 6); I did not audit the LP formulation beyond reading the checker's docstring.

## 1. Status source, fetched once
- URL: https://codetables.de/QECC.php?q=4&n=167&k=2
- Command: curl -s -A "V3R1T4S-verexxi" -o work/cell.html -w '%{http_code}' with that URL. One request, no retry.
- Local UTC clock: start 2026-10-17T05:58:37Z, end 2026-10-17T05:58:38Z. curl exit 0. HTTP status 200. 1523 bytes.
- sha256 of work/cell.html: d26f775ad3a031e70da81ef53f066165b4dc4efd993892c19d6241caad4b3869
- Values on the page ("Bounds on [[167,2]]"): lower bound 33, upper bound 57. Construction block: "Construction of a [[167,2,33]] quantum code ... Missing Construction". The page's own note says that for n above 100 the upper bounds on qubit codes are weak (and not necessarily monotone in k). Page footer: "Last change: 10.06.2024".
- The file is byte-identical to claim/data/QECC_q4_n167_k2_claimtime.html (cmp reported identical; same sha256 as CLAIM.md records). So the record the claimant quoted (fetched 2026-10-17T05:33:52Z by the claimant) was unchanged when I read it.
- Clock note: every time in this note is the local PC clock (date -u). Against GitHub Date headers and PR created_at stamps that clock ran about 25 to 55 seconds behind GitHub's. The codetables.de server clock was not recorded.

## 2. Propagation closure from the live table
I did not re-fetch the big table (the rule is one fetch of the status page). I used claim/data/qubit_table_full_n1-256.html; its sha256 is 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6, equal to the value CLAIM.md records. My own parser (not the claimant's scripts) read 33152 cells, 0 unparsable. Its cell (167,2) is 33-57, agreeing with the live cell page. Neighbours: (167,1) 33-57, (168,2) 33-57, (166,3) 32-56.

Closure under d(n,k) at most d(n,k-1) for k at least 2, d(n,k) at most d(n+1,k), d(n,k) at most d(n-1,k+1)+1: a bound u at a cell (n,k) with k at least 1 gives u + c at (167,2), where c is the largest of 0, 167 minus n, and k minus 2. Result at (167,2): 56, from source (162,7) with bound 51 plus 5 steps of the third rule; the next best is 57. A separate fixed-point relaxation over the whole table (16 sweeps) also gives 56. This matches claim/check/propagation_check.txt. So 54 is not implied by live cells.

Side observation: for k = 1, 2 and 3, 142 of the 156 cells with n from 101 to 256 carry exactly the closed form 2*floor((n+1)/6)+1 (plus 1 when n mod 6 = 4); (167,k) is 57 for k = 1 to 4 and the formula gives 57. The 14 exceptions are all lower than the formula (the first eight are n = 101, 106, 107, 108, 112, 113, 114, 118). So the large-n small-k entries are formula values, not per-cell linear-program results, which fits the page's "weak" note.

## 3. Pull requests (repository elder-plinius/V3R1T4S)
Pass 1, HTML search pages, one plain request per page, User-Agent "V3R1T4S-verexxi", all HTTP 200:
- page 1: 2026-10-17T06:00:14Z to 06:00:18Z, 25 PRs, header totalCount 38 (37 open, 1 closed), sha256 46c56366d70bbcd4ff0948cb7f6dca379d87648a6f2f35cdfc70d5717b45b205
- page 2: 06:01:02Z, 14 PRs, totalCount 39, sha256 b55a5bfc8e6fa2f4286d631356d77ea70bd0ff6bcaab5f205c19b8ae2cfbed9b
- page 3: 06:01:05Z, 0 PRs (currentPage 3, totalPages 2, totalCount 40), sha256 3a68a5f07a3766bca251ca28dfef4e79f74056ae51ca4cf74b7b1596658c4f77
- The HTML embeds parseable JSON. The count grew during the pass (38, 39, 40) because new claim PRs were being opened, and #274 showed on both page 1 and page 2, so pass 1 saw 38 distinct PRs.

REST cross-check (the pass-1 list was shifting; this also covers PRs that do not carry the search keyword): https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=N for N = 1 to 4, all HTTP 200, 06:01:45Z to 06:02:54Z. Page sizes 100, 100, 100, 20 = 320 rows, 316 distinct PRs, numbers 1 to 324 (numbers 61, 152, 232, 233, 240, 253, 254 and 286 are not in the PR list). 43 of them carry the target codetables-qubit-upper-bounds-n101-256. Titles mentioning codetables, qubit, quantum or [[ that are not this target: 15 PRs on codetables-binary-linear (classical linear-code lower bounds, closed), which are irrelevant.

Pass 2 (final), HTML search pages again, all HTTP 200:
- page 1: 06:09:49Z, 25 PRs, sha256 starts e6a25319279445ae
- page 2: 06:09:52Z, 22 PRs, sha256 starts 48b2203d645bd906
- page 3: 06:09:54Z to 06:09:55Z, 0 PRs, sha256 starts 982fe12acfa5c1c7 (stop)
- Header on all three pages: totalCount 47, 46 open, 1 closed. A consistent snapshot of 47 PRs, numbers #257 to #328, 47 distinct cells, no duplicates, every title parsed. All 47 are authored by the account verexxi (the name in the User-Agent I was told to use). The newest, #328, was created 06:03:05Z on GitHub's clock and nothing newer existed about seven minutes later, so the claim batch looks finished.

Cells claimed in the 47 PRs (new bound is the number after "to"): [[105,4]], [[110,2]], [[110,5]], [[115,2]], [[120,2]], [[122,1]], [[123,2]], [[125,4]], [[127,2]], [[129,2]], [[132,1]], [[133,2]], [[135,1]], [[135,8]], [[139,1]], [[140,2]], [[142,2]], [[145,1]], [[146,2]], [[148,2]], [[150,1]] (the one closed PR, #260), [[152,1]], [[154,1]], [[155,6]], [[158,1]], [[159,2]], [[161,2]], [[164,1]], [[165,2]], [[165,6]], [[171,1]], [[173,2]], [[177,1]], [[183,1]], [[185,3]], [[195,2]], [[200,2]], [[200,5]], [[200,10]], [[207,2]], [[213,2]], [[215,6]], [[219,2]], [[225,2]], [[230,3]], [[230,5]], [[230,10]].

Checks:
- No PR is for [[167,2]]. None for [[167,1]], [[166,3]], or a k = 2 cell with n from 168 to 172.
- Implied bound at (167,2) from each claimed cell, by the same formula as section 2: lowest are 55 from #276 ([[165,2]], 55 to 53; chain: raise k twice to (165,4), then two steps of the third rule) and 55 from #303 ([[171,1]], 57 to 55; chain: (171,2) at most 55, then four steps of the second rule). Next: 56 from #267 ([[164,1]], 55 to 53), 56 from #327 ([[165,6]], 53 to 52) and 56 from #319 ([[173,2]], 59 to 56); then 57 from #277 and 58 from #318. No claimed cell implies 54 or lower.

## 4. TROPHY_CASE.md on main
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md fetched 2026-10-17T06:03:40Z (server Date header 06:04:33 GMT), HTTP 200, 30936 bytes, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9.
- The claim's pinned copy claim/data/TROPHY_CASE_pinned_9b1d444.md (sha256 cdfe852481ba85e35ccbc386d64ce88de92a56eb73d1ec3e44cdc9a3b86345ad, 100 carriage returns) equals main once carriage returns are stripped (both then hash to 738c07a3...). So main has not changed from the pinned version.
- Content: six result families (degree-diameter graphs, constant-weight codes, matrix multiplication, the Lehmer bound, VNN-COMP counterexamples, a RobustBench attack) plus two cipher commitments, 53 rows. No row about codetables, quantum codes or [[167,2]]. (A grep for 167 hits only "1677" in a matrix-multiplication row.)

## 5. Literature, last 24 months (from 2024-10-17)
What failed, said plainly:
- arXiv API (export.arxiv.org): 2 requests, 2026-10-17T06:04:21Z and 06:07:19Z to 06:07:50Z, both HTTP 429 with body "Rate exceeded." I made no further arXiv requests. Used the allowed fallback.
- OpenAlex: 12 queries returned HTTP 200 (list below). Four more (06:11:03Z to 06:11:08Z) returned HTTP 429 because the free daily budget of the shared IP was used up; they returned nothing, which is not the same as zero hits.
- Web search: 2 queries ran; 2 more were refused by the session's search budget.

What ran (OpenAlex works endpoint, from_publication_date 2024-10-17): relevance searches on LP bounds for quantum codes (2518 matches, top 30 read), shadow enumerator nonexistence (14, all read), upper bounds for additive quantum codes (203, top 25 read), minimum distance bounds for qubit stabilizer codes at large length (505, top 25 read), additive self-dual codes over GF(4) with shadow bounds (15, all read), Grassl code tables (119, top 25 read), quantum weight enumerator LP nonexistence (12, all read), plus one date-sorted query; and four boolean title/abstract filters: stabilizer with LP/shadow/weight enumerator/MacWilliams (39, all read), quantum with upper bound, minimum distance and table/nonexistence (2, all read), additive codes over GF(4)/qubit with bounds (3, all read), codetables.de/Grassl table mentions (357, top 60 read). Web search: the exact cell "[[167,2]]" with stabilizer/upper bound, and LP/shadow bounds with tables up to length 256 and codetables.de.

Closest hits, none of which covers this cell:
- "SDP bounds on quantum codes: rational certificates", arXiv 2603.19901, 2026-03-20: improves 18 upper bounds for n-qubit codes with n from 6 to 19.
- "A Quantum Analog of Delsarte's Linear Programming Bounds", arXiv 2502.14165 (thesis): general framework, no large-n qubit table. "Quantizing Delsarte Theory", arXiv 2026-10-07: association-scheme theory.
- "Check-weight-constrained quantum codes: Bounds and examples", arXiv 2601.15446: LP bounds for codes with limited check weight, not general [[167,2]].
- "Invariant Theory, Magic State Distillation, and Bounds on Classical Codes", arXiv 2501.10163: nonexistence of extremal Hermitian self-dual GF(4) codes [12m,6m,4m+2].
- Zenodo 10.5281/zenodo.23303034 (2026-10-11): 38 qubit stabilizer codes improving LOWER bounds in Grassl's table, lengths 17 to 55. Zenodo 10.5281/zenodo.21874337 (2026-08-10): no [[14,3,5]]. Zenodo 10.5281/zenodo.23304194 (2026-10-11): machine-checked shadow certificate that no pure [[4,1,3]] exists.
- Older and out of window, surfaced by web search: Rains, "Quantum shadow enumerators" (quant-ph/9611001) and CRSS (quant-ph/9608006). They define the LP and the shadow constraints the claim uses; neither tabulates n = 167.

## 6. Checker re-run (courtesy, not my mandate)
python -I check/check_cert.py on result/cert_167_2_57_sh.json and on result/cert_167_2_55_sh.json both printed a line starting "VERIFIED" with "shadow=True: value=1374 digits" and "54+2+54 multipliers" (the line also states that the max column coefficient is non-positive), exit code 0. sha256 of result/cert_167_2_55_sh.json: 369035bd91729d561e6fcf74b55007e80893c98f6742b499de3778fdd6f29f8a; of result/cert_167_2_57_sh.json: 16e64df3c1ba04712bdbcb4f79bc711f912a3aeb8f65fbb218b41de91daa35d9. Note for strictness: the d = 57 certificate alone proves only "at most 56", which would tie the table closure (56). The headline 54 rests on the d = 55 certificate.

## 7. Reasoning
- Against the live table: 54 is 3 below 57. Against the closure of live cells under the three rules: 2 below 56. Against the best bound implied by any pull request, including the claimant's own 46 open ones: 1 below 55. Against TROPHY_CASE.md: no entry to tie. Not a tie anywhere.
- The claim is plausible as a first appearance: the table says its n-above-100 bounds are weak, 142 of 156 small-k cells are a bare closed form, and the only in-window papers on LP/SDP quantum bounds that I found work at n at most 19 or in general settings.
- Limits: literature search is abstract-level and missing arXiv, four OpenAlex queries and two web searches; a table buried in a paper's full text cannot be excluded. The PR snapshot ends about 06:09:55Z (local clock); a later PR could change the picture. I did not re-read the full table, only the claimant's saved copy, whose [[167,2]] cell matches the live page. Scratch files for all of the above are in work/.
- Judgment: every source I was able to read is strictly beaten, and I found no counter-evidence, so I pass it, with the coverage gaps above stated rather than hidden.

pass: true
