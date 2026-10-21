context: subagent (Claude Code headless on the owner's PC, fresh context)

# Criterion skeptic verdict, [[185,3]]

## What I did and real output
- Read CLAIM.md, REPRODUCE.md, check/check_cert.py (read the code in full: exact integer Farkas check, column coefficients <= 0, positive value, multiplier index and sign ranges validated, shadow rows require nonnegative multipliers).
- Ran `python3 -I check/check_cert.py result/cert_185_3_63_sh.json` -> `VERIFIED [[185,3,63]] shadow=True: value=1695 digits, max column coefficient <= 0, 60+2+59 multipliers`
- Ran `python3 -I check/check_cert.py result/cert_185_3_61_sh.json` -> `VERIFIED [[185,3,61]] shadow=True: value=1695 digits, max column coefficient <= 0, 60+2+59 multipliers`
- Ran check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html; printed cell (185,3) and closure: `[36, 63] 61`. Neighbours: (184,4) = [35,62], (184,3) = [36,62], (185,2) = [36,63], (186,3) = [36,63].
- Claim-time page data/QECC_q4_n185_k3_claimtime.html reads "Bounds on [[185,3]]" with upper bound 63 (consistent with CLAIM.md).

## Reasoning
- Literal criterion: n in 101..256 (185 ok); a proof that no [[n,k,d]] exists for d equal to the live upper bound (63), via an exact Farkas certificate of the weight-enumerator LP with A_i<=B_i, A_i=B_i for 0<i<d, nonnegativity and shadow nonnegativity, checked in integer arithmetic by an independent script. The d=63 certificate is itself verified by the checker, so the literal reading is met directly, not only via d=61.
- Hidden quantifier check: the LP used is the standard one for stabilizer (additive) codes. Equality only below d, inequality above, so impure codes are not excluded. Shadow constraints are valid for any additive code. Nothing restricts the code family (no purity or linearity assumption). The checker's docstring proof is sound.
- Null model / subsumption: the closure of the live table under the three propagation rules at (185,3) is 61, so a bound of 60 (and even 62) is not implied by other live cells. The claim of at most 60 is strictly below the propagation-implied 61, and below the live 63. The proof is a genuine exact LP infeasibility, not a propagation consequence.
- Caveat noted: the live table sits above its own propagation closure (63 vs 61), so part of the gap 63 -> 61 is table staleness, but the criterion only demands non-subsumption by propagation of other live cells and a lowering by at least 1; the certificate excludes d=61 which goes beyond even the closure.

confirmed_scope: For the qubit cell [[185,3]], the checked exact integer Farkas certificates (with Rains shadow constraints) show no stabilizer code [[185,3,d]] exists for d = 61 and for d = 63 (the live upper bound of 63 at claim time), giving an upper bound of at most 60, which is not implied by propagation rules applied to the live table (closure value 61).

pass: true
