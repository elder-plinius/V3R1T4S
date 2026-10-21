context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty panel report, claim q230-3 ([[230,3]], d=75 excluded, bound 74)

## Primary table fetch (once, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=230&k=3
- Fetched at (date -u): 2026-10-16T21:11:58Z (finished 21:11:59Z), after sleep 5
- HTTP status: 200 (no challenge page; page is 1523 bytes, file novelty_fetch.html)
- sha256 (sha256sum novelty_fetch.html): ac4e69556df8a90aafeb48b2131844e601841034c3127372a23300b7238480c3
- Value quoted: "Bounds on [[230,3]]: lower bound: 44, upper bound: 77".
- The hash is identical to the claim-time fetch recorded in CLAIM.md, so the live upper bound is unchanged at 77. The claim (74) is strictly below 77.
- check/propagation_check.txt (claimant's own output, not independently verified by me) reports that the neighbours (n,k-1), (n+1,k), (n-1,k+1) all have upper bound 77, so propagation from the live table gives 77 and not 74.

## Open pull requests
- One API call (https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=1), HTTP 200, saved as pulls.json. It returned 78 PRs (fewer than 100, so this is the whole list).
- Searched titles and bodies for "230", "[[230", "3]]", codetables, the target id, quantum, stabilizer and shadow.
- The same-target PRs are for other cells only: #257 [[132,1]], #258 [[139,1]], #259 [[145,1]], #260 [[150,1]], #261 [[152,1]], #262 [[154,1]], #266 [[158,1]], #267 [[164,1]]. None mentions (230,3).
- The only PRs matching "230" are unrelated targets (#214 fmm-additive-complexity-records, #210, #208).
- No open PR claims or ties [[230,3]].

## TROPHY_CASE.md
- Read raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md (HTTP 200, 30936 bytes, saved as TROPHY_CASE.md).
- It has zero matches for qubit, codetables, quantum, or [[230. No existing trophy for this target or cell.

## Literature, last 24 months (arXiv API, three queries, titles and abstracts read for the closest)
- arXiv 2603.19901 (2026-03), "SDP bounds on quantum codes: rational certificates": rational infeasibility certificates, improves 18 upper bounds for n-qubit codes with 6 <= n <= 19. Range n<=19, far from n=230. It does not tie or beat the claim.
- arXiv 2610.18130 (2026-10), "Distance Prediction for Quantum Codes": about bivariate bicycle codes, distance heuristics. Not an upper-bound result for [[230,3]].
- arXiv 2601.15446 (2026-01), "Check-weight-constrained quantum codes: Bounds and examples": a different setting (weight-constrained), not read in detail.
- Other hits (locally recoverable, qLDPC, decoding, Tanner codes) are not upper-bound tables for n in 101..256.
- Limits of my search: only the arXiv API, with few queries. I found no paper covering LP/SDP/shadow bounds at n around 230 that would give 74 or lower. I could not exclude unpublished or non-arXiv improvements. The codetables.de page itself (upper bound 77) is the only authoritative status I fetched.

## Verdict
No tie or better value was found in the live table, the open PRs, the trophy case, or recent literature. The live bound is 77 and the claimed bound is 74, a strict improvement of 3. Correctness of the certificate was not assessed (not my role).

pass: true
