context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic verdict for [[195,2,65]] nonexistence (upper bound 65 -> 64)

## What I did
1. Read CLAIM.md and REPRODUCE.md. Listed the folder. Inspected only the structure of result/cert_195_2_65_sh.json (keys: n,k,d,shadow,u_E0,u_E1,u_Q[1..64],v_G[67,68],v_H[64 indices]) before reading any author code.
2. Wrote my own checker (scratch file my_check.py) from the definition, not from the author's code. Definition used: the quantum LP for a qubit stabilizer code [[n,k,d]], with A_j the stabilizer weight distribution and M = 2^(n-k) = 2^193. K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s) is the quaternary Krawtchouk polynomial. Rows, scaled by M:
   - E0: A_0 = 1.
   - E1: sum A_i = M.
   - Q_j: sum_i K_j(i) A_i - M A_j = 0, for 1 <= j <= d-1 = 64.
   - G_j: sum_i K_j(i) A_i - M A_j >= 0, for j >= d (A_j <= B_j).
   - H_j: sum_i (-1)^i K_j(i) A_i >= 0 (Rains shadow).
   Farkas rule: with free multipliers on equalities and nonnegative multipliers on >= rows, if every column coefficient c_i of the combination is <= 0 and u_E0 + u_E1*M > 0, then value = sum c_i A_i - sum v*(G,H rows) <= 0 for any feasible A >= 0. That contradicts value > 0, so the LP is infeasible.
3. My first run used the wrong sign convention for the inequality rows, which is my error, not the certificate's. It produced FAIL (a positive column coefficient). I re-derived the sign from the Farkas argument above and fixed the script. Only after that did I read check/check_cert.py. Its docstring states the same convention (G, H as >= rows with nonnegative multipliers).
4. Real output of the corrected my_check.py (python -I my_check.py): max column coefficient 0, rhs > 0 True (rhs has 2189 digits), maxcol<=0 True, 195 nonzero columns, OK. It asserted that the u_Q indices are exactly 1..64, that all v_G indices are >= 65, and that all multipliers are nonnegative. It also asserted K_j(0) = 3^j C(n,j) as a sanity check on the Krawtchouk code. The output is identical on a repeat run (same md5), so it is deterministic.
5. Ran python -I check/check_cert.py result/cert_195_2_65_sh.json. It printed "VERIFIED [[195,2,65]] shadow=True: value=2189 digits, max column coefficient <= 0, 64+2+64 multipliers", exit code 0. Its output md5 equals check/checker_output.txt.
6. Table record. The sha256 of data/QECC_q4_n195_k2_claimtime.html and of data/qubit_table_full_n1-256.html both match CLAIM.md. The claim-time page says "lower bound: 38, upper bound: 65" for [[195,2]]. I parsed the full table with my own regex and read these cells: (195,2) = 38-65, (195,1) = 38-65, (196,2) = 38-66, (194,3) = 37-65.
7. Propagation. I applied the stated rules by hand to the neighbours:
   - R1: d(195,2) <= d(195,1) <= 65.
   - R2: d(195,2) <= d(196,2) <= 66.
   - R3: d(195,2) <= d(194,3)+1 <= 66.
   None gives 64, so the new bound is not implied by those direct neighbours.
   I ran check/parse_table.py and check/propagate.py. The full closure at (195,2) is 65, and the printed pair is [38, 65] 65. Closure output is deterministic (identical file on a second run). check/propagation_check.txt agrees.

## Reasoning
- The certificate is an exact integer Farkas certificate with 64 equality multipliers, 2 G multipliers and 64 shadow multipliers. My independently written checker confirms that every column coefficient is <= 0 (the maximum is exactly 0) and that the value is positive. This holds under the standard, valid LP: MacWilliams, A_j = B_j below d, A_j <= B_j, and Rains shadow nonnegativity.
- Using a subset of the G constraints (only j = 67 and 68) is sound, since any subset of valid constraints is valid.
- The LP exhaustively covers all real nonnegative A, so no sampling is involved. The check is complete for every column 0..195.
- The table record matches the saved page and hashes, and the propagation closure leaves 65 as the implied bound. The claim is therefore a genuine lowering to 64 relative to the saved record. I could not and did not check the live table, since I made no web requests and was told to rely on the saved page.
- No mismatch, missing object or non-determinism was found.

pass: true
