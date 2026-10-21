context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic verdict for [[167,2]] (claim: no [[167,2,55]] stabilizer code, upper bound <= 54)

## Definition I checked against (quoted from the LP as I applied it)
Stabilizer S of an [[n,k,d]] qubit code, |S| = 2^(n-k), weight distribution A_0..A_n >= 0.
Normalizer enumerator B_j = 2^-(n-k) sum_i K_j(i) A_i, with K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s) (quaternary MacWilliams).
Shadow S_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i >= 0 (Rains). Constraints: A_0 = 1, sum A_i = 2^(n-k), A_j = B_j for 1 <= j <= d-1, A_j <= B_j for j >= d, shadow >= 0.
These are valid necessary conditions for any stabilizer code with distance >= d, so infeasibility for d = 55 means no [[167,2,>=55]] code exists.
Farkas rule: integer multipliers (free sign on equalities, >= 0 on inequalities) whose combined column coefficients c_i are all <= 0, with positive right-hand side u_E0 + u_E1 * 2^(n-k), prove infeasibility over A >= 0.

## What I did
1. Before reading check/check_cert.py code, I looked only at the certificate JSON structure (keys u_E0, u_E1, u_Q for j=1..54, v_G for j=57,58, v_H for 54 indices) and wrote my own checker (exact Python integers, no floats). I took the row layout from the checker's docstring, which matches the definition above.
2. My checker asserts: Q indices lie in 1..d-1; G indices >= d and multipliers >= 0; H multipliers >= 0; every column i = 0..167 has c_i <= 0; and the value u_E0 + u_E1 * 2^165 > 0.
   Output:
   - result/cert_167_2_55_sh.json OK n,k,d 167 2 55 max col coeff 0 value>0 digits 1374 nQ 54 nG 2 nH 54
   - result/cert_167_2_57_sh.json OK n,k,d 167 2 57 max col coeff 0 value>0 digits 1374 nQ 54 nG 2 nH 54
3. The author's checker, run as in REPRODUCE.md:
   - python3 -I check/check_cert.py result/cert_167_2_57_sh.json gave: VERIFIED [[167,2,57]] shadow=True: value=1374 digits, max column coefficient <= 0, 54+2+54 multipliers
   - python3 -I check/check_cert.py result/cert_167_2_55_sh.json gave: VERIFIED [[167,2,55]] shadow=True: value=1374 digits, max column coefficient <= 0, 54+2+54 multipliers
   - exit code 0.
   Both runs were repeated and gave identical results, so no non-determinism.
4. Table record: sha256 of data/QECC_q4_n167_k2_claimtime.html is d26f775a...3869 and of data/qubit_table_full_n1-256.html is 26245491...0b6, both matching CLAIM.md. The saved page text reads "Bounds on [[167,2]] ... lower bound: 33 upper bound: 57".
5. Propagation: ran check/parse_table.py and check/propagate.py on the saved full table. Output: "live (167,2): [33, 57] closure of the live table at (167,2): 56 neighbours R1 (n,k-1): [33, 57] R2 (n+1,k): [33, 57] R3 (n-1,k+1): [32, 56]". So the other live cells imply at most 56, and the claimed 54 is not implied by propagation.
   (The final one-liner in REPRODUCE.md step 3 failed only because of a temp-path mix-up in my shell, not a claim problem; the same numbers appear in the propagate.py output above.)

## Reasoning
- The certificate is an exact integer Farkas certificate. My independently written checker confirms every column coefficient is <= 0 (maximum is exactly 0) and the right-hand side is positive. This is a full check of all 168 columns, not a sample.
- The d = 57 certificate is the d = 55 one with the same multipliers (G rows 55 and 56 carry zero multiplier, so relabelling them as equalities changes nothing). It verifies independently, so the live upper bound 57 is refuted too, and the d = 55 certificate gives the stronger bound 54.
- The new bound 54 is below both 57 (the live bound) and 56 (the propagation closure), so it is a genuine improvement under the stated success criterion.
- Caveat: I did not re-fetch the live table, since I was not permitted web access. I relied on the saved claim-time page.

pass: true
