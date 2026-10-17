# Criterion skeptic verdict, q200-10

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I did and real output
Read CLAIM.md, REPRODUCE.md and check/check_cert.py (about 85 lines, standard library only, integer arithmetic). I ran the checker on both certificates.

    VERIFIED [[200,10,67]] shadow=True: value=1864 digits, max column coefficient <= 0, 64+1+63 multipliers
    VERIFIED [[200,10,63]] shadow=True: value=1864 digits, max column coefficient <= 0, 62+3+63 multipliers

I re-ran check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html. Output: live (200,10) = [37, 67]; propagation closure at (200,10) = 63; neighbours R1 (200,9) = [37,67], R2 (201,10) = [37,67], R3 (199,11) = [36,67]. I also looked in data/QECC_q4_n200_k10_claimtime.html and found the "upper bound" text, which the claim says reads 67.

## Reasoning
- The LP is the standard one. A_0 = 1, the sum of A_i is 2^(n-k), A_j = B_j for 1 <= j < d, A_j <= B_j (S is contained in N), A >= 0, and the Rains shadow S_j >= 0 with the (-1)^i sign. The checker implements exactly this and the Farkas rule. Its logic is sound: for every column the combined coefficient must be <= 0, the value must be > 0, and the inequality multipliers must be >= 0. Index ranges are enforced.
- The d = 63 equalities are shared by every code with d' >= 63. So infeasibility at 63 means no [[200,10,d']] code exists for any d' >= 63, and the upper bound is at most 62.
- Hidden quantifier check: the certificate is for one cell (200,10), which is inside 101 <= n <= 256. The exact-d wording is handled by the 63 certificate. The 67 certificate gives the literal "d = live bound" reading and also verifies.
- Null-model and subsumption check: the closure of the live table by R1, R2 and R3 gives 63 at (200,10). The claimed bound of 62 is strictly below that, so it is not implied by the standard propagation rules applied to other live cells. The live 67 is already above the propagation closure (the table page itself says its upper bounds are not necessarily monotone). That makes the bound-66 consequence of the 67 certificate alone implied by propagation. The 63 certificate gives the real, non-subsumed improvement, down to 62.
- Limits: I did not re-fetch the live table. I relied on the claim-time saved page, as instructed. The relation between the claim-time table and the live state is not independently confirmed. The claim is a lowering of the upper bound only, with no construction.

confirmed_scope: The exact integer Farkas certificate result/cert_200_10_63_sh.json, checked by check/check_cert.py, proves that no [[200,10,d]] qubit stabilizer code exists for any d >= 63, which lowers the claim-time table upper bound of 67 to at most 62 and is below the value of 63 obtained by propagating the other claim-time table cells.

pass: true
