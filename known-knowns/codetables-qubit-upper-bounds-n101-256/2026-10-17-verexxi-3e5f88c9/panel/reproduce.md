context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic verdict, [[225,2]] upper bound 75 -> 74

## What I did
1. Read CLAIM.md and REPRODUCE.md. Before opening any author code I inspected only the certificate data (result/cert_225_2_75_sh.json). It holds n=225, k=2, d=75, shadow=true, integers u_E0 and u_E1 (2636 and 2569 digits), u_Q (74 keys, j=1..74), v_G (2 keys, j=77 and 78) and v_H (75 keys, j in 0..81).
2. I wrote my own checker (scratch scripts my_check.py and my_check2.py, since deleted) from the definition, using only exact Python integers. The definition is the one quoted in REPRODUCE.md step 2.
   - A_0 = 1.
   - Sum of A_i = 2^(n-k).
   - B_j = 2^-(n-k) * Sum_i K_j(i) A_i, where K_j(i) = Sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
   - A_j = B_j for 1 <= j < d.
   - A_j <= B_j for j >= d.
   - Sh_j = 2^-(n-k) * Sum_i (-1)^i K_j(i) A_i >= 0.
   - A_i >= 0.
   - I scaled the B and Sh rows by 2^(n-k) to keep them integer.
3. Sanity check of my K, B and Sh formulas on the known [[5,1,3]] code (A = 1 + 15 x^4). I got B = Sh = [1,0,0,30,15,18], so A_j = B_j for j < 3 and Sh >= 0, as expected.
4. I formed F(A) = u_E0(A_0-1) + u_E1(Sum A - 2^(n-k)) + Sum u_Q*(equality rows) + Sum v_G*(B_j - A_j rows) + Sum v_H*(shadow rows). I computed every column coefficient and the constant exactly.
   - My first sign guess (all +) failed. I enumerated the 32 sign choices per multiplier group. The equality groups are sign-free, so flipping the sign of the u_Q group is legitimate.
   - The choice E0 +, E1 +, Q flipped, G +, H + gives max column coefficient <= 0 (all 226 columns) and constant < 0. This was confirmed for both E-sign choices.
   - Checks that held: all v_G and v_H are >= 0; the u_Q keys are exactly 1..74; the v_G keys 77, 78 are >= d; the v_H keys lie in the valid range 0..225.
   - Any feasible nonnegative A satisfies F(A) >= 0 (equalities give 0, inequalities >= 0). But F(A) = Sum coef_i*A_i + const <= const < 0. That is a contradiction, so the LP with d=75 is infeasible. So no [[225,2,75]] stabilizer code exists, and the upper bound is <= 74.
5. I ran the author's checker, python3 -I check/check_cert.py result/cert_225_2_75_sh.json. It printed "VERIFIED [[225,2,75]] shadow=True: value=2636 digits, max column coefficient <= 0, 74+2+75 multipliers" with exit 0. A second run gave a byte-identical output hash, and it matches check/checker_output.txt. So there is no non-determinism.
6. Table and propagation:
   - sha256 of data/QECC_q4_n225_k2_claimtime.html is e7790e91af4cc9b264e7d2211744d741aaff4435417e790eb03bd09aede35759, and of data/qubit_table_full_n1-256.html is 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6. Both match CLAIM.md.
   - The saved cell page reads "Bounds on [[225,2]] ... lower bound: 44 upper bound: 75".
   - I wrote my own regex parser of the full table (33152 cells) and got (225,2) = (44,75).
   - Direct propagation sources: R1 from (225,1) gives 75, R2 from (226,2) gives 76, R3 from (224,3)+1 gives 76. None gives 74.
   - I ran the author's parse_table.py and propagate.py. They gave "[44, 75] 75", as in REPRODUCE.md. The closure at (225,2) is 75, so 74 is not implied by other live cells.
   - I made no web requests, so I cannot independently confirm the live-table value. I rely on the saved claim-time page.

## Reasoning
The certificate is a genuine exact Farkas dual for the standard quantum weight-enumerator LP with the Rains shadow rows. I re-derived the combination with my own implementation, using exact integers. The LP constraints are all valid for any additive (stabilizer) code, so infeasibility rules out [[225,2,75]]. The new bound 74 is below the table's 75 and is not implied by the propagation rules from the saved table.

## Limitation
I verified the live-table status only from the saved claim-time file, per the instructions. The LP rows are the standard ones, and I checked the formulas on [[5,1,3]].

pass: true
