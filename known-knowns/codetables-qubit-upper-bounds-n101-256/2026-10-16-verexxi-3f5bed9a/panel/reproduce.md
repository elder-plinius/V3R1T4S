context: subagent (same VM)

# REPRODUCE verdict for claim: no [[139,1,46]] qubit stabilizer code (upper bound <= 45; live upper bound 47)

Scope: I read and ran files only inside this folder (CLAIM.md, REPRODUCE.md, result/, data/, check/); no web, no GitHub.

## Definition implemented (my own checker, scratch/my_check.py), quoted from my own header
"S = stabilizer of an [[n,k,d]] code, |S| = 2^(n-k), A_i = #elements of S of (symplectic) weight i.
Normalizer N = S^perp, |N| = 2^(n+k); B_j = 2^-(n-k) sum_i K_j(i) A_i (quaternary MacWilliams),
K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s). Shadow Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i >= 0 (Rains).
Constraints: A_0=1; sum A_i = 2^(n-k); A_j=B_j (1<=j<d); A_j<=B_j (j>=d); Sh_j>=0; A_i>=0.
Farkas: if exist u (free) on equalities and v>=0 on >= rows with sum u*row_eq + sum v*row_ge <= 0 on every
column (A>=0) and u.b > 0 (b = rhs of equalities; >= rows have rhs 0) then LP infeasible."

Why each constraint holds for every [[n,k,d]] stabilizer code (derived by me):
- A_0=1 (only identity has weight 0 in S, -I not in S); sum A_i=|S|=2^(n-k).
- B = MacWilliams transform of A since N = S^perp under the trace-symplectic form on GF(4)^n; B_0=1 is equivalent to sum A = 2^(n-k).
- Distance d means every element of N\S has weight >= d, so A_j=B_j for j<d (j>=1) and trivially A_j<=B_j since S subset N.
  A code with distance > d also satisfies these rows, so the d=46 certificate excludes all d>=46 (no purity assumption).
- Shadow: S(x,y)=2^-(n-k) A(x+3y, y-x) has non-negative coefficients (Rains), coefficient of weight j is the (-1)^i-weighted Krawtchouk sum.
- Farkas step: for feasible A>=0, sum_i c_i A_i = (u.b) + sum v*G(A) + sum v*H(A) >= u.b > 0, but c_i <= 0 forces sum c_i A_i <= 0. Contradiction.
  Here u.b = u_E0*1 + u_E1*2^(n-k).

Sanity of my LP rows (scratch/sanity.py, exact Fractions): [[5,1,3]] A=[1,0,0,0,15,0], B=[1,0,0,30,15,18], Sh=B; [[7,1,3]] A=[1,0,0,0,21,0,42,0],
B=[1,0,0,21,21,126,42,45], Sh=B; both satisfy all my constraints (output "True" for both).

## Commands run and real output
1. python3 -I scratch/sanity.py
   5,1,3 [1, 0, 0, 0, 15, 0] ['1', '0', '0', '30', '15', '18'] ['1', '0', '0', '30', '15', '18'] True
   7,1,3 [1, 0, 0, 0, 21, 0, 42, 0] ['1', '0', '0', '21', '21', '126', '42', '45'] ['1', '0', '0', '21', '21', '126', '42', '45'] True
2. python3 -I scratch/my_check.py result/cert_139_1_46_sh.json result/cert_139_1_47_sh.json   (exit 0)
   result/cert_139_1_46_sh.json VERIFIED rhs>0: True max column coef<=0: True positive columns: 0
   result/cert_139_1_47_sh.json VERIFIED rhs>0: True max column coef<=0: True positive columns: 0
   (my checker asserts: u_Q indices in 1..d-1, v_G indices >= d, all v_G, v_H >= 0; columns i=0..139 all coefficients <= 0; u.b > 0; all in Python ints.)
3. python3 -I check/check_cert.py result/cert_139_1_46_sh.json  -> exit 0
   VERIFIED [[139,1,46]] shadow=True: value=1270 digits, max column coefficient <= 0, 45+2+44 multipliers
   python3 -I check/check_cert.py result/cert_139_1_47_sh.json  -> exit 0
   VERIFIED [[139,1,47]] shadow=True: value=1101 digits, max column coefficient <= 0, 46+2+46 multipliers
   (run a second time for 46: identical output; matches check/checker_output.txt; deterministic.)
4. Propagation (REPRODUCE.md step 3, outputs to scratch/ instead of the folder root):
   python3 -I check/parse_table.py data/qubit_table_full_n1-256.html scratch/parsed.json   -> cells 33152 n-range 1 256
   python3 -I check/propagate.py scratch/parsed.json scratch/closure.json   -> cells k>=1: 32896  live > implied: 1075  of which n>100: 1072  n<=100: 3
   python3 -c "...print(T['139']['1'], C['139,1'])"   -> [29, 47] 47     (matches check/propagation_check.txt, which also shows R2 (140,1)=[30,47], R3 (138,2)=[28,47])
5. My own independent propagation (scratch/my_prop.py, own regex parse + own fixed-point closure over R1,R2,R3):
   33152 47 29
   closure 139,1 = 47  live neighbours: (140,1) 47  (138,2) 47
   would 45 be implied? False
6. sha256sum data/*.html matches CLAIM.md: QECC_q4_n139_k1_claimtime.html 22fe191a...ba2e, qubit_table_full_n1-256.html 26245491...0b6 (both equal to the values stated in CLAIM.md).
   The saved cell page says "Bounds on [[139,1]] lower bound: 29 upper bound: 47"; parsed table gives lower 29, upper 47.

## Mismatches / caveats
- No mismatch in the certificates: both verify, no positive column, positive objective, deterministic across reruns.
- Process disclosure: my first checker draft used the opposite sign for the Q_j equality row (M(A_j-B_j) instead of M(B_j-A_j)) and failed
  (positive columns remained). Since u_Q multipliers are sign-free this is only a convention for which sign the certificate stores; I then opened
  check/check_cert.py (after my checker's first verdict) to learn the stored sign convention (Q_j = K_j(i) - 2^(n-k)[i==j]), changed my row accordingly,
  and my checker (its own K_j, row construction, and test code) then verified. The sign of equality multipliers does not affect soundness; the certificate's
  convention is documented in the author's docstring but not inside the JSON files themselves.
- The live-status re-fetch (REPRODUCE step 4) was not done: no network allowed for this panel role; the claim-time saved page (sha256 matches) was used.
  I cannot confirm that the live table has not changed since the saved fetch; within the folder, everything checks out.
- Both d=46 and d=47 certificates verified, so ruling out d>=46 gives upper bound <= 45, not implied by propagation (closure of live table at (139,1) is 47).

pass: true
