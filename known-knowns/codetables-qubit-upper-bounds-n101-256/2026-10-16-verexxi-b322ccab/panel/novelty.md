context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty review, cell [[165,2]] qubit

## Table fetch (once, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=165&k=2
- Fetched after `sleep 5`, UTC 2026-10-16T21:05:39Z to 21:05:40Z (`date -u`), HTTP status 200, saved as novelty_fetch.html (1523 bytes).
- sha256sum output: c38c91cf8ef8660e6746443d1db91f1310d04704347531a08f5a121f6afa5e1b  novelty_fetch.html (identical to the claim-time hash recorded in CLAIM.md).
- Value in the page: "Bounds on [[165,2]]: lower bound: 32, upper bound: 55". No challenge or block page.
- The claimed result (no [[165,2,54]], so upper bound 53) strictly lowers the live bound 55 by 2.
- check/propagation_check.txt: neighbours (165,1) [33,55], (166,2) [32,56], (164,3) [32,55]; closure at (165,2) is 55, so the new bound is not implied by propagation from the live table.

## Open pull requests, github.com/elder-plinius/V3R1T4S
- GitHub API, state=open, per_page=100, page 1 returned 77 PRs (fewer than 100, so no further pages); all 77 titles and bodies were scanned for 165, "[[", codetables, stabilizer, quantum, QECC.
- Related hits are all the same bank entry (codetables-qubit-upper-bounds-n101-256) but for other cells: #267 [[164,1]], #266 [[158,1]], #262 [[154,1]], #261 [[152,1]], #260 [[150,1]], #259 [[145,1]], #258 [[139,1]], #257 [[132,1]]. None targets [[165,2]] or [[165,1]]/[[165,k]]; none of them can lower the [[165,2]] bound by the propagation rules (they are k=1 cells at other n, and the rules for (165,2) use cells (165,1), (166,2), (164,3)).
- No open PR claims [[165,2]].

## TROPHY_CASE.md (main branch, raw file, HTTP 200, 30936 bytes)
- Searched for 165, codetables, "[[", quantum, qubit, stabilizer: no matches. No existing record for this cell.

## Literature, last 24 months (arXiv API, searches on quantum code upper bounds, linear programming, weight enumerator, shadow enumerator, additive quantum codes)
- arXiv 2603.19901 (2026-03): rational SDP certificates, improves 18 bounds for n-qubit codes with 6 <= n <= 19 only; not relevant to n=165.
- arXiv 2502.14165 (2025-02): quantum analog of Delsarte LP bounds, general theory, no n=165 table entry.
- arXiv 2601.15446, 2606.02418, 2610.04694, 2608.06304, 2601.19848: other topics (check-weight-constrained codes, bivariate bicycle search, general phase spaces, time-reversal, low-weight codes); none reports a [[165,2]] bound.
- Searches are keyword based via the arXiv API; no paper found giving a d <= 53 bound for [[165,2]]. Absence cannot be proven absolutely, but nothing found ties or beats the claim.

## Verdict
The live upper bound is 55; the claim gives 53 with no tying or earlier record found in the table, open PRs, TROPHY_CASE.md or recent arXiv. Strictly better than everything found. (Correctness of the certificate is outside this novelty role.)

pass: true
