context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic verdict for [[213,2,71]] nonexistence (claimed upper bound 71 -> 70)

## What I did
1. Read CLAIM.md and REPRODUCE.md, then inspected the keys and sizes of result/cert_213_2_71_sh.json (n=213, k=2, d=71, shadow=true; u_E0, u_E1, u_Q with 70 keys 1..70, v_G with 2 keys 73 and 74, v_H with 71 keys). Only after that did I read the docstring of check/check_cert.py, which states the LP. I did not read the body of the author's code before writing my own checker.
2. Wrote my own checker (scratch script my_check.py, standard library only, big integers) from the definition:
   - Stabilizer S has |S| = 2^(n-k) and weight distribution A_i, with A_0 = 1 and sum A_i = 2^(n-k).
   - The normalizer has B_j = 2^-(n-k) * sum_i K_j(i) A_i, with K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s), the quaternary MacWilliams identity.
   - A_j = B_j for 1 <= j < d, and A_j <= B_j for all j.
   - Rains shadow: Sh_j = 2^-(n-k) * sum_i (-1)^i K_j(i) A_i >= 0.
   - Farkas: integer multipliers, free sign on equalities and >= 0 on inequalities, with every column coefficient c_i <= 0 and the right-hand side u_E0 + 2^(n-k) u_E1 > 0.
   I checked these constraints are valid for every stabilizer code. The A_j <= B_j rows are stated for j >= d only, and the Q rows only for j <= d-1, so the certificate uses only valid rows.
3. Ran my checker on the certificate. Real output: `n,k,d 213 2 71 nQ 70 nG 2 nH 71 value>0 True max c_i<=0 True ... PASS`. I covered all 214 columns i = 0..213. The multiplier index ranges and signs checked out: Q indices in 1..70, G indices in 71..213 with nonnegative values, H indices in 0..213 with nonnegative values. Sanity asserts on my Krawtchouk function passed (K_j(0) = 3^j C(n,j), and the orthogonality sums). The run was deterministic: the output md5 was identical across two runs. A negative control, dropping the v_H[0] multiplier, produced `FAIL col 69`, so my checker does discriminate.
4. Ran the author's `python -I check/check_cert.py result/cert_213_2_71_sh.json`. Output: `VERIFIED [[213,2,71]] shadow=True: value=2622 digits, max column coefficient <= 0, 70+2+71 multipliers`, exit code 0, identical to check/checker_output.txt.
5. Propagation: I ran check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html and got `[41, 71] 71`. Independently from the parsed table, the neighbours are (213,1) = [42,71], (214,2) = [42,72] and (212,3) = [41,71]. R1 gives 71, R2 gives 72 and R3 gives 71+1 = 72, so the minimum implied upper bound is 71. A bound of 70 is therefore not implied by propagation from other live cells.
6. Table record: the saved claim-time page data/QECC_q4_n213_k2_claimtime.html reads "Bounds on [[213,2]] lower bound: 41 upper bound: 71". The sha256 values of both saved html files match the ones stated in CLAIM.md (c8103c84... and 26245491...). I made no web requests, so I did not re-check the live table, and the saved claim-time page is the only evidence for the cell's status.

## Reasoning
The certificate is a complete, exact Farkas certificate: every column coefficient is <= 0 (the maximum is exactly 0) and the right-hand side is positive. Since A >= 0, any feasible stabilizer weight distribution would give value <= 0, a contradiction, so no [[213,2,71]] stabilizer code exists. The upper bound for [[213,2]] is therefore at most 70, and the cell is currently listed at 71. The check is exhaustive over all columns and was reproduced by two independent implementations, with no mismatch, missing object or non-determinism.

pass: true
