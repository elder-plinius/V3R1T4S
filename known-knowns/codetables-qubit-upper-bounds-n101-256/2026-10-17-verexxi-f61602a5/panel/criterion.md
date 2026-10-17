context: subagent (Claude Code headless on the owner's PC, fresh context)

# Criterion skeptic verdict, claim q215-6 ([[215,6]], upper bound 73 -> 71)

## What I did
Read CLAIM.md, REPRODUCE.md and check/check_cert.py (full source, about 85 lines, standard library, integer arithmetic only). Ran:

- python3 -I check/check_cert.py result/cert_215_6_73_sh.json
  -> VERIFIED [[215,6,73]] shadow=True: value=1994 digits, max column coefficient <= 0, 71+2+71 multipliers
- python3 -I check/check_cert.py result/cert_215_6_72_sh.json
  -> VERIFIED [[215,6,72]] shadow=True: value=1994 digits, max column coefficient <= 0, 71+2+71 multipliers
- python3 -I check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html, then read cell (215,6).
  -> live cell [41, 73], propagation closure of all live cells at (215,6) = 72. Neighbours: (214,7) = [40, 72], (216,6) = [41, 73], (215,5) = [41, 73].
  The checker output in check/propagation_check.txt matches.
- grep of data/QECC_q4_n215_k6_claimtime.html confirms an "upper bound" page for the cell; the claim-time record states 41 / 73.

## Reasoning
1. Criterion: a proof that no [[n,k,d]] exists for d = live upper bound, lowering it by at least 1, via an exact Farkas certificate of the quantum weight-enumerator LP (MacWilliams linking, A_i <= B_i, A_i = B_i for 0 < i < d, nonnegativity, shadow nonnegativity), checked in exact integers by an independent script, and NOT implied by propagation of other live cells.
2. The checker encodes exactly that LP: A_0 = 1, sum A = 2^(n-k), equalities below d, inequalities from d on, Rains shadow rows >= 0. The Farkas rule is correct: every column coefficient is <= 0 and the right-hand side value is positive, so no nonnegative A exists. I read the column loop and sign handling and found no error. The shadow constraint is a valid constraint for stabilizer codes (Rains), so it is a permitted "where used" extension.
3. Hidden quantifier check. The literal d = 73 certificate (cert_215_6_73_sh.json) is only the weaker statement; it is implied by propagation, since the closure of the live table already gives 72. The claim does not rest on it. The claim rests on d = 72: no [[215,6,72]] code, hence no [[215,6,d]] with d >= 72 (a code with larger distance also satisfies the LP for d = 72, because the equalities A_j = B_j for j < 72 hold). So the upper bound is at most 71. The claim text states 71, not 72, so the stated bound is not stretched.
4. Null model: the propagation closure is 72, and 71 < 72, so the new bound is strictly stronger than anything the standard rules (R1, R2, R3) derive from other live cells. This is also not a mere table-inconsistency fix: the stale 73 versus closure 72 gap is a free improvement of 1, but the certificate gives 2. The claim is therefore not subsumed. The part from 73 to 72 is implied by propagation; the part from 72 to 71 is genuinely new.
5. The live-table re-fetch "immediately before claiming" was recorded at 2026-10-17T05:36:07Z in the claim folder (HTTP 200, sha256 stated). I could not and did not re-fetch it; I rely on the saved page, as instructed.
6. Residual caveats: the d = 73 certificate was derived by relabelling rows from the d = 72 one, but it verifies independently, so this is harmless. The checker is the claimant's own script, but it is short, standard-library only, and I audited its logic by reading it.

confirmed_scope: The exact integer-checked Farkas certificate (shadow-enhanced quantum weight-enumerator LP) in result/cert_215_6_72_sh.json shows no qubit stabilizer code [[215,6,72]] exists, so the [[215,6]] distance upper bound is at most 71, which is below both the saved claim-time table value 73 and the propagation closure 72 of the saved full table (no claim about lower bounds or any other cell).

pass: true
