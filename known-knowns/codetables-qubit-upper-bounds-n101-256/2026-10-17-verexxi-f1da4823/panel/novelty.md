# Novelty skeptic verdict, [[195,2]]

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I ran
1. Table fetch, exactly once, after sleep 8: curl -s -A "V3R1T4S-verexxi" -o novelty_cell_page.html on https://codetables.de/QECC.php?q=4&n=195&k=2
   - HTTP status: 200
   - UTC time (date -u): 2026-10-17T00:44:22Z
   - sha256 of novelty_cell_page.html: db84e866276bb307905e0c3a6637edeaa1c3c9e50ed10d0c87721a5a46ac1030 (identical to the claim-time file hash in CLAIM.md)
   - Page text: "Bounds on [[195,2]] ... lower bound: 38 upper bound: 65". The page footer says "Last change: 10.06.2024". It is a normal page, not a challenge page.
2. TROPHY_CASE.md fetched as a raw file from the V3R1T4S repo (HTTP 200, saved as TROPHY.md). A grep for 195 found only constant-weight-code rows (A(33,8,8), A(34,8,8)). No qubit [[195,2]] entry.
3. Open PRs: one curl request (HTTP 200, saved as pulls.html) for the query is:pr codetables-qubit. Grepping for [[n,k]] cells gave: [[105,4]] [[132,1]] [[133,2]] [[139,1]] [[140,2]] [[142,2]] [[145,1]] [[146,2]] [[148,2]] [[150,1]] [[152,1]] [[154,1]] [[158,1]] [[159,2]] [[164,1]] [[165,2]] [[177,1]] [[183,1]] [[200,2]] [[200,5]] [[230,3]] [[230,5]]. [[195,2]] is not among them.
4. Literature: one web search covering 2025 to 2026 for [[195,2]] upper bound, LP and shadow enumerator nonexistence. It found only general LP-bound papers and nothing on this cell. The search is weak evidence, but nothing contradicts novelty.

## Reasoning
- The live upper bound is 65. The claim is that no [[195,2,65]] code exists, which gives an upper bound of 64. That is strictly below the live value.
- The claim folder's propagation check reports that the closure of other live cells at (195,2) is 65, so the bound is not implied by other cells. I did not re-run it, because that belongs to a different skeptic.
- No TROPHY_CASE entry, no open PR and no literature hit covers this cell.
- The table itself says its upper bounds for n>100 are weak, which fits a LP-with-shadow improvement being plausible. Whether the certificate is correct is outside the novelty scope.

Result: the claim is novel and strictly beats the live table value (64 vs 65), with nothing in TROPHY_CASE, open PRs or the literature search that ties or beats it.

pass: true
