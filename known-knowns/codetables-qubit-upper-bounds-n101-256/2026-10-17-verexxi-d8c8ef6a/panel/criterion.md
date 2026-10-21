context: subagent (Claude Code headless on the owner's PC, fresh context)

# Criterion skeptic verdict, [[161,2]]

## What I did and real output
Ran in the claim folder:
- python3 -I check/check_cert.py result/cert_161_2_55_sh.json
  -> VERIFIED [[161,2,55]] shadow=True: value=1317 digits, max column coefficient <= 0, 52+2+52 multipliers (rc=0)
- python3 -I check/check_cert.py result/cert_161_2_53_sh.json
  -> VERIFIED [[161,2,53]] shadow=True: value=1317 digits, max column coefficient <= 0, 52+2+52 multipliers (rc=0)
- python3 -I check/parse_table.py data/qubit_table_full_n1-256.html, then check/propagate.py, then the REPRODUCE one-liner
  -> [31, 55] 54  (live cell and propagation closure)
- check/propagation_check.txt: "live (161,2): [31, 55]  closure of the live table at (161,2): 54; R1 (n,k-1): [33, 55]; R2 (n+1,k): [32, 55]; R3 (n-1,k+1): [31, 54]".
- data/QECC_q4_n161_k2_claimtime.html: header "Bounds on the minimum distance of additive quantum codes", record consistent with upper bound 55 as stated in CLAIM.md. I could not re-fetch it live (no web access allowed).

## Reasoning
- Criterion requires: an exact Farkas certificate of the weight-enumerator LP (MacWilliams-linked, A_i<=B_i, A_i=B_i below d, nonnegativity, shadow) checked in exact integer arithmetic by a separate script; lowering the live upper bound by at least 1; and not implied by propagation.
- The checker docstring states the LP precisely (E0, E1, equality rows Q_j for 1<=j<d, inequality rows G_j for j>=d, shadow rows H_j) and the Farkas rule; arithmetic is integer only. Both certificates verify.
- Hidden quantifier check: the literal criterion asks for d equal to the live upper bound (55); cert_161_2_55_sh.json covers exactly that and verifies on its own. The d=53 certificate is stronger: the LP with equalities below 53 and A_j<=B_j for all j>=53 covers every code with distance >=53, so it also rules out 54 and 55. The lowering is from 55 to at most 52 (3 steps), not merely 1. The 55-certificate being derived from the 53 one is not a defect: it verifies independently.
- Null model / subsumption: propagation closure of all live cells at (161,2) is 54, so an upper bound of 52 (or even 54 via d=55 alone) is not implied by neighbours under R1, R2, R3. The result is non-subsumed. The propagation uses the claim-time complete table, which is the best available evidence.
- Residual caveats: the "live immediately before claiming" fetch is only evidenced by the saved claim-time page; the checker and LP formulation are by the same author as the certificate generator (the checker is a separate script, which is what the criterion requires). The shadow constraint is the accepted Rains one. The certificate proves nonexistence of stabilizer (additive) qubit codes; this is the table's scope.

confirmed_scope: For qubit stabilizer codes [[161,2]], an exact integer-arithmetic Farkas certificate of the weight-enumerator LP with Rains shadow constraints, verified by check/check_cert.py, shows no [[161,2,d]] code exists with d>=53 (including d=55, the claim-time table upper bound), so the upper bound is at most 52, and this is not implied by propagation from the claim-time table (closure 54).

pass: true
