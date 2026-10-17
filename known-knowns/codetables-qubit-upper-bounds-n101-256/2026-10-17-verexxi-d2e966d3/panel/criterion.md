context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: The exact integer Farkas certificate result/cert_122_1_41_sh.json, verified by check/check_cert.py, shows the quantum weight-enumerator LP (A_0=1, sum A_i=2^121, A_j=B_j for 1<=j<=40, A_j<=B_j for j>=41, shadow enumerator nonnegativity) is infeasible for [[122,1,41]], so no qubit stabilizer code [[122,1,41]] exists and the [[122,1]] upper bound is at most 40 against the claim-time table value of 41, and this value is not implied by the propagation rules R1, R2, R3 applied to the claim-time table.

What I ran (real output):
- python3 -I check/check_cert.py result/cert_122_1_41_sh.json printed "VERIFIED [[122,1,41]] shadow=True: value=866 digits, max column coefficient <= 0, 40+1+39 multipliers", exit code 0. It matches check/checker_output.txt.
- I read the checker source. It is standard library only, integer arithmetic only. It enforces the index ranges for the u_Q, v_G, v_H multipliers, requires v_G and v_H >= 0, requires a positive value, and checks every column coefficient <= 0. The Farkas rule in its docstring is correct. The rows are the standard LP rows (quaternary MacWilliams identity and Rains shadow), scaled by 2^(n-k).
- I re-ran check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html. It reported live (122,1) = [25, 41] and a closure of 41 at (122,1). The neighbours (121,1), (123,1), (121,2) and (122,2) are all [25, 41], so R1, R2 and R3 give no better than 41. The new bound of 40 is therefore not implied by other cells.

Reasoning:
- The criterion requires four things: an exact rational Farkas certificate of the weight-enumerator LP with A_i<=B_i, A_i=B_i below d, and shadow constraints; checking by an independent script in exact integers; d equal to the live upper bound (41, shown in the claim-time page); and no implication by propagation. All four are met.
- Hidden quantifiers: the claim is for the single cell (122,1) with d=41, which is the live upper bound. n=122 is inside 101..256. It says stabilizer codes only, which is what the criterion says. The claim states the LP and its sources and makes no wider statement about non-stabilizer codes.
- Null model: the live table value 41 equals the closure, so the table has no stronger source bound. The certificate uses the shadow constraints, which is why it may beat the table's earlier LP. A table entry could in principle rest on an LP without shadow constraints, but that does not affect the claim.
- Residual caveat: the "independent script" is by the same author as the certificate and uses the same LP. Its LP statement is standard, so I accept it as an independent exact checker.
- Residual caveat: the live table was not re-fetched by me (no web access). I rely on the saved claim-time page, which the claim's own checks cover.

pass: true
