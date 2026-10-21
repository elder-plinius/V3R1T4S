context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE verdict for [[219,2]] upper bound 73 -> 72

## What I did (real output)
1. Read CLAIM.md and REPRODUCE.md. Looked only at the structure of result/cert_219_2_73_sh.json (keys n=219, k=2, d=73, shadow=true, u_E0, u_E1, u_Q with 72 entries (j=1..72), v_G with 2 entries (j=75,76), v_H with 73 entries (j in 0..79)), not at the author's code.
2. Wrote my own checker (scratch scripts mychk.py and mychk2.py, since deleted) from the definition: A_0..A_n >= 0, |S| = 2^217, B_j = 2^-217 sum_i K_j(i) A_i with K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s), shadow Sh_j = 2^-217 sum_i (-1)^i K_j(i) A_i >= 0, A_0 = 1, sum A_i = 2^217, A_j = B_j for 1 <= j < 73, A_j <= B_j for j >= 73. My first attempt got the signs of the free equality multipliers wrong. I tried all four sign combinations of (equality multipliers, inequality multipliers). The consistent convention is c_i = u_E0[i=0] + u_E1 + sum_j w_j (K_j(i) - 2^217 [i=j]) + sum_j v_Hj (-1)^i K_j(i), with w = u_Q + v_G.
   Farkas argument: sum_i c_i A_i = value + sum v_G G(A) + sum v_H H(A) for any A satisfying the equalities. If A >= 0 is feasible, the right side is >= value > 0 while the left side is <= 0 when every c_i <= 0. That is a contradiction.
3. My independent exact integer (Python big int) result for this convention: index ranges legal (u_Q in 1..72, v_G in 73..219, v_H in 0..219); all v_G, v_H >= 0; value = u_E0 + u_E1*2^217 > 0; all 220 column coefficients c_i <= 0 (some are strictly negative, not all strictly). A sanity check K_5(0) = 3^5 C(219,5) held. Re-running my checker twice gave identical output (same md5), so it is deterministic.
4. After that I read check/check_cert.py. Its LP and Farkas rule are the same as mine and it matches the definition. Its output: "VERIFIED [[219,2,73]] shadow=True: value=2627 digits, max column coefficient <= 0, 72+2+73 multipliers", exit code 0, identical to check/checker_output.txt.
5. Checked that the LP is a valid necessary condition for a qubit stabilizer code with parameters [[n,k,d]]: the MacWilliams relation, the Rains shadow nonnegativity, S contained in its normalizer (A_j <= B_j), and A_j = B_j below d are all standard, and the 2^(n-k) normalization is right for |S| = 2^(n-k). The identity is checked over all 220 columns, so this is exhaustive and not a sample.
6. Table record: sha256 of data/QECC_q4_n219_k2_claimtime.html and data/qubit_table_full_n1-256.html match CLAIM.md exactly (6af37db3... and 26245491...). The saved page says "lower bound 42, upper bound 73" for [[219,2]]. Ran check/parse_table.py and check/propagate.py: 33152 cells parsed, [42, 73] and closure 73 at (219,2). I checked the neighbours by hand from the parsed table: ub(219,1)=73, ub(220,2)=74, ub(218,3)+1=74. So no rule (R1, R2, R3) gives 72 and the new bound is not implied by propagation.
7. No web requests were made. Scratch files were removed.

## Reasoning
The certificate is an exact integer Farkas infeasibility proof of the quantum weight-enumerator LP with shadow constraints for d = 73. It verified under my independently written checker and under the author's checker, with deterministic output. The claimed cell is 219 in 101..256, the saved table upper bound is 73, and propagation from other live cells does not imply 72. The reproduced claim is that no [[219,2,73]] stabilizer code exists, so the upper bound is at most 72.
Caveat: the live table could not be re-fetched (no access allowed), so "live at claim time" rests on the saved page and its hash.

pass: true
