context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: The exact-integer Farkas certificate result/cert_200_2_66_sh.json (verified by check/check_cert.py) proves that no qubit stabilizer code [[200,2,d]] with d >= 66 exists, so the [[200,2]] upper bound (67 in data/QECC_q4_n200_k2_claimtime.html) is lowered to at most 65, and the closure of the rules R1-R3 over data/qubit_table_full_n1-256.html at (200,2) is 67, so this is not implied by neighbouring cells.

## Reasoning
Criterion: for a qubit cell with 101<=n<=256, prove no [[n,k,d]] stabilizer code at d = live upper bound by an exact Farkas certificate of the weight-enumerator LP (MacWilliams link, A_i<=B_i, A_i=B_i below d, nonnegativity, optional shadow), checked in integer arithmetic by an independent script, and not implied by standard propagation.

Commands run (inside the claim folder):
- python3 -I check/check_cert.py result/cert_200_2_66_sh.json -> VERIFIED [[200,2,66]] shadow=True: value=2417 digits, max column coefficient <= 0, 65+2+66 multipliers
- python3 -I check/check_cert.py result/cert_200_2_67_sh.json -> VERIFIED [[200,2,67]] shadow=True: value=2342 digits, max column coefficient <= 0, 66+2+66 multipliers
- Re-ran check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html: cells (200,2) live [39, 67], closure 67; neighbours (199,2), (201,2), (200,1), (200,3) all have upper bound 67 with closure 67. check/propagation_check.txt agrees (R1 67, R2 67, R3 (199,3) 67).
- data/QECC_q4_n200_k2_claimtime.html records "upper bound: 67" for [[200,2]].

Checker audit (read check/check_cert.py): integer-only, rows match the LP stated in its docstring (E0, E1, Q_j equalities for 1<=j<d, G_j for d<=j<=n, shadow H_j for all j with (-1)^i K_j(i)). Index ranges and sign constraints on multipliers are enforced; every column coefficient is tested <= 0 and value = u_E0 + u_E1*2^(n-k) > 0. The Farkas argument is sound; the shadow inequality is valid for stabilizer codes (Rains).

Hidden-quantifier / definition checks:
- Literal reading (d = live bound 67): the d=67 certificate verifies, so the criterion is met literally, lowering 67 to at most 66.
- Stronger d=66 certificate: its constraints (A_j=B_j for j<66) hold for every code with d>=66, so it rules out all d>=66, giving bound 65. Valid, and it subsumes the d=67 certificate.
- Scope: stabilizer (additive, pure-LP-style) qubit codes only, as the criterion states; no claim about nonadditive codes. The LP uses k=2 only via |S|=2^198; no extra assumptions seen.
- Null model / propagation: closure of R1-R3 is 67, so the new bound is not derivable from other live cells. Caveat: "live" status rests on the saved snapshots (the full table is 4 minutes older than the single-cell record); I did not re-fetch, as instructed. The checker was authored by the claimant, but it is short, standard-library, and I audited it above.
- Not a named partial win being stretched: it is the full criterion.

pass: true
