# Novelty skeptic verdict for [[120,2]] (claim: upper bound 40 lowered to 39)

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I did (real output)
- Read CLAIM.md and REPRODUCE.md in the claim package.
- Fetched the status source once, no retries, after sleep 32, with the prescribed User-Agent V3R1T4S-verexxi:
  URL: https://codetables.de/QECC.php?q=4&n=120&k=2
  HTTP status: 200
  UTC time: Sat Oct 17 00:34:47 UTC 2026
  sha256: 992696ad605b36e1e26626457066c36aa9661a55be10541d8001ad85bd5c04a9 (file novelty_cell_page.html, 59657 bytes)
  Value on page: "Bounds on [[120,2]] lower bound: 25, upper bound: 40" (construction listed is a [[120,2,25]] code).
  This hash is identical to the claimant's claim-time page (data/QECC_q4_n120_k2_claimtime.html), so the live value is unchanged and the claim's target, 40 to 39, is a strict improvement over the live value.
- Pull requests: one request to https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit (HTTP 200). The listed titles ("codetables-qubit-upper-bounds-n101-256: [[n,k]] upper bound lowered from X to Y") cover these cells: [[105,4]], [[132,1]], [[133,2]], [[139,1]], [[140,2]], [[142,2]], [[145,1]], [[146,2]], [[148,2]], [[150,1]], [[152,1]], [[154,1]], [[158,1]], [[159,2]], [[164,1]], [[165,2]], [[177,1]], [[183,1]], [[200,2]], [[200,5]], [[230,3]], [[230,5]]. None is [[120,2]] or [[120,1]]. Cells with n greater than 120 only constrain [[120,2]] through d(n,k) <= d(n+1,k) with bounds of 43 or more, weaker than 40. [[105,4]] (34) does not bound [[120,2]] through the standard rules. The page was a single results page, so I could not rule out further result pages. That is a small residual risk.
- TROPHY_CASE.md (raw file from github.com/elder-plinius/V3R1T4S, main, 30936 bytes): grep for "120", "codetables", "quantum", "qubit" found no entry mentioning [[120,2]].
- Literature: one web search for [[120,2,40]] nonexistence / LP / shadow bounds found no 2024-2026 paper claiming a bound at or below 39 for [[120,2]]. The results were SDP bounds on quantum codes (arXiv 2408.10323) and other generic LP-bound papers. Only one search was made, so this is not exhaustive.
- Propagation: the claimant's check/propagation_check.txt and REPRODUCE.md state that the closure of all live cells at (120,2) is 40, so 39 is not implied by other live cells. I did not re-run it.

## Reasoning
The live upper bound is 40. The claimed bound 39 is strictly lower. Nothing I could reach (live table, open PR list, TROPHY_CASE.md, literature search) shows 39 or lower for this cell, and the claimant reports that the propagation closure does not imply it. This is a strict improvement, not a tie. This verdict covers novelty only. The validity of the Farkas certificate is for the other skeptics.

pass: true
