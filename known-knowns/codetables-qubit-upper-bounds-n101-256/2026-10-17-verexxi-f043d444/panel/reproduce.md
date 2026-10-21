context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE verdict for [[125,4]], claim: no [[125,4,41]] stabilizer code (upper bound 41 -> 40)

## What I did
1. Read CLAIM.md and REPRODUCE.md, and listed the folder. Before opening check/check_cert.py I looked only at the structure of result/cert_125_4_41_sh.json. Keys: n=125, k=4, d=41, shadow=True, u_E0, u_E1 (free-sign equality multipliers), u_Q (indices 1..40), v_G (indices 43, 44), v_H (39 indices in 0..42, with 20 and 38 and 40 and 41 absent).
2. Wrote my own checker, mychk.py, from the definition. I did not read the author's checker first.
   - Definition used: for an [[n,k,d]] stabilizer code with stabilizer weight distribution A_i (|S| = N = 2^(n-k)), B_j = N^-1 sum_i K_j(i) A_i is the normalizer distribution and Sh_j = N^-1 sum_i (-1)^i K_j(i) A_i is the shadow distribution. K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s) (the quaternary Krawtchouk polynomial).
   - Constraints: A_0 = 1, sum A_i = N, A_j = B_j for 1 <= j < d (rows u_Q), B_j - A_j >= 0 (rows v_G), Sh_j >= 0 (rows v_H), A >= 0.
   - Farkas test: form sum u_r*row_r + sum v_s*row_s and check that every column coefficient is <= 0, that the right-hand side u_E0*1 + u_E1*N is > 0, and that all v are >= 0.
   - I also checked the Krawtchouk implementation by orthogonality (sum_i K_3(i) K_i(5) = 0 and sum_i K_5(i) K_5... = 4^n), so the K_j(i) definition and index convention are right.
   - Real output: u_Q covers exactly 1..40 (True). v_G is [43, 44] and v_H is non-negative, so all inequality multipliers are >= 0 (True). With rows as the integer rows (E0 and E1 unscaled, Q/G as N*(B_j - A_j), H as sum (-1)^i K_j(i) A_i): `max column coefficient <= 0: True`, `rhs > 0: True`, rhs has 803 digits. The other scaling/sign variants I tried were inconsistent combinations and failed, as expected. Only the consistent set passes.
3. Ran the author's checker: `python3 -I check/check_cert.py result/cert_125_4_41_sh.json` printed `VERIFIED [[125,4,41]] shadow=True: value=803 digits, max column coefficient <= 0, 40+2+39 multipliers`, exit code 0. A repeat run gave an identical md5 of the output (deterministic). The 803-digit value agrees with my independent computation, and the output equals check/checker_output.txt.
4. Re-derived the validity of each constraint. A_j = B_j for j < d holds because the normalizer minus the stabilizer has weight >= d, and this does not need purity. A_j <= B_j holds since S is a subset of N(S). Sh_j >= 0 is Rains' shadow inequality, with the (-1)^i sign. The sum A_i = N and A_0 = 1 are the definitions. The Farkas argument is sound: LHS = sum u*b + sum v*(s.A) >= sum u*b > 0, while the column coefficients are <= 0 and A >= 0 force LHS <= 0. This is a contradiction, so no [[125,4,41]] stabilizer code exists. The certificate uses arbitrary-size integers with exact arithmetic.
5. Table and propagation: sha256 of data/QECC_q4_n125_k4_claimtime.html and data/qubit_table_full_n1-256.html match CLAIM.md exactly (7907ff3b..., 26245491...). The saved page shows "lower bound: 24, upper bound: 41" for [[125,4]]. I ran check/parse_table.py and check/propagate.py on the saved full table. The output was `[24, 41] 41`, and the neighbours are R1 (125,3): 41, R2 (126,4): 42, R3 (124,5): 41. The closure is 41, so a bound of 40 is not implied by propagation from other live cells. I removed the generated parsed.json and closure.json afterwards.

## Limits
I did not recompute the propagation closure independently of the author's two scripts. I only checked their output and the neighbour values they print. No web access was used, so "live" status is taken from the saved claim-time page only. The certificate check (the substantive part) was independently reproduced.

## Verdict
The certificate verifies exactly by my own from-definition checker and by the author's checker, deterministically. The table record and the non-implication by propagation are confirmed from the saved files.

pass: true
