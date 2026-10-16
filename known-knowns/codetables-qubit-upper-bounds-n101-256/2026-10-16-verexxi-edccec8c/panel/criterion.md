context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: Given the saved table record (data/QECC_q4_n230_k3_claimtime.html: [[230,3]] upper bound 77, lower 44, unchanged by the R1/R2/R3 closure over the saved full table), result/cert_230_3_77_sh.json and result/cert_230_3_75_sh.json are exact integer Farkas certificates of the qubit weight-enumerator LP with Rains shadow constraints that pass check/check_cert.py, so no [[230,3,d]] stabilizer code exists for d >= 75 and the upper bound on [[230,3]] is at most 74; this is not a proof about anything beyond that cell, and "live at claim time" rests on the saved record only.

## Reasoning

Criterion read literally: for some qubit cell 101<=n<=256, an exact rational Farkas certificate of the quantum weight-enumerator LP (MacWilliams link, A_i<=B_i, A_i=B_i for 0<i<d, nonnegativity, shadow nonnegativity where used), checked in exact integer arithmetic by an independent script, for d equal to the live upper bound, lowering it by at least 1, and not implied by propagation. Cell (230,3) is inside 101..256.

1. Certificates verify (commands run in the claim folder):

    python3 -I check/check_cert.py result/cert_230_3_75_sh.json
    VERIFIED [[230,3,75]] shadow=True: value=3163 digits, max column coefficient <= 0, 74+4+74 multipliers  (rc=0)
    python3 -I check/check_cert.py result/cert_230_3_77_sh.json
    VERIFIED [[230,3,77]] shadow=True: value=2462 digits, max column coefficient <= 0, 76+3+75 multipliers  (rc=0)

2. Soundness of the checker, read line by line (check/check_cert.py). Integer-only arithmetic. Rows: Q_j equality for 1<=j<=d-1 (A_j=B_j, valid for pure and impure codes), G_j inequality for d<=j<=n (A_j<=B_j), H_j shadow >=0, E0 A_0=1, E1 sum A=2^(n-k). Farkas argument re-derived by me: for feasible A>=0, value = uE0+uE1*2^(n-k) = sum c_i A_i - sum vG*G(A) - sum vH*H(A) - sum uQ*Q(A) <= 0 when all c_i<=0, v>=0, contradicting value>0. Checker enforces index ranges, sign of v_G and v_H, positive value, and c_i<=0 for all i=0..n. No hidden quantifier found: nothing is left to be assumed about purity, and the shadow constraint is valid for every stabilizer code (Rains). The checker is stdlib only and does not depend on the solver.

3. Null/sanity models I ran: Krawtchouk orthogonality identity holds (n=12, True). For the [[5,1,3]] code A=[1,0,0,0,15,0], B=Sh=[1,0,0,30,15,18], sizes sum to 64 and B_j=A_j below d, so the formulas are correctly normalised. Perturbed certificates all FAIL: d=74 ("u_Q index outside 1..d-1"), k=4 ("column 77 has positive combined coefficient"), n=229 ("column 0 has positive combined coefficient"), shadow dropped ("column 78 has positive combined coefficient"). So the checker does not accept everything, and the shadow rows are essential to the 75 certificate.

4. Table record: data/QECC_q4_n230_k3_claimtime.html sha256 ac4e69556df8a90aafeb48b2131844e601841034c3127372a23300b7238480c3 (matches CLAIM.md), contains "lower bound: 44" and "upper bound: 77".

5. Propagation (not subsumed): re-ran check/parse_table.py then check/propagate.py on data/qubit_table_full_n1-256.html (33152 cells). Result [44, 77] 77, i.e. table entry for (230,3) is [44,77], closure is 77. Neighbours: (230,2)=[45,77], (231,3)=[44,77], (229,4)=[44,77]. No neighbour rule gives below 77, so the new bound is not implied by R1/R2/R3 on the saved table.

6. Caveats (limit scope, do not defeat the pass): I did not and may not re-fetch the live page, so "re-fetched immediately before claiming" is taken from the saved timestamped record. The result is an LP-infeasibility bound only; no claim about existence of a [[230,3,74]] code. The claim text's "at most 74" is conservative and matches cert 75; the literal criterion (d=77) is also covered by cert_230_3_77_sh.json.

pass: true
