# Novelty skeptic verdict for [[219,2]]

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I ran
- Read CLAIM.md and REPRODUCE.md in the claim folder. Claim: no [[219,2,73]] qubit code, so the upper bound drops from 73 to 72.
- Table fetch, exactly once, after sleep 44, with User-Agent V3R1T4S-verexxi: https://codetables.de/QECC.php?q=4&n=219&k=2
  - HTTP status: 200
  - UTC time (date -u): Sat Oct 17 00:45:39 UTC 2026
  - Saved file: novelty_cell_page.html (1523 bytes), sha256 6af37db32446cc5a70ab0ca1d21d9bc154d598ba1e6af22b4e3cf828b22857b3
  - Value shown: "Bounds on [[219,2]] 2 lower bound: 42 upper bound: 73". It is a normal page with no challenge. The sha256 matches the claimant's claim-time snapshot, so the cell is unchanged.
  - The page notes that for n>100 the upper bounds are weak and not necessarily monotone in k.
- Pull requests: one curl request for https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit, HTTP 200, saved as pulls.html (325456 bytes). Every [[n,k]] cell found in the file: [[105,4]], [[132,1]], [[133,2]], [[139,1]], [[140,2]], [[142,2]], [[145,1]], [[146,2]], [[148,2]], [[150,1]], [[152,1]], [[154,1]], [[158,1]], [[159,2]], [[164,1]], [[165,2]], [[177,1]], [[183,1]], [[200,2]], [[200,5]], [[230,3]], [[230,5]]. [[219,2]] is not among them.
- TROPHY_CASE.md: fetched raw from the main branch, HTTP 200, saved as trophy.md (30936 bytes). The only lines containing "219" are unrelated (a constant-weight code value 41219 and a matrix-multiplication rank), with no [[219,2]] entry.
- Literature: one web search (nonexistence of a [[219,2,73]] stabilizer code by LP bounds) found only general LP/SDP bound papers (for example arXiv 2408.10323 SDP bounds on quantum codes) and nothing that treats [[219,2]] or sets its bound below 73.

## Reasoning
- The live upper bound is 73. The claim gives 72, which is strictly lower, so it is not a tie.
- No open pull request, no TROPHY_CASE.md row and no literature hit covers this exact cell.
- The claim's own propagation check (check/propagation_check.txt, REPRODUCE.md step 3) reports a closure of 73 for (219,2) over the complete live table, so 72 is not implied by neighbouring cells. I did not rerun it. The table's own statement that its bounds above n=100 are not monotone supports the same reading.
- Scope: this verdict covers novelty only. Validity of the certificate belongs to the other skeptics.
- Limit of my search: one web search plus the repo and PR listing. The pulls list is a single page and could be truncated or paginated. I found no conflicting record.

pass: true
