context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty review, claim q148-2 ([[148,2,49]] nonexistence, upper bound 50 -> 48)

## Table fetch (single request, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=148&k=2
- UTC time of request: 2026-10-16T21:05:21Z (after a 30 s sleep; completed 21:05:22Z)
- HTTP status: 200 (no challenge page)
- File: novelty_fetch.html (89472 bytes)
- sha256 (real output of sha256sum): d59b202d91deade3d265d1144a3eda548db859b69f7d8ea0dc7a98136aeb98c0
- Value on page: lower bound 30, upper bound 50 for [[148,2]]. Same sha256 as the claim-time record (data/QECC_q4_n148_k2_claimtime.html), so the table is unchanged since the claim was made. The live upper bound is 50, and the claim (<= 48) strictly lowers it by 2.

## Propagation
- The claim folder's check/propagation_check.txt and REPRODUCE.md report a closure of 50 at (148,2) under the three standard rules, so 48 is not implied by other live cells. I did not re-run the propagation scripts.
- I did run check/check_cert.py on result/cert_148_2_49_sh.json: "VERIFIED [[148,2,49]] shadow=True ... max column coefficient <= 0, 48+2+49 multipliers", exit code 0. (Correctness of the LP is another skeptic's role.)

## TROPHY_CASE.md
- Live main branch copy (raw.githubusercontent.com, HTTP 200) and the pinned copy data/TROPHY_CASE_pinned_9b1d444.md: no mention of 148, QECC, codetables or quantum.

## Open and closed pull requests of elder-plinius/V3R1T4S (GitHub API, read-only, first 260 PRs)
- Qubit-bound claims found: #257 [[132,1]], #258 [[139,1]], #259 [[145,1]], #260 [[150,1]], #261 [[152,1]], #262 [[154,1]], #266 [[158,1]], #267 [[164,1]]. All are k=1 cells, all open.
- No PR for [[148,2]] or any k=2 cell. None of the k=1 cells feeds [[148,2]] through the propagation rules (R1 uses d(148,1), which is not claimed; R2 uses d(149,2); R3 uses d(147,3)). So no tie or prior claim on this cell.

## Literature, last 24 months (arXiv API queries; titles and abstracts only)
- Anglès Munné, Nemec, Huber, "SDP bounds on quantum codes" (2408.10323) and "SDP bounds on quantum codes: rational certificates" (2603.19901): improve bounds only for n between 6 and 19.
- Other hits (A Quantum Analog of Delsarte's Linear Programming Bounds, Theory of low-weight quantum codes, MacWilliams Identities for Intrinsic Quantum Codes, and similar) do not address n=148, k=2.
- I found nothing in this search that states a bound of 48 or lower for [[148,2]]. The search was limited to arXiv API keyword queries, so it is not exhaustive.

## Verdict
The live table gives 50 and nothing found (TROPHY_CASE, open PRs, recent arXiv) claims 48 or better for [[148,2]]. The claim, a bound of at most 48, strictly beats every known value I could find.

pass: true
