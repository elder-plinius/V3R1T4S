# REPRODUCE verdict: A(33,10,7) <= 145

context: subagent (fresh executor, saw only claim/A33_10_7/)

Role: REPRODUCE. I worked only in this folder. My own code is in `mine/` (sibling of `claim/`). I wrote it from the
definitions before opening `claim/A33_10_7/verify.py`. Paths below are relative to the claim folder
(`claim/A33_10_7/`), except `mine/...`, which is my scratch code next to it.

## Definitions I used (quoted / stated)
- Johnson scheme J(n,w): vertices are the w-subsets of an n-set. Relation x means |u \ v| = x (Hamming distance 2x).
  Eigenvalues (Eberlein): P_x(k) = sum_j (-1)^j C(k,j) C(w-k,x-j) C(n-w-k,x-j). Valency v_x = C(w,x)C(n-w,x),
  multiplicity m_k = C(n,k)-C(n,k-1). Dual eigenvalues come from the standard orthogonality relation
  Q_k(x)/m_k = P_x(k)/v_x.
- Delsarte (1973), as CLAIM.md states it: "sum_x a_x Q_k(x) >= 0 for k = 1..w", with the inner distribution
  "a_x = (1/|C|) #{(u,v) in C x C : x(u,v) = x}: a_0 = 1, a_x = 0 for 0 < x < delta ... |C| = 1 + sum a_x".
  Every column of my Q matched an independent brute-force computation (below), so the formula is not taken on trust.

## 1. Brute-force calibration of Q (`mine/jq.py`)
I built the distance-1 adjacency matrix of J(n,w). I took its w+1 distinct integer eigenvalues (found numerically,
then rounded and checked) and formed the exact primitive idempotents E_k = prod_(j!=k) (A1 - th_j)/(th_k - th_j)
in integer/Fraction arithmetic. Then Q_k(x) = |X| * E_k[u0,v] for v at distance x. I checked that this value is
the same for every v at distance x, and that it equals the formula for every k and x.
```
calibrated Q formula vs brute-force idempotents of J(8,3): OK; random subsets aQ>=0 OK; P-in-place-of-Q violations on random small subsets: 323
calibrated Q formula vs brute-force idempotents of J(9,4): OK; random subsets aQ>=0 OK; P-in-place-of-Q violations on random small subsets: 404
calibrated Q formula vs brute-force idempotents of J(10,3): OK; random subsets aQ>=0 OK; P-in-place-of-Q violations on random small subsets: 320
calibrated Q formula vs brute-force idempotents of J(7,2): OK; random subsets aQ>=0 OK; P-in-place-of-Q violations on random small subsets: 318
```
I also cross-checked the author's dual-Hahn `Q` in verify.py against mine on J(33,7), J(26,7), J(24,8), J(8,3)
and J(9,4): 0 mismatches.

## 2. Re-derivation of R_x (normalisation included)
a_x = (1/|C|) sum_(c in C) N_x(c), where N_x(c) = #{v in C : |c \ v| = x}. Fix c. A codeword v with
|c \ v| = x is fixed by R = c \ v (an x-subset of c, C(w,x) choices) and S = v \ c (an x-subset of the n-w
points outside c). For two codewords with the same R, the Hamming distance equals d_H(S,S') as weight-x words of
length n-w, so it is >= d. So each R allows at most A(n-w,d,x) codewords, N_x(c) <= C(w,x) A(n-w,d,x), and so does
the average a_x. With x = w = 7 and n-w = 26 this gives a_7 <= 1*A(26,10,7). Correct.

## 3. Rebuilding every certificate row (`mine/cert_check.py`, exact Fractions)
```
D1: stored coeffs ['-272/91', '256/91', '112/13'] rhs 32 | rebuilt ['-272/91', '256/91', '112/13'] rhs 32 | match=True | y=91/1147 y>=0:True
D2: stored coeffs ['1419/91', '891/91', '-2079/65'] rhs 495 | rebuilt ['1419/91', '891/91', '-2079/65'] rhs 495 | match=True | y=91/1147 y>=0:True
R7: stored coeffs ['0', '0', '1'] rhs 36 | rebuilt ['0', '0', '1'] rhs 36 | match=True | y=528/185 y>=0:True
column x=5: sum_r y_r row_r(x) = 1  >=1: True
column x=6: sum_r y_r row_r(x) = 1  >=1: True
column x=7: sum_r y_r row_r(x) = 1  >=1: True
certified value 1+sum y_r rhs_r = 26928/185 = 145.55675675675676 | stored 26928/185 match: True
floor = 145 claimed 145
ALL CHECKS: PASS
```
All 3 rows (D1, D2, R7) match my rebuild exactly, all multipliers are >= 0, and every column x = 5, 6, 7 sums to
exactly 1. The value is 1 + sum y_r rhs_r = 26928/185 = 145.5568, so the bound is 145.

## 4. LP sanity (own exact vertex-enumeration LP, with a trivial box a_x <= v_x to keep it bounded)
```
== target cell ==
plain Delsarte: A(33,10,7) <= 5456/35 = 155.885714 -> 155; tight ['D1', 'D2', 'D3']; a=['546/5', '91/15', '832/21']
Delsarte + R7(A(26,10,7)<=36): A(33,10,7) <= 26928/185 = 145.556757 -> 145; tight ['D1', 'D2', 'R7']; a=['18606/185', '1477/185', '36']
Delsarte + R5,R6,R7 (A(26,10,5)=5, A(26,10,6)<=13 table, A(26,10,7)<=36): A(33,10,7) <= 26928/185 = 145.556757 -> 145; tight ['D1', 'D2', 'R7']; a=['18606/185', '1477/185', '36']
== Steiner sanity ==
plain Delsarte (S(5,8,24)): A(24,8,8) <= 759 = 759.000000 -> 759; tight ['D1', 'D2', 'D3', 'D4', 'D5']; a=['280', '0', '448', '0', '30']
plain Delsarte (S(3,4,8)): A(8,4,4) <= 14 = 14.000000 -> 14; tight ['D1', 'D2', 'D3']; a=['12', '0', '1']
plain Delsarte (S(5,6,12)): A(12,4,6) <= 132 = 132.000000 -> 132; tight ['D1', 'D2', 'D3', 'D4', 'D5']; a=['45', '40', '45', '0', '1']
```
- Plain Delsarte gives 155. Adding R7 brings the LP optimum to exactly 26928/185, so the certificate is optimal
  for this LP. Adding R5 and R6 changes nothing.
- The method reproduces exact Steiner values: A(24,8,8) = 759 with inner distribution (280,0,448,0,30), the
  octad intersection numbers. It also gives A(8,4,4) = 14 and A(12,4,6) = 132.

## 5. Table cells (snapshot and live)
- `sha256sum table_snapshot/Andw.html` = 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8 (matches REPRODUCE.md).
- Snapshot, section "Bounds on A(n,10,w)", row 26, column w=7: `<a href="cwc/d10/i26.7">30</a><sup>c</sup></span>-36`, which reads "30-36".
- Snapshot, "Values of A(n,10,7)", n=33: `<a href="cwc/d10/i33.7">72</a><sup>g</sup>-150`, which reads "72-150".
- I fetched the live page once with plain curl on 2026-10-17 at about 04:39 EDT: HTTP 200, 127383 bytes, same
  sha256 as the snapshot. Same two cells. Mirror cell A(33,10,26) = A(33,10,7) by complementation.

## 6. Independent first-principles proof of the input A(26,10,7) <= 36
LP and Johnson alone are too weak (plain Delsarte gives 42; Delsarte + R(A(19,10,x)) also gives 42):
```
== first-principles derivation of A(26,10,7) <= 36 ==
plain Delsarte: A(19,10,6) <= 95/17 = 5.588235 -> 5; tight ['D1', 'nn6']; a=['78/17', '0']
plain Delsarte: A(19,10,7) <= 95/11 = 8.636364 -> 8; tight ['D1', 'nn6', 'nn7']; a=['84/11', '0', '0']
first Johnson bound A(19,10,6) <= floor(95/17) = 5
first Johnson bound A(19,10,7) <= floor(95/11) = 8
inputs used: {(19, 10, 5): 3, (19, 10, 6): 5, (19, 10, 7): 8}
plain Delsarte: A(26,10,7) <= 3250/77 = 42.207792 -> 42; tight ['D1', 'D2', 'nn6']; a=['399/11', '0', '380/77']
Delsarte + R7 only: A(26,10,7) <= 3250/77 = 42.207792 -> 42; tight ['D1', 'D2', 'nn6']; a=['399/11', '0', '380/77']
Delsarte + R5,R6,R7: A(26,10,7) <= 3250/77 = 42.207792 -> 42; tight ['D1', 'D2', 'nn6']; a=['399/11', '0', '380/77']
```
Here is a combinatorial proof. The arithmetic is mechanised in `mine/input_proof.py`, and its convexity helper was
brute-force checked.
- (a) A(25,10,6) <= 10. The blocks are 6-sets meeting pairwise in <= 1 point. Take 11 of them with point degrees
  r_q. Then sum r_q = 66 and sum C(r_q,2) = #(meeting block pairs) <= C(11,2) = 55. But 25 integers summing to 66
  have sum C(r,2) >= 57. Contradiction.
- (b) Johnson's recursion gives A(26,10,7) <= floor(26*10/7) = 37. Suppose there are 37 words (7-sets meeting
  pairwise in <= 2 points). Then sum r_p = 259 with every r_p <= 10, so exactly one point z has degree 9 and the
  rest have degree 10. At a degree-10 point p, the derived code is 10 six-sets on 25 points, so
  sum C(r,2) >= 45 = C(10,2). Equality forces every two blocks to meet, so any two words through p meet in exactly
  2 points. Now take a word B that avoids z (there are 28 of them). Every word meeting B shares a degree-10 point
  of B, so it meets B in exactly 2 points. Then sum_(p in B) (r_p - 1) = 63 = 2*n2(B), which is impossible since
  63 is odd. So A(26,10,7) <= 36.
```
convexity helper brute-force-checked on small cases: OK
A(25,10,6): M=11 needs min sum C(r,2) = 57 <= C(11,2) = 55 -> False
A(26,10,7): M=37 gives sum r_p = 259 over 26 points with r_p <= 10 -> 26*10 - S = 1 point(s) of degree 9, rest degree 10
  derived (25,10,6) code of size 10: min sum C(r,2) = 45 = C(10,2) = 45 -> equality: every two blocks meet, so two words through a degree-10 point meet in exactly 2 points
  a word B avoiding the degree-9 point: sum_{p in B}(r_p-1) = 63 = 2*n2(B) must be even -> False
  words avoiding the degree-9 point: 28 > 0 -> contradiction, so A(26,10,7) <= 36
```
So the one external input is proved here independently, and the bound A(33,10,7) <= 145 holds from first
principles. Sensitivity: an input of 37 would give 148 and 38 would give 151, so the 36 is essential for 145.
```
== sensitivity of target to the input A(26,10,7) ==
Delsarte+R7 input 36: A(33,10,7) <= 26928/185 = 145.556757 -> 145; tight ['D1', 'D2', 'R7']; a=['18606/185', '1477/185', '36']
Delsarte+R7 input 37: A(33,10,7) <= 27456/185 = 148.410811 -> 148; tight ['D1', 'D2', 'R7']; a=['19047/185', '1379/185', '37']
Delsarte+R7 input 38: A(33,10,7) <= 27984/185 = 151.264865 -> 151; tight ['D1', 'D2', 'R7']; a=['19488/185', '1281/185', '38']
Delsarte+R7 input 40: A(33,10,7) <= 5456/35 = 155.885714 -> 155; tight ['D1', 'D2', 'D3']; a=['546/5', '91/15', '832/21']
Delsarte+R7 input 42: A(33,10,7) <= 5456/35 = 155.885714 -> 155; tight ['D1', 'D2', 'D3']; a=['546/5', '91/15', '832/21']
== Johnson-recursion route to the input ==
plain Delsarte: A(25,10,6) <= 125/11 = 11.363636 -> 11; tight ['D1', 'nn6']; a=['114/11', '0']
A(26,10,7) <= floor(26/7 * A(25,10,6)); with table A(25,10,6)=10: 37 ; with A(25,10,6)<=11: 40
A(33,10,7) <= floor(33/7 * A(32,10,6)) with table A(32,10,6)=31: 146
```
Note: the table's own A(32,10,6) = 31 already gives A(33,10,7) <= floor(33*31/7) = 146 by Johnson. The printed 150
is therefore weaker than what other table entries imply. 145 still beats both 150 and that 146.

## 7. Nearby cells: no undercutting of printed lower bounds (`mine/nearby.py`, table inputs)
```
A(21,10,7): printed 13-13; plain Delsarte 15; Delsarte+R(table inputs) 15 
A(22,10,7): printed 16-16; plain Delsarte 22; Delsarte+R(table inputs) 22 
A(23,10,7): printed 20-20; plain Delsarte 25; Delsarte+R(table inputs) 25 
A(24,10,7): printed 24-24; plain Delsarte 30; Delsarte+R(table inputs) 30 
A(25,10,7): printed 28-32; plain Delsarte 35; Delsarte+R(table inputs) 35 
A(26,10,7): printed 30-36; plain Delsarte 42; Delsarte+R(table inputs) 42 
A(27,10,7): printed 36-48; plain Delsarte 50; Delsarte+R(table inputs) 50 
A(28,10,7): printed 38-56; plain Delsarte 60; Delsarte+R(table inputs) 60 
A(29,10,7): printed 42-66; plain Delsarte 72; Delsarte+R(table inputs) 72 
A(30,10,7): printed 48-85; plain Delsarte 88; Delsarte+R(table inputs) 88 
A(31,10,7): printed 62-109; plain Delsarte 110; Delsarte+R(table inputs) 106 below printed upper
A(32,10,7): printed 64-139; plain Delsarte 141; Delsarte+R(table inputs) 131 below printed upper
A(33,10,7): printed 72-150; plain Delsarte 155; Delsarte+R(table inputs) 145 below printed upper
A(34,10,7): printed 85-160; plain Delsarte 170; Delsarte+R(table inputs) 160 
A(35,10,7): printed 102-170; plain Delsarte 187; Delsarte+R(table inputs) 170 
A(36,10,7): printed 116-180; plain Delsarte 204; Delsarte+R(table inputs) 180 
A(37,10,7): printed 134-222; plain Delsarte 222; Delsarte+R(table inputs) 222 
A(26,10,8): printed 68-104; plain Delsarte 116; Delsarte+R(table inputs) 116 
A(27,10,8): printed 76-121; plain Delsarte 142; Delsarte+R(table inputs) 142 
A(28,10,8): printed 85-168; plain Delsarte 175; Delsarte+R(table inputs) 175 
A(29,10,8): printed 96-203; plain Delsarte 217; Delsarte+R(table inputs) 217 
A(30,10,8): printed 108-247; plain Delsarte 271; Delsarte+R(table inputs) 271 
cells undercutting printed lower bounds: 0
```
No cell goes below its printed lower bound. For n = 34, 35, 36 the method gives exactly the printed uppers
160, 170, 180, which is a strong sign it matches how the table was built. It goes below the printed upper only at
n = 31, 32, 33.

## 8. Author's verify.py (run only after all of the above), run twice
```
$ python3 verify.py cert_A33_10_7.json     (exit 0, both runs byte-identical)
selftest: Delsarte inequalities hold on 150 random subsets; P-for-Q control fails; scheme sums zero: OK
  column x=5: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=6: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=7: sum_r y_r row_r(x) = 1  (needs >= 1)
certified: A(33,10,7) <= 26928/185 = 145.556757, hence A(33,10,7) <= 145
VERIFIED bound 145
```
This agrees with my independent result on every row, every column sum and the value 26928/185, and the output is
deterministic.

## Scope / not checked
I did not search arXiv:2608.13906, arXiv:2607.19550 or newer papers for a better upper bound on this cell. That is
a literature/novelty check outside the REPRODUCE role. The claim's mathematics is confirmed.

## Verdict
Confirmed. A(33,10,7) <= 145. I rebuilt every row, checked the multipliers and column sums, recomputed the
certified value 26928/185, matched the input cell to the snapshot and live table, proved the input independently,
and ran verify.py with matching results. There are no mismatches, missing objects or non-determinism.

pass: true
