context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic report, claim q171-1 ([[171,1,56]] nonexistence)

Definition I coded from (quoted from CLAIM.md/REPRODUCE.md, before reading the author's checker): variables A_0..A_n >= 0; A_0 = 1; sum A_i = 2^(n-k); B_j = 2^-(n-k) sum_i K_j(i) A_i; Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i >= 0; A_j = B_j for 1 <= j < d; A_j <= B_j for j >= d; K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s); Farkas: multipliers with every column coefficient <= 0 and positive right-hand side.

Step 1. Own checker written first (own K_j via exact binomial sums, integer arithmetic only, rows scaled by 2^(n-k)). The certificate JSON schema was inferred from keys (u_E0, u_E1, u_Q, v_G, v_H); my first sign convention for the equality rows (u_Q) was opposite to the author's and produced positive columns, so I fixed the sign (equalities are sign-free, so this is only a convention) and then read the author's docstring, which states the same convention I ended with. Sanity of my formulas: [[5,1,3]] with A=(1,0,0,0,15,0) gives B=(1,0,0,30,15,18) and Sh=(1,0,0,30,15,18) (correct known values); sum_j K_j(0)=4^n and sum_j K_j(i)=0 for i>0 asserted for n=171.

Step 2. Output of my checker (run twice per certificate, identical):
  171 1 56 all columns<=0: True #positive cols: 0 value>0: True valuedigits 1827 #zero cols 1
  171 1 57 all columns<=0: True #positive cols: 0 value>0: True valuedigits 2066 #zero cols 1
Multiplier index sets: u_Q covers exactly 1..d-1; v_G only indices >= d; all v_G, v_H >= 0.

Step 3. Author's checker: python3 -I check/check_cert.py result/cert_171_1_56_sh.json -> "VERIFIED [[171,1,56]] shadow=True: value=1827 digits, max column coefficient <= 0, 55+2+56 multipliers", rc=0; same for the d=57 certificate ("value=2066 digits ... 56+2+57"), rc=0. Matches check/checker_output.txt.

Step 4. Proof logic re-derived: for feasible A >= 0, value = u_E0*1+u_E1*2^(n-k) = sum_i c_i A_i - sum v_G G(A) - sum v_H H(A) <= 0, contradicting value > 0. The d=56 constraints (A_j=B_j for j<56) also hold for any code of distance >= 56, so the d=56 certificate excludes d=56 and d=57 codes: upper bound <= 55.

Step 5. Table: sha256sum of data files match CLAIM.md (QECC_q4_n171_k1_claimtime.html c92ff980...c20c; qubit_table_full_n1-256.html 26245491...b6). The claim-time page shows lower 34, upper 57. My own regex parse of the full table: 33152 cells, (171,1) = 57. Own propagation (R1 k>=2, R2 (n+1,k), R3 (n-1,k+1)+1, iterated to a fixed point with the (171,1) cell removed): bound implied for (171,1) by other cells = 58 (raw neighbours (172,1)=58, (170,2)=57), so 55 is not implied by propagation.

Not independently done: I did not re-fetch the live page (instructed not to open websites); the live status rests on the saved fetch files only.

Findings: no mismatch, no missing object, no non-determinism. Both certificates verified in exact integer arithmetic by two independent checkers (mine and the author's); the new bound is not implied by propagation on the saved table.

pass: true
