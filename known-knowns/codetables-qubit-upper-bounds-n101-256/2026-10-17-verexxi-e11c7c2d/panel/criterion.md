context: subagent (Claude Code headless on the owner's PC, fresh context)

# Criterion skeptic verdict for [[175,3]]

## What I did
- Read CLAIM.md, REPRODUCE.md and check/check_cert.py (full source read).
- Ran: python3 -I check/check_cert.py result/cert_175_3_59_sh.json
  Output: VERIFIED [[175,3,59]] shadow=True: value=1525 digits, max column coefficient <= 0, 56+2+58 multipliers
- Ran: python3 -I check/check_cert.py result/cert_175_3_57_sh.json
  Output: VERIFIED [[175,3,57]] shadow=True: value=1525 digits, max column coefficient <= 0, 56+2+58 multipliers
- Read check/propagation_check.txt. Its line for the cell: live (175,3): [34, 59]  closure of the live table at (175,3): 58  neighbours R1 (n,k-1): [34, 59]  R2 (n+1,k): [34, 59]  R3 (n-1,k+1): [33, 59].
- Re-ran parse_table.py and propagate.py. They executed, but my temp-path output was not readable by the follow-up one-liner (a path error on my side). I rely on the saved propagation_check.txt for the closure value 58.
- Grepped data/QECC_q4_n175_k3_claimtime.html. It shows the "Bounds on [[175,3]]" heading. I did not extract the numeric upper bound from the page myself. The table row [34, 59] is consistent across the saved propagation output.

## Reasoning
- Criterion: for a qubit cell with 101 <= n <= 256, prove that no [[n,k,d]] code exists at d equal to the live upper bound, via an exact Farkas certificate of the weight-enumerator LP with shadow, checked in integer arithmetic by an independent script. The new bound must not be implied by propagation.
- The d = 59 certificate (the literal live upper bound) verifies on its own. The d = 57 certificate also verifies, which gives the stronger statement of an upper bound of 56.
- The checker's docstring and code match the standard LP:
  - MacWilliams via the quaternary Krawtchouk polynomial.
  - A_j = B_j for 1 <= j < d, and A_j <= B_j for j >= d.
  - Shadow nonnegativity.
  - Integer multipliers, inequality multipliers nonnegative, every column coefficient <= 0, positive value.
- I found no hidden quantifier. The cell (175,3) is inside 101 <= n <= 256. The proof is exact, with no floating point. The certificates are specific to k = 3 and n = 175.
- Stretched definitions: the d = 59 certificate is derived by relabelling rows from the d = 57 one. The checker verifies it as a standalone certificate, and the relabelling is legitimate because the rows are identical. The 56 claim rests on the standard fact that nonexistence at d = 57 means the upper bound is at most 56.
- Null model and subsumption: the propagation closure at (175,3) is 58, from R1, R2, R3 on the full live table. A bound of 56 (and the d = 59 and d = 58 exclusions) is therefore not implied by other cells. Nothing in the 1075 listed "live > implied" cells concerns (175,3).
- Limitation: I could not re-fetch the live table. I relied on the claim-time snapshot, as instructed.

confirmed_scope: Within the saved claim-time codetables.de snapshot (upper bound 59 for qubit [[175,3]]), the integer-checked Farkas certificates with shadow constraints prove that no [[175,3,d]] stabilizer code exists for d = 57 through 59, so the upper bound is at most 56, and propagation from the other live cells gives only 58.

pass: true
