context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE verdict for [[230,10]] (no [[230,10,73]] code, upper bound <= 72)

## Definition I checked against (quoted from the LP statement in CLAIM.md / REPRODUCE.md)
"A_0 = 1, sum A_i = 2^(n-k), A_j = B_j for 1 <= j < d, A_j <= B_j for j >= d, Sh_j >= 0", with
B_j = 2^-(n-k) sum_i K_j(i) A_i, Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i, K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
I re-derived that these are the right constraints for a qubit stabilizer code: S is contained in its normalizer (A_j <= B_j), the quaternary MacWilliams identity gives B, distance d means A_j = B_j below d, and Rains' shadow A(x+3y, y-x) gives the (-1)^i factor. A code with distance greater than 73 also satisfies the d=73 rows, so infeasibility at 73 gives the bound <= 72.
Farkas step re-derived: for feasible A >= 0, sum_i c_i A_i = value + (v_G . G) + (v_H . H) >= value, because the Q rows vanish. So value > 0 together with all c_i <= 0 is a contradiction.

## What I did
1. Before opening any author checker code, I wrote my own checker (outside the claim folder, in a temp directory). It uses Python big integers only, with Krawtchouk K_j(i) from the explicit binomial sum. It reads the JSON multipliers and asserts the index ranges: u_Q in 1..d-1, v_G in d..n and >= 0, v_H in 0..n and >= 0. It builds every column coefficient c_i for i = 0..230 and checks max c_i <= 0 and value = u_E0 + u_E1 * 2^(n-k) > 0.
   - result/cert_230_10_73_sh.json: nQ 72 (complete 1..72), nG 4 (min index 75, none negative), nH 73; max column coefficient <= 0: True; value > 0: True; output OK.
   - result/cert_230_10_77_sh.json: nQ 74, nG 2 (min index 77, none negative), nH 73; max column coefficient <= 0: True; value > 0: True; output OK.
   - Negative control: halving v_H[1] in a copy of the 73 certificate gave "max col coef <= 0: False" and FAIL, so my checker does discriminate.
2. Ran the author's checker twice, as REPRODUCE.md says: `python3 -I check/check_cert.py result/cert_230_10_73_sh.json` and `python3 -I check/check_cert.py result/cert_230_10_77_sh.json`. Both printed VERIFIED with exit code 0:
   "VERIFIED [[230,10,73]] shadow=True: value=2408 digits, max column coefficient <= 0, 72+4+73 multipliers"
   "VERIFIED [[230,10,77]] shadow=True: value=2408 digits, max column coefficient <= 0, 74+2+73 multipliers"
   This matches check/checker_output.txt, and the results were identical across my runs (deterministic).
3. Table record:
   - sha256sum of data/QECC_q4_n230_k10_claimtime.html is 3ad6f4cb846fc5e018c1ca6b9a665bd4610c10326dadf48bc0518656c423bc7c, matching CLAIM.md.
   - sha256sum of data/qubit_table_full_n1-256.html is 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6, matching CLAIM.md.
   - The saved cell page reads "Bounds on [[230,10]] lower bound: 42 upper bound: 77".
   - The full table also shows 42-77 for (230,10).
4. Propagation, with my own parser and closure (rules R1 d(n,k) <= d(n,k-1) for k >= 2, R2 d(n,k) <= d(n+1,k), R3 d(n,k) <= d(n-1,k+1)+1, iterated to a fixpoint on all 33152 parsed cells). Neighbours (230,9), (231,10) and (229,11) all have upper bound 77. The closure at (230,10) is 75, which agrees with check/propagation_check.txt and the expected 75 in REPRODUCE.md. The new bound 72 is below 75, so it is not implied by the live cells.

## Reasoning
Both certificates verify exactly under an independently written integer checker and under the author's checker. The LP is the standard one with the shadow constraints. The 77 certificate is the literal live-bound reading, and the 73 certificate gives the stronger conclusion, an upper bound of at most 72, which lowers the live 77 by 5. The cell data matches the stated hashes, and propagation closure (75) does not already give 72.

Limits: I made no web request, as instructed, so I could not re-fetch the live page. I rely on the saved claim-time page, which hashes correctly. I did not check the truthfulness of the live page at claim time beyond that.

pass: true
