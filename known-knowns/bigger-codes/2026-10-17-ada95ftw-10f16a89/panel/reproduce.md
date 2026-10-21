# REPRODUCE verdict: A(32,10,7) <= 131

context: subagent (fresh executor, saw only claim/A32_10_7/)

All file names are relative to the claim folder (claim/A32_10_7/). My own scripts are in ../mine/ (jq.py, calib.py, lp.py, check_cert.py, table.py, sanity.py, input_check.py). I wrote and ran them **before** I opened verify.py.

## Definition I used (quoted from CLAIM.md, then my own formalisation)
> "Inner distribution a_x = (1/|C|) #{(u,v) in C x C : x(u,v) = x}: a_0 = 1, a_x = 0 for 0 < x < delta, a_x >= 0, |C| = 1 + sum_{x = delta..w} a_x.
> 1. Delsarte (1973): sum_x a_x Q_k(x) >= 0 for k = 1..w, Q_k the dual eigenvalues of the Johnson scheme J(32,7).
> 2. R_x: a_x <= C(w,x) * A(n-w,d,x). ...
> 3. With nonnegative multipliers y_r (cert) such that sum_r y_r row_r(x) >= 1 for every x = delta..w, |C| <= 1 + sum_r y_r rhs_r = 46624/355."

My formalisation (../mine/jq.py): E_k is the primitive idempotent of J(n,w) for the eigenvalue theta_k=(w-k)(n-w-k)-k of A_1, and Q_k(x) = |X|·E_k(u,v) for x(u,v)=x. The closed form I implemented is Eberlein: Q_k(x) = m_k·P_x(k)/v_x, with P_x(k)=sum_j (-1)^j C(k,j)C(w-k,x-j)C(n-w-k,x-j), m_k=C(n,k)-C(n,k-1), v_x=C(w,x)C(n-w,x). The brute-force calibration builds E_k = prod_{j!=k}(A_1-theta_j)/(theta_k-theta_j) exactly in Fractions on the whole scheme.

## 1. Calibrating Q by brute force (../mine/calib.py)
```
J(8,3) brute-force idempotent Q == Eberlein closed form: True
  k=0 ['1', '1', '1', '1']
  k=1 ['7', '49/15', '-7/15', '-21/5']
  k=2 ['20', '4/3', '-10/3', '6']
  k=3 ['28', '-28/5', '14/5', '-14/5']
J(9,4) brute-force idempotent Q == Eberlein closed form: True
J(10,4) brute-force idempotent Q == Eberlein closed form: True
P_x(k) used as Q_k(x) matches? False
```

## 2. Rebuilding every certificate row and checking the dual (../mine/check_cert.py)
```
D1: my row ['-93/35', '527/175', '217/25'] rhs 31 | cert row ['-93/35', '527/175', '217/25'] rhs 31 | match=True dual=7/71 y>=0:True
D2: my row ['232/15', '1508/175', '-812/25'] rhs 464 | cert row ['232/15', '1508/175', '-812/25'] rhs 464 | match=True dual=168/2059 y>=0:True
R7: my row ['0', '0', '1'] rhs 32 | cert row ['0', '0', '1'] rhs 32 | match=True dual=992/355 y>=0:True
column x=5: sum_r y_r row_r(x) = 1  >=1: True
column x=6: sum_r y_r row_r(x) = 1  >=1: True
column x=7: sum_r y_r row_r(x) = 1  >=1: True
1 + sum y_r rhs_r = 46624/355 = 131.33521126760564 | cert certified_value 46624/355 equal: True
floor: 131 ALL OK: True
primal LP {D1,D2,R7}: 46624/355
pure Delsarte D1..D7: 992/7 141.71428571428572 a= ['105', '0', '250/7']
Delsarte D1..D7 + R7: 46624/355 131.33521126760564 a= ['33999/355', '182/71', '32']
all Q_k(x), k=1..7, x=0,5,6,7:
 k=1 ['31', '93/35', '-527/175', '-217/25']
 k=2 ['464', '-232/15', '-1508/175', '812/25']
 k=3 ['4464', '-2232/115', '45756/805', '-7812/115']
 k=4 ['31000', '815300/5313', '-207700/1771', '21700/253']
 k=5 ['165416', '-97092/385', '46748/385', '-3596/55']
 k=6 ['704816', '222952/1265', '-406348/6325', '176204/6325']
 k=7 ['2459664', '-409944/8855', '614916/44275', '-32364/6325']
```
I solved the primal LP exactly by vertex enumeration in Fractions (../mine/lp.py). With all of D1..D7 plus R7, the optimum is 46624/355. That equals the dual value, so the certificate is optimal and adding D3..D7 does not help. The primal optimum is a_5=33999/355, a_6=182/71, a_7=32.

## 3. Re-deriving the proof steps
- **Delsarte:** with Q_k(x)=|X|E_k(u,v), sum_x a_x Q_k(x) = (|X|/|C|)·chi_C^T E_k chi_C >= 0 because E_k is PSD. The normalisation matches a_0=1. The rows are written as -sum_{x>=5} Q_k(x)a_x <= Q_k(0)=m_k, and Q_1(0)=31 and Q_2(0)=464 match the cert's rhs values.
- **R_x (proved):** fix c in C and let N_x(c) be the number of v in C with |c\v|=x. Such a v equals (c\S) ∪ T, where S is an x-subset of c and T is an x-subset of the n-w outside coordinates. If v and v' share the same S, then d_H(v,v')=|T Δ T'| >= d. So for each S the T's form an (n-w,d,x) constant-weight code, which gives N_x(c) <= C(w,x)·A(n-w,d,x). Averaging over c: a_x = (1/|C|)·sum_c N_x(c) <= C(w,x)A(n-w,d,x), so the normalisation is correct. For x=w=7, this just says the codewords disjoint from c form a (25,10,7) code, so a_7 <= A(25,10,7).
- **Weak duality:** for any feasible a >= 0, |C| = 1+sum_x a_x <= 1+sum_x a_x·sum_r y_r row_r(x) = 1+sum_r y_r(row_r·a) <= 1+sum_r y_r rhs_r. This uses y >= 0 and column sums >= 1. All three hold exactly (section 2).

## 4. The table input and the target cell in table_snapshot/Andw.html (../mine/table.py parses the d=10 main table)
```
117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8  table_snapshot/Andw.html
d=10 header w: [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
A(25, 10, 7) printed: '28-32'
A(32, 10, 7) printed: '64-139'
```
Raw HTML for row 25, w=7: `<td><a href="cwc/d10/i25.7">28</a><sup>c</sup>-32</td>`. The secondary table "Values of A(n,10,7)", column 32, prints `<a href="cwc/d10/i32.7">64</a><sup>c</sup>-139</td>`. The hash matches REPRODUCE.md and table_record.md.

**Caveat resolved: the input does not rest on the table alone.** I proved A(25,10,7) <= 32 myself (../mine/input_check.py). For A(24,10,6), weight 6 at distance >= 10 means blocks meet in at most 1 point, so sum C(r_p,2) <= C(b,2). After that comes the Johnson bound A(25,10,7) <= floor(25/7·A(24,10,6)).
```
b=8: min sum C(r_p,2)=24, C(b,2)=28, feasible=True
b=9: min sum C(r_p,2)=36, C(b,2)=36, feasible=True
b=10: min sum C(r_p,2)=48, C(b,2)=45, feasible=False
b=11: min sum C(r_p,2)=60, C(b,2)=55, feasible=False
A(25,10,7) <= floor(25*9/7) = 32
table A(24,10,6) printed: '9'
```
That gives A(24,10,6) <= 9, which agrees with the table's "9", and hence A(25,10,7) <= 32. The bound 131 is therefore unconditional.

## 5. LP sanity checks (../mine/sanity.py)
```
A(24,8,8)=759 [S(5,8,24)]: pure Delsarte = 759 (759.000); Delsarte+R[4, 6, 8] = 759 (759.000) -> floor 759
   undercuts 759? False
A(23,8,7)=253 [S(4,7,23)]: pure Delsarte = 253 (253.000); Delsarte+R[4, 5, 6, 7] = 253 (253.000) -> floor 253
   undercuts 253? False
d=10,w=7 cells, R5 (A(m,10,5)=floor(m/5)), R6/R7 from table where printed:
  A(19,10,7) table '8': pure Delsarte = 95/11 (8.636); Delsarte+R[5, 6] = 95/11 (8.636) -> floor 8
     below table lower bound? False; below table upper? False
  A(20,10,7) table '10': pure Delsarte = 100/9 (11.111); Delsarte+R[5, 6] = 100/9 (11.111) -> floor 11
     below table lower bound? False; below table upper? False
  A(21,10,7) table '13': pure Delsarte = 15 (15.000); Delsarte+R[5, 6, 7] = 15 (15.000) -> floor 15
     below table lower bound? False; below table upper? False
  A(22,10,7) table '16': pure Delsarte = 22 (22.000); Delsarte+R[5, 6, 7] = 22 (22.000) -> floor 22
     below table lower bound? False; below table upper? False
  A(23,10,7) table '20': pure Delsarte = 1265/49 (25.816); Delsarte+R[5, 6, 7] = 1265/49 (25.816) -> floor 25
     below table lower bound? False; below table upper? False
  A(24,10,7) table '24': pure Delsarte = 2760/91 (30.330); Delsarte+R[5, 6, 7] = 2760/91 (30.330) -> floor 30
     below table lower bound? False; below table upper? False
  A(25,10,7) table '28-32': pure Delsarte = 250/7 (35.714); Delsarte+R[5, 6, 7] = 250/7 (35.714) -> floor 35
     below table lower bound? False; below table upper? False
  A(26,10,7) table '30-36': pure Delsarte = 3250/77 (42.208); Delsarte+R[5, 6, 7] = 3250/77 (42.208) -> floor 42
     below table lower bound? False; below table upper? False
  A(27,10,7) table '36-48': pure Delsarte = 351/7 (50.143); Delsarte+R[5, 6, 7] = 351/7 (50.143) -> floor 50
     below table lower bound? False; below table upper? False
  A(28,10,7) table '38-56': pure Delsarte = 60 (60.000); Delsarte+R[5, 6, 7] = 60 (60.000) -> floor 60
     below table lower bound? False; below table upper? False
  A(29,10,7) table '42-66': pure Delsarte = 145/2 (72.500); Delsarte+R[5, 6, 7] = 145/2 (72.500) -> floor 72
     below table lower bound? False; below table upper? False
  A(30,10,7) table '48-85': pure Delsarte = 4350/49 (88.776); Delsarte+R[5, 6, 7] = 4350/49 (88.776) -> floor 88
     below table lower bound? False; below table upper? False
  A(31,10,7) table '62-109': pure Delsarte = 775/7 (110.714); Delsarte+R[5, 6, 7] = 2015/19 (106.053) -> floor 106
     below table lower bound? False; below table upper? True
  A(32,10,7) table '64-139': pure Delsarte = 992/7 (141.714); Delsarte+R[5, 6, 7] = 46624/355 (131.335) -> floor 131
     below table lower bound? False; below table upper? True
```
- The pure Delsarte LP for the target is 992/7 = 141.71. That is above the table's 139, so it is consistent with the table and does not beat it on its own.
- On the Steiner systems S(5,8,24) and S(4,7,23), the method gives exactly 759 and 253. These codes meet every R-row with equality, so the R-rows are valid and tight there.
- Across all 14 cells A(n,10,7), n=19..32, the method never falls below a printed lower bound.
- Side observation, not part of this claim: the same rows give A(31,10,7) <= 106, which is below the table's 109.

## 6. Author's verify.py, run only after all of the above
```
117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8  table_snapshot/Andw.html
selftest: Delsarte inequalities hold on 150 random subsets; P-for-Q control fails; scheme sums zero: OK
  column x=5: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=6: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=7: sum_r y_r row_r(x) = 1  (needs >= 1)
certified: A(32,10,7) <= 46624/355 = 131.335211, hence A(32,10,7) <= 131
VERIFIED bound 131
exit=0
```
Comparing verify.py's dual-Hahn Q with my Eberlein Q:
```
author dual-Hahn Q == my Eberlein Q on all k,x of J(32,7): True
... and on J(31,7), J(25,7), J(24,8): True
```
Determinism: two runs of each script gave identical output hashes. verify.py gave d03c288d…aad208 both times, and ../mine/check_cert.py gave 34d81095…31140e both times. Everything is exact rational arithmetic; the only randomness is verify.py's self-test, which uses a fixed seed.

Note: verify.py takes the table value from the cert's `table_inputs` field and does not parse the snapshot itself. I checked the snapshot independently (section 4).

## Verdict
- All three certificate rows match my independently computed Delsarte and R rows exactly.
- All multipliers are >= 0, and every column sum for x=5,6,7 is exactly 1.
- The certified value is 46624/355 = 131.335, so A(32,10,7) <= 131. That is strictly below the printed 139 and above the printed lower bound 64.
- The R_x inequality is proved, with the correct normalisation.
- The input A(25,10,7) <= 32 is what the snapshot prints, and I re-proved it independently.
- verify.py agrees with all of the above.

I did not do a literature search for an existing bound below 139 elsewhere (e.g. in SDP papers); that was outside this role.

pass: true
