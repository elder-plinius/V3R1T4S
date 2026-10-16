context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic report, claim q183-1 ([[183,1,60]] does not exist)

## 1. Independent checker (written from the definition before opening check/*.py)
Definition used (CLAIM.md / REPRODUCE.md step 2): variables A_0..A_n >= 0, n=183, k=1, M=2^(n-k)=2^182;
K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s); B_j = (1/M) sum_i K_j(i) A_i; Sh_j = (1/M) sum_i (-1)^i K_j(i) A_i.
Valid constraints: A_0=1; sum A_i = M; A_j=B_j for 1<=j<d; A_j<=B_j for j>=d; Sh_j>=0.
I only looked at the certificate JSON (fields u_E0, u_E1, u_Q[1..d-1], v_G[j>=d], v_H[0..n]) and inferred the row
conventions by trying sign/scale variants; the single convention that is also logically valid (nonnegative multipliers on
the inequality rows B_j-A_j>=0 and Sh_j>=0, free sign on equalities, E1 row = sum A_i = M with coefficient 1) is:
  col_i = u_E1 + u_E0*[i=0] + sum_j u_Q[j](K_j(i)-M[i=j]) + sum_j v_G[j](K_j(i)-M[i=j]) + sum_j v_H[j](-1)^i K_j(i)
  rhs   = u_E0 + u_E1*M
For any feasible A>=0, sum_i col_i A_i = rhs + (nonneg terms) >= rhs; if all col_i <= 0 and rhs > 0 this is impossible
(Farkas). My own sanity test: [[5,1,3]] stabilizer weight distribution 1+15x^4 gives B=[1,0,0,30,15,18] (asserted, passes).
My checker also asserts: u_Q keys are exactly 1..d-1, v_G keys j>=d, all v_G,v_H >= 0.

Real output (my checker, exact Python integers):
  result/cert_183_1_60_sh.json d= 60 maxcol<=0 True #cols==0 1 rhs>0 True rhs digits 1980 nQ 59 nG 2 nH 60
  result/cert_183_1_61_sh.json d= 61 maxcol<=0 True #cols==0 1 rhs>0 True rhs digits 2476 nQ 60 nG 2 nH 61
Re-run twice on the d=60 certificate: identical md5 of output both times (deterministic).
Since a [[183,1,d>=60]] code satisfies the d=60 LP (A_j=B_j for j<60), the d=60 certificate alone excludes all d>=60,
so the upper bound is <= 59.

## 2. Author's checker
  python3 -I check/check_cert.py result/cert_183_1_60_sh.json
  VERIFIED [[183,1,60]] shadow=True: value=1980 digits, max column coefficient <= 0, 59+2+60 multipliers   (exit 0)
  python3 -I check/check_cert.py result/cert_183_1_61_sh.json
  VERIFIED [[183,1,61]] shadow=True: value=2476 digits, max column coefficient <= 0, 60+2+61 multipliers   (exit 0)
Matches check/checker_output.txt and my independent result (same digit counts 1980 / 2476).

## 3. Propagation (own parser, written separately from check/parse_table.py)
data/qubit_table_full_n1-256.html sha256 = 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6 (matches CLAIM.md);
data/QECC_q4_n183_k1_claimtime.html sha256 = 5dc930c084ce6566ab47d2af41b6f0275a0854c06a1118cc6cde873efc10d2c0 (matches);
it says "lower bound: 36, upper bound: 61".
My parser: cells 33152, all parsed; (183,1) = 36-61. Fixpoint closure with R1 (k>=2 only), R2 d(n,k)<=d(n+1,k),
R3 d(n,k)<=d(n-1,k+1)+1: 16 iterations, closure(183,1) = 61. Neighbours: (184,1)=62, (183,2)=61, (182,2)=61.
So 59 is not implied by propagation from live cells. Author's check/parse_table.py + check/propagate.py ran and agree
(live (183,1): [36, 61], closure 61; R2 (184,1) [36,62]; R3 (182,2) [35,61]).

## 4. Limits / caveats
- I was forbidden to open any website, so the "live re-fetch immediately before claiming" step was not reproduced; I only
  confirmed the saved snapshot matches its recorded hashes and contents. The saved page shows "Last change: 10.06.2024".
- The correctness of the LP constraint set itself (MacWilliams, Rains shadow, A_j<=B_j) is taken from the cited papers;
  I re-derived the shadow sign convention (A(x+3y, y-x) = (-1)^i factor on K_j) and sanity-tested B on [[5,1,3]].
- Claim is an LP-type bound of the kind the table notes call "weak" for n>100, so a surprise is possible, but the
  certificate checks exactly and nothing mismatched, was missing, or was non-deterministic.

pass: true
