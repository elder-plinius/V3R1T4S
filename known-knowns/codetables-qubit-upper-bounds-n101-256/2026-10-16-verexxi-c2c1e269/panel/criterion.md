# VERDICT (criterion skeptic)

context: subagent (same VM)

Only files inside this folder were read or run. I created work/ (my own scripts and outputs).

## Clause-by-clause

1. "some qubit cell (n,k) with 101 <= n <= 256": cell is (164,1); 101 <= 164 <= 256. OK.

2. "live table upper bound, re-fetched live immediately before claiming": I have no web access, so I can only check the stored fetch.
   - `sha256sum data/*.html` gives 05af667a...ab1d8 (cell page) and 26245491...de4b0b6 (full table). Both match CLAIM.md.
   - The cell page text reads "Bounds on [[164,1]] ... lower bound: 33 upper bound: 55".
   - The parsed full table (`parse_table.py`) gives T[164][1] = [33, 55].
   - The fetch time (19:44:32Z and 19:43:25Z) is recorded in CLAIM.md only, not inside the HTML. The folder was written at 20:00. I cannot independently confirm "immediately before" or that the live site is unchanged now. This is a limit of the evidence, not a contradiction.

3. "proof that no [[n,k,d]] exists for d equal to the live upper bound (55)": result/cert_164_1_55_sh.json is a certificate for d = 55.
   - `python3 -I check/check_cert.py result/cert_164_1_55_sh.json` prints `VERIFIED [[164,1,55]] shadow=True: value=1830 digits ... 54+2+55 multipliers`, exit 0.
   - So the literal reading (d = live upper bound) is covered, not only d = 54.

4. "thereby lowering it by at least 1": result/cert_164_1_54_sh.json is a certificate for d = 54.
   - `python3 -I check/check_cert.py result/cert_164_1_54_sh.json` prints `VERIFIED [[164,1,54]] shadow=True: value=1685 digits ... 53+2+53 multipliers`, exit 0.
   - A [[164,1,55]] code is also a [[164,1,54]] code, and the d = 54 LP is a relaxation of the d = 55 LP, so the d = 54 certificate is the stronger one. The upper bound drops from 55 to 53, a lowering of 2 (at least 1). OK.

5. "exact rational Farkas certificate of the stated LP with exactly the stated constraints":
   - I read check/check_cert.py and wrote my own checker in a different style (work/mycheck.py). It builds the Krawtchouk table by polynomial multiplication of (1+3z)^(n-i)(1-z)^i, not by the binomial sum, with exact Python integers and no floats.
   - Output: `(164, 1, 54, True, True, 53, 2, 53, ...)` and `(164, 1, 55, True, True, 54, 2, 55, ...)`. The two True values are (value > 0, max column coefficient <= 0). Index ranges are asserted: u_Q on 1..d-1, v_G on d..n, v_H on 0..n, and all v >= 0. Equality multipliers (u_Q, u_E0, u_E1) may have any sign. An extra scan found no negative v_G or v_H.
   - Soundness of the Farkas argument: sum c_i A_i = value + sum v_G*G(A) + sum v_H*H(A) >= value > 0, while c_i <= 0 and A >= 0 force the left side to be <= 0. Contradiction.
   - Rows used are the stated ones: A_0 = 1; sum A = 2^(n-k) (equivalent to B_0 = 1); A_j = B_j for 0 < j < d; A_j <= B_j for j >= d; A >= 0; and shadow >= 0. B comes from the MacWilliams identity.
   - Integer multipliers are rational. Hidden-quantifier check: A_0 = 1 and the total-size normalisation are not listed word for word in the criterion. They are the definition of the stabilizer enumerator and are not extra restrictions.
   - Null-model check of the LP itself: I enumerated the stabilizers of [[5,1,3]], [[7,1,3]] and [[9,1,3]] and checked the same formulas. A_j = B_j below d, A <= B, shadow >= 0 and shadow divisible by 2^(n-k) all hold. So the constraints are valid for real codes and the infeasibility is not an artifact of a wrong formula. I did not re-derive that the LP is feasible for lower d, because no LP solver is installed.

6. "independent script": check/check_cert.py uses the standard library only and is separate from the certificate. The generator is not in this folder. My own re-check is a second independent implementation. OK.

7. "NOT already implied by the propagation rules applied to other live cells":
   - Commands: `python3 -I check/parse_table.py data/qubit_table_full_n1-256.html work/parsed.json`, then `python3 -I check/propagate.py work/parsed.json work/closure.json`.
   - Printed `[33, 55] 55`: the closure at (164,1) is 55, so 53 is not implied.
   - I read propagate.py. R1 needs k >= 2 and does not apply at k = 1. R2 uses (165,1) = [33,55]. R3 uses (163,2) = [32,55] and gives 56.
   - The rules are applied to k >= 1 only. Table cells outside k >= 1 do not feed the rules for a k = 1 cell, so this is a reasonable reading.
   - The live table is non-monotone elsewhere, with 1075 cells above their closure. That does not affect (164,1).
   - The rules are applied to the stored snapshot, not to the live table now.

8. Direction: min upper bound, 55 -> 53. OK.

## Residual caveats
- Freshness is attested by CLAIM.md and by file hashes, not reproducible offline.
- The success concerns the upper-bound entry for (164,1) only.
- data/TROPHY_CASE_pinned_9b1d444.md contains no mention of this cell (grep for qubit, stabilizer, codetables and [[ returned nothing).

confirmed_scope: Within the stored 2026-10-16 codetables.de snapshot (upper bound 55 for qubit cell (164,1), closure of the propagation rules R1-R3 over that snapshot also 55), integer-multiplier Farkas certificates for d = 54 and d = 55 were verified exactly by two independent scripts, so the quantum weight-enumerator LP with MacWilliams, A_j = B_j for 0 < j < d, A_j <= B_j and shadow nonnegativity is infeasible and no [[164,1,54]] or [[164,1,55]] stabilizer code exists, which lowers that cell's upper bound from 55 to 53 and is not implied by other cells of that snapshot.

pass: true
