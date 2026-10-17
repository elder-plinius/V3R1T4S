# REPRODUCE verdict: claim A(31,10,7) <= 106

context: subagent (fresh executor, saw only claim/A31_10_7/)

Scope: I read only claim/A31_10_7/ (CLAIM.md, REPRODUCE.md, table_record.md, cert_A31_10_7.json, table_snapshot/Andw.html) and wrote my own checker in mine/ (sibling of claim/) **before** opening verify.py. I made one web request: a plain curl for the AVZ PDF linked from the snapshot. It timed out (HTTP 000, 0 bytes) and I did not retry. I took no outward action.

## 1. Definition used for my own checker (mine/johnson.py)
"Johnson scheme J(n,w): vertices are the w-subsets of [n]; relation x is |u \ v| = x. P_k(x) = E_k(x) = sum_j (-1)^j C(x,j) C(w-x,k-j) C(n-w-x,k-j) (Eberlein). Dual eigenvalues: Q_k(x) = m_k * P_x(k) / v_x, where m_k = C(n,k)-C(n,k-1) and v_x = C(w,x)C(n-w,x). Delsarte: sum_x a_x Q_k(x) >= 0."
Brute-force calibration (mine/calib.py): I built the primitive idempotents E_k numerically from inclusion-matrix projections and compared |X|*E_k[u,v] with Q_k(dist):
```
calib J(7,3) max|N*E_k - Q_k| = 1.70e-14
calib J(8,3) max|N*E_k - Q_k| = 1.87e-14
calib J(8,4) max|N*E_k - Q_k| = 6.51e-14
calib J(9,4) max|N*E_k - Q_k| = 1.21e-13
calib J(10,3) max|N*E_k - Q_k| = 2.84e-14
calib J(10,5) max|N*E_k - Q_k| = 5.12e-13
Delsarte with Q holds on 600 random codes; P-in-place-of-Q violations: 24
```

## 2. Rebuilding the certificate from my own Q (mine/rebuild.py, exact Fractions)
```
Q_k(0)=m_k: [1, 30, 434, 4030, 26970, 138446, 566370, 1893294]
D1 stored==rebuilt: True y= 196/1653 y>=0: True rhs= 30
D2 stored==rebuilt: True y= 46/551 y>=0: True rhs= 434
R7 stored==rebuilt: True y= 155/57 y>=0: True rhs= 24
column x=5 sum = 1 >=1: True
column x=6 sum = 1 >=1: True
column x=7 sum = 1 >=1: True
1+sum y*rhs = 2015/19 = 106.05263157894737 matches claim 2015/19: True
ALL OK: True
```
Duality step (re-derived): a_x >= 0, y >= 0 and column sums >= 1 give sum_x a_x <= sum_r y_r (row_r . a) <= sum_r y_r rhs_r. So |C| <= 1 + 2015/19, which gives |C| <= 106.

## 3. The R_x inequality (re-derived)
Fix c in C. A codeword v at Johnson distance x from c is fixed by R = c\v (an x-subset of c) and S = v\c (an x-subset of the n-w points outside c). Take two such words with the same R. They share c\R, so they intersect in (w-x)+|S∩S'|, and their Hamming distance is 2(x-|S∩S'|) = d_H(S,S'). That is at least d, so for each R the S-sets form an (n-w,d,x) code. Hence the count is at most C(w,x)·A(n-w,d,x) for every c, and the average a_x obeys the same bound. For x = w = 7 and n-w = 24, the codewords disjoint from c form a (24,10,7) code, so a_7 <= A(24,10,7). This is correct.

## 4. Exact LP (my own vertex enumeration, mine/lp.py) and sensitivity to the input
```
plain Delsarte A(31,10,7): 775/7 = 110.7143   (does NOT beat 109 alone)
Delsarte + a7<=23: 310/3 = 103.3333 floor=103
Delsarte + a7<=24: 2015/19 = 106.0526 floor=106
Delsarte + a7<=25: 6200/57 = 108.7719 floor=108
Delsarte + a7<=26: 775/7 = 110.7143 floor=110
Delsarte + a7<=24, a5<=84, a6<=63: 2015/19   (extra R5/R6 rows do not help)
```
In the active range the bound is 2015/19 + (t-24)·155/57. It is below 109 iff t < 25.08. **The largest input that still gives a bound <= 108 is A(24,10,7) <= 25.** The printed 109 is the Johnson bound floor(31·85/24) = 109 (the other Johnson form gives floor(31·25/7) = 110), consistent with the legend "For n > 28 unmarked upper bounds are from the Johnson bound".

## 5. The key input A(24,10,7): how it is printed, and what I could prove myself
- sha256 of table_snapshot/Andw.html = 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8 (matches table_record.md).
- Raw HTML of the cell: `<th>24</th><td>9</td> <td><a href="cwc/d10/i24.7">24</a><sup>c</sup></td>`. It is a single value "24" with mark c and no range. The target cell is `62 c -109`.
- Legend: the d=4 section says "For now, lower bounds only. Optimum values are indicated by a dot." The page gives no explicit legend for single values in d>=6. "Unmarked upper bounds (for n <= 28) are taken from AVZ" (Agrell–Vardy–Zeger 2000).
- Internal evidence that a single value in the d=10 main table means lower = upper:
  (a) The cell A(21,10,8) is printed as the single value "21 c" (no dot). The page's note says "[BSSS] showed A(21,10,8) ≥ 21, but the period indicating equality may have been a mistake. However, equality follows from [AVZ] (26)". So the single value encodes equality.
  (b) The table's own upper bound A(25,10,8) <= 75 (cell "51-75", unmarked so from AVZ) equals floor(25·A(24,10,7)/8) with A(24,10,7) = 24. Nothing else I computed gives 75: plain Delsarte gives 8625/91 = 94.78, the other Johnson form gives floor(25·60/17) = 88, and A(24,10,7) <= 27 would give 84. So the table itself uses A(24,10,7) <= 24 as an upper bound.
  (c) Spot checks of other single-valued cells (d=16, n=29: 6, 9, 10) match the Johnson/Plotkin bound δn/(w²-wn+δn) exactly. They are exact values.
- My own first-principles attempt (mine/firstprinciples.py, mine/lp2.py):
```
A(23,10,6) <=  8  (convexity: b=9 needs sum C(r,2) >= 39 > C(9,2)=36)
A(17,10,6) <=  3 ; A(17,10,7) <= 5 ; A(17,10,5) <= 17//5 = 3
Johnson part 1: A(24,10,7) <= floor(24*8/7) = 27 ; part 2 with A(23,10,7)=20 (table): 28
LP max 1+sum a with all linear constraints: 192/7 27.43   (Delsarte J(24,7) + R_x from the A(17,10,x) bounds + point-degree 2a5+a6<=49 + outside-incidence 5a5+6a6+7a7<=136)
M=24..27 feasible with integer-rounded second moments; M=28 infeasible
```
  I also derived a structural lemma: a degree-8 point has a near-design derived structure, with λ_pq >= 1 for all q and at most one q with λ_pq = 1. For a disjoint pair B, B' this gives sum_{p∈B} T(p) <= 2e_2(B') <= R_B' - 7 - e_1(B'), where T(p) counts the blocks through p other than B that meet B' in 2 points and e_i(B') counts the blocks meeting B' in exactly i points. This did not close the gap.
  **My best self-proved bound is A(24,10,7) <= 27. That is not enough: the claim needs <= 25.** The claim therefore rests on the published AVZ value A(24,10,7) <= 24. I could not read AVZ itself: the single fetch timed out.

## 6. Author's verify.py (run only after the above)
```
$ python3 verify.py cert_A31_10_7.json   (run twice; outputs byte-identical, exit 0 both times)
selftest: Delsarte inequalities hold on 150 random subsets; P-for-Q control fails; scheme sums zero: OK
  column x=5: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=6: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=7: sum_r y_r row_r(x) = 1  (needs >= 1)
certified: A(31,10,7) <= 2015/19 = 106.052632, hence A(31,10,7) <= 106
VERIFIED bound 106
author dual-Hahn Q == my Eberlein-derived Q on J(31,7), all k,x: True   (also J(24,7): True)
```
verify.py uses the dual-Hahn closed form. On every (k,x) it agrees exactly with my independently calibrated Eberlein-based Q. Its self-test uses a fixed seed, so it is deterministic.

## 7. Sanity checks
- Plain Delsarte alone gives 110.71, so the improvement comes only from the R7 row with the table input.
- No undercutting of printed lower bounds: A(31,10,7) lower bound 62 <= 106. Cells bounded above by A(31,10,7): A(30,10,7) >= 48, A(30,10,6) = 25, A(31,10,6) = 31, A(32,12,8) >= 36, A(33,12,8) >= 36 (Honkala, A(n-2,d-2,w-1) >= A(n,d,w)). Johnson consequences: A(32,10,8) <= 4·106 = 424 >= 145 and A(32,10,7) <= floor(32·106/25) = 135 >= 64. All consistent.
- The mirror cell A(31,10,24) = A(31,10,7) by complementation.

## Verdict
Every certificate row, multiplier, column sum and the value 2015/19 is reproduced exactly from my own definition-level checker, and the R_x inequality and the duality step are re-derived. The single external input A(24,10,7) <= 24 is the published AVZ upper bound. The snapshot's own conventions show that the single printed "24" is an exact value: the A(21,10,8) equality note, and the table's own bound A(25,10,8) <= 75 = floor(25·24/8). The claim is honestly labelled as conditional on that input. Caveat: I could not prove A(24,10,7) <= 25 from first principles (I reached 27), and I could not read AVZ directly. If the published value were wrong by 2 or more, the claim would fail; an error of 1 (A(24,10,7) <= 25) still gives 108 < 109.
pass: true
