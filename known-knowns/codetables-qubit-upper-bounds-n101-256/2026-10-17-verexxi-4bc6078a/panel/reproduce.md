context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic verdict for q110-5 ([[110,5,36]] nonexistence)

## Step 1: own checker written before reading any author code
I only read CLAIM.md, REPRODUCE.md and the certificate JSON structure (keys: n,k,d,shadow,u_E0,u_E1,u_Q[1..35],v_G[38,39],v_H[0..31,36,37]).
Definition used (quoted from REPRODUCE.md and cross-checked with the standard theory, CRSS quant-ph/9608006 and Rains quant-ph/9611001):
variables A_0..A_n >= 0, the stabilizer weight distribution, |S| = 2^(n-k) = M; B_j = (1/M) sum_i K_j(i) A_i;
Sh_j = (1/M) sum_i (-1)^i K_j(i) A_i; K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
Valid facts for any [[n,k,d]] stabilizer code: A_0 = 1; sum A_i = M; A_j = B_j for 1 <= j < d; A_j <= B_j for all j (S inside its normalizer);
Sh_j >= 0 (Rains). I built these rows scaled by M (integers) in Python big-integer arithmetic (my own file, not in the package).
Farkas rule: if the combination (free-sign multipliers on equalities, nonnegative on the >= 0 rows B_j - A_j >= 0 and M*Sh_j >= 0) has every column coefficient <= 0 and positive right-hand side, then no A >= 0 satisfies the system, because the combined left side would be both <= 0 and >= rhs > 0.
My code also asserts: Q rows only for 1 <= j < d, G rows only for j >= d, all inequality multipliers >= 0.

Note: my first attempt used the opposite sign for the inequality multipliers and failed; I scanned the 32 sign conventions, found the one convention (rows written as B_j - A_j >= 0 and Sh_j >= 0 added with the multipliers) that works, and re-derived above that it is the mathematically correct dual direction (not a fitted fudge): the combination col.A equals rhs + (nonnegative terms) >= rhs > 0 yet col <= 0 forces col.A <= 0.

Output of my checker:

    result/cert_110_5_36_sh.json n,k,d= 110 5 36 max column coeff: 0 rhs>0: True rhs digits 583 -> VALID INFEASIBLE   (exit 0)
    result/cert_110_5_37_sh.json n,k,d= 110 5 37 max column coeff: 0 rhs>0: True rhs digits 583 -> VALID INFEASIBLE   (exit 0)

Run twice, identical md5 of output (deterministic).

## Step 2: author's checker
    python3 -I check/check_cert.py result/cert_110_5_37_sh.json
    VERIFIED [[110,5,37]] shadow=True: value=583 digits, max column coefficient <= 0, 35+2+34 multipliers   (exit 0)
    python3 -I check/check_cert.py result/cert_110_5_36_sh.json
    VERIFIED [[110,5,36]] shadow=True: value=583 digits, max column coefficient <= 0, 35+2+34 multipliers   (exit 0)
Agrees with my independent result. (The d=37 certificate does not use a Q_36 row, so it is simply a certificate with a subset of valid rows; it is valid on its own. Since d=36 nonexistence implies d=37 nonexistence anyway, the stated bound 35 stands.)

## Step 3: table record
sha256sum of data/QECC_q4_n110_k5_claimtime.html = 22454f4e...071767c and data/qubit_table_full_n1-256.html = 26245491...de4b0b6, both matching CLAIM.md.
The saved cell page shows "lower bound: 23, upper bound: 37" for [[110,5]]. The full table parsed by my own regex gives 33152 cells, (110,5) = 23-37.

## Step 4: propagation (independent re-implementation)
I parsed every cell of data/qubit_table_full_n1-256.html and iterated to fixpoint the rules U(n,k) <= U(n,k-1) (k >= 2), U(n,k) <= U(n+1,k), U(n,k) <= U(n-1,k+1)+1:
"iters 16 closure(110,5)= 36 table 37; cells changed: 1100".
Closure at (110,5) is 36, so an upper bound of 35 (or the claimed lowering from 37 to 35) is not implied by propagation from other live cells. Matches check/propagation_check.txt (closure 36). Neighbours: U(110,4)=37, U(111,5)=37, U(109,6)=37.

## Limits
I did not re-fetch the live page (no web access allowed); I rely on the saved claim-time page, as instructed. The correctness of the LP constraints themselves (Rains shadow, MacWilliams) is taken from the cited literature; I re-derived the algebra of the Farkas step and the Krawtchouk definitions myself.

## Verdict
All properties verified exactly with an independently written checker, the author's checker agrees, saved file hashes match, propagation closure re-derived (36, so not implied), outputs deterministic. No mismatch, missing object or non-determinism found.

pass: true
