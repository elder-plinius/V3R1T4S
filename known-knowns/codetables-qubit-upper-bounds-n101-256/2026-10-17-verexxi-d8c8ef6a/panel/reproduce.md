context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE verdict, claim [[161,2]] (no [[161,2,53]] stabilizer code, upper bound <= 52)

## What I did

1. Read CLAIM.md and REPRODUCE.md. Looked at result/cert_161_2_53_sh.json and result/cert_161_2_55_sh.json as data only (keys: n, k, d, shadow, u_E0, u_E1, u_Q rows 1..52, v_G rows 55,56, v_H 52 shadow rows). I did not read the author's code before writing mine.

2. Wrote my own exact checker from the definition in REPRODUCE.md section 2 (quoted): "variables A_0..A_n >= 0 ... B_j = 2^-(n-k) sum_i K_j(i) A_i ... Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i; K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s). ... A_0 = 1, sum A_i = 2^(n-k), A_j = B_j for 1 <= j < d, A_j <= B_j for j >= d, Sh_j >= 0." I also re-derived Rains' shadow coefficient myself: S(x,y) = 2^-(n-k) A(x+3y, y-x), and (y-x)^i = (-1)^i (x-y)^i, which gives the (-1)^i K_j(i) factor.
   My checker uses Python big integers with all rows scaled by 2^(n-k) = 2^159. It builds the combination of equality rows (free multipliers u) and >= rows (multipliers v), asserts every v >= 0, that every row index is in range (Q rows have j < d, G rows have j >= d), that every column coefficient of the combination is <= 0, and that the combined right-hand side is > 0. By Farkas this contradicts A >= 0, so the LP is infeasible.
   Sanity tests of my checker:
   - On the [[5,1,3]] code with A = (1,0,0,0,15,0), my K gives B = (1,0,0,30,15,18) and shadow = (1,0,0,30,15,18), as expected.
   - Perturbing one multiplier (u_Q[10] + 1) makes the check fail, with max column coefficient > 0.

   Output of my checker on both certificates:
   - result/cert_161_2_53_sh.json: negative multipliers on >= rows = 0, max column coefficient <= 0 is True (the maximum is exactly 0), RHS > 0 is True (1317 digits).
   - result/cert_161_2_55_sh.json: the same result (0 negative, max column coefficient 0, RHS > 0, 1317 digits).
   The two certificates are therefore valid on my independent code.

3. Ran the author's checker twice, with `python3 -I check/check_cert.py ...`, exit code 0 both times, identical output (deterministic):
   VERIFIED [[161,2,55]] shadow=True: value=1317 digits, max column coefficient <= 0, 52+2+52 multipliers
   VERIFIED [[161,2,53]] shadow=True: value=1317 digits, max column coefficient <= 0, 52+2+52 multipliers
   This matches check/checker_output.txt.

4. Inference step. The d = 53 LP covers every code with d >= 53, because such a code has A_j = B_j for all j < 53, and A_j <= B_j and Sh_j >= 0 hold for all j. Infeasibility of the d = 53 LP therefore rules out all d >= 53, including 54 and 55. The upper bound is then <= 52. The d = 55 certificate is just a relabelling (rows 53 and 54 get multiplier 0), and it verifies on its own.

5. Table and propagation.
   - sha256 of data/QECC_q4_n161_k2_claimtime.html and data/qubit_table_full_n1-256.html both match CLAIM.md (f7271221... and 26245491...).
   - The claim-time page says "Bounds on [[161,2]]" and the full table cell (161,2) is "31-55".
   - I did my own parse of the full table with a regex (33152 cells) and my own fixpoint closure of R1 (k >= 2), R2 and R3. I got (161,2) upper = 55, neighbours (161,1) = 55, (162,2) = 55, (160,3) = 54, and a closure at (161,2) of 54.
   - The author's parse_table.py and propagate.py give the same: [31, 55] and closure 54.
   - The new bound of 52 is below the propagation closure of 54, so it is not implied by other live cells.
   - Side note: the live table itself is not closed under its propagation rules (55 versus 54), which does not affect this claim. Even 54 is above 52.

## Reasoning
The Farkas certificate verifies in exact integer arithmetic under an independently written checker, and under the author's checker, with no non-determinism. The LP rows match the definition, including the shadow rows. The propagation check is independently confirmed, and the saved table records match their stated hashes. I did not make any live web check. Per my instructions, I relied on the saved claim-time page.

pass: true
