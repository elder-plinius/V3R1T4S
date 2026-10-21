# Criterion skeptic verdict, claim q155-3

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I did and real output
Read CLAIM.md, REPRODUCE.md, check/check_cert.py in full. Ran, inside the claim folder:

    python3 -I check/check_cert.py result/cert_155_3_53_sh.json
    VERIFIED [[155,3,53]] shadow=True: value=1210 digits, max column coefficient <= 0, 50+2+50 multipliers   (rc=0)
    python3 -I check/check_cert.py result/cert_155_3_51_sh.json
    VERIFIED [[155,3,51]] shadow=True: value=1210 digits, max column coefficient <= 0, 50+2+50 multipliers   (rc=0)

Reran check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html; output for the cell:
`[30, 53] 52` (live bounds, closure of the live table by R1, R2, R3). check/propagation_check.txt agrees: R1 (n,k-1) gives 53, R2 (n+1,k) gives 53, R3 (n-1,k+1)+1 gives 52.
sha256 of both saved HTML files match the values in CLAIM.md. The saved cell page reads "lower bound: 30, upper bound: 53".

## Reasoning
- Checker: integer-only, standard library. It rebuilds the Krawtchouk coefficients itself and tests every column c_i <= 0 with positive value. Index ranges and signs of the multipliers are validated. The Farkas argument in its docstring is correct: value = sum c_i A_i - sum v_G G - sum v_H H <= 0 for any feasible A >= 0, contradicting value > 0.
- The LP is valid for stabilizer codes. A_0 = 1, sum A = 2^(n-k), A_j = B_j for j < d (this holds for impure codes too, since N-elements of weight < d lie in S), A_j <= B_j, and shadow nonnegativity (Rains). Dropping any valid constraint only weakens the LP, so infeasibility is a sound proof. "Exists with d >= 51" is the table convention, so excluding d = 51 excludes all larger d, giving upper bound <= 50.
- Criterion check: (n,k) = (155,3) is in 101..256. The target d is the live upper bound (53); cert_155_3_53 verifies on its own. The stronger cert for 51 lowers the bound by 3. A Farkas certificate is exact and checked by a separate script. Shadow constraints are explicitly allowed.
- Null model / subsumption: the standard propagation closure at this cell is 52, so a bound of 52 would be implied by other cells, but 50 is not. Even the 53 certificate alone yields <= 52, which equals the closure, so it would be subsumed. The claim's 50 is not subsumed. The claim is worded correctly (<= 50, via d = 51).
- Possible quibbles: the live page was fetched once, so "immediately before" cannot be re-verified without network access; the claim-time record is internally consistent. The 53 certificate is derived from the 51 one, but it is checked independently, so there is no hidden quantifier.

confirmed_scope: No qubit stabilizer code [[155,3,d]] with d >= 51 exists, shown by an exact integer-checked Farkas certificate (quantum weight-enumerator LP with Rains shadow constraints) in result/cert_155_3_51_sh.json, so the [[155,3]] upper bound drops from the saved claim-time table value of 53 to at most 50, below the propagation closure of 52 from the other saved table cells.

pass: true
