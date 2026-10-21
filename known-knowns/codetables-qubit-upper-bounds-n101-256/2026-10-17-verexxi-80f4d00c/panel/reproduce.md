context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic verdict for [[200,10]] (claim: no [[200,10,63]], so upper bound <= 62)

## Definition used (from CLAIM.md / REPRODUCE.md, written before reading check/check_cert.py)
Variables A_0..A_n >= 0 (stabilizer weight distribution, n=200, k=10, M = 2^(n-k) = 2^190).
K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
Rows (all multiplied by M so integer):
- A_0 = 1 (E0), sum A_i = M (E1)
- Q_j, 1<=j<d: sum_i K_j(i) A_i - M A_j = 0 (A_j = B_j)
- G_j, j>=d: sum_i K_j(i) A_i - M A_j >= 0 (A_j <= B_j)
- H_j: sum_i (-1)^i K_j(i) A_i >= 0 (Rains shadow, M*Sh_j)
Farkas rule: column coefficient c_i = u0*[i=0] + u1 + sum uQ*rowQ + sum vG*rowG + sum vH*rowH must be <= 0 for every i, with u0 + u1*M > 0, equalities sign-free, inequality multipliers >= 0. Then sum c_i A_i <= 0 < u0 + u1*M <= sum c_i A_i for any feasible A, contradiction.

## What I ran
1. My own checker (a scratch script outside the claim folder, standard library, exact Python integers) on result/cert_200_10_63_sh.json and result/cert_200_10_67_sh.json.
   First a sanity test of my K_j and shadow formulas on [[5,1,3]] (A=(1,0,0,0,15,0)): B = [1,0,0,30,15,18], M*Sh divisible by M, sum Sh = 64 = 2^(n+k). Passed.
   Output for the d=63 certificate: Q keys are exactly 1..62; G keys [65, 66, 67] (all multipliers >= 0, indices >= 63); H keys 63 entries, all multipliers >= 0, max index 70; max column coefficient <= 0: True; number of positive columns: 0; u0 + u1*M > 0: True; nonzero columns 200.
   Output for the d=67 certificate: same result (column max <= 0, rhs > 0). It has Q rows 1..62, 65, 66 and G row 67; rows 63, 64 carry zero multipliers (omitted), which is consistent with the stated derivation from the d=63 certificate.
2. Author's check/check_cert.py (run after mine): both certificates print VERIFIED, exit code 0, matching check/checker_output.txt. Re-running gave identical output (deterministic). sha256 of result files: 80f4d00c... (d=63), 0a830960... (d=67).
3. Table record: sha256 of data/QECC_q4_n200_k10_claimtime.html = 4e64d779...5de56 and data/qubit_table_full_n1-256.html = 26245491...de4b0b6, both matching CLAIM.md. The claim-time page says "Bounds on [[200,10]] lower bound: 37 upper bound: 67".
4. Propagation, own parser of data/qubit_table_full_n1-256.html (33152 cells parsed; (200,10) = 37-67). Fixed-point closure with R1 U(n,k)<=U(n,k-1) (k>=2), R2 U(n,k)<=U(n+1,k), R3 U(n,k)<=U(n-1,k+1)+1 gives U(200,10)=63. So 62 is not implied by other live cells; matches check/propagation_check.txt ("closure ... 63").

## Reasoning
The certificate is a valid Farkas infeasibility proof for the LP with equalities for 0<j<63, inequalities A_j<=B_j for j>=63, and shadow nonnegativity, all of which hold for any [[200,10,d>=63]] stabilizer code (pure or impure). It was verified exhaustively over all 201 columns in exact integers by two independent implementations. The criterion's literal reading (d = live upper bound 67) is met by the second certificate, also verified. The new bound (62) is strictly below the propagation closure (63), so it is genuinely new relative to the saved table. Caveat: I did not re-fetch the live page (no web access allowed); I rely on the saved, hash-matching claim-time pages.

No mismatch, missing object or non-determinism found.

pass: true
