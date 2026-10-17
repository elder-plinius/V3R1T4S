# Novelty skeptic verdict for [[123,2]] (claim: upper bound 41 lowered to 40)

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I did (real output)
1. Read CLAIM.md and REPRODUCE.md in the panel folder. The claim: no [[123,2,41]] qubit code exists, so the upper bound becomes 40.
2. Table fetch, exactly once, after sleep 20, with the required User-Agent:
   - URL: https://codetables.de/QECC.php?q=4&n=123&k=2
   - UTC time: Sat Oct 17 00:37:21 UTC 2026 (before the request) to 00:37:22 (after)
   - HTTP status: 200 (no challenge page; the page parsed normally)
   - Saved as novelty_cell_page.html, 62574 bytes
   - sha256: e9456087a9727b8bab30fb2a7349a1e6ff783a93202a8e43134974101282116b
     This is identical to the claim-time page hash in CLAIM.md, so the table is unchanged.
   - Value on the page: "Bounds on [[123,2]]  lower bound: 25  upper bound: 41".
3. TROPHY_CASE.md of elder-plinius/V3R1T4S, fetched once from raw.githubusercontent.com (HTTP 200, 30936 bytes, saved as trophy.md). A grep for "123", "codetables", "qubit" and "quantum" returned 0 matches, so it has no entry for this cell or any qubit table cell.
4. Pull requests:
   - One `git ls-remote ... 'refs/pull/*/head'` call returned 281 pull refs. It gives no titles, so I used it only as a count.
   - One page fetch of https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit (WebFetch summary, not raw HTML) reported 22 open pull requests with that label, all by the same author, opened 2026-10-16. The titles it listed cover other cells (for example [[230,5]], [[230,3]], [[200,5]], [[200,2]], [[183,1]]), and none were [[123,2]]. The summary said "visible" titles only, so I did not read every title myself; that is a mild limitation.
5. Literature: one web search on the nonexistence of [[123,2,41]], LP bounds and shadow enumerators for 2025-2026. It turned up general LP and SDP bound papers (for example arXiv 2408.10323, 2311.07111) but nothing on a [[123,2,41]] nonexistence result or a table-lowering announcement.
6. Propagation: REPRODUCE.md states that the closure of the other live cells at (123,2) is 41, so 40 is not implied by neighbouring cells. I did not rerun it. That is the other skeptics' scope, and the claim's own check output records it.

## Reasoning
The live upper bound is 41 and the claim asserts 40, which is strictly lower. I found no record of an equal or better bound in the table, TROPHY_CASE.md, the visible open pull requests or the literature search. So the claim is novel as far as I can confirm, and it strictly beats the known value rather than tying it. Residual risk: the search was shallow and the pull request list was a summary. Novelty is plausible but not exhaustively proven. I judge the evidence sufficient to pass.

pass: true
