context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE panel report, claim [[230,5,74]] nonexistence (and [[230,5,77]])

## Method
Before opening check/check_cert.py I looked only at the key structure of result/cert_230_5_74_sh.json
(u_E0, u_E1, u_Q[1..d-1], v_G, v_H) and wrote my own exact checker from the definition in CLAIM.md/REPRODUCE.md item 2
("A_0 = 1, sum A_i = 2^(n-k), A_j = B_j for 1 <= j < d, A_j <= B_j for j >= d, Sh_j >= 0",
B_j = 2^-(n-k) sum K_j(i) A_i, Sh_j = 2^-(n-k) sum (-1)^i K_j(i) A_i, K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s)).
Mine builds each LP row times 2^(n-k) with Python big integers, forms the multiplier combination column by column
(A_0..A_230), and tests: every column coefficient <= 0, constant (value) > 0, inequality multipliers >= 0, equality
multipliers' index range exactly 1..d-1. Because the multiplier orientation convention was not stated in the data, my
script tried all 8 sign orientations of the three equality families (E0, E1, Q) and both scalings of E0; it reports which pass.

## My checker's output (real)
    result/cert_230_5_74_sh.json 230 5 74 Qkeys 1 73 73 Gkeys [76, 77, 78] Hkeys 0 81 75
    OK ((1, 1, 1, 'one'), True, True, 2520)        (max column <= 0, value > 0, value has 2520 digits)
    result/cert_230_5_77_sh.json 230 5 77 Qkeys 1 76 76 Gkeys [79, 80, 81] Hkeys 0 82 76
    OK ((1, 1, 1, 'one'), True, True, 2301)
    OK ((1, -1, 1, 'one'), True, True, 2223)
For d=74 exactly one orientation passes, the natural one (A_0 = 1 and sum A = 2^(n-k) taken as written, Q rows as
sum K_j(i)A_i - 2^(n-k) A_j = 0). All G and H multipliers are positive (nonnegativity respected). So an independent
implementation confirms: the linear combination of valid constraints gives sum_i c_i A_i >= value > 0 with every c_i <= 0,
impossible for A >= 0. Proof step re-derived: for feasible A, value = sum c_i A_i - (nonnegative G terms) - (nonnegative H terms) <= 0,
contradiction. The constraints used are valid for every [[n,k,d']] stabilizer code with d' >= d (Calderbank-Rains-Shor-Sloane
MacWilliams identity with A_j = B_j below the distance and A_j <= B_j everywhere; Rains shadow nonnegativity), so
nonexistence at d=74 covers all d >= 74, i.e. upper bound <= 73 for [[230,5]].

## Author's checker and determinism (run after mine)
    $ python3 -I check/check_cert.py result/cert_230_5_74_sh.json
    VERIFIED [[230,5,74]] shadow=True: value=2520 digits, max column coefficient <= 0, 73+3+75 multipliers   (exit 0)
    $ python3 -I check/check_cert.py result/cert_230_5_77_sh.json
    VERIFIED [[230,5,77]] shadow=True: value=2301 digits, max column coefficient <= 0, 76+3+76 multipliers   (exit 0)
    (74 run a second time: identical output.)
Reading check/check_cert.py afterwards: its docstring LP and its code (index-range checks, nonnegative G/H multipliers,
value = u_E0 + u_E1*2^(n-k) > 0, column loop over all i = 0..n, shadow sign (-1)^i) agree with my independent reading. Output matches
check/checker_output.txt. No mismatch, no missing object, no non-determinism seen.

## Table / propagation (saved files only; I did not fetch anything)
    $ sha256sum data/*.html
    aabd159795d970a2eaee7503c56c62ebbc5aa4ea761e8de015a1eaa529f3dbdb  data/QECC_q4_n230_k5_claimtime.html
    26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6  data/qubit_table_full_n1-256.html
Both hashes equal those in CLAIM.md. The cell page says "lower bound: 44, upper bound: 77"; the full table cell n=230,k=5 reads 44-77.
My own table parse (regex on title="n=..,k=.."): 33152 cells, 230,5 -> upper 77; neighbours (230,4)=77, (231,5)=77, (229,6)=77,
(230,6)=77, (231,4)=77. My own fixed-point closure with R1 (k>=2), R2, R3 over all cells with k>=1 gives closure(230,5) = 77.
Author's scripts: parse_table.py -> "cells 33152 n-range 1 256"; propagate.py closure at 230,5 -> "[44, 77] 77".
So 73 is not implied by propagation from other live cells; the table bound 77 stands at the claimed time. The criterion
literally asks about d = live upper bound (77): the 77 certificate verifies too, and the 74 certificate is the stronger result.

## Limits
I was not allowed to re-fetch the live page, so "live immediately before claiming" rests on the saved, hash-matching, timestamped
(2026-10-16T20:56:42Z per CLAIM.md) record; the HTML page itself carries no fetch timestamp. Nothing else was unconfirmed.

pass: true
