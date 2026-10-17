context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic verdict for [[127,2,42]] nonexistence

## Definition used (stated in CLAIM.md / REPRODUCE.md, standard CRSSS + Rains)
Variables A_0..A_127 >= 0. For a stabilizer code [[n,k,d]], A_0 = 1, sum A_i = 2^(n-k), B_j = 2^-(n-k) sum_i K_j(i) A_i with K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s), A_j = B_j for 1 <= j < d, A_j <= B_j for j >= d, and Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i >= 0. These constraints are valid for every stabilizer code, so any subset of the rows may be used in a Farkas combination.

## What I did
1. Before reading any author code, I wrote my own checker (scratch script mychk.py, bare name). It reads result/cert_127_2_42_sh.json (keys n, k, d, u_E0, u_E1, u_Q for j=1..41, v_G for j=44,45, v_H for j in 0..40 except 27). It builds the Krawtchouk rows itself with exact Python integers and applies these row meanings:
   - E0: A_0 - 1 = 0
   - E1: sum A_i - 2^125 = 0
   - Q_j: (2^125 B_j - 2^125 A_j) = 0, for j = 1..41
   - G_j: (2^125 B_j - 2^125 A_j) >= 0
   - H_j: 2^125 Sh_j >= 0
   It asserts that all v_G and v_H multipliers are >= 0. It then computes the combined column coefficients and the right-hand side (u_E0*1 + u_E1*2^125).
   Real output: the maximum column coefficient is <= 0 (it is exactly 0), and the right-hand side value is > 0. With A >= 0 the combination is <= 0 on the left but must be >= the positive value, so the LP is infeasible (Farkas). The multiplier signs were not assumed; I asserted them. The alternative scaling of the E rows (by 2^125) gave a positive column coefficient. That is only a different, inconsistent scaling choice of mine, and the consistent one passes.
   Distinct constraints used: equalities for 1..41 (exactly d-1 = 41, matching d = 42), inequalities A_44 <= B_44 and A_45 <= B_45, and 40 shadow rows. All are valid rows, so the proof is sound.
2. I ran the author's checker: `python3 -I check/check_cert.py result/cert_127_2_42_sh.json`. Output: "VERIFIED [[127,2,42]] shadow=True: value=906 digits, max column coefficient <= 0, 41+2+40 multipliers", exit code 0. It was deterministic across two runs (same md5 of output). It matches check/checker_output.txt.
3. Table record: sha256 of data/QECC_q4_n127_k2_claimtime.html and data/qubit_table_full_n1-256.html match the hashes in CLAIM.md exactly (cae0ee29...3b1 and 26245491...6b6). The claim-time page text reads "Bounds on [[127,2]] lower bound: 25 upper bound: 42". So the live upper bound is 42 and the claim of 41 is a lowering by 1.
4. Propagation: I ran check/parse_table.py (33152 cells parsed, n 1..256) and check/propagate.py. Real output: T[127][2] = [25, 42] and closure = 42. I also checked the neighbours directly from the parsed full table: (127,1) = [27,42], (128,2) = [25,43], (126,3) = [25,42], (127,3) = [25,42]. R1 gives <= 42, R2 gives <= 43, and R3 gives 42+1 = 43. None implies 41, so the new bound is not implied by the standard rules. (I deleted my generated parsed.json and closure.json afterwards.)

## Reasoning
The certificate is an exact integer Farkas certificate, independently re-verified by code I wrote from the definition. The needed rows are all valid constraints, and the result is consistent with the author's checker. The table state and non-propagation both reproduce from the saved files, with no mismatches, missing objects or non-determinism. Limitation: I did not rely on or consult the live site (no web access), only the saved claim-time page. Also, the full-table propagation closure was taken from the author's propagate.py (I only independently checked the one-step neighbours), but the one-step neighbour check already shows the bound is not implied, since R2 and R3 give >= 42 and the closure rules only lower bounds through those cells.

pass: true
