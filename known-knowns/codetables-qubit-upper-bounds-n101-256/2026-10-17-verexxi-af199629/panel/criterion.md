context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: For the single qubit cell [[219,2]], the saved claim-time codetables.de record (upper bound 73) is lowered to 72 because result/cert_219_2_73_sh.json is an exact integer Farkas certificate, checked by check/check_cert.py, that no [[219,2,d]] stabilizer code with d >= 73 satisfies the quantum weight-enumerator LP with Rains shadow constraints, and the propagation closure of the saved complete table at (219,2) is 73, so 72 is not implied by other cells.

What I ran (real output):
- python3 -I check/check_cert.py result/cert_219_2_73_sh.json printed "VERIFIED [[219,2,73]] shadow=True: value=2627 digits, max column coefficient <= 0, 72+2+73 multipliers", exit code 0. This matches check/checker_output.txt.
- I re-ran check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html. The result was live [42, 73] and closure 73 at (219,2). The neighbours were (219,1) closure 73, (220,2) closure 74, and (218,3) closure 73. R1 gives 73, R2 gives 74, and R3 gives 73+1 = 74. So no rule applied to other live cells yields 72.
- sha256 of data/QECC_q4_n219_k2_claimtime.html and data/qubit_table_full_n1-256.html match the values in CLAIM.md. The saved page reads "Bounds on [[219,2]] lower bound: 42 upper bound: 73".
- I read check/check_cert.py in full. It builds the integer Krawtchouk polynomials from the explicit binomial sum and uses integer arithmetic only. It requires multiplier index ranges to be correct, nonnegative inequality multipliers, a positive certificate value, and every column coefficient <= 0.

Reasoning:
- The criterion needs an exact Farkas certificate of the weight-enumerator LP (MacWilliams link, A_i <= B_i, A_i = B_i for 0 < i < d, nonnegativity, shadow nonnegativity), checked independently in exact arithmetic. It also needs the new bound not to follow from the standard propagation rules. Both hold.
- Hidden quantifiers: the LP uses d = 73 only through A_j = B_j for j < 73. That holds for every stabilizer code of distance >= 73, so the certificate excludes all d >= 73 and the bound 72 follows. The scope is additive (stabilizer) codes, which is what the table covers. The cell is inside 101 <= n <= 256. The bound drops by exactly 1, from 73 to 72.
- The constraint forms (MacWilliams, A_j <= B_j, and shadow Sh_j = 2^-(n-k) sum (-1)^i K_j(i) A_i >= 0) match the standard Calderbank-Rains-Shor-Sloane and Rains formulations. The checker's Farkas argument is sound: value = sum c_i A_i - sum v_G G(A) - sum v_H H(A) <= 0 for any feasible A >= 0, contradicting the positive value.
- Null model and subsumption: the propagation closure is computed from the complete saved table, which has many non-monotone n>100 cells. Even so, (219,2) is not implied below 73. The weakness of the table for n>100 is documented on the page itself, which makes a genuine improvement plausible.
- Remaining limits: the live re-fetch is only as of the saved claim time, and I made no web request. Only the saved page and table are relied on, and both match their recorded hashes.

pass: true
