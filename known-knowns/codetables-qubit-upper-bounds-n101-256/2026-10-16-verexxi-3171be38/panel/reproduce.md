# VERDICT (REPRODUCE skeptic)

context: subagent (same VM)

I read only files inside this folder; no web and no GitHub tool. I wrote my checker (mycheck/my_checker.py) before opening check/check_cert.py.

## Definition implemented (quoted from my checker's docstring)
S = stabilizer of an [[n,k,d]] qubit code = additive (n, 2^(n-k)) code over GF(4), self-orthogonal under the trace-Hermitian form; N = S^perp (normalizer), |N| = 2^(n+k).
A_i = #{s in S: wt(s)=i}, B_i = #{v in N: wt(v)=i}.
 (0) A_0 = 1.   (1) sum_i A_i = 2^(n-k).
 (2) MacWilliams (quaternary): B_j = 2^-(n-k) sum_i K_j(i) A_i, K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).
 (3) S subset N, so A_j <= B_j for all j.  (4) distance d: N\S has no word of weight < d, so A_j = B_j for 0 < j < d.
 (5) Rains shadow: Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i >= 0 for all j (it is the weight enumerator of the shadow, a set of words).
 (6) A_i >= 0.
LP infeasible if Farkas multipliers y exist (y free on equalities, >= 0 on rows 'c.A >= b') with sum y_r c_r <= 0 columnwise and sum y_r b_r > 0; for feasible A >= 0, y.(cA) >= y.b > 0 contradicts the columnwise <= 0. All rows scaled by 2^(n-k) so coefficients are integers.

Why each constraint holds for every [[n,k,d]] (re-derived): (0),(1) from S being a group of order 2^(n-k) containing 0. (2) is MacWilliams for additive GF(4) codes with the trace-Hermitian dual. (3) holds because S is self-orthogonal, so S is inside S^perp. (4) holds because a word of N\S of weight < d would be an undetectable error of weight < d, so the stabilizer-code distance would be less than d. Min distance >= d suffices, so a nonexistence proof for d=50 also excludes d>=50 and gives the bound <= 49. (5) is Rains' theorem: the shadow is {u : <u,s> = wt(s) mod 2 for all s in S}, whose enumerator is the formula in (5).

## Validation of my definitions by brute force (mycheck/validate_defs.py)
I enumerated S, N and the shadow directly (symplectic representation) for [[5,1,3]], Steane [[7,1,3]], [[8,3,3]] and four small codes with odd-weight stabilizers ([[2,1,1]] etc., where (-1)^i matters). In every case M*B_j and M*Sh_j equalled the K-sums exactly, and A_j <= B_j and A_j = B_j for j < d held. Output of `python3 -I mycheck/validate_defs.py` ended with `odd3 [[4,1,1]] A [1, 2, 2, 2, 1] B [1, 4, 10, 12, 5] Sh [0, 0, 4, 8, 20] OK` and no assertion errors. The odd4 case aborted on an invalid generator set in my own test, which does not affect the other cases.

## Certificate format
I inferred it from the JSON shape before reading the author's code: u_E0 and u_E1 multiply A_0=1 and sum A=2^(n-k); u_Q[j] for j=1..d-1 multiply the equalities A_j=B_j; v_G[j] multiply the A_j<=B_j rows; v_H[j] multiply the shadow rows. My first orientation of the Q rows was sign-flipped. Since u_Q is free on equalities, I flipped it to K_j(i) - M[i==j] and the result is the same combination, not a change of the claim. I did not tune any other sign, and v_G and v_H are asserted >= 0.

## Commands and real output
$ python3 -I mycheck/my_checker.py result/cert_152_1_50_sh.json result/cert_152_1_51_sh.json
result/cert_152_1_50_sh.json n,k,d= 152 1 50 rhs>0: True max col coeff<=0: True bad cols: [] nG 2 nH 49 rhs sign 1 rhs bits 4916
result/cert_152_1_51_sh.json n,k,d= 152 1 51 rhs>0: True max col coeff<=0: True bad cols: [] nG 2 nH 50 rhs sign 1 rhs bits 4902
MY VERDICT True        (exit 0; two runs gave identical output hashes, so it is deterministic)
My checker asserts that the Q indices are exactly 1..d-1, uses only exact Python integers and has no floats. The two certificates have 152 columns each, and every combined column coefficient is <= 0.

$ python3 -I check/check_cert.py result/cert_152_1_50_sh.json
VERIFIED [[152,1,50]] shadow=True: value=1480 digits, max column coefficient <= 0, 49+2+49 multipliers   (exit 0)
$ python3 -I check/check_cert.py result/cert_152_1_51_sh.json
VERIFIED [[152,1,51]] shadow=True: value=1476 digits, max column coefficient <= 0, 50+2+50 multipliers   (exit 0)
The output is byte-identical to check/checker_output.txt. The author's LP, as stated in its docstring, matches my definition row for row.

Propagation. I wrote my own parser and closure (mycheck/my_prop.py) before running the author's:
$ python3 -I mycheck/my_prop.py
cells parsed 33152 distinct 33152 (152,1)= 51
anchors with title n=: 33152
closure(152,1)= 51
(152, 1) live 51 closure 51 / (153, 1) live 51 closure 51 / (151, 2) live 51 closure 51 / (152, 2) live 51 closure 51 / (151, 1) live 51 closure 51
direct neighbours: R2 (153,1)= 51  R3 (151,2)+1= 52
The author's version, following REPRODUCE.md step 3:
$ python3 -I check/parse_table.py data/qubit_table_full_n1-256.html parsed.json && python3 -I check/propagate.py parsed.json closure.json && python3 -c "..."
cells 33152 n-range 1 256
cells k>=1: 32896  live > implied: 1075  of which n>100: 1072  n<=100: 3
[33, 51] 51
The two propagation computations agree. Cell (152,1) is not above its closure, and neither 49 nor 50 is implied by other live cells under R1-R3.

Saved data. sha256 of data/QECC_q4_n152_k1_claimtime.html and data/qubit_table_full_n1-256.html match the hashes in CLAIM.md. The cell page says "lower bound: 33 upper bound: 51" and the full table cell reads 33-51.

## Mismatches found
None. I found no mismatch, no missing object and no non-determinism.

## Limits, stated honestly
- I could not re-fetch the live table, because the web was off-limits. The criterion's "re-fetched live immediately before claiming" is only supported by the saved snapshot, which is consistent with the claim.
- The propagation rules R1-R3 are taken as given. R3 is stated for all codes, which only makes the closure stronger, so it is conservative for the "not implied" test.
- That the nonexistence of an [[152,1,50]] code is not already known elsewhere is outside the folder's scope. I verified only the mathematics and the reproduction.

pass: true
