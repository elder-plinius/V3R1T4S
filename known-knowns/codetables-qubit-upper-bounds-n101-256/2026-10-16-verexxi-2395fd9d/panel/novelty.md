context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty panel: [[133,2,44]] nonexistence (claimed upper bound 43)

## Table fetch (single attempt, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=133&k=2
- Time: 2026-10-16T21:04:04Z (request), response by 21:04:05Z
- HTTP status: 200 (plain page, no challenge; 1523 bytes)
- Value quoted: "Bounds on [[133,2]]  lower bound: 26  upper bound: 45"; page footer "Last change: 10.06.2024".
- Matches the CLAIM.md record (upper bound 45). Claimed new bound 43 is strictly below the live 45.
- check/propagation_check.txt reports live (133,2) = [26, 45] and neighbours R1 (133,1) [27,45], R2 (134,2) [26,45], R3 (132,3) [26,45]; so propagation from neighbouring cells gives 45, not 43 or 44. The claim is not implied by the standard propagation rules on the table as published.

## Repo checks (read-only)
- Open pull requests of elder-plinius/V3R1T4S (read via a summarizing fetch): the codetables-qubit-upper-bounds-n101-256 claims are for [[132,1]], [[139,1]], [[145,1]], [[150,1]], [[152,1]], [[154,1]], [[158,1]], [[164,1]]. None is for [[133,2]]. Caveat: list came through a summarizer, and closed PRs were not examined.
- TROPHY_CASE.md (main): only classical constant-weight code entries; no quantum code entries, nothing for n=133.

## Literature, last 24 months (arXiv, limited search)
- Grassl's recent arXiv listing: nothing on upper bounds for qubit stabilizer codes at n>100.
- arXiv API search (quantum codes + linear programming + upper bound): 2603.19901 (SDP bounds, rational certificates) covers only 6 <= n <= 19; 2502.14165 (quantum Delsarte LP analog); 2601.15446 (check-weight-constrained codes); none addresses [[133,2]] or n>100 table upper bounds.
- No source found that gives an upper bound below 45 for [[133,2]].

## Assessment
- Strictly below live table value (43 < 45), not a tie, not implied by propagation, no competing PR or prior result found.
- Limits: literature search was not exhaustive (no full-text or Scholar search); novelty only, the certificate correctness is outside this role (checker output in check/checker_output.txt reports both certificates VERIFIED, not re-run by me).

pass: true
