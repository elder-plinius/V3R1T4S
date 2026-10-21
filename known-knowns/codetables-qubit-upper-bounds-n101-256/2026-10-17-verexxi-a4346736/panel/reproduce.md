context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic verdict for [[190,2]] (claim: no [[190,2,63]] code, so upper bound at most 62)

## Procedure
1. Read CLAIM.md and REPRODUCE.md. Inspected only the structure of result/cert_190_2_63_sh.json (keys: n, k, d, shadow, u_E0, u_E1, u_Q for j=1..62, v_G for j=65 and 66, v_H for 64 shadow indices in 0..69).
2. Before opening any author code (check/*.py), I wrote my own checker from the definition. LP, over integers, with M = 2^(n-k) = 2^188 and K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s):
   - variables A_0..A_n >= 0 (stabilizer weight distribution);
   - E0: A_0 = 1; E1: sum A_i = M;
   - Q_j (1 <= j < d): sum_i K_j(i) A_i - M A_j = 0 (that is, A_j = B_j, with B_j = (1/M) sum K_j(i) A_i, the MacWilliams identity);
   - G_j (j >= d): sum_i K_j(i) A_i - M A_j >= 0 (that is, A_j <= B_j);
   - H_j (any j): sum_i (-1)^i K_j(i) A_i >= 0 (Rains shadow Sh_j >= 0).
   The Farkas rule I checked: the combination col = sum u*eq_row + sum v*ineq_row, with v >= 0 on G and H and free sign on equalities, must satisfy col_i <= 0 for every i and rhs = u_E0 + u_E1*M > 0. Then any feasible nonnegative A would give col.A <= 0 but col.A = rhs + (nonnegative terms) > 0, a contradiction.
   Sanity check inside my script: the row sums of K match 4^n at i=0 and 0 elsewhere.
3. Ran my checker on both certificates:
   - cert_190_2_63_sh.json: n,k,d 190 2 63, max col <= 0: True, columns equal to 0: 1, rhs > 0: True (rhs is 7112 bits), shadow True. All G and H multipliers are >= 0, all G indices are >= d, and u_Q keys are exactly 1..62 = 1..d-1.
   - cert_190_2_64_sh.json: n,k,d 190 2 64, max col <= 0: True, columns equal to 0: 1, rhs > 0: True, shadow True. It uses only Q_1..Q_62 and G_65, G_66, a subset of the d=64 constraints (A_j = B_j for j < 64, A_j <= B_j for j >= 64), so it is valid for d = 64 as well. The claim text's "relabelled" description does not matter, because dropping constraints only weakens the premises.
   - Since a code with d' > 63 also satisfies A_j = B_j for j < 63 and A_j <= B_j for j >= 63, the d=63 certificate excludes every distance >= 63, so d <= 62.
4. Then ran the author's checker: `python3 -I check/check_cert.py result/cert_190_2_64_sh.json` and `python3 -I check/check_cert.py result/cert_190_2_63_sh.json`. Output (both): `VERIFIED [[190,2,64]] shadow=True: value=2141 digits, max column coefficient <= 0, 62+2+64 multipliers` and the same line for [[190,2,63]]. Exit code 0. A second run of the 63 checker gave byte-identical output (deterministic). check/checker_output.txt matches.
5. Table record: sha256sum of data/QECC_q4_n190_k2_claimtime.html is 36d83bf11f5ab16750c67c59692941cb2c0f80013f3e25951e59c63821687798 and of data/qubit_table_full_n1-256.html is 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6. Both match CLAIM.md. The saved cell page reads "Bounds on [[190,2]]" and the full table cell n=190&k=2 reads 37-64, so the live upper bound is 64.
6. Propagation, independently of the author's script: I parsed all 33152 cells of the saved full table with my own regex and iterated to a fixpoint the rules d(n,k) <= d(n,k-1) for k >= 2, d(n,k) <= d(n+1,k), d(n,k) <= d(n-1,k+1)+1. Neighbours: (190,1) = 37-64, (191,2) = 37-65, (189,3) = 36-63. Closure at (190,2) is 63. Output: `closure 63`. This agrees with check/propagation_check.txt (closure 63). So the bound of 62 is not implied by the other live cells; the claim lowers the bound from 64 to 62.

## Reasoning
The certificate satisfies the Farkas conditions exactly in big-integer arithmetic under an LP I wrote from the standard definitions (quaternary MacWilliams identity for the normalizer, Rains shadow, A_j = B_j below d, A_j <= B_j above). The LP is therefore infeasible, so no [[190,2,d]] stabilizer code with d >= 63 exists. The saved table confirms the prior bound of 64, and propagation closure (63) is strictly weaker than the new bound (62). No mismatch, missing object or non-determinism was found. I did not read the remaining author code in depth; the independent checker made that unnecessary. Only the saved claim-time files were used, with no web access.

pass: true
