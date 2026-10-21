context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: Within the standard stabilizer-code LP with Rains shadow constraints, result/cert_159_2_53_sh.json and result/cert_159_2_52_sh.json are exact integer Farkas certificates (verified by check/check_cert.py) that no qubit stabilizer code [[159,2,53]] or [[159,2,52]] exists, lowering the saved-record codetables.de upper bound for cell (159,2) from 53 to at most 51, and that value is not implied by the propagation rules R1-R3 applied to the saved full table (closure at (159,2) is 53).

## Reasoning (commands run in the claim folder)

1. Certificates. `python -I check/check_cert.py result/cert_159_2_53_sh.json` printed `VERIFIED [[159,2,53]] shadow=True: value=1238 digits, max column coefficient <= 0, 52+2+53 multipliers`; the same for cert_159_2_52_sh.json printed `VERIFIED [[159,2,52]] ... value=1527 digits ... 51+2+52 multipliers`.
2. Checker audit (read check/check_cert.py in full). The Farkas argument is sound: for feasible A >= 0, value = sum_i c_i A_i - sum v_G G(A) - sum v_H H(A) <= 0, contradicting value > 0. The LP rows are the correct ones (A_0=1, sum A = 2^(n-k), A_j=B_j for 1<=j<d, A_j<=B_j for j>=d, shadow >= 0), the Krawtchouk polynomial is the quaternary one, and it uses integer arithmetic only. It enforces index ranges and non-negativity of inequality multipliers. Nonexistence at d=52 covers all d>=52 since those codes also satisfy the d=52 constraints. Null/tamper tests I ran: changing d, k or n in either certificate gives FAILED (reasons: index outside range, positive column coefficient, or non-positive value), so the checker does not accept just anything.
3. Propagation. `python -I check/parse_table.py data/qubit_table_full_n1-256.html p.json; python -I check/propagate.py p.json c.json` then reading cell (159,2) gave `[31, 53] 53`. Neighbours from the saved table: (159,1)=[33,53], (160,2)=[31,54], (158,3)=[31,53], so R1, R2 and R3(+1) all give >=53. A bound of 51 is not implied by other live cells.
4. Table record. data/QECC_q4_n159_k2_claimtime.html contains the [[159,2]] page, with upper bound 53 (the CLAIM reports a fetch at 2026-10-16T21:00:59Z, within the stated session). Cell is in range 101<=n<=256. Criterion is met literally: the d equal to the live upper bound (53) is refuted by an exact Farkas certificate including shadow, and the bound is lowered by at least 1 (indeed 2).

## Caveats / residual risk
- I could not re-fetch the live site (not permitted), so "live immediately before claiming" rests on the saved records.
- The checker was written by the claimant's pipeline, not a third party; I audited it manually and it is short and standard.
- The LP is classical (CRSS + Rains); the novelty is only the cell value. The scope above makes no claim beyond this cell and bound.
- Why the table has 53 despite the LP being standard: unknown; possibly the table's LP was run in floating point or without full shadow rows. This does not affect exact validity of the certificate.

pass: true
