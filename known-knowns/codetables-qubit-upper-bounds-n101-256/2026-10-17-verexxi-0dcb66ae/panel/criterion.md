# Criterion skeptic verdict: [[150,3]]

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I did
Read CLAIM.md, REPRODUCE.md and check/check_cert.py in full. I ran the exact checker on both certificates and re-ran the propagation check from the saved complete table. I also grepped the saved cell page.

Real output:
- `python3 -I check/check_cert.py result/cert_150_3_51_sh.json` gave `VERIFIED [[150,3,51]] shadow=True: value=1256 digits, max column coefficient <= 0, 48+2+49 multipliers`
- `python3 -I check/check_cert.py result/cert_150_3_49_sh.json` gave `VERIFIED [[150,3,49]] shadow=True: value=1256 digits, max column coefficient <= 0, 48+2+49 multipliers`
- The saved cell page data/QECC_q4_n150_k3_claimtime.html reads "lower bound: 29", "upper bound: 51".
- check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html, then the cell lookup, printed `[29, 51] 50`. The live cell is [29, 51] and the propagation closure at (150,3) is 50.
- The neighbours are R1 (150,2) = [30,51], R2 (151,3) = [29,51], R3 (149,4) = [29,51]. None gives a bound below 50.

## Reasoning
- The checker is short and uses only integer arithmetic. It enforces these rules:
  - Index ranges: Q_j for 1..d-1, G_j for d..n, H_j for 0..n.
  - Inequality multipliers must be nonnegative.
  - The combined coefficient of every column must be <= 0.
  - The certificate value u_E0 + u_E1 * 2^(n-k) must be positive.
- The Farkas argument is correct. For feasible A >= 0 the value equals the sum of c_i A_i minus nonnegative terms, so it would be <= 0, a contradiction.
- The LP constraints are valid for every qubit stabilizer code of minimum distance at least d:
  - A_0 = 1.
  - The sum of A_i is 2^(n-k).
  - A_j = B_j for j < d, and A_j <= B_j for j >= d.
  - The shadow enumerator is nonnegative (Rains), including for degenerate codes.
- So there is no [[150,3,49]] code, and the same holds for d = 49 and above. A d = 51 certificate also verifies, which is the literal reading of the criterion ("d equal to the live upper bound").
- Hidden quantifiers: n = 150 lies in 101..256, k = 3 is a qubit cell, and d = 51 (the live bound) is excluded by the d = 51 certificate. The proven new upper bound is 48, a drop of 3, which is at least 1.
- The certificate is exact and rational (integer), and the checker is independent of the LP solver. It uses a standard-library-only explicit Krawtchouk sum.
- Null model and subsumption: propagation from other live cells gives only 50, so 48 is not implied. Reaching 48 needs the LP certificate.
- The claim states "at most 48". I do not claim it is tight. The evidence shows only that d = 49 is excluded. The d = 50 case is not separately certified, though 49 excluded implies 50 excluded.
- Residual caveat: I verified the table record only from the saved claim-time snapshot, since I had no web access. Live status was not re-fetched by me.

confirmed_scope: No qubit stabilizer code [[150,3,d]] with d >= 49 exists, per exact integer Farkas certificates (d=49 and d=51) of the shadow-augmented quantum weight-enumerator LP, so the upper bound at cell (150,3) is at most 48 against the claim-time table value of 51, which the other live cells' propagation closure (50) does not imply.

pass: true
