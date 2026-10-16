# Criterion skeptic verdict

context: subagent (same VM)

Only files inside this folder were read or run. No web or GitHub tool was used. Work files are in work/ (indep.py, sanity.py, parsed.json, closure.json).

## Clause-by-clause

1. "some qubit cell (n,k) with 101 <= n <= 256": the cell is (132,1), so n = 132 is in range. MET.

2. "a proof that no [[n,k,d]] stabilizer code exists for d equal to the live table upper bound ... thereby lowering it by at least 1":
   - The saved page data/QECC_q4_n132_k1_claimtime.html says "Bounds on [[132,1]] ... lower bound: 27 upper bound: 45". The saved page's sha256 matches CLAIM.md.
   - The saved full table lists the cell as `title="n=132, k=1" ... 27-45`. Its sha256 also matches CLAIM.md.
   - The d = 45 certificate (result/cert_132_1_45_sh.json) is the literal live upper bound, so it lowers 45 to 44.
   - The d = 44 certificate (result/cert_132_1_44_sh.json) is stronger and lowers 45 to 43. The LP uses A_j = B_j only for j < d and A_j <= B_j for j >= d. So it excludes every [[132,1,d']] with d' >= 44, and "at most 43" is not stretched.
   - The headline d = 44 is not literally "d equal to the live upper bound". The d = 45 certificate covers the literal reading, and 44 gives the stronger statement. MET.

3. "re-fetched live immediately before claiming": I cannot re-fetch because I had no web access. I only confirmed that the folder holds timestamped fetches (19:43:25Z and 19:43:40Z, HTTP 200, today's date) whose hashes match and whose content agrees with each other. The page footer reads "Last change: 10.06.2024". This is a process clause I can check for consistency only, not for liveness. Accepted on the recorded evidence, and flagged as the one non-reproducible clause.

4. "exact rational infeasibility certificate (Farkas dual) of the quantum weight-enumerator LP", with the stated constraints:
   - The constraints in check/check_cert.py are: A_0 = 1; sum A_i = 2^(n-k); MacWilliams row j with A_j = B_j for 1 <= j <= d-1; A_j <= B_j for d <= j <= n; nonnegativity of A (the Farkas rule uses c_i <= 0); and shadow rows Sh_j >= 0 for 0 <= j <= n.
   - The criterion lists exactly these: the MacWilliams link, A_i <= B_i, A_i = B_i for 0 < i < d, nonnegativity, and shadow nonnegativity "where used". Normalisation A_0 = 1 and the total count are standard, and are implied by B_0 = 1 for a stabilizer code. There is no extra, unjustified constraint: no integrality, evenness, purity or divisibility rows.
   - I checked the model is sound (null-model test). Script work/sanity.py brute-forces real stabilizer codes [[5,1,3]], [[7,1,3]], [[8,3,3]] and [[9,1,3]]. For each, B_j = 2^-(n-k) sum K_j(i) A_i holds exactly, the shadow Sh_j = 2^-(n-k) sum (-1)^i K_j(i) A_i is >= 0, and the Farkas algebra identity (sum c_i A_i = value + sum vG*G + sum vH*H, with the Q rows equal to 0) holds with random multipliers. So every real code satisfies every constraint, and the certificate's infeasibility therefore proves nonexistence for stabilizer codes.
   - Multipliers: u_Q (equalities) may have any sign. v_G and v_H are nonnegative, which is checked. Indices are in range (u_Q in 1..d-1, v_G in d..n). The value u_E0 + u_E1*2^(n-k) is positive. Every column coefficient is <= 0. MET.

5. "checked in exact integer arithmetic by an independent script":
   - `python3 -I check/check_cert.py result/cert_132_1_44_sh.json` printed "VERIFIED [[132,1,44]] shadow=True: value=1095 digits, max column coefficient <= 0, 43+2+41 multipliers" and exited 0.
   - `python3 -I check/check_cert.py result/cert_132_1_45_sh.json` printed "VERIFIED [[132,1,45]] shadow=True ... 44+2+44 multipliers" and exited 0.
   - I wrote my own checker, work/indep.py, which uses polynomial expansion of (1+3z)^(n-i)(1-z)^i instead of the binomial-sum formula, and Python ints throughout. `python3 -I work/indep.py result/cert_132_1_44_sh.json result/cert_132_1_45_sh.json` printed "INDEP OK" for both, with value > 0 and all column coefficients <= 0.
   - The checker is by the same author as the certificate, but it is standard-library only, contains no LP solver, and agrees with my re-implementation. MET.

6. "NOT already implied by applying the standard propagation rules to other live cells":
   - I ran `python3 -I check/parse_table.py data/qubit_table_full_n1-256.html work/parsed.json`. It printed "cells 33152 n-range 1 256", which is the expected total (256*257/2 + 256).
   - I ran `python3 -I check/propagate.py work/parsed.json work/closure.json`.
   - The last command printed `[27, 45] 45`.
   - Neighbours: (133,1) = 27-45, so R2 gives 45. (131,2) = 26-45, so R3 gives 46. R1 does not apply at k = 1. The minimum k = 1 upper bound over n >= 132 in the live table is 45.
   - The closure at (132,1) is 45, so 43 and 44 are not implied by the rules named in the criterion. The page's note "for n>100 the upper bounds on qubit codes are weak (and not necessarily monotone in k)" is consistent with the stated bound. MET.

## Hidden quantifiers and stretched definitions
- "No [[132,1,44]] stabilizer code" means additive/stabilizer qubit codes. It does not cover nonadditive codes. The criterion itself says stabilizer, so this is not a stretch, but the scope sentence must stay limited to it.
- The table's own upper bound is not shown to come from an LP. The page says upper bounds for n > 100 are weak. So the win is real against the live table, but I did not and cannot check the literature outside the folder.
- Liveness (clause 3) is checked by recorded hashes only.
- The check/ directory also holds a large family of other cells that are above their closure (1072 cells with n > 100). Those are irrelevant to this cell and are not claimed.

confirmed_scope: For qubit stabilizer codes, the exact integer Farkas certificates result/cert_132_1_44_sh.json and result/cert_132_1_45_sh.json (quantum weight-enumerator LP with Rains shadow constraints, verified by check/check_cert.py and by my independent re-implementation) show that no [[132,1,d]] code exists for any d >= 44, lowering the recorded table upper bound of 45 (from the saved fetches, not re-fetched by me) to at most 43, and that value is not implied by R1/R2/R3 propagation from the other cells of the saved table (closure at (132,1) = 45).

pass: true
