# VERDICT (REPRODUCE skeptic)

context: subagent (same VM)

I read only files inside this folder. No web access. I did not re-fetch the live codetables.de page; the only table evidence I could check is the saved copies in data/.

## Definition implemented (quoted from the docstring of mycheck/my_checker.py, written before I read check/check_cert.py)

> A qubit stabilizer code [[n,k,d]] is an additive self-orthogonal (n, 2^(n-k)) code S over GF(4) (trace-Hermitian inner product), with normalizer N = S^perp of size 2^(n+k); d = min wt(N minus S) (d = min wt(N) if N = S). A_i = #{s in S: wt s = i}, B_i = #{v in N: wt v = i}.
> Quaternary MacWilliams identity (CRSS 1996): B_j = 2^-(n-k) * sum_i K_j(i) A_i, K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
> Rains shadow enumerator: Sh(x,y) = 2^-(n-k) A(x+3y, y-x), so Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i >= 0.
> Constraints (A_0..A_n >= 0, m = n-k, rows scaled by 2^m):
> (E0) A_0 = 1;  (E1) sum_i A_i = 2^m;  (Q) sum_i K_j(i)A_i - 2^m A_j = 0 for 1<=j<=d-1;  (G) the same expression >= 0 for all j (S subset of N, A_j <= B_j);  (H) sum_i (-1)^i K_j(i) A_i >= 0 for all j (Rains).
> Farkas: F(A) = u_E0*A_0 + u_E1*sum A + sum u_Q[j]Q_j + sum v_G[j]G_j + sum v_H[j]H_j = sum_i c_i A_i. Any feasible A has F(A) >= u_E0 + u_E1*2^m =: rhs. If all c_i <= 0 and rhs > 0, then F(A) <= 0 < rhs for every A >= 0, so the LP is infeasible and no such code exists.

My derivation of why each constraint holds for every code with distance >= d: A_0 = 1 (zero vector); |S| = 2^(n-k); N\S has min weight >= d, so B_j = A_j for 0<j<d (impure codes allowed); S is a subset of N, so A_j <= B_j for all j; Rains' shadow has nonnegative coefficients for every additive self-orthogonal code. The check that the certificate refutes the LP is the one-line Farkas argument above. Distance >= 50 is exactly what is used, so a code with d >= 50 (and hence a [[150,1,51]]) would have to satisfy the same LP.

My checker contains self-tests that all pass: [[5,1,3]] gives B=(1,0,0,30,15,18) and a nonnegative shadow; the hexacode [[6,0,4]] gives B=A and a nonnegative shadow; and sum_j K_j(i) = 4^n for i=0 and 0 otherwise (n=7).

## Commands and real output

    python3 -I mycheck/my_checker.py result/cert_150_1_50_sh.json result/cert_150_1_51_sh.json

    selftest ok
    result/cert_150_1_50_sh.json {'n': 150, 'k': 1, 'd': 50, 'ok': True, 'all_ci_nonpos': True, 'n_pos': 0, 'n_zero': 1, 'rhs_positive': True, 'rhs_digits': 1362, 'probs': [], 'nQ': 49, 'nG': 2, 'nH': 48, 'Qkeys': (1, 49), 'Gkeys': [52, 53], 'Hkeys': [1..21, 23..48, 54]}
    result/cert_150_1_51_sh.json {'n': 150, 'k': 1, 'd': 51, 'ok': True, 'all_ci_nonpos': True, 'n_pos': 0, 'n_zero': 1, 'rhs_positive': True, 'rhs_digits': 1485, 'probs': [], 'nQ': 50, 'nG': 3, 'nH': 49, 'Qkeys': (1, 50), 'Gkeys': [52, 53, 54], 'Hkeys': [0, 2..39, 41, 43..46, 48, 51, 53..55]}
    MY VERDICT: ALL VERIFIED       (exit 0, 0.6 s; two runs give an identical output sha256 c4bad681...)

Every multiplier in v_G and v_H is nonnegative. u_Q keys lie in 1..d-1 and v_G keys in d..n (the cert uses G only for j >= d). There are no duplicate JSON keys. Exactly one column coefficient is 0 and none is positive.

Negative controls (python3 -I mycheck/neg.py): the original passes; perturbing u_Q[10], negating v_H[5], dropping v_G[52], or declaring d=49 with the same cert all fail on c_i <= 0; perturbing u_E0 makes rhs <= 0 and fails.

Author's checker, run after my verdict:

    python3 -I check/check_cert.py result/cert_150_1_50_sh.json   -> VERIFIED [[150,1,50]] shadow=True: value=1362 digits, max column coefficient <= 0, 49+2+48 multipliers  (exit 0)
    python3 -I check/check_cert.py result/cert_150_1_51_sh.json   -> VERIFIED [[150,1,51]] shadow=True: value=1485 digits, max column coefficient <= 0, 50+3+49 multipliers  (exit 0)

These agree with check/checker_output.txt and with my verdict. The author's LP (E0, E1, Q, G, H, row scaling, Farkas rule) is the same as mine.

Table records. sha256sum of data/ matches CLAIM.md for all four HTML files (47511f9f..., 36226d71..., 594f4f1b..., 26245491...). The saved pages say [[150,1]] upper 51 (lower 33), [[151,1]] upper 51, [[149,2]] upper 51. In the full table the cells read 33-51, 33-51, 30-51.

Propagation (my own parser and closure, mycheck/my_prop.py, rules U(n,k)<=U(n,k-1) for k>=2, U(n,k)<=U(n+1,k), U(n,k)<=U(n-1,k+1)+1, over all 32896 cells with k>=1):

    cells 33152 distinct 33152
    live (150,1) 33 51 closure 51 (151,1) 51 (149,2) 51
    direct candidates for (150,1):  R2 U(151,1)= 51  R3 U(149,2)+1= 52
    closure<=49 ? False  closure<=50 ? False
    min U(n,1) for n>=150: 51

Author's propagation, run exactly as in REPRODUCE.md step 3: `[33, 51] 51 [33, 51] [30, 51]` (matches the expected output). So 49 (and 50) is not implied by other live cells.

## Mismatches found

- None in the mathematics or the numbers.
- Convention note, not a failure: my first attempt used rows scaled by 2^-(n-k) with the certificate's multipliers read as-is, and it failed. The certificate's Q/G rows are the integer rows K_j(i) - 2^(n-k) delta_ij and the H rows are the unscaled shadow sums. That is the same LP with the inequality rows multiplied by the positive constant 2^(n-k), so it is a valid proof; with that scaling both certificates pass with the plain sign convention.

## Limits

- I did not re-fetch the live table. "Live upper bound 51" rests on the saved HTML (hashes match) and on the 2026-10-16T18:15Z timestamps recorded in CLAIM.md, which I cannot confirm.
- Soundness rests on the standard theorems (MacWilliams for additive GF(4) codes, Rains shadow positivity), which I derived and used but did not re-prove from scratch.

pass: true
