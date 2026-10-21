context: subagent (Claude Code headless on the owner's PC, fresh context)

# REPRODUCE skeptic report, claim q105-4 ([[105,4,35]] does not exist)

## Method
Before reading check/check_cert.py I wrote my own checker (scratch file, not part of the claim folder) from the
definition quoted in REPRODUCE.md step 2: "A_0 = 1, sum A_i = 2^(n-k), A_j = B_j for 1 <= j < d, A_j <= B_j for j >= d,
Sh_j >= 0", with B_j = 2^-(n-k) sum_i K_j(i) A_i, Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i,
K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s). Rows multiplied by 2^(n-k) = 2^101.
Farkas combination: u_E0*[A_0=1] + u_E1*[sum A = 2^101] + sum u_Qj (K_j(i) - 2^101 [i=j]) + sum v_Gj (same row)
+ sum v_Hj (-1)^i K_j(i) is the column coefficient c_i; need every c_i <= 0 over i = 0..105, v >= 0 on
inequalities, and u_E0 + u_E1*2^101 > 0. Then sum c_i A_i <= 0 < value <= sum c_i A_i for any feasible A >= 0: contradiction.
I re-derived this proof step: equalities contribute exactly their rhs, G and H rows are >= 0 so they only increase the sum
above the rhs value; correct. The LP constraints themselves are the standard ones (S subset of N gives A<=B; N\S has
min weight >= d gives A_j=B_j below d; |S| = 2^(n-k); shadow nonnegativity per Rains).
(My first attempt used the opposite sign for the G/H rows and failed; that was my sign error, fixed by re-deriving above.)

## Results (real output)
My own checker on result/cert_105_4_35_sh.json (run twice, identical):
    max col coef <=0: True max True nonzero cols 105 rhs>0: True
    positive cols []
    VERIFIED
Multiplier checks in my checker: u_Q indices 1..34 (= d-1, sign free), v_G indices 37,38 (>= d, all positive), v_H indices
1..35 (all positive); all asserts passed.

Author's checker: `python3 -I check/check_cert.py result/cert_105_4_35_sh.json`
    VERIFIED [[105,4,35]] shadow=True: value=517 digits, max column coefficient <= 0, 34+2+32 multipliers
    exit 0
This matches check/checker_output.txt exactly. Both checkers agree.

LP sanity test of my definitions on the real [[5,1,3]] code (A = 1,0,0,0,15,0): B = shadow = [1,0,0,30,15,18];
A=B for j<3 True, A<=B True, shadow>=0 True (definitions are not vacuous).

Table record: sha256sum of data/qubit_table_full_n1-256.html = 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6
and data/QECC_q4_n105_k4_claimtime.html = 93d5fd17b2cb6c3e8fd97bf84154faa5b88c0922c31d7ea4a21ddf75e4e079b0; both match CLAIM.md.
The saved single-cell page contains "Bounds on [[105,4]]"; the full table cell reads 21-35.

Propagation: author's `check/parse_table.py` + `check/propagate.py` gave "cells 33152 n-range 1 256" and (105,4) = [21, 35]
with closure 35. I independently re-parsed the table with my own regex and computed my own closure of rules R1, R2, R3
(k >= 1 cells, 32896 cells): upper bound U(105,4) = 35, closure(105,4) = 35. Neighbours: (105,3)=21-35, (106,4)=22-35,
(104,5)=20-34 (so R3 gives 35). Hence 34 is not implied by propagation from the saved live table.

## Not checked
The live re-fetch of codetables.de was not done (instructed not to open any website); only the saved files and their hashes
were verified. Non-determinism: none seen (integer arithmetic, repeated runs identical). No missing objects.

pass: true
