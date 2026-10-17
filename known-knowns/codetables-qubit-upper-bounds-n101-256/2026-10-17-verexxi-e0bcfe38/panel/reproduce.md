context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic verdict for the claim "no [[115,4,38]] qubit stabilizer code, upper bound at most 37"

## Definition I checked against (written before reading the author's code)
For a stabilizer code [[n,k,d]] with weight distribution A_0..A_n of the stabilizer S, |S| = 2^(n-k) = M:
- A_0 = 1 and sum A_i = M.
- B_j = (1/M) sum_i K_j(i) A_i, with K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s) (quaternary MacWilliams).
- A_j = B_j for 1 <= j < d, A_j <= B_j for j >= d.
- Shadow (Rains): Sh_j = (1/M) sum_i (-1)^i K_j(i) A_i >= 0. This is the coefficient extraction of A(x+3y, y-x), which is valid for every additive self-orthogonal code.
- Farkas: with sign-free multipliers on equalities and nonnegative multipliers on inequalities, if every column of the combination is <= 0 and the right-hand side (u_E0 + u_E1*M) is > 0, then no A >= 0 satisfies the system.

The saved certificate has the fields n, k, d, u_E0, u_E1, u_Q, v_G, v_H. I had to read the row orientation from the author's docstring (K - M*delta for the Q and G rows, +(-1)^i K for the H rows). My first attempts used the opposite orientation and failed. After I switched to the documented orientation, I derived the sign rule myself and agreed with it. The rule is: sum c_i A_i = value + (G and H terms, all >= 0), so c <= 0 together with value > 0 is a contradiction.

## What I ran
1. My own checker (own Krawtchouk function with sanity asserts: K_0 = 1, K_2(0) = 9*C(7,2), and sum_j K_j(i) = 4^n * delta_i0 for n = 7). It also checks index ranges (Q in 1..d-1, G in d..n, H in 0..n) and nonnegativity of the G and H multipliers. Its output:
   - result/cert_115_4_38_sh.json: n,k,d = 115,4,38, max col<=0: True, value>0: True, 666 digits
   - result/cert_115_4_39_sh.json: n,k,d = 115,4,39, max col<=0: True, value>0: True, 666 digits
   The certificate has 37 Q multipliers (j = 1..37), 2 G multipliers (j = 40 and 41), and 36 H multipliers.
2. The author's checker, run as `python3 -I check/check_cert.py ...`:
   - VERIFIED [[115,4,39]] shadow=True: value=666 digits, max column coefficient <= 0, 37+2+36 multipliers (exit 0)
   - VERIFIED [[115,4,38]] shadow=True: value=666 digits, max column coefficient <= 0, 37+2+36 multipliers (exit 0)
   These match check/checker_output.txt.
3. Table record: sha256 of data/QECC_q4_n115_k4_claimtime.html is b40fb6f88b7879f4f6d454220f5c8c5b5ec97ee57e9679a9c492d512ad378f97, and of data/qubit_table_full_n1-256.html is 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6. Both match CLAIM.md. The saved cell page says "Bounds on [[115,4]] lower bound: 24 upper bound: 39".
4. Propagation, with my own regex parser of the saved full table and my own closure loop (R1: d(n,k) <= d(n,k-1) for k >= 2; R2: d(n,k) <= d(n+1,k); R3: d(n,k) <= d(n-1,k+1)+1; only k >= 1). The parser read 33152 cells. The live (115,4) upper bound is 39 and the lower bound is 24. The closure at (115,4) is 38. The neighbours are (115,3) = 39, (116,4) = 39, and (114,5) = 38 live with closure 37. The author's check/parse_table.py and check/propagate.py reported the same: the closure is 38, and (115,4) is one of the live cells above its closure.

## Reasoning
- The certificate is an exact integer Farkas certificate, and it verified in two independent implementations. The shadow constraints are mathematically valid. So no [[115,4,38]] stabilizer code exists, and by the same LP (equalities for j < 38 only get weaker for larger d) no code with d >= 38 exists. Hence d <= 37.
- The d = 39 certificate also verifies on its own. The multiplier at j = 38 is zero, so the relabelling the author describes is harmless.
- The live bound 39 is already above its propagation closure of 38, so the table is internally stale at this cell. The claimed bound 37 is below the closure of 38, so it is not implied by the standard rules applied to other live cells. This is the substantive novelty condition, and it holds.
- Everything is exact and deterministic. Two runs of each checker gave identical output.
- Caveat: I did not fetch the live page (no web access was allowed). I relied on the saved claim-time page, as instructed.

pass: true
