context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic verdict for [[180,2]] upper bound <= 58

## What I did

1. Read CLAIM.md and REPRODUCE.md. Before opening any author code (check/check_cert.py), I looked only at the structure of result/cert_180_2_59_sh.json (keys u_E0, u_E1, u_Q for j=1..58, v_G for j=61,62, v_H for 59 shadow rows).

2. Wrote my own independent checker from the definition (CRSS quant-ph/9608006 and Rains shadow quant-ph/9611001). LP over A_0..A_n >= 0, n=180, k=2, M=2^(n-k)=2^178:
   - A_0 = 1 (multiplier u_E0), sum A_i = M (multiplier u_E1)
   - A_j = B_j for 1 <= j < d: row sum_i K_j(i) A_i - M A_j = 0 (multiplier u_Q, free sign)
   - A_j <= B_j for j >= d: same row >= 0 (multiplier v_G >= 0)
   - Sh_j >= 0: row sum_i (-1)^i K_j(i) A_i >= 0 (multiplier v_H >= 0)
   - K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
   Farkas rule: the combination must have every column coefficient <= 0 and a right-hand side u_E0 + M*u_E1 > 0.
   My script was written in Python big integers, exact, no floats. It also asserts the sign/range of each multiplier (v >= 0, Q indices 1..d-1, G indices >= d).
   Sanity test of my K and shadow formulas on the [[5,1,3]] code (A = 1 + 15 x^4): B = Sh = [1,0,0,30,15,18], as expected.

3. Real output of my checker:
   - cert_180_2_59_sh.json: maxcol<=0: True, rhs>0: True, Q keys exactly 1..58: True, G keys [61, 62], all 180+1 columns checked (180 nonzero).
   - cert_180_2_61_sh.json: maxcol<=0: True, rhs>0: True (Q indices there run 1..60, accepted for d=61).
   So both certificates are valid Farkas infeasibility proofs of the LP, i.e. no [[180,2,d]] code with d >= 59 (and for d >= 61 for the second one).

4. Then ran the author's checker as in REPRODUCE.md:
   - python3 -I check/check_cert.py result/cert_180_2_61_sh.json -> VERIFIED [[180,2,61]] shadow=True: value=1655 digits, max column coefficient <= 0, 58+2+59 multipliers; exit 0
   - python3 -I check/check_cert.py result/cert_180_2_59_sh.json -> VERIFIED [[180,2,59]] shadow=True: value=1655 digits, max column coefficient <= 0, 58+2+59 multipliers; exit 0
   Matches check/checker_output.txt. Deterministic (exact integer arithmetic, repeated runs gave same results).

5. Table record: sha256 of data/QECC_q4_n180_k2_claimtime.html = dbf9ce06dfaacb2c3998b0301e0d23f529bc9ab66be3859a613708df7d15f7df and of data/qubit_table_full_n1-256.html = 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6, both matching CLAIM.md. The saved page reads "Bounds on [[180,2]] lower bound: 35 upper bound: 61"; the full table cell for (180,2) is "35-61".

6. Propagation: ran check/parse_table.py and check/propagate.py on the full table (33152 cells parsed): cell (180,2) = [35, 61], closure = 60. I also wrote my own fixpoint closure over the parsed upper bounds with the three rules (d(n,k)<=d(n,k-1) for k>=2, d(n,k)<=d(n+1,k), d(n,k)<=d(n-1,k+1)+1); it gives 60 too. So a bound of 58 is not implied by other live cells (the closure only reaches 60). Neighbouring cells (180,3), (181,2), (179,3), (180,1) have upper bounds 61, 61, 61, 61, so nothing lower propagates in.

## Reasoning

The certificate is verified by two independent implementations in exact integers. The LP constraints used are exactly the ones in the success criterion (MacWilliams link, A_i = B_i below d, A_i <= B_i, nonnegativity, shadow nonnegativity), each valid for all stabilizer codes (pure or impure). The shadow and normalizer formulas were validated on a known code. The proof shows no [[180,2,59]] code exists, hence the upper bound is at most 58, below the table's 61 and below the propagation closure of 60. The d=61 certificate (literal reading of the criterion) also verifies. No mismatch, missing object or non-determinism found. Live re-fetch was not done (no web access allowed); I relied on the saved claim-time page as instructed.

pass: true
