# Novelty skeptic verdict, claim q122-1 ([[122,1]] qubit upper bound 41 -> 40)

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I ran
1. Read CLAIM.md and REPRODUCE.md in the package. The claim: no [[122,1,41]] stabilizer code exists, so the upper bound drops from 41 to 40.
2. One live fetch of the status source (sleep 8, one request, user agent V3R1T4S-verexxi, no retries):
   - URL: https://codetables.de/QECC.php?q=4&n=122&k=1
   - HTTP status: 200
   - UTC time: 2026-10-17T00:37:00Z
   - sha256: d1b0f2dfad44f149c46c0e3bfd7b947ad837ce5397fbdd71d9cf61d7fb6c599f (file novelty_cell_page.html, 61794 bytes). This is identical to the hash of data/QECC_q4_n122_k1_claimtime.html recorded in CLAIM.md.
   - Value on the page: "Bounds on [[122,1]]: lower bound: 25, upper bound: 41". It is a normal page, not a challenge or block.
3. Literature search (web search, last 24 months, queries on LP/shadow enumerator/SDP bounds for qubit stabilizer codes with [[122,1]] and d=41). Results were about small-n codes (SDP bounds on quantum codes, arXiv 2408.10323, and the 2026 rational-certificates follow-up for n between 6 and 19), check-weight-constrained codes, low-weight codes and distance-finding algorithms. None mentions [[122,1]] or an upper bound of 40 for it.
4. TROPHY_CASE: I searched data/TROPHY_CASE_pinned_9b1d444.md for 122, qubit, quantum and codetables. It has no qubit or quantum entry and no [[122,1]] entry. I did not fetch the live TROPHY_CASE.md; the pinned copy is my only evidence for this check.
5. Pull requests: one `git ls-remote ... 'refs/pull/*/head'` returned 281 refs. That does not show titles, so I also made one request to the pulls web page filtered on codetables-qubit. The fetch tool's summary said 22 open PRs, all by the same author and titled "[claim] codetables-qubit-upper-bounds-n101-256: [[X,Y]] upper bound lowered from A to B", with examples [[230,5]], [[230,3]] and [[200,5]]. It reported that none concerns n=122 or [[122,1]]. The summary is second-hand and did not list all 22 titles, which is a limitation. I used two PR requests (ls-remote plus the web page) where the instruction allowed one or the other.

## Reasoning
- The live table upper bound is 41. A proof that d=41 is impossible gives an upper bound of 40, which is strictly below the live value, so it is not a tie.
- The claim package's propagation check (check/propagation_check.txt, REPRODUCE.md step 3) says the closure of all other live cells at (122,1) is 41, so the bound of 40 is not implied by propagation from other cells. I did not re-run it. That is outside the novelty scope, and the other skeptics cover validity.
- I found no recent paper, no TROPHY_CASE entry and no open PR for this exact cell that already claims 40 or lower.
- Residual risks: the PR check relies on a summarised page, and the literature search is a web search rather than an exhaustive arXiv sweep.

pass: true
