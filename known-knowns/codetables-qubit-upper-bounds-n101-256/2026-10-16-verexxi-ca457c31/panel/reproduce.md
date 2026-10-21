# VERDICT (REPRODUCE skeptic)

context: subagent (same VM)

I read only files inside this folder. I did not use the web, so I could not re-fetch the live table. I checked the saved snapshot only.

## Order of work
1. I read CLAIM.md and REPRODUCE.md, then looked at the certificate JSON keys. I did not read check/*.py at this point.
2. I wrote my own checker from the definition: my_checker.py. Its diagnostic helper is my_diag.py, its self-test is my_selftest.py, and my propagation closure is my_prop.py.
3. Only after my checker gave a verdict did I read check/check_cert.py, check/parse_table.py, check/propagate.py and the saved outputs, and re-run them.

## Definition implemented (quoted from the docstring of my_checker.py)
```
Definition implemented (qubit stabilizer code [[n,k,d]], S = stabilizer, |S| = M = 2^(n-k)):
  A_i = number of elements of S of (symplectic/Hamming) weight i  (A_0 = 1, sum A_i = M).
  Quaternary MacWilliams: B_j = (1/M) sum_i K_j(i) A_i, K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s)
     (B = weight distribution of normalizer N(S) = S^perp, |N(S)| = 2^(n+k)).
  Rains shadow: Sh_j = (1/M) sum_i (-1)^i K_j(i) A_i >= 0.
  Distance d: B_j = A_j for 0 <= j < d;  S subset N(S) gives A_j <= B_j for all j.
LP (all rows multiplied by M, so integer coefficients), variables A_0..A_n >= 0:
  E0: A_0 = 1;  E1: sum A_i = M;
  Q_j (1<=j<=d-1): sum_i K_j(i) A_i - M*A_j = 0 (same equality as M*A_j - sum K A = 0);
  G_j (j>=d):      sum_i K_j(i) A_i - M*A_j >= 0;
  H_j (0<=j<=n):   sum_i (-1)^i K_j(i) A_i >= 0.
Farkas: multipliers u (free) on equalities, v >= 0 on inequalities; if the combined column
coefficient c_i <= 0 for all i = 0..n and the combined rhs R = u_E0*1 + u_E1*M > 0 then
c.A >= R > 0 contradicts c.A <= 0 for A >= 0, so the LP is infeasible.
```

Why each constraint holds for every [[n,k,d]] code (my derivation):
- A_0 = 1 and sum A_i = |S| = 2^(n-k) hold because S is a group with a single identity.
- B is the weight distribution of S^perp. The quaternary MacWilliams identity for additive codes over GF(4) gives B(x,y) = (1/|S|) A(x+3y, x-y). Expanding (x+3y)^(n-i)(x-y)^i gives the coefficient K_j(i) above.
- Distance d means every normalizer element of weight < d lies in S. So B_j = A_j for j < d, and j = 0 gives A_0 = B_0 = 1. This also covers degenerate (impure) codes.
- S is a subset of N(S), so A_j <= B_j for every j.
- Rains' shadow is S(x,y) = (1/|S|) A(x+3y, y-x). The factor (-1)^i comes from (y-x)^i, and the shadow counts the weights of a coset of N(S), so Sh_j >= 0.
- Farkas: for any feasible A >= 0 we have c.A = sum u(row.A) + sum v(row.A) >= R. If every c_i <= 0 then c.A <= 0, so R <= 0, which contradicts R > 0.

## Commands run and real output

### 1. My checker on both certificates (exact integer arithmetic, no floats)
`python3 -I my_checker.py result/cert_145_1_48_sh.json result/cert_145_1_49_sh.json`
```
result/cert_145_1_48_sh.json n,k,d= (145, 1, 48) max col coeff sign: True max col <= 0 -> False R>0: True nonzero cols: 145 num multipliers Q/G/H: 47 2 46
  R bits= 4198 max col bits= 4199 []
MYVERDICT INFEASIBLE-PROVEN
result/cert_145_1_49_sh.json n,k,d= (145, 1, 49) max col coeff sign: True max col <= 0 -> False R>0: True nonzero cols: 145 num multipliers Q/G/H: 48 2 49
  R bits= 4451 max col bits= 4453 []
MYVERDICT INFEASIBLE-PROVEN
```
Exit code 0.

Convention finding, not a mismatch. My first run used the Q_j row as M*A_j - sum K A and reported FAIL on both certificates. The multiplier on an equality row has a free sign, so this was a row-orientation convention. I enumerated all 2^5 sign flips of the five multiplier groups with my_diag.py. The only pattern that works for d=48 is the one with Q_j oriented as sum K A - M*A_j = 0. This is the same equality, and check/check_cert.py documents exactly this orientation. I then fixed my checker's convention and it accepts. All other multiplier groups (E0, E1, G, H) use the natural orientation.

### 2. Self-test of my formulas (brute force), and tamper tests
`python3 -I my_selftest.py`
For [[5,1,3]], [[7,1,3]] and [[4,2,2]] I built the stabilizer group from its generators and enumerated the normalizer by brute force over all 4^n Paulis. In each case the MacWilliams B equals the brute-force normalizer distribution, Sh_j is a non-negative integer, and A_j <= B_j for all j. The distance read off from B versus A matches the expected value.
```
[[5,1,3]] A= [1, 0, 0, 0, 15, 0] B= [1, 0, 0, 30, 15, 18] Sh= [1, 0, 0, 30, 15, 18] distance(pure/impure formula)= 3 expected 3
[[7,1,3]] A= [1, 0, 0, 0, 21, 0, 42, 0] B= [1, 0, 0, 21, 21, 126, 42, 45] Sh= [1, 0, 0, 21, 21, 126, 42, 45] distance(pure/impure formula)= 3 expected 3
[[4,2,2]] A= [1, 0, 0, 0, 3] B= [1, 0, 18, 24, 21] Sh= [1, 0, 18, 24, 21] distance(pure/impure formula)= 2 expected 2
```

Tamper tests on the d=48 certificate:
- Flipping the sign of v_G[50]: rejected.
- Adding 1 to u_E1: rejected.
- Dropping v_H[0]: rejected.
- Relabelling d=49 with the d=48 data: accepted. This is expected. The d=49 LP contains all the d=48 constraints plus more, so a d=48 proof is also a valid d=49 proof. It is not a bug.

### 3. Author's checker, run twice (determinism), compared with the saved output
`python3 -I check/check_cert.py result/cert_145_1_48_sh.json` and the same for `..._49_sh.json`, repeated twice:
```
VERIFIED [[145,1,48]] shadow=True: value=1264 digits, max column coefficient <= 0, 47+2+46 multipliers
exit 0
VERIFIED [[145,1,49]] shadow=True: value=1340 digits, max column coefficient <= 0, 48+2+49 multipliers
exit 0
(second pass identical)
```
`diff` of the output against check/checker_output.txt printed SAME_AS_SAVED. The author's constraint set and sign conventions are identical to mine, and the author's code does the same exact-integer column test. My code and the author's are different implementations that agree. No floats appear in either decision.

### 4. Propagation check
My own parser and closure: `python3 -I my_prop.py`
```
cells 33152 parsed 33152 dups 0
(145,1): 33 49
iterations 16
closure (145,1): 49  direct neighbours: R2 (146,1) up 49  R3 (144,2) up+1 50  R1 n/a (k=1)
cells where closure < table upper: 1100 [((6, 0), 4, 3), ((12, 0), 6, 5), ((18, 0), 8, 7), ((24, 0), 10, 9), ((68, 16), 27, 19)]
implied bound <=47 at (145,1)? False
lo>up cells: []
```
My closure also applies the rules to k=0 cells, which accounts for 1100 versus the author's 1075. The k=0 cells cannot feed (145,1): R1 needs the source k >= 1, and R2 and R3 only reach (145,1) from (146,1) and (144,2). So this difference is irrelevant.

REPRODUCE.md step 3 exactly (into scratch_prop/):
```
cells 33152 n-range 1 256
cells k>=1: 32896  live > implied: 1075  of which n>100: 1072  n<=100: 3
   ...
[33, 49] 49
```
This matches the expected `[33, 49] 49`.

The saved snapshots hash to the values stated in CLAIM.md. sha256sum gave 50d08374...3 for the (145,1) page and 26245491...b6 for the full table.

## Mismatches found
- Both certificates are valid Farkas certificates of the exact LP I defined. None of the numerical or logical checks mismatched.
- The only discrepancy was the equality row-orientation convention described in section 1. I counted it as a sign convention on a free multiplier, not a mathematical error. The author documents it explicitly.
- Not independently verifiable here, because the web is off limits: that the "live" upper bound is still 49 at claim time. I confirmed only that the saved page and the saved full table both say 33-49 at (145,1). Another panel member needs to cover the live re-fetch.
- The claimed new bound of 47 is not implied by propagation. The closure at (145,1) is 49, and the neighbours are (146,1) with upper bound 49 and (144,2) with upper bound 49, giving 50.
- Non-determinism: none found. Repeated runs produced identical output.
- Missing objects: none. Both certificates, the checker, the outputs and both table files are present.

pass: true
