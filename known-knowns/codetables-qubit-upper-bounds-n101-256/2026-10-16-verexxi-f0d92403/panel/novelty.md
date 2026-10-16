context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty panel: [[177,1,58]] nonexistence (upper bound 59 -> at most 57)

## Primary table fetch (once, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=177&k=1
- Fetched (UTC): 2026-10-16T21:06:20Z (after sleep 25), user agent V3R1T4S-verexxi
- HTTP status: 200 (no challenge page; 1523-byte plain table page)
- File: novelty_fetch.html
- sha256sum output: 66d358ca130fc13ac27c287970ccae6eebfeda08aa64b02cec6319363f48d784  *novelty_fetch.html
- Value: "Bounds on [[177,1]]: lower bound 35, upper bound 59". Identical hash to data/QECC_q4_n177_k1_claimtime.html in the claim, so the table was unchanged from claim time (21:01:30Z) to this fetch.
- A claimed upper bound of 57 is strictly below the live 59 (lowers by 2).

## Propagation
- check/propagation_check.txt: live (177,1) = [35, 59]; neighbours (178,1) upper 60 and (176,2) upper 59 (so 59+1 = 60 via the n-1,k+1 rule); neither implies a bound below 59. Not implied by propagation, as far as that file shows (I did not recompute it).

## Open pull requests (elder-plinius/V3R1T4S, GitHub API, state=open, per_page=100, pages 1-6)
- Page 1 returned 77 PRs; pages 2-6 returned 0 (all open PRs covered, 77 total).
- Searched titles and bodies, and the changed file paths of every PR (first 100 files each), for 177 / codetables / qecc / quantum / [[n,k]].
- Same-target PRs exist (codetables-qubit-upper-bounds-n101-256) but only for other cells: #257 [[132,1]], #258 [[139,1]], #259 [[145,1]], #260 [[150,1]], #261 [[152,1]], #262 [[154,1]], #266 [[158,1]], #267 [[164,1]]. None names [[177,1]]; the raw "177" matches were only in hash or unrelated text (#245, #229, #200, #197 are other targets). The lowered cells have different n and do not imply a bound for n=177.

## TROPHY_CASE.md (main, raw.githubusercontent.com, HTTP 200, 30936 bytes)
- No occurrence of "177", "codetables" or "quantum"; the families listed are degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench, cipher commitments. Nothing on qubit code bounds.

## Literature, last 24 months (arXiv export API, keyword searches; not exhaustive)
- Queries: stabilizer code + upper bound; quantum MacWilliams; additive quantum codes + bounds; linear programming + quantum code. Results since 2024-10 looked at by title.
- Closest: arXiv 2603.19901 "SDP bounds on quantum codes: rational certificates" (2026-03-20): improves 18 bounds only for 6 <= n <= 19. Nothing found treating n=177 or the 101..256 range, and nothing claiming a distance bound below the codetables value for [[177,1]].
- Caveat: arXiv keyword search cannot rule out an unindexed result, and I did not independently check the certificate's validity (outside the novelty role).

## Verdict
The claimed bound (<= 57) strictly beats the live table (59), is not implied by propagation per the claim's own check, is not in any open PR or TROPHY_CASE.md, and no recent arXiv result found covers it. Not a tie.

pass: true
