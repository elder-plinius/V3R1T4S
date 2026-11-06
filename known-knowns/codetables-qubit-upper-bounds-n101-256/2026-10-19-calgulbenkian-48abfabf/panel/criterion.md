context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report: qubit-ub-n107-k2-d35

Cell: [[107,2]] qubit stabilizer codes, claimed new upper bound 35 (certificate excludes d = 36, the live upper bound). Target id: codetables-qubit-upper-bounds-n101-256. Win claimed: Full. The contributor's hash list checked from inside the package folder: all files OK.

## Full success criterion, clause by clause

Criterion (verbatim, the target's success criterion): "Success means, for some qubit cell (n,k) with 101 <= n <= 256, a proof that no [[n,k,d]] stabilizer code exists for d equal to the live table upper bound (https://codetables.de/QECC.php?q=4&n={n}&k={k}, re-fetched live immediately before claiming), thereby lowering it by at least 1 (direction: min upper bound), where the proof is an exact rational infeasibility certificate (Farkas dual) of the quantum weight-enumerator LP (stabilizer and normalizer enumerators linked by the quaternary MacWilliams identity, A_i <= B_i, A_i = B_i for 0 < i < d, nonnegativity, plus shadow-enumerator nonnegativity where used), checked in exact integer arithmetic by an independent script; and the new bound is NOT already implied by applying the standard propagation rules (d(n,k) <= d(n,k-1) for k >= 2, d(n,k) <= d(n+1,k), d(n,k) <= d(n-1,k+1)+1 or as stated by the table) to other live cells."

Disclosure: to learn which multiplier family belongs to which LP row I read the docstring and check function of the author's qubit_cert_check.py (first 60 lines; I did not run it). I then wrote my own checker (written from scratch, not shipped in this package) with its own Krawtchouk code and rebuilt every LP row from the criterion text. The row meanings are exactly those the criterion lists: E0 (A_0 = 1), E1 (sum of A_i = 2^(n-k)), Q_j (B_j - A_j = 0 for 1 <= j <= d-1), G_j (B_j - A_j at least 0 for d <= j <= n), H_j (shadow, sum over i of (-1)^i K_j(i) A_i at least 0, j = 0..n), A_i at least 0, with B_j = (1/2^(n-k)) sum_i K_j(i) A_i and K the quaternary Krawtchouk polynomial with 3 = q - 1.

My output for this cell: [[107,2]] excluded d=36 claimed ub 35: live lower/upper (23, 36); cert valid=True [] rhs>0=True (Q35,G2,H33); closure live only=36; live+PR=36; live+PR+other claims=36; strictly below closure=True

- n between 101 and 256: met (107).
- d equals the live upper bound, lowering it by at least 1: met. Live cell fetched once by me: https://codetables.de/QECC.php?q=4&n=107&k=2 at 2026-10-19T05:22:27Z, HTTP 200, page sha256 cd8672d070b92d78748383d7ff4ffab25f7080c546dbefc7c069c50530f0c78c; it reads lower bound 23 upper bound 36. Excluding d = 36 lowers the upper bound by exactly 1, to 35.
- Exact integer Farkas certificate: met. Multiplier signs (G, H at least 0; E, Q free), index ranges, right-hand side u_E0 + u_E1 * 2^(n-k) strictly positive, and the combined coefficient of every variable A_0..A_107 at most 0, all verified in Python integers.
- LP is the one the criterion names and is not over-constrained: I tested the constraint set (B at least A, B = A below d, shadow nonnegative) on real codes: [[5,1,3]], [[7,1,3]], [[6,0,4]] (my own sanity script, not shipped in this package): all satisfy it, so a feasible code is not excluded by a wrong row. The rows use no purity assumption (B = A is imposed only below d), so the certificate also excludes impure codes (Open question 1).
- Not implied by the standard rules applied to other live cells: met. I took the full live table extract (33152 cells), applied the three rules to a fixed point (rule 1 for k at least 2): the closure value of this cell is 36 from the live table alone and 36 after adding the 56 merged and open pull-request values listed in the folder. 35 is strictly below both. Open question 2: counting or not counting open pull requests gives the same closure here.
- Neighbours listed in the folder (for the three one-step rules): "R1: U(n,k) <= U(n,k-1), k >= 2",107,1,23,36,0; "R2: U(n,k) <= U(n+1,k)",108,2,24,36,0; "R3: U(n,k) <= U(n-1,k+1) + 1",106,3,22,35,1.
- Open question 4 (second Krawtchouk implementation): my checker is that second implementation and it agrees.
- No newer-paper or pull-request conflict that I know of: no pull request in a snapshot of all V3R1T4S pull requests (titles and bodies; 473, fetched 2026-10-19T04:30:31Z) carries this cell; merged siblings of the same kind exist for other cells (for example #269, #297).

Fetch note: I fetched each page below once (curl with the honest user agent, no retry); times are UTC from the machine clock, status 200 for all.

confirmed_scope: Exact integer Farkas certificate (quantum weight-enumerator LP with shadow constraints, no purity assumption) that no qubit stabilizer code [[107,2,d]] with d at least 36 exists, so the upper bound for [[107,2]] is at most 35 against the live value 36 fetched 2026-10-19; the value is below the propagation closure of the live table plus the 56 listed pull-request values plus the other claimed cells.

pass: true
