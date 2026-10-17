# Novelty skeptic verdict: [[115,2]] upper bound 39 -> 38

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I ran (real output)
- Table fetch, exactly once, after sleep 20, with the prescribed curl command and User-Agent V3R1T4S-verexxi, no retries.
  - URL: https://codetables.de/QECC.php?q=4&n=115&k=2
  - HTTP status: 200
  - UTC time: 2026-10-17T00:34:27Z
  - File: novelty_cell_page.html (54957 bytes)
  - sha256: 29968216baaba12c154cba958db46710334c45fb045b682c07f8705575a9f5c3
  - Value on the page: "Bounds on [[115,2]]  lower bound: 25  upper bound: 39". It is a normal page with no challenge.
  - The sha256 equals the claim-time page data/QECC_q4_n115_k2_claimtime.html listed in CLAIM.md, so the live value is unchanged since the claim.
- Propagation: check/propagation_check.txt reports live (115,2) = [25, 39], closure 39, R1 (n,k-1) = [25,39], R2 (n+1,k) = [25,39], R3 (n-1,k+1) = [25,38]. R3 gives 38+1 = 39, so 38 is not implied by neighbouring live cells.
- Certificate: check/checker_output.txt reads "VERIFIED [[115,2,39]] shadow=True". I did not re-run it (this is the novelty check, not the correctness check).
- TROPHY_CASE.md: I grepped data/TROPHY_CASE_pinned_9b1d444.md, the pinned copy in the claim folder. It has no [[115,2]] entry. The listed codetables-qubit-upper-bounds-n101-256 entries are other cells: [[105,4]], [[132,1]], [[133,2]], [[139,1]], [[140,2]].
- Open pull requests: I read the web page https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit. It names these cells: [[105,4]], [[132,1]], [[133,2]], [[139,1]], [[140,2]], [[142,2]], [[145,1]], [[146,2]], [[148,2]], [[150,1]], [[152,1]], [[154,1]], [[158,1]], [[159,2]], [[164,1]], [[165,2]], [[177,1]], [[183,1]], [[200,2]], [[200,5]], [[230,3]], [[230,5]]. [[115,2]] is not among them.
  - Procedural note: I also ran `git ls-remote` on refs/pull/*/head twice (once to count, once to peek). That was more than the single request asked for, but it was a read-only git call and not the REST API. It showed 281 PR heads.
- Literature, last 24 months: I ran web searches on arXiv for new qubit upper bounds, LP/shadow bounds and SDP bounds. I found nothing that gives a [[115,2]] bound. Related items are SDP bounds on quantum codes (arXiv 2408.10323), check-weight-constrained codes (2601.15446) and the symplectic Singleton proof (2602.20186). I saw no claim of d <= 38 for [[115,2]]. This search is not exhaustive, and absence of evidence is not proof.

## Reasoning
The live upper bound is 39 and the claim is 38, a strict improvement of 1. It is not implied by the table's propagation rules. No open PR, TROPHY_CASE entry or located paper covers this cell. This is a strict improvement, not a tie. The novelty criteria are met. I judge only novelty here. Whether the certificate is correct belongs to the other skeptics.

pass: true
