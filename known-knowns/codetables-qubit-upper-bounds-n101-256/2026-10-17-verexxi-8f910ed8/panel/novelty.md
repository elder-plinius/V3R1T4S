# Novelty verdict for [[230,10]] qubit upper bound

context: subagent (Claude Code headless on the owner's PC, fresh context)

## Claim
No [[230,10,73]] code exists, so the upper bound would be 72 (live table says 77).

## What I did and real output
1. Read CLAIM.md and REPRODUCE.md in the claim folder.
2. Primary table fetch, exactly once (inside the folder): sleep 20; curl -s -A "V3R1T4S-verexxi" -o novelty_fetch.html -w '%{http_code}' https://codetables.de/QECC.php?q=4&n=230&k=10
   - UTC time before the request: 2026-10-17T05:39:25Z (after: 05:39:26Z)
   - HTTP status: 200 (no challenge page; page is 1526 bytes)
   - sha256: 3ad6f4cb846fc5e018c1ca6b9a665bd4610c10326dadf48bc0518656c423bc7c (file novelty_fetch.html), identical to the claimant's fetch hash.
   - Quoted value: "Bounds on [[230,10]]  lower bound: 42  upper bound: 77".
3. TROPHY_CASE.md (raw file from the V3R1T4S main branch, and the pinned copy data/TROPHY_CASE_pinned_9b1d444.md): grep for 230 shows only unrelated degree-diameter and constant-weight rows; no qubit-code row, nothing for [[230,10]].
4. Pull requests: web page https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit (pages 1 and 2; I made a few page loads in total, not the REST API). Titles listing cells in the 220-239 range:
   - [[225,2]] upper bound lowered from 75 to 74
   - [[230,3]] upper bound lowered from 77 to 74
   - [[230,5]] upper bound lowered from 77 to 73
   No PR for [[230,10]] itself (0 occurrences of 230,10).
5. Literature search (last ~24 months, arXiv and web): no paper found giving a [[230,10]] upper bound or a distance-73 nonexistence result. Hits were general LP-bound or Monte Carlo papers only.

## Reasoning
- Live value is 77. The claimed 72 is strictly below it.
- Propagation: the claimant's closure on the live table gives 75 for (230,10), so 72 is not implied by live cells.
- Pending PR [[230,5]] <= 73 would propagate by d(n,k) <= d(n,k-1) to [[230,10]] <= 73. That is a bound of 73 if merged; the claimed 72 is still strictly smaller. [[230,3]] <= 74 and [[225,2]] <= 74 give nothing tighter than 73 for this cell.
- No literature or trophy entry beats or equals 72.
- Caveat: this verdict covers novelty only. Validity of the certificate is for the other skeptics. A tie against a possible 72 from a PR on another cell was not found.

pass: true
