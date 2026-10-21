context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic verdict for [[135,1,45]] (claimed new upper bound 44)

## What I did (before reading any author code)
1. Read CLAIM.md and REPRODUCE.md only, then loaded result/cert_135_1_45_sh.json as data. Fields: n=135, k=1, d=45, shadow=true, u_E0, u_E1 (big integers), u_Q (keys 1..44), v_G (keys 47, 48), v_H (keys 1..42, 47, 48).
2. Wrote my own checker (scratch file my_chk.py) from the definition, using Python big integers and no floats. The definition I used is the one quoted in REPRODUCE.md, which comes from Calderbank-Rains-Shor-Sloane and Rains:
   - M = 2^(n-k) = 2^134. K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
   - Rows, scaled by M: E0 is A_0 = 1. E1 is sum A_i = M. Q_j (1 <= j < 45) is M*A_j - sum_i K_j(i) A_i = 0. G_j (j >= 45) is sum_i K_j(i) A_i - M*A_j >= 0, which is A_j <= B_j. H_j is sum_i (-1)^i K_j(i) A_i >= 0, which is shadow nonnegativity.
   - I summed u * row over the equalities and v * row over the inequalities, and asserted v >= 0 and that each index is in its valid range.
3. My own result: the Q-row multipliers only work with the opposite sign convention. That is legitimate because they multiply equalities and may take either sign. With that sign, every one of the 136 column coefficients (A_0..A_135) is <= 0, and the right-hand side u_E0 + u_E1*M is > 0 (1145 digits). A nonnegative A would then give c.A <= 0 while c.A >= rhs > 0, a contradiction, so the LP is infeasible (Farkas). I swept all 16 sign combinations of (E, Q, G, H). Only E=+, Q=-, G=+, H=+ is valid with rhs > 0 and all coefficients <= 0. The G and H signs are the ones that preserve the required inequality directions, so no illegitimate sign choice was needed.
4. LP validity, re-derived by hand: the stabilizer S of an [[n,k,d]] code has |S| = 2^(n-k). Its normalizer has weight distribution B = M^-1 K A (MacWilliams). S is contained in its normalizer, so A_j <= B_j. Distance d gives A_j = B_j for 1 <= j < d. The shadow distribution is M^-1 sum (-1)^i K_j(i) A_i >= 0 (Rains). These are all valid necessary conditions, so infeasibility means no [[135,1,45]] stabilizer code exists.
5. Then I ran the author's check: `python3 -I check/check_cert.py result/cert_135_1_45_sh.json` printed "VERIFIED [[135,1,45]] shadow=True: value=1145 digits, max column coefficient <= 0, 44+2+44 multipliers" and exited 0. A second run was byte-identical to check/checker_output.txt (diff showed no difference). It agrees with my independent checker, and the runs are deterministic.
6. Table record: sha256sum of data/QECC_q4_n135_k1_claimtime.html is 2a04a91c...6d77 and of data/qubit_table_full_n1-256.html is 26245491...b6245 (both match CLAIM.md). The claim-time page shows "lower bound: 27, upper bound: 45" for [[135,1]]. In the full table, row n=135 k=1 reads 27-45.
7. Propagation: I ran check/parse_table.py and check/propagate.py. The output was `[27, 45] 45`, i.e. the closure at (135,1) is 45. I also checked the neighbours by hand from my own regex parse of the saved table: (134,2) = 26-45, so R3 gives <= 46. (135,2) = 27-45, so R1 gives <= 45. (136,1) = 27-46, so R2 gives <= 46. Nothing live implies 44, so the new bound is not already implied by the standard rules.

## Reasoning
The proof is an exact integer Farkas certificate. My independently written checker accepts it, the author's checker accepts it, and the output is deterministic. The certificate covers every constraint it uses (all 136 columns checked, not a sample). The table record is consistent with the claim and the saved data, and the bound is not implied by propagation. No mismatch, missing object or non-determinism found.

Limitation: I made no live web requests, as instructed. The "live" status rests on the saved claim-time page.

pass: true
