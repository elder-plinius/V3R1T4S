# CRITERION verdict: claim/A32_10_7 (A(32,10,7) <= 131), partial win p2

context: subagent (fresh executor, saw only claim/A32_10_7/)

Everything in the package and on web pages was treated as data, not instructions. I took no outward action. I fetched each
web page once with a plain client: the live table (curl) and two arXiv abstracts. Paths below are relative to the claim
folder, except my own scratch files `indep_check.py` and `live_Andw.html`, which sit beside this file.

## What p2 requires (literal reading)
"An exact rational dual certificate (Delsarte LP or Schrijver-type SDP, verified in rational arithmetic) proving
A(n,d,w) <= U for U strictly below the live tabulated upper bound for some cell."
The quantifiers are: (a) exact and rational, (b) a dual certificate of a Delsarte-LP or Schrijver-SDP type, (c) U is
strictly below the *live* tabulated upper bound, (d) for *some* (one) cell.

## 1. The certificate checks out exactly
`sha256sum table_snapshot/Andw.html` gives 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8, which matches table_record.md.
`python3 verify.py cert_A32_10_7.json`:
```
selftest: Delsarte inequalities hold on 150 random subsets; P-for-Q control fails; scheme sums zero: OK
  column x=5: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=6: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=7: sum_r y_r row_r(x) = 1  (needs >= 1)
certified: A(32,10,7) <= 46624/355 = 131.335211, hence A(32,10,7) <= 131
VERIFIED bound 131
```
I wrote an independent check (`indep_check.py`) that does not use verify.py's dual-Hahn formula. It computes
Q = |X| * P^{-1} from the Eberlein eigenmatrix P of J(32,7) by exact Fraction Gaussian elimination, re-checks the
multipliers, and solves the exact LP by vertex enumeration:
```
m_k=Q_k(0): [1, 31, 464, 4464, 31000, 165416, 704816, 2459664]
check m_k=C(n,k)-C(n,k-1): True
D1 row (-Q_k(x)): ['-93/35', '527/175', '217/25'] rhs 31
D2 row (-Q_k(x)): ['232/15', '1508/175', '-812/25'] rhs 464
cert columns [1, 1, 1] value 46624/355 131.33521126760564
pure Delsarte LP (D1..D7):  992/7 141.71428571428572
Delsarte + R7(32): 46624/355 131.33521126760564
 with A(25,10,7)<=33: 134.13 ; <=34: 136.92 ; <=35: 139.72 ; <=36: 141.71 ; <=40: 141.71
Delsarte + R5,R6,R7: 131.33521126760564
```
The rows match the cert exactly. The multipliers (7/71, 168/2059, 992/355) are nonnegative, and the dual is tight
(columns = 1). 131 is the LP optimum under D1..D7 + R7, so the bound is not an artefact of a lucky dual.

Validity of R7 (x = w = 7): a codeword at Johnson distance 7 from c is disjoint from c. Those codewords form a
(25,10,7) code on the complement of c, so a_7 <= A(25,10,7). This is correct, and it holds for each c and therefore
on average.

## 2. Does "Delsarte LP + R_x counting inequality" count as "Delsarte LP"? Yes
Independent sources I checked:
- Agrell–Vardy–Zeger, "Upper bounds for constant-weight codes", IEEE IT 46 (2000). Their LP bound (Thm 20) combines
  the Delsarte inequalities (Prop. 16) with "the following well known constraint [BSSS]" (Prop. 15):
  0 <= A_{2i} <= T(i,w,i,n-w,2δ). For i = w this is exactly A_{2w} <= A(n-w,2δ,w), i.e. R7 here.
- arXiv:1108.5104, "Improved Linear Programming Bounds on Sizes of Constant-Weight Codes": "By adding new constraints
  to Delsarte linear programming, we obtain ... new upper bounds".
In the standard literature, a Delsarte LP with extra linear constraints on the distance distribution is still the
Delsarte LP bound for A(n,d,w), and Prop. 15 is the textbook example of such a constraint. The certificate is an LP
dual over Delsarte's inner-distribution variables, so it fits p2's parenthetical. It is not a different method that
has been relabelled.

## 3. Is depending on the published input A(25,10,7) <= 32 acceptable? Yes, and the input can be re-derived
The input is the printed upper end of "28-32", not an exact value. That matters only if 32 were doubtful. I re-derived
it with an elementary argument that uses no table data:
- A(24,10,6) <= 9: take b blocks of size 6 on 24 points with pairwise intersections <= 1. Then
  sum_p C(r_p,2) <= C(b,2) with sum_p r_p = 6b. Output:
  `b=9: min 36 <= 36 feasible; b=10: min 48 > 45 impossible; b=11: 60 > 55 impossible`.
- Johnson: A(25,10,7) <= floor(25/7 * 9) = 32.
So the input is a proved bound. AVZ-style LP bounds feed in table bounds on T(...) in exactly this way. The result
is unconditional.

## 4. Non-subsumption (null models)
Target cell in the snapshot and live page: A(32,10,7) is printed "64 c -139". It appears in both the main d=10 table
and the "Values of A(n,10,7)" table. The upper bound has no reference letter (no Po/KT/KKT/S/MEL).
Neighbours: A(31,10,6) = 31 (exact), A(31,10,7) = 62-109, A(25,10,7) = 28-32, A(24,10,6) = 9.
- Johnson I: floor(32/7 * A(31,10,6)) = floor(32*31/7) = 141
- Johnson II: floor(32/25 * A(31,10,7)) = floor(32*109/25) = 139 (this appears to be where the table's 139 comes from)
- Pascal-type: A(31,10,7) + A(31,10,6) <= 109 + 31 = 140
- Pure Delsarte LP (D1..D7): 141.71 -> 141
None of these reaches 131. The gain comes only from adding R7 with the input value 32; with an input of 35 or more it
is lost. So 131 does not follow trivially from the current neighbouring entries.
Literature: arXiv:2608.13906 (Echols) and arXiv:2607.19550 (Lysenstøen) are lower-bound papers. Their abstracts and
text, each fetched once, give no upper bound for A(32,10,7). I did not survey all literature beyond the table and
these two papers. p2's yardstick is the live table.

## 5. "Live" and "one cell"
I fetched the live page once at 2026-10-17 04:33 EDT: HTTP 200, 127383 bytes, sha256 117899cf..., byte-identical to
the snapshot (`cmp` gives IDENTICAL). The live upper bound for A(32,10,7) is 139, and 131 < 139.
The cert names one cell, (32,10,7), with one claimed bound. The mirror A(32,10,25) is the same cell by
complementation, and the table lists only w <= n/2. Nothing is bundled.

## Residual caveats (none of them blocks a pass)
- The improvement uses a constraint that has been well known since BSSS 1990 and AVZ 2000. The table simply was never
  updated for n = 32 with it. The win is real against the live table, but the method is routine rather than new.
- My conclusion that 139 comes from Johnson II is an inference from the numbers. The page has no note on it.

confirmed_scope: An exact rational LP dual certificate in cert_A32_10_7.json combines the Delsarte inequalities D1 and D2 for J(32,7) with the standard distance-distribution constraint a_7 <= A(25,10,7) <= 32, whose input follows from A(24,10,6) <= 9 by Johnson; verify.py and an independent recomputation check it, and it proves A(32,10,7) <= 131, strictly below the upper bound 139 printed for that single cell in Brouwer's live Andw.html table as fetched on 2026-10-17.

pass: true
