context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic report, claim q140-2 ([[140,2,46]] nonexistence)

Method: before reading check/check_cert.py I wrote my own checker from the definition stated in CLAIM.md/REPRODUCE.md
("A_0=1, sum A_i = 2^(n-k), A_j = B_j for 1<=j<d, A_j <= B_j for j>=d, Sh_j >= 0; B_j = 2^-(n-k) sum_i K_j(i) A_i,
Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i, K_j(i)=sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s)").
I only inspected the JSON key names of result/cert_*.json (u_E0, u_E1, u_Q, v_G, v_H) to learn the format; my checker is independent (Python big ints, rows scaled by M=2^(n-k) with no division).

1. Sanity of my K/B/Sh code on real codes (not the claim): [[5,1,3]] (A=1+15x^4) and [[7,1,3]] Steane (1+21x^4+42x^6):
   sum A = 2^(n-k) True, A_j=B_j for j<d True, Sh_j>=0 True for both. B/M for [[5,1,3]] = [1,0,0,30,15,18] (correct normalizer enumerator).

2. My exact Farkas check (rows: E0 A_0=1, E1 sum A=M, Q_j: M*B_j - M*A_j = 0 for j=1..d-1, G_j: M*B_j - M*A_j >= 0 for j>=d, H_j: M*Sh_j >= 0).
   Structural asserts: u_Q keys are exactly 1..d-1; v_G keys all >= d and all positive; all v_H >= 0 with j in 0..140.
   Output:
     46 max col 0 num zero cols 1 all<=0 True rhs>0 True rhs digits 1105
     47 max col 0 num zero cols 1 all<=0 True rhs>0 True rhs digits 919
   (combined column coefficient <= 0 for every A_0..A_140, equality right-hand side u_E0 + u_E1*2^138 > 0; so no nonnegative A satisfies the LP: Farkas.)
   Because a distance >=46 code satisfies every d=46 constraint, nonexistence of d=46 also excludes d=47 and above. Both certificates verified independently.

3. Author checker run (after mine), fresh shell, python3 -I:
     VERIFIED [[140,2,47]] shadow=True: value=919 digits, max column coefficient <= 0, 46+2+46 multipliers   (rc=0)
     VERIFIED [[140,2,46]] shadow=True: value=1105 digits, max column coefficient <= 0, 45+2+45 multipliers  (rc=0)
   Matches check/checker_output.txt. My checker run twice gave identical output (md5 identical): deterministic.

4. Table / propagation (my own parser and closure, not the author's):
   sha256sum data/*.html: ec703213... (QECC_q4_n140_k2_claimtime.html) and 26245491... (qubit_table_full_n1-256.html), both match CLAIM.md.
   The saved single-cell page reads lower bound 30, upper bound 47 for [[140,2]]; the full table has 33152 distinct cells and cell (140,2) = "30-47".
   Neighbours: (140,1)=47, (141,2)=47, (139,2)=47, (139,3)=47 (R3 gives 48). My fixpoint closure of rules R1,R2,R3 over all live cells:
     closure (140,2): 47 live 47
   So the bound 45 is not implied by propagation from other live cells. The author's parse_table.py also parsed 33152 cells.

Not done / limits: I did not re-fetch the live site (not permitted); the live-status claim rests on the saved HTML only. The validity of the LP constraints (MacWilliams, Rains shadow) was confirmed by sanity on two known codes, and is the cited theory (quant-ph/9608006, quant-ph/9611001), not re-proved here.

Verdict: certificates for d=46 and d=47 verify exactly; no mismatch, missing object or non-determinism found.
pass: true
