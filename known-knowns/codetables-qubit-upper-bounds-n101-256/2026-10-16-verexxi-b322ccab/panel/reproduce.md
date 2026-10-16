context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic: claim q165-2 ([[165,2,54]] does not exist)

Instruction followed: write my own checker from the definition (the LP in REPRODUCE.md step 2) before reading the author's code; verify every property and the value from the saved files; fail on any mismatch.

## 1. Independent certificate check (written before opening check/check_cert.py)
My own script rebuilt the LP rows from the definition. M = 2^(n-k) = 2^163; K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s) (exact integers). Rows:
- E0: A_0 = 1.
- E1: sum A_i = M.
- Q_j (1 <= j < d): A_j = B_j, so M*A_j - sum_i K_j(i) A_i = 0, with a free-sign multiplier.
- G_j (j >= d): B_j - A_j >= 0, with a multiplier >= 0.
- H_j: Sh_j >= 0, so sum_i (-1)^i K_j(i) A_i >= 0, with a multiplier >= 0.

The combination gives a coefficient per column A_i. The certificate is valid when every coefficient is <= 0 and the RHS (u_E0*1 + u_E1*M) is > 0. A >= 0 then gives LHS <= 0, while the same combination equals RHS + (nonnegative terms) > 0, which is a contradiction (Farkas).

My script also asserted these things: n=165 and k=2; the Q keys are exactly 1..d-1; every G key is >= d; every G and H multiplier is >= 0. Its output (the sign convention was fixed by trying all sign combinations on the equality block, which is legitimate because equality multipliers are free-sign):

  result/cert_165_2_54_sh.json d=54 shadow=True max col<=0: True rhs>0: True nQ/nG/nH 53 2 54 Q keys complete 1..d-1: True
  result/cert_165_2_55_sh.json d=55 shadow=True max col<=0: True rhs>0: True nQ/nG/nH 54 2 55 Q keys complete 1..d-1: True

A second run gave a byte-identical output (md5 eaea2de8aaf009e5edfbe1c80d87b9b6 on both runs), so I saw no non-determinism.

The certificate for d=54 covers every d >= 54. The rows only use A_j = B_j for j < 54, and a code of distance >= 54 satisfies those. So the upper bound is <= 53.

## 2. Author's checker, run after mine
  python3 -I check/check_cert.py result/cert_165_2_55_sh.json
  VERIFIED [[165,2,55]] shadow=True: value=1432 digits, max column coefficient <= 0, 54+2+55 multipliers   (exit code 0)
  python3 -I check/check_cert.py result/cert_165_2_54_sh.json
  VERIFIED [[165,2,54]] shadow=True: value=1569 digits, max column coefficient <= 0, 53+2+54 multipliers   (exit code 0)
This matches check/checker_output.txt.

## 3. Table record and propagation
- sha256sum of the data files: data/QECC_q4_n165_k2_claimtime.html is c38c91cf...a5e1b and data/qubit_table_full_n1-256.html is 26245491...de4b0b6. Both match CLAIM.md.
- data/QECC_q4_n165_k2_claimtime.html reads "lower bound: 32, upper bound: 55".
- My own parser of the full table found 33152 cells, none unparsable. It gave (165,2)=32-55, (165,1)=33-55, (166,2)=56, (164,3)=55.
- My own fixpoint closure under R1 d(n,k)<=d(n,k-1) for k>=2, R2 d(n,k)<=d(n+1,k), R3 d(n,k)<=d(n-1,k+1)+1 converged in 16 iterations and gave closure(165,2)=55. So 53 is not implied by other live cells.
- The author's pipeline (check/parse_table.py then check/propagate.py) printed "[32, 55] 55", the same result.

## 4. Limits
- I was told not to open any website, so I did not re-fetch the live page. I only confirmed the saved claim-time files and their hashes. The "live immediately before claiming" part rests on the saved record. I did not check whether the live table has moved since.
- I did not independently re-derive the Rains shadow theorem or the MacWilliams identity. I checked that the K_j(i) I used satisfies the symmetry identity C(n,i)3^i K_j(i) = C(n,j)3^j K_i(j) at sample points, and I applied the definitions as stated in REPRODUCE.md.

Result: the certificate checks exactly under my independent code and the author's code, the saved table data and hashes match, and the propagation closure does not imply the bound.

pass: true
