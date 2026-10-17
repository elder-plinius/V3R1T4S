# REPRODUCE skeptic verdict: [[135,6]] claim

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I did
1. Read CLAIM.md and REPRODUCE.md. Looked only at the certificate JSON layout (keys n,k,d,shadow,u_E0,u_E1,u_Q,v_G,v_H), not at any code.
2. Wrote my own checker from the definition (CRSSS quaternary MacWilliams plus Rains shadow). The LP is: A_i >= 0; A_0 = 1; sum A_i = 2^(n-k); B_j = 2^-(n-k) sum_i K_j(i) A_i with K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s); A_j = B_j for 0 < j < d; A_j <= B_j for j >= d; Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i >= 0. My Farkas rule: with row g.A >= 0 or = 0, u free on equalities and v >= 0 on inequalities, if every column of (u a + v g) is <= 0 and the right-hand side u.b is > 0, then the LP is infeasible. This is valid because the combination sums to (rhs + nonnegative terms) >= rhs > 0 but also <= 0. All arithmetic is exact Python integers.
3. My first attempt flipped the sign convention on the Q rows. It gave a column with a positive coefficient. That only reflects my row orientation; u is free on equalities. After orienting the Q rows the same way as G (K_j(i) - 2^(n-k) delta_ij), my checker gave this output:
   - cert_135_6_44_sh.json: all 136 column coefficients <= 0 (135 strictly negative, 1 zero), right-hand side u_E0 + u_E1 * 2^129 > 0, and all v_G, v_H >= 0, so the result is True.
   - cert_135_6_45_sh.json: the same, True.
   I also tried scaling the E0 row by 2^129. That fails, but it is just a wrong scaling of a different row and not the stated LP. The natural row A_0 = 1 passes.
4. Then read check/check_cert.py. Its LP statement, index ranges and Farkas rule match my own derivation. Ran it:
   - python -I check/check_cert.py result/cert_135_6_45_sh.json prints "VERIFIED [[135,6,45]] shadow=True: value=898 digits, max column coefficient <= 0, 43+2+43 multipliers", exit 0.
   - python -I check/check_cert.py result/cert_135_6_44_sh.json prints "VERIFIED [[135,6,44]] shadow=True: value=898 digits, max column coefficient <= 0, 43+2+43 multipliers", exit 0.
   The output matches check/checker_output.txt.
5. The index structure is sound. u_Q covers 1..43 (the 45 certificate has equality rows up to 44, and the missing Q_44 multiplier is 0, which is legal). v_G sits on 46 and 47 (both >= d), and v_H on 0..45 (all in range).
6. Table record: sha256sum of data/QECC_q4_n135_k6_claimtime.html is 867633fb...62c6b5 and of data/qubit_table_full_n1-256.html is 26245491...de4b0b6, both matching CLAIM.md. The saved page shows lower bound 25 and upper bound 45 for [[135,6]].
7. Propagation: I ran check/parse_table.py then check/propagate.py. The parse is deterministic, since two parses compare byte-identical. The result is table [25, 45] and closure 44 at (135,6). By hand, R3 from (134,7) with upper bound 43 gives 44, and the other neighbours (135,5) and (136,6) give 45. So an upper bound of 43 is not implied by the standard propagation rules, and the claim is a genuine improvement of 45 to at most 43. A scratch directory I made inside the folder was deleted afterwards.

## Reasoning
The certificate is an exact integer Farkas dual that I confirmed with an independently written checker, and also with the author's checker. The shadow constraints are valid for stabilizer codes. A code of distance at least 44 still satisfies A_j = B_j for j < 44, so ruling out d = 44 rules out all d >= 44. The d = 45 certificate (the literal live upper bound) also verifies. The new bound is not derived from other live cells. There was no non-determinism and no missing object. I did not access the live table, and none is needed since the claim-time page is saved.

pass: true
