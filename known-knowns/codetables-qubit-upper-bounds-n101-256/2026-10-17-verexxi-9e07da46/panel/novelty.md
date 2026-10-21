# Novelty check: [[165,6]] qubit stabilizer code, claim "no [[165,6,53]], so the upper bound is at most 52"

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)

novelty: new as a table entry: the live codetables.de upper bound for [[165,6]] is 53 (HTTP 200, 2026-10-17T05:26:50Z), the claimed 52 is strictly lower and is not implied by propagation over the live table or by any cell claimed in the repo, and no earlier bound was found; caveat: the arXiv API search itself was blocked (HTTP 429 on all 6 requests), so the literature step rests on fallback indexes and web search

## 1. Primary status page (fetched once, no retry)

- Command: curl -s -A "V3R1T4S-verexxi" -o work/cell.html -w '%{http_code}' 'https://codetables.de/QECC.php?q=4&n=165&k=6'
- UTC time (date -u before and after the call): 2026-10-17T05:26:50Z and 2026-10-17T05:26:51Z
- HTTP status: 200. File size 1523 bytes.
- sha256 (sha256sum work/cell.html): 2ab973981689cd1731fa749a17b6cc4d48c6eb1e956fbc0658ef732dcdc33bb2
- Values parsed from the page: heading "Bounds on [[165,6]]", lower bound 31, upper bound 53. Footer stamp: "Last change: 10.06.2024". The page's own note says that for n above 100 the qubit upper bounds are weak and not necessarily monotone in k.
- cmp against the claimant's copy (claim/data/QECC_q4_n165_k6_claimtime.html, fetched 2026-10-17T00:30:04Z per CLAIM.md): byte-identical, and the sha256 equals the one in CLAIM.md. The cell did not move between claim time and now.
- Number to beat: 53. The claim (at most 52) is lower by 1, so it is not a tie.

## 2. This repo (github.com/elder-plinius/V3R1T4S)

TROPHY_CASE.md on main
- URL: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, fetched 2026-10-17T05:28:44Z, HTTP 200, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 (saved as work/TROPHY_CASE_main.md).
- The claimant's pinned copy (claim/data/TROPHY_CASE_pinned_9b1d444.md, sha256 cdfe852481ba85e35ccbc386d64ce88de92a56eb73d1ec3e44cdc9a3b86345ad) differs only in line endings: after stripping carriage returns, diff output is 0 lines; both have 100 lines.
- 53 numbered rows (degree-diameter graphs, constant-weight codes, Lehmer, matrix multiplication, cipher commitments, VNN-COMP, RobustBench). grep for quantum, stabiliz, qubit, codetables, QECC, Grassl: 0 matches in both copies. So there is no [[165,6]] row, and no qubit cell of any kind, in the trophy case.

Pull requests (open and closed)
- Page 1: https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit fetched 2026-10-17T05:28:51Z, HTTP 200 (sha256 b678008b3dd42751f02e368a79f18d08521245617067bd97a59026020ede179b).
- Page 2: same URL plus &page=2, fetched 2026-10-17T05:30:02Z, HTTP 200 (sha256 d63da28b767dcbf64e9f7ea6aee0543aad5d4401bd9be626ea10e205cdecfb63).
- The embedded page data says totalCount 34, openCount 33, closedCount 1, totalPages 2. All 34 are authored by verexxi (the same name as the user-agent string I was told to use, so they look like the claimant's own drafts; this is an inference). All are titled "[claim] codetables-qubit-upper-bounds-n101-256: [[n,k]] upper bound lowered from X to Y". PR numbers: 257 to 262 (260 is the closed one), 266, 267, 269 to 282, 296 to 307.
- Cells claimed (n,k): k=1: 122, 132, 135, 139, 145, 150, 152, 154, 158, 164, 171, 177, 183. k=2: 110, 120, 123, 127, 129, 133, 140, 142, 146, 148, 159, 165, 200, 207, 213, 219, 225. k=3: 230. k=4: 105. k=5: 200 and 230. There is no claim at [[165,6]]. The nearest are [[165,2]] 55 to 53 (PR 276) and [[164,1]] 55 to 53 (PR 267); the title search also matches nothing at (166,6), (164,7), (165,5) or (165,7).
- REST call 1 of 3: GET https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&sort=created&direction=desc at 2026-10-17T05:37:54Z, HTTP 200. It returned 100 PRs, numbers 210 to 315 (authors: verexxi 44, calgulbenkian 17, stevebelew 15, joshuacalebs 9, others fewer). The only quantum-code PRs are the 34 above. Six other PRs matched my keyword scan (numbers like 165/166, the word table) but belong to unrelated bank entries (matrix-multiplication addition counts, LABS merit factor, group testing). No title or body matches 165,6.
- Rules check against these claimed cells: running the propagation closure (section 3) with all 34 PR cells applied as overrides leaves the closure at (165,6) at 53. (165,2) at 53 gives (165,6) at most 53 through the k-1 rule, which is a tie with the live value, not 52.

## 3. Propagation (rules: d(n,k) at most d(n,k-1) for k at least 2; d(n,k) at most d(n+1,k); d(n,k) at most d(n-1,k+1)+1)

- Table used: the claimant's copy claim/data/qubit_table_full_n1-256.html (sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6; CLAIM.md says fetched 2026-10-17T00:27:18Z; its footer stamp is "Last change: 23.05.2024"). I did not re-fetch it, to keep to one fetch of the primary source. The cell I did fetch live is byte-identical to the claim-time page, and the table is stamped as unchanged since 2024.
- My own regex parse found 33152 cells (the expected count for n up to 256, k from 0 to n), (165,6) = lower 31, upper 53, and 0 mismatches against the claimant's parse_table.py output.
- Claimant's propagate.py rerun by me (work/closure.json): closure at (165,6) = 53. With the 34 PR cells as overrides: 53.
- My own closure code: rules 1 to 3: 53; rules 1 to 3 plus the 34 PR cells: 53; adding the extra standard rule d(n,k) at most d(n-1,k)+1: 53, with and without the 34 PR cells; leaving out the pure-code-only rule 3: 53.
- Neighbours in the table copy (live value, closure): (165,5) [31,55], 54; (166,6) [31,53], 53; (164,7) [31,53], 52; (165,7) [31,53], 53; (164,6) [31,53], 53; (167,6) [31,53], 53. The binding neighbour is (166,6) at 53 through the n+1 rule; (164,7) closes to 52 but the +1 rule then gives only 53.
- The table is not propagation-closed for n above 100 (the claimant's script lists 1075 cells whose live upper bound is above their closure), but at (165,6) the closure equals the live 53, so 52 is not implied by other live cells.
- For context, closed-form published bounds at n=165, k=6: quantum Singleton gives d at most 80; quantum Hamming (script: largest t with the sphere sum at most 2^159 is t = 30; the script printed d at most 61 as 2t+1, and with t = floor((d-1)/2) even d = 62 also fits) gives d at most 62. Both are far above 52, so neither already gives the claimed bound.

## 4. Literature, last 24 months (2024-10-17 to 2026-10-17)

arXiv API (the prescribed channel): FAILED, no content obtained
- 6 requests to https://export.arxiv.org/api/query (submittedDate window as above, spaced 7 s apart), all failed: 2026-10-17T05:32:59Z HTTP 429; 05:33:06Z HTTP 429; 05:33:13Z HTTP 429; 05:33:20Z HTTP 429; 05:33:28Z read timeout; 05:34:35Z HTTP 429. The 6-request budget is used up and I made no further arXiv requests. The arXiv step of the protocol was therefore not completed.

Fallbacks (not arXiv hosts; weaker evidence, title and abstract level only)
- OpenAlex API (https://api.openalex.org/works, publication date filter 2024-10-17 to 2026-10-17): 6 requests, all HTTP 200 (05:35:43Z, then 05:36:08Z to 05:36:21Z; the first run was repeated because my print crashed on a Unicode character), 5 distinct queries, 110 unique works. Abstracts scanned for codetables, Grassl, 256, length NNN, 165: only two hits, both about new lower-bound codes (homothetic-BCH quantum codes; evolutionary search for n at most 20). No abstract gives an upper bound at n above 100.
- Most relevant works found: Munne and Huber, "SDP bounds on quantum codes: rational certificates" (arXiv 2603.19901, 2026-03-20): improves 18 upper bounds on n-qubit code sizes for n from 6 to 19, so far from n=165. Okada, "A Quantum Analog of Delsarte's Linear Programming Bounds" (arXiv 2502.14165, a thesis): its abstract describes a general framework and mentions no per-cell table. Zhang et al., arXiv 2606.15558 and 2606.22538: the quantum Hamming bound also holds for degenerate codes; far weaker than 52 here. Ostrev (IEEE Trans. Inf. Theory, 2026): finite-blocklength rate bounds, not distance tables. None gives a bound for [[165,6]].
- Semantic Scholar API: 2 requests, both HTTP 429 (2026-10-17T05:38:56Z and 05:39:01Z), no data.
- WebSearch tool (a search engine, not arXiv requests): 6 queries, including one extended and two restricted to arxiv.org. Results were only Rains (shadow enumerators, quant-ph/9611001), Calderbank-Rains-Shor-Sloane (quant-ph/9608006), "Upper Bounds on the Size of Quantum Codes" (quant-ph/9709049), Lai-Ashikhmin (entanglement-assisted, length up to 20), the SDP and Hamming papers above, and Grassl's table as the reference for longer lengths. No result reports a new non-existence result or table for lengths above 100.
- Limits: this cannot see a number buried in the body of a paper, and I could not read arXiv listings. Prior art at exactly [[165,6]] would be unusual because the table itself calls its n above 100 bounds weak, but this part is "nothing found", not "proved absent".

## 5. Side check of the certificate (soundness, not part of the novelty verdict)

- Ran the claimant's checker: python3 -I check/check_cert.py result/cert_165_6_53_sh.json printed "VERIFIED [[165,6,53]] shadow=True: value=1454 digits, max column coefficient at most 0 (printed with a less-than-or-equal sign), 52+2+54 multipliers", exit 0.
- Also re-checked in my own code (work/my_check.py, different Krawtchouk construction by polynomial products, symmetry identity sampled with 0 violations, big-integer arithmetic): value positive (1454 digits), no column with a positive coefficient, VERIFIED. I did not review the LP formulation beyond reading the checker's docstring; another reviewer should own that.

## 6. Reasoning

- The record to beat is the live table value 53, read once, and the claim is 52: strictly lower.
- The table's own propagation rules do not already give 52 at (165,6), even after adding the repo's 34 claimed cells and one extra standard rule; the closure stays at 53.
- The repo has no [[165,6]] claim in TROPHY_CASE.md or in any open or closed PR matching codetables-qubit, and a wider scan of the 100 newest PRs found nothing else about qubit codes. The 34 sibling drafts are the claimant's own and do not touch this bound.
- No published or listed bound at or below 52 for [[165,6]] turned up in the fallback literature search.
- The result is new as a table entry only: the method (quantum weight-enumerator LP with Rains shadow constraints) is the classical one from the 1996 to 1997 papers cited in CLAIM.md.
- Open gaps, stated plainly: (1) arXiv search blocked, so the literature step used OpenAlex and web search; (2) propagation used the claimant's table copy, not a second live fetch of the whole table; (3) rerunning the arXiv queries once the rate limit clears would close gap 1.
- Decision: every named check is clean and the only gap is a blocked search channel, with other channels clean, so I confirm novelty with the caveats above.

pass: true
