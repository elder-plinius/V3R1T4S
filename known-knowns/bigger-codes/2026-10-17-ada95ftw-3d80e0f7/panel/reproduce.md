# REPRODUCE verdict: A(34,10,8) <= 618
context: subagent (fresh executor, saw only claim/A34_10_8/)

Every path below is relative to the claim folder `claim/A34_10_8/`. My own scripts are in `../../mine/`, which is the reproduce folder's `mine/` directory: johnson.py, lp.py, check_cert.py, sanity.py, input.py, extra.py.
I wrote these scripts before I read verify.py. All arithmetic uses fractions.Fraction.

## Definitions used (quoted from my johnson.py header)
- J(n,w): the vertices are the w-subsets of [n]. The Johnson distance is x(u,v) = w - |u∩v| = Hamming distance / 2.
- The valency is v_x = C(w,x)C(n-w,x). The eigenspace V_k has dimension m_k = C(n,k) - C(n,k-1).
- Eigenvalue of A_x on V_k (Eberlein): P_x(k) = sum_j (-1)^j C(k,j) C(w-k,x-j) C(n-w-k,x-j).
- Dual eigenvalue: Q_k(x) = m_k P_x(k) / v_x. Dual-Hahn closed form: Q_k(x) = m_k sum_j (-1)^j C(k,j)C(n+1-k,j)C(x,j)/(C(w,j)C(n-w,j)).
- E_k = (1/N) sum_x Q_k(x) A_x. Delsarte: sum_x a_x Q_k(x) = (N/|C|) 1_C^T E_k 1_C >= 0, where a_x = #{(u,v) in C^2 : x(u,v)=x}/|C|.

## 1. Calibration by brute force (johnson.py)
I built every A_x and E_k as exact matrices and checked that E_k^2 = E_k, E_kE_l = 0, sum E_k = I, tr E_k = m_k, and A_1E_k = P_1(k)E_k. I also checked that the Eberlein and Hahn forms of Q are equal, and that random subsets satisfy the Delsarte inequalities.
```
calibrated J(8,3): N=56, E_k idempotent/orthogonal/sum=I/trace=m_k, A_1 E_k = P_1(k) E_k, Eberlein==Hahn, 30 random subsets Delsarte>=0 (min 7/55)
calibrated J(9,4): N=126, E_k idempotent/orthogonal/sum=I/trace=m_k, A_1 E_k = P_1(k) E_k, Eberlein==Hahn, 30 random subsets Delsarte>=0 (min 0)
calibrated J(7,2): N=21, E_k idempotent/orthogonal/sum=I/trace=m_k, A_1 E_k = P_1(k) E_k, Eberlein==Hahn, 30 random subsets Delsarte>=0 (min 0)
```

## 2. Counting inequality R7, re-derived
Fix c in C. Take a codeword v at Johnson distance 7 from c. It is fixed by S = c \ v (a 7-subset of c, so there are C(8,7) = 8 choices) and by T = v \ c (a 7-subset of the 26 coordinates outside c).
Two codewords with the same S agree on c\S, so their Hamming distance is |T Δ T'| >= 10. Their T-sets therefore form a (26,10,7) code.
So #{v : x(c,v) = 7} <= 8·A(26,10,7) for every c. Averaging over c gives a_7 <= 8·A(26,10,7) under the 1/|C| normalisation.
With A(26,10,7) <= 36 this is a_7 <= 288. The inequality uses n-w = 26, d = 10 and weight x = 7, so A(26,10,7) is the correct input.
Brute-force spot check of R_x on J(12,4) with d=6 (extra.py):
```
brute force A(8,6,3), A(8,6,4) = {3: 2, 4: 2}
R_x held on 200 random maximal (12,6,4) codes; max a_x seen: {3: 8.0, 4: 1.0} caps: {3: 8, 4: 2}
```

## 3. Certificate rebuilt by my own checker (check_cert.py)
Each row has the form -sum_x Q_k(x) a_x <= Q_k(0) = m_k. The check is: y >= 0, and the column sum is >= 1 for every x = 5..8.
```
cell 34 10 8
D1: stored row == recomputed: True; rhs 33; y=195/1147 (>=0: True)
D2: stored row == recomputed: True; rhs 527; y=91/1147 (>=0: True)
D3: stored row == recomputed: True; rhs 5423; y=819/33263 (>=0: True)
R7: stored row == recomputed: True; rhs 288; y=561/370 (>=0: True)
column x=5: sum_r y_r coeff = 1  (>=1: True)
column x=6: sum_r y_r coeff = 1  (>=1: True)
column x=7: sum_r y_r coeff = 1  (>=1: True)
column x=8: sum_r y_r coeff = 1  (>=1: True)
certified value 1+sum y*rhs = 114444/185 = 618.6162162162162 ; stored: 114444/185 match: True
floor: 618 claimed: 618 match: True
ALL OK
```
I also solved the LP exactly myself, by full vertex enumeration of both the primal and the dual (sanity.py). The primal and dual optima agree, so the certificate is optimal for this constraint set:
```
A(34,10,8) Delsarte+R7 (A(26,10,7)<=36): primal max 1+sum a = 114444/185 (618.6162) ; dual min = 114444/185; floor 618; a*=['49616/185', '5908/185', '288', '1091/37']
A(34,10,8) Delsarte+R5..R8 (A(26,10,5)=5,A(26,10,6)=13,A(26,10,7)<=36,A(26,10,8)<=104): primal max 1+sum a = 114444/185 (618.6162) ; dual min = 114444/185; floor 618; a*=['49616/185', '5908/185', '288', '1091/37']
```

## 4. Table input and target cell (table_snapshot/Andw.html, parsed by extra.py)
sha256 = 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8. This matches REPRODUCE.md and table_record.md. I did not fetch the live page.
```
main table row n=26: {'6': '13', '7': '30-36', '8': '68-104', '9': '91-213', '10': '130-397', '11': '168-565', '12': '208-691', '13': '234-754'}
Values of A(n,10,8) block1: {'29': '91-203', '30': '108-247', '31': '124-322', '32': '145-402', '33': '165-573', '34': '181-637', '35': '210-700', '36': '245-765', '37': '259-832'}
```
The snapshot prints A(26,10,7) as "30-36" and the target cell as "181-637". The certified 618 is below 637 and above the lower bound 181.

## 5. Independent proof of the input bound: partial
- A(24,10,5) <= 4, because the 5-sets must be pairwise disjoint.
- A(25,10,6) <= 10. The 6-sets meet pairwise in at most 1 point, so every point degree is <= 4. Then sum_p C(r_p,2) <= C(M,2). For M = 11 the convexity minimum is 57 > 55, a contradiction. (Plain Delsarte gives only 11.)
- So A(26,10,7) <= floor(26·10/7) = 37. That is the Johnson bound, proved here from first principles.
- I could not prove 36 from first principles. Plain Delsarte for J(26,7) gives 42, adding R5/R6/R7 does not move it, and pair convexity does not exclude M = 37.
- How the result depends on the input:
```
A(34,10,8) Delsarte+R7 with A(26,10,7)<=42: ... floor 662
A(34,10,8) Delsarte+R7 with A(26,10,7)<=37: primal max 1+sum a = 116688/185 (630.7459) ; ... floor 630
A(34,10,8) Delsarte+R7 with A(26,10,7)<=36: primal max 1+sum a = 114444/185 (618.6162) ; ... floor 618
```
So the exact value 618 depends on the printed table value 36. That is the claim's own label: "PROVED-HERE given the published input bound".
Even without that value, my first-principles 37 still gives A(34,10,8) <= 630 < 637, so the improvement over the table holds either way.

## 6. Method sanity checks (sanity.py)
```
A(34,10,8) plain Delsarte: primal max 1+sum a = 23188/35 (662.5143) ; dual min = 23188/35; floor 662
A(24,8,8) plain Delsarte (Steiner S(5,8,24): 759): primal max 1+sum a = 759 (759.0000) ; dual min = 759; floor 759; a*=['280', '0', '448', '0', '30']
A(26,10,8) Delsarte+R7 (A(18,10,7)<=6); table 68-104: ... floor 116   undercuts lower bound? False ; below printed upper? False
A(30,10,8) Delsarte+R7 (A(22,10,7)<=16); table 108-247: ... floor 271   undercuts lower bound? False ; below printed upper? False
A(32,10,8) Delsarte+R7 (A(24,10,7)<=24); table 145-402: ... floor 424   undercuts lower bound? False ; below printed upper? False
A(33,10,8) Delsarte+R7 (A(25,10,7)<=32); table 165-573: ... floor 541   undercuts lower bound? False ; below printed upper? True
A(35,10,8) Delsarte+R7 (A(27,10,7)<=48); table 210-700: ... floor 748   undercuts lower bound? False ; below printed upper? False
A(36,10,8) Delsarte+R7 (A(28,10,7)<=56); table 245-765: ... floor 841   undercuts lower bound? False ; below printed upper? False
```
- The Steiner value 759 comes out exactly.
- Plain Delsarte alone gives 662, which does not beat 637. The R7 row is what produces the improvement.
- No nearby cell falls below its printed lower bound.
- Side observation: the same method also appears to beat the printed upper bound of A(33,10,8), giving 541 against 573. That is not part of this claim.

## 7. Author's verify.py, run after my own checks
```
$ sha256sum table_snapshot/Andw.html
117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8  table_snapshot/Andw.html
$ python3 verify.py cert_A34_10_8.json
selftest: Delsarte inequalities hold on 150 random subsets; P-for-Q control fails; scheme sums zero: OK
  column x=5: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=6: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=7: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=8: sum_r y_r row_r(x) = 1  (needs >= 1)
certified: A(34,10,8) <= 114444/185 = 618.616216, hence A(34,10,8) <= 618
VERIFIED bound 618
exit=0 ; two runs byte-identical (deterministic)
```
verify.py agrees with my checker on every row, every right-hand side, every multiplier and the value. Its Q formula is the dual-Hahn form I calibrated above.
One gap in verify.py: it asserts the floor of the value, but it does not compare against the stored `certified_value` string. My checker does compare them, and they match.

## Verdict
The certificate is exact, uses only valid inequalities (Delsarte D1-D3 and a correctly derived R7), and gives A(34,10,8) <= 114444/185, so A(34,10,8) <= 618. That is strictly below the printed 637 in the snapshot.
The only external input is A(26,10,7) <= 36, which the snapshot prints as "30-36".
I could not independently prove 36; the strongest bound I proved from first principles is 37, which gives <= 630, still below 637.
I did not check the live page or newer arXiv papers for a later bound on this cell.
pass: true
