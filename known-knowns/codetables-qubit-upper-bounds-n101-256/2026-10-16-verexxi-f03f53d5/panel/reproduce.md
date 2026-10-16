# VERDICT (REPRODUCE skeptic) - claim q158-1: no [[158,1,52]] (and no [[158,1,53]]) qubit stabilizer code

context: subagent (same VM)

Only files inside this folder were read or run. I wrote my own checker (my_checker.py, my_prop.py, sanity_defs.py)
BEFORE opening check/check_cert.py, using only the certificate JSON field names and CLAIM.md/REPRODUCE.md.

## Definition used (quoted from REPRODUCE.md, which I re-derived below)
"variables A_0..A_n >= 0, the weight distribution of the stabilizer S of an [[n,k,d]] code (|S| = 2^(n-k));
B_j = 2^-(n-k) sum_i K_j(i) A_i is the weight distribution of the normalizer (quaternary MacWilliams identity)
and Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i that of the shadow (Rains); K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
Every [[n,k,d]] code satisfies A_0 = 1, sum A_i = 2^(n-k), A_j = B_j for 1 <= j < d, A_j <= B_j for j >= d, Sh_j >= 0."

Why each row holds for every [[n,k,d]] stabilizer code (S = additive self-orthogonal GF(4)-code, |S|=2^(n-k), N=S^perp its
trace-Hermitian dual, |N|=2^(n+k)):
- A_0=1: only the identity has weight 0; sum A_i=|S|=2^(n-k).
- B_j = weight distribution of S^perp = 2^-(n-k) sum_i K_j(i) A_i by the quaternary (additive) MacWilliams identity.
- S is contained in N (self-orthogonal), so A_j <= B_j for all j.
- Distance d means every element of N \ S has weight >= d, so for 1 <= j < d: A_j = B_j. (A code of larger distance
  also satisfies this, so infeasibility at d=52 excludes all d >= 52, giving upper bound 51.)
- Shadow (Rains): Sh = {v : <v,s> = wt(s) mod 2 for all s in S}; its enumerator is 2^-(n-k) sum_i (-1)^i K_j(i) A_i, a
  count of vectors, hence >= 0.
Farkas: rows are multiplied by 2^(n-k) (integers). Take u free on equalities (A_0=1, sum A=2^(n-k), B_j-A_j=0 for 1<=j<d),
v>=0 on inequality rows (B_j-A_j>=0 for j>=d; Sh_j>=0). If the combined column coefficients are all <= 0 and the
combined right-hand side (u_E0*1 + u_E1*2^(n-k)) is > 0, then for any A>=0 satisfying all rows: 0 >= c.A = sum u*(eq lhs) +
sum v*(ineq lhs) >= rhs > 0, contradiction. So the LP is infeasible, no such code exists.

## Validation of my definition by brute force (sanity_defs.py)
For [[5,1,3]], Steane [[7,1,3]], [[4,2,2]], [[4,0]] GHZ4, an impure [[4,1]], GHZ3 (odd weights, Sh != B), single Z, and
[[3,1]], I enumerated all 4^n Pauli vectors and confirmed exactly (integers): sum_i K_j(i)A_i = 2^(n-k) B_j (normalizer
counted directly by commutation), sum_i (-1)^i K_j(i)A_i = 2^(n-k) Sh_j (shadow counted directly from its definition),
A_j<=B_j, A_j=B_j below the distance, Sh_j>=0. Also in the checker: K_j(0)=3^j C(n,j), sum_j K_j(i)=4^n delta_{i0},
sum_i K_j(i)K_i(l)=4^n delta_{jl} for several (j,l) at n=158. All passed.

## Commands and real output
    python3 -I sanity_defs.py   (PYTHONPATH=.)   -> all 8 small codes pass (last lines:
        GHZ3 n,k= 3 0 A= [1, 0, 3, 4] B= [1, 0, 3, 4] Sh= [0, 3, 0, 5] d= 4
        single Z n,k= 1 0 A= [1, 1] B= [1, 1] Sh= [0, 2] d= 2
        [[3,1]] odd n,k= 3 1 A= [1, 0, 3, 0] B= [1, 3, 3, 9] Sh= [1, 3, 3, 9] d= 1 )
    python3 -I my_checker.py result/cert_158_1_52_sh.json result/cert_158_1_53_sh.json
    result/cert_158_1_52_sh.json n,k,d= 158 1 52 shadow True max col coeff <=0: True (#positive cols 0) rhs>0: True nonzero Q/G/H: 51 2 51 => INFEASIBLE
    result/cert_158_1_53_sh.json n,k,d= 158 1 53 shadow True max col coeff <=0: True (#positive cols 0) rhs>0: True nonzero Q/G/H: 52 2 52 => INFEASIBLE
    exit 0   (two runs gave byte-identical output: deterministic)
My row mapping: u_E0 -> A_0=1, u_E1 -> sum A_i = 2^(n-k), u_Q[j] -> (B_j - A_j)=0 rows j=1..d-1, v_G[j] -> (B_j - A_j)>=0 rows
j>=d (keys 54,55 for d=52; 55,56 for d=53; all >=0, all >= d), v_H[j] -> Sh_j>=0 rows (all >=0). Equality row orientation is
sign-free; my first guess of orientation (A_j-B_j) failed and the opposite orientation (B_j-A_j) passed, which is legitimate
(not a mismatch: u_Q is the multiplier for the row written as B_j - A_j = 0).
Tamper tests on the 52 certificate (u_E1+1, v_H[0] halved, shadow rows dropped, d relabelled 51): all rejected.

Only after the verdict above I ran the author's checker:
    python3 -I check/check_cert.py result/cert_158_1_52_sh.json -> VERIFIED [[158,1,52]] shadow=True: value=1683 digits, max column coefficient <= 0, 51+2+51 multipliers (exit 0)
    python3 -I check/check_cert.py result/cert_158_1_53_sh.json -> VERIFIED [[158,1,53]] shadow=True: value=1609 digits, max column coefficient <= 0, 52+2+52 multipliers (exit 0)
Matches my result and check/checker_output.txt.

## Table record and propagation
- sha256 of data/QECC_q4_n158_k1_claimtime.html = d31b4dac...9540 and of data/qubit_table_full_n1-256.html = 26245491...4b0 : both
  match CLAIM.md. The saved single-cell page reads "Bounds on [[158,1]] lower bound: 33 upper bound: 53".
- REPRODUCE.md step 3 re-run (parse_table.py, propagate.py, one-liner) printed "[33, 53] 53". 
- My own independent closure (my_prop.py: own regex parse, own fixpoint of R1 d(n,k)<=d(n,k-1) k>=2, R2 d(n,k)<=d(n+1,k),
  R3 d(n,k)<=d(n-1,k+1)+1 over all 33152 cells): live ub(158,1)=53, ub(159,1)=53, ub(157,2)=53 (so R3 gives 54), closure(158,1)=53.
  So 51 (and 52) is not implied by other saved live cells.

## Mismatches / caveats
- No mismatch, no missing object, no non-determinism found.
- Not checkable here (no web by instruction): that the table was live at claim time; I can only confirm the saved files and their hashes.
- The 53 certificate is the literal reading of the success criterion (d = live upper bound); the 52 certificate gives the stronger claim; both verify.
- The saved table is itself not propagation-closed elsewhere (my closure improves 1100 other cells); irrelevant to cell (158,1).

pass: true
