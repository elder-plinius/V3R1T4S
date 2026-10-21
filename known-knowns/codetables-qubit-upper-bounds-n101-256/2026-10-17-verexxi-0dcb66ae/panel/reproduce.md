context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE verdict for the claim: no [[150,3,49]] qubit stabilizer code (upper bound 51 lowered to at most 48)

## What I did

1. Read CLAIM.md and REPRODUCE.md. The claim is a Farkas certificate for the quantum weight-enumerator LP with Rains shadow constraints, for n=150, k=3, d=49. A second certificate (result/cert_150_3_51_sh.json, d=51) covers the literal reading of the criterion.

2. Before opening any author code, I wrote my own checker from the definition. I worked out the JSON layout from the certificate data only. It has u_E0, u_E1 (free multipliers on A_0=1 and sum A_i=2^147), u_Q (free multipliers for j=1..48), v_G (non-negative multipliers for j>=d) and v_H (non-negative multipliers on the shadow rows).

   The definition I used, from REPRODUCE.md and the quaternary MacWilliams identity:
   - K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
   - B_j = 2^-(n-k) sum_i K_j(i) A_i.
   - Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i.
   - Rows, all scaled by M = 2^(n-k) = 2^147 so the coefficients are integers: A_0 = 1; sum A_i = M; M*A_j = sum_i K_j(i) A_i for 1 <= j < d; M*B_j - M*A_j >= 0 for j >= d; M*Sh_j >= 0.

   The Farkas rule: combine the rows with multipliers (free on equalities, >= 0 on ">= 0" rows) so that every column coefficient is <= 0 and the right-hand side is > 0. Then c.A = rhs + (non-negative terms) >= rhs > 0 contradicts c.A <= 0 for A >= 0.

   My checker is in plain Python integers, with sanity asserts on the Krawtchouk table: K_j(0) = 3^j C(n,j), and the sum over j of K_j(i) equals 4^n at i=0 and 0 at i=3.

   My first run had the wrong sign convention for the inequality rows, so it gave False. I enumerated all 16 sign choices. Exactly one choice makes the column coefficients <= 0 with rhs > 0, and it is the logically correct convention above (B-A >= 0 and Sh >= 0 rows with non-negative multipliers). I then fixed the checker to that convention. This was a choice of sign convention that I justified on logical grounds. I did not tune it until the result looked right, because only one of the 16 combinations works.

3. Output of my checker (python3 -I, run on both certificates):
   - cert_150_3_49_sh.json: max column coefficient <= 0 is True; rhs > 0 is True (rhs has 4170 bits).
   - cert_150_3_51_sh.json: max column coefficient <= 0 is True; rhs > 0 is True (rhs has 4170 bits).
   - Combined result: True.
   - I ran the d=49 certificate alone a second time and got the same result.
   - I checked that the multipliers in v_G and v_H are all >= 0, that u_Q only uses j in 1..d-1, and that v_G only uses j >= d.

4. I then ran the author's checker, twice, on both certificates:
   - Each run printed "VERIFIED [[150,3,51]] shadow=True: value=1256 digits, max column coefficient <= 0, 48+2+49 multipliers" and "VERIFIED [[150,3,49]] shadow=True: ..." with exit code 0.
   - Both runs were identical (deterministic).
   - The output matches check/checker_output.txt.

5. Table record and propagation:
   - sha256 of data/QECC_q4_n150_k3_claimtime.html is 8607e7f6566d983596e9faf28762b7aecdc7929b713831e16531442e02282c49, and of data/qubit_table_full_n1-256.html is 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6. Both match CLAIM.md.
   - The saved page reads "Bounds on [[150,3]] lower bound: 29, upper bound: 51".
   - I ran check/parse_table.py and check/propagate.py. They parsed 33152 cells, and the output for (150,3) was "[29, 51] 50".
   - Direct neighbour check from the parsed table: d(150,2) upper bound 51, d(151,3) upper bound 51, d(149,4) upper bound 51 so R3 gives 52. Rules R1 and R2 give 51, and the full closure gives 50.
   - So a bound of 48 (or 49) is not implied by propagation from other live cells.

## Reasoning

- The certificate is a valid exact infeasibility proof of the LP. Every constraint used is a true property of an [[n,k,d]] stabilizer code: A_0=1, sum A = 2^(n-k), A_j = B_j for j<d, A_j <= B_j, Sh_j >= 0, A >= 0. I verified it in integer arithmetic with my own independently written code. It uses 48 equality rows, 2 G rows (j=51 and 52), 49 shadow rows and the two E rows.
- No [[150,3,49]] code exists. A code with distance >= 49 satisfies the d=49 LP, so the upper bound is at most 48.
- The d=51 certificate (the literal live bound) also verifies on its own.
- The bound of 48 is below the propagation closure of 50, so it is a genuine improvement over the live table (51).
- Limit of this check: I did not re-fetch the live table, since I had no web access by instruction. I relied on the saved claim-time page.
- Nothing was a sample or spot check. The verification covers every column (0..150) of the certificate.

pass: true
