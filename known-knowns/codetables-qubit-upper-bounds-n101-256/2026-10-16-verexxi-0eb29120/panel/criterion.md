# VERDICT (criterion skeptic)

context: subagent (same VM)

Scope of reading: only files inside this folder (CLAIM.md, REPRODUCE.md, check/, data/, result/, plus my own scratch/ files). No web, no GitHub.
Offline limit: I cannot re-fetch codetables.de, so "re-fetched live immediately before claiming" is checked only against the recorded fetch metadata and the saved HTML.

## Clause-by-clause

1. Cell range 101 <= n <= 256, qubit cell. Cell is (n,k) = (154,1), q=4 file (QECC_q4_n154_k1). PASS (154 is in range).

2. d equal to the live table upper bound.
   - `grep` on data/QECC_q4_n154_k1_claimtime.html: "Bounds on [[154,1]] ... lower bound: 33 ... upper bound: 52"; sha256 of the saved file equals the one in CLAIM.md (beef68a1...). The full table parse gives [33, 52] for (154,1).
   - Literal reading needs a proof for d = 52. result/cert_154_1_52_sh.json is exactly that (n=154,k=1,d=52). The d=51 certificate is not the literal reading but is stronger: its LP (A_j=B_j for j<51, A_j<=B_j for j>=51) is satisfied by every code of distance >= 51, so it also excludes d=52. So the "d = live upper bound" clause is covered by cert_52, and the claim's stronger "<= 50" by cert_51.
   - Freshness: file timestamps in CLAIM.md say 2026-10-16T19:44:15Z (cell) and 19:43:25Z (table). I could only check consistency, not liveness. Taken on trust.

3. Lowering by at least 1. Live upper bound 52. Claimed new bound 50 (cert_51), i.e. lowered by 2; the literal d=52 certificate alone gives <= 51 (lowered by 1). Either satisfies ">= 1". PASS.

4. Exact rational infeasibility (Farkas) certificate of the stated LP, exactly the stated constraints.
   Constraints in check/check_cert.py docstring: A_0=1; sum A_i = 2^(n-k) (B_0=1); A_j=B_j for 1<=j<=d-1 (u_Q, free sign); A_j<=B_j for j>=d (v_G >=0); shadow Sh_j>=0 (v_H >=0); A>=0 (via column coefficient <= 0). That matches the criterion list (MacWilliams link, A_i<=B_i, A_i=B_i for 0<i<d, nonnegativity, shadow). Multipliers are integers (rows scaled by 2^(n-k)), which is an exact rational certificate.
   - I validated that the LP formulas are correct on real codes (scratch/valid.py): [[5,1,3]] (A_4=15) and Steane [[7,1,3]] (A_4=21, A_6=42) satisfy B integral, A_j=B_j for j<d, A_j<=B_j, Sh_j>=0. Output: `5 1 3 ok B= [1, 0, 0, 30, 15, 18]`, `7 1 3 ok B= [1, 0, 0, 21, 21, 126, 42, 45]`.
   - cert_51: 50 u_Q (covering exactly 1..50), 2 v_G, 51 v_H; cert_52: 51 u_Q (1..51), 2 v_G, 49 v_H. All indices in the allowed ranges, all v >= 0.
   PASS.

5. Checked in exact integer arithmetic by an independent script.
   - `python3 -I check/check_cert.py result/cert_154_1_51_sh.json` -> `VERIFIED [[154,1,51]] shadow=True: value=1439 digits, max column coefficient <= 0, 50+2+51 multipliers`, exit 0.
   - `python3 -I check/check_cert.py result/cert_154_1_52_sh.json` -> `VERIFIED [[154,1,52]] shadow=True: value=1540 digits, max column coefficient <= 0, 51+2+49 multipliers`, exit 0.
   - I wrote my own checker (scratch/indep.py; Krawtchouk by polynomial product of (1+3x)^(n-i)(1-x)^i, not the binomial sum; separate index/sign logic). Output: both certificates pass, `val>0 True ok`, all 155 column coefficients <= 0, Q rows cover exactly 1..d-1.
   - Null/tamper tests on cert_51 with the claimant's checker: adding 10^3000 to one v_H multiplier -> FAILED; deleting all shadow multipliers -> FAILED (column 50 positive); truncating to d=33 with no G rows -> FAILED (column 0 positive). So the checker is not vacuous and the shadow constraints are load-bearing.
   - Caveat: "independent" = a script separate from the LP solver that produced the certificate; check_cert.py is the claimant's own, but my re-implementation agrees.
   PASS.

6. NOT implied by the propagation rules on other live cells.
   - `python3 -I check/parse_table.py data/qubit_table_full_n1-256.html scratch/parsed.json` -> `cells 33152 n-range 1 256`; `propagate.py` -> closure; printed `[33, 52] 52`.
   - Neighbours: R1 (n,k-1) n/a (k=1); R2 (155,1) = 33-53 -> 53; R3 (153,2)+1 = 51+1 = 52. Closure at (154,1) = 52 > 50 (and > 51). The k=0 cells cannot give an upper bound for (154,1) under the stated rules (R3 gives only d(155,0) <= d(154,1)+1, a lower bound on d(154,1)).
   - Remark: the table is non-monotone elsewhere (1075 cells where live > implied, 1072 with n>100), but not at (154,1).
   PASS.

## Hidden quantifiers / stretched definitions hunted
- "For some qubit cell": one cell suffices; no all-cells claim made.
- Claim text says upper bound "at most 50" while criterion's literal d = live upper bound (52): both certificates present; d=51 cert implies d>=51 excluded, consistent.
- "Distance exactly d" vs "at least d": the LP uses A_j=B_j for j<d, which holds for distance >= d, so infeasibility excludes all distances >= d. No stretch.
- Impure codes are not excluded (A_j<=B_j, not equality, for j>=d). Good.
- The certificate proves LP infeasibility, hence nonexistence; it does not depend on any unproven assumption beyond the cited quantum LP + Rains shadow bounds (tested on two known codes above).
- data/TROPHY_CASE_pinned_9b1d444.md does not mention qubit tables or this cell; not relevant to the claim.
- Not verified: live status at the instant of claiming (offline); nothing about a peer-reviewed status (not required).

confirmed_scope: In the saved codetables.de record (cell [[154,1]], lower 33, upper 52, plus the saved full qubit table whose propagation closure at (154,1) is 52), two integer Farkas certificates (d=52 and d=51, with Rains shadow constraints) pass both the claimant's exact checker and my independent integer re-implementation, so no [[154,1,d]] stabilizer code with d >= 51 exists under the quantum weight-enumerator LP, lowering the table upper bound from 52 to 50 and not implied by the stated propagation rules, with live freshness resting on the recorded fetch timestamps.
pass: true
