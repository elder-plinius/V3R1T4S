# VERDICT (criterion skeptic)

context: subagent (same VM)

Only files inside this folder were read or run. No web access was used. I created work/mycheck.py (my own checker); the temporary parsed/closure json files in work/ were deleted.

## Clause-by-clause

1. Cell in range: (n,k) = (158,1), 101 <= 158 <= 256. OK.
   Table record: grep of the saved full qubit table shows `title="n=158, k=1" ... >33-53`. The saved cell page says "Bounds on [[158,1]] ... lower bound: 33 upper bound: 53".
   Both saved files match the sha256 values in CLAIM.md (`sha256sum data/*.html`).

2. "d equal to the live upper bound", with a proof of nonexistence for that d. The live upper bound is 53.
   `python3 -I check/check_cert.py result/cert_158_1_53_sh.json` printed `VERIFIED [[158,1,53]] shadow=True: value=1609 digits ... 52+2+52 multipliers`, exit code 0.
   So the literal reading is met: there is a certificate for d = 53 itself.
   The headline claim (no [[158,1,52]], bound <= 51) rests on `python3 -I check/check_cert.py result/cert_158_1_52_sh.json`, which printed `VERIFIED [[158,1,52]] shadow=True: value=1683 digits ... 51+2+51 multipliers`, exit code 0.
   The d=52 result implies the d=53 result (an LP-feasible d=53 point is d=52-feasible), so the claimed drop is 53 -> 51, which is at least 1 (it is 2).
   OK.

3. "re-fetched live immediately before claiming". I cannot re-fetch (no web). The record is internally consistent: fetch at 2026-10-16T19:44:24Z (cell page) and 19:43:25Z (full table), HTTP 200, hashes match.
   The page footer says "Last change: 10.06.2024" and the cell was last modified 2009-02-08, so the snapshot is not stale by construction. NOT independently verified by me; I accept the timestamps as recorded.

4. Exact rational Farkas certificate of the stated LP with exactly the stated constraints.
   The constraints are A_0 = 1, sum A_i = 2^(n-k), A_j = B_j for 1 <= j < d, A_j <= B_j for j >= d, A >= 0, and shadow Sh_j >= 0 for all j.
   Here B and Sh are the MacWilliams and Rains transforms with the quaternary Krawtchouk polynomials.
   - The checker's docstring and code match this. Index guards: u_Q only on 1..d-1, v_G only on d..n, v_H >= 0, v_G >= 0.
   - Certificate contents: the 52-cert has u_Q on exactly 1..51, v_G on {54,55}, and v_H on 51 indices. The 53-cert has u_Q on 1..52, v_G on {55,56}, and 52 v_H indices.
   - The Farkas logic is correct. If every column coefficient is <= 0 and the right-hand side is > 0, then sum c_i A_i = value + (nonnegative slacks) >= value > 0 while sum c_i A_i <= 0. Contradiction.
   - The certificate is integer (the rows are scaled by 2^(n-k)), so it is exact.
   - Shadow constraints are "where used", which the criterion allows.

5. Checked in exact integer arithmetic by an independent script.
   check/check_cert.py uses the standard library and integers only.
   I also wrote my own checker (work/mycheck.py) that rebuilds the combined column coefficients from scratch with a different binomial routine. Its output:
   `max col coeff<=0: True rhs>0: True ineq multipliers all >=0: True` for both certificates, with Q covering 1..d-1.
   "Independent" here means independent of the LP solver that produced the certificates. The checker is by the same author as the claim, but it is short and I re-derived it.
   Null model: the same LP row definitions accept real codes. [[5,1,3]] (A_0=1, A_4=15) is LP+shadow feasible, and correctly infeasible at d=4. Steane [[7,1,3]] (A_0=1, A_4=21, A_6=42) is feasible.
   So the constraint set is not trivially infeasible and the sign and shadow conventions are right.
   The table notes say "For n>100, the upper bounds on qubit codes are weak", which is consistent with an LP beating the listed 53.

6. NOT implied by propagation rules applied to other live cells.
   Commands: `python3 -I check/parse_table.py data/qubit_table_full_n1-256.html work/parsed.json`, then `python3 -I check/propagate.py work/parsed.json work/closure.json`, then the printing one-liner. Output: `[33, 53] 53`.
   Parse: 33152 cells, n 1..256. The closure covers k >= 1 (k = 0 is excluded as a different distance notion). R1, R2 and R3 are the stated rules.
   Neighbours in the table: (159,1) = 33-53 (so R2 gives 53), (157,2) = 31-53 (so R3 gives 54), and (158,2) = 31-53.
   The closure value at (158,1) is 53, so neither 51 nor 52 is implied by other live cells. OK.
   Caveat: the closure is computed with the claim's own scripts. I read them and they implement the three stated rules.

## Hidden quantifiers and stretched definitions
- One cell only: (158,1). Not a family or range claim.
- The "at most 51" headline is the d=52 certificate; the literal criterion (d = live bound 53) is also certified separately.
- The result is a bound on stabilizer (additive, qubit) codes, which is what the table covers.
- The live value is read from a snapshot I cannot refresh. The only unverifiable clause is liveness.
- data/TROPHY_CASE_pinned_9b1d444.md is unrelated context (other families) and plays no role in the evidence.

confirmed_scope: For the single qubit cell (n,k)=(158,1), the exact integer Farkas certificates in result/cert_158_1_53_sh.json (the table's listed upper bound 53) and result/cert_158_1_52_sh.json both pass the standalone integer checker and my own re-derived checker, so no [[158,1,52]] or [[158,1,53]] stabilizer code exists (upper bound 51, versus 53 in the saved codetables.de snapshot), and the propagation closure over all other cells of that snapshot still gives 53; the snapshot's liveness at claim time (2026-10-16T19:44Z) was taken from recorded timestamps and hashes, not re-fetched by me.
pass: true
