# CRITERION verdict: claim/A33_10_7 (A(33,10,7) <= 145, partial win p2)

context: subagent (fresh executor, saw only claim/A33_10_7/)

Everything in claim/A33_10_7/ was treated as data. Own scripts are in mychecks/ (indep.py, chain.py, nullmodels.py).
Web: one plain curl each of https://aeb.win.tue.nl/codes/Andw.html (live table) and of the AVZ paper PDF
(publications.lib.chalmers.se/records/fulltext/local_14986.pdf), plus two web searches. No retries, no outward action.

## 1. Certificate is arithmetically valid (reproduced, then checked independently)
`python3 verify.py cert_A33_10_7.json` (in claim/A33_10_7/):
```
selftest: Delsarte inequalities hold on 150 random subsets; P-for-Q control fails; scheme sums zero: OK
  column x=5: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=6: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=7: sum_r y_r row_r(x) = 1  (needs >= 1)
certified: A(33,10,7) <= 26928/185 = 145.556757, hence A(33,10,7) <= 145
VERIFIED bound 145
```
Independent check (mychecks/indep.py): Q is computed a different way, as |X|·P^{-1} from the Eberlein P-matrix
(not the dual-Hahn formula verify.py uses). The primal LP is solved exactly by enumerating vertices in rational arithmetic, with all D1..D7:
```
Q_1(5..7)= ['272/91', '-256/91', '-112/13']  Q_2(5..7)= ['-1419/91', '-891/91', '2079/65'] m1,m2= 32 495
pure Delsarte LP (all Q_1..Q_7, a>=0): 5456/35 155.88571428571427 -> floor 155
Delsarte + a_7<=36: 26928/185 145.55675675675676 -> floor 145 opt a= ['18606/185', '1477/185', '36']
```
The rows of cert_A33_10_7.json for D1 and D2 match my independently computed -Q_1 and -Q_2. The primal optimum equals
the dual value 26928/185, so the certificate is optimal for that LP. As a sign sanity check, a random greedy (33,10,7) code of size 39
satisfies all seven Delsarte inequalities with my Q (mychecks/nullmodels.py).

## 2. Is "Delsarte LP + R_x" still a "Delsarte LP" in the sense of p2?
- The pure Delsarte LP (Q_1..Q_7 only) gives 155, which is not a win. The win needs the extra row R7: a_7 <= A(26,10,7).
- Independent literature: Agrell–Vardy–Zeger, "Upper bounds for constant weight codes", IEEE IT 46 (2000) (fetched PDF).
  Sec. V-C "Linear Programming" states Proposition 15, which it calls a "well-known constraint [8]":
  0 <= A_{2i} <= T(i,w,i,n-w,2δ). Theorem 20 defines "the linear programming bound" for constant-weight codes as
  the Delsarte inequalities plus Props 15–17 and 19. At i = w, T(w,w,w,n-w,2δ) = A(n-w,2δ,w), so R7 here is exactly
  AVZ Prop 15 at i = w. (For x < w the package's R_x, C(w,x)A(n-w,d,x), is a weaker but valid relaxation of T. Only R7 is used.)
  Brouwer's table legend has "L: Delsarte linear programming bound" for this kind of LP.
- My reading: an LP over the inner distribution, with Delsarte's inequalities plus the standard shell constraint, falls under
  "Delsarte LP" as the term is used for constant-weight codes, and the dual certificate is exact and rational. A strict reader who allows only
  Delsarte's inequalities would get 155 and no win. I accept the standard (AVZ) meaning and state the augmentation in the scope sentence.

## 3. Dependence on the published input A(26,10,7) <= 36
- Live table (=snapshot) prints A(26,10,7) as "30 c -36". The legend says "Unmarked upper bounds (for n ≤ 28) are taken from AVZ".
  AVZ Table IV (Bounds on A(n,10,w)), w=7 column, gives n=26 as "28 36 14", i.e. upper bound 36 from AVZ Theorem 14
  (Freiman–Berger–Johnson bound). So the input is a peer-reviewed published upper bound, and substituting published upper bounds
  for exact values is standard practice (AVZ Sec. VII).
- Sensitivity of the bound to the input (mychecks/indep.py):
```
 A(26,10,7)<=36 gives A(33,10,7)<= 26928/185 (145.5568) floor 145
 A(26,10,7)<=37 gives A(33,10,7)<= 27456/185 (148.4108) floor 148
 A(26,10,7)<=38 gives A(33,10,7)<= 27984/185 (151.2649) floor 151
 A(26,10,7)<=40 gives A(33,10,7)<= 5456/35 (155.8857) floor 155
```
- Can it be derived unconditionally? Not by me. I built a from-scratch chain (mychecks/chain.py) using only Johnson part 1 and part 2,
  complementation, and Delsarte LP + shell rows, with no table inputs. It gives U(26,10,7) = 40 and U(33,10,7) = 150, so it only matches
  the table and gives no improvement. Johnson from the published A(25,10,6) = 10 gives A(26,10,7) <= 37, which only yields 148, and that is
  already beaten by the Johnson null model below. **The non-subsumed result therefore depends on exactly the AVZ Theorem 14 value 36.**
  I did not re-derive it. The result is conditional on that published bound, and I did not prove it unconditionally.

## 4. Non-subsumption (null models, snapshot values A(32,10,6)=31, A(32,10,7)=139)
```
Johnson part1 floor(33/7*A(32,10,6)) = 146
Johnson part2 floor(33/26*A(32,10,7)) = 176
Pascal-type A(32,10,7)+A(32,10,6) = 170
Johnson with old A(32,10,6)<=32: floor(33/7*32) = 150 (reproduces table 150)
2nd Johnson bound denominator w^2-wn+delta*n = -17 (negative => not applicable)
Delsarte + R5,R6,R7 (table inputs): 26928/185 145.556 145
Delsarte + R5,R6 only (no A(26,10,7) input): 1056/7 150.857 150
```
Important caveat: the printed 150 is stale. The table says "For n > 28 unmarked upper bounds are from the Johnson bound", and
that bound with the table's own current A(32,10,6) = 31 already gives 146. So the real margin over what follows trivially from
the table is 146 -> 145, one codeword, not 150 -> 145. It is still strictly below every neighbour-Johnson null model (146, 176, 170),
so it is not subsumed. A web search for "A(33,10,7)" found no published sharper bound. I did not inspect arXiv:2608.13906 or
2607.19550 for upper bounds, since the table cites them as lower-bound (code) sources.

## 5. Live-table check, cell identity, quantifiers
- Live fetch Sat Oct 17 2026 04:38 EDT: HTTP 200, 127383 bytes, sha256 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8,
  byte-identical to table_snapshot/Andw.html.
- "Values of A(n,10,7)", header 29..33: "42 c -66, 48 s -85, 62 c -109, 64 c -139, 72 g -150". The n=33 cell is 72–150, and n=32
  (64–139) matches the main d=10 table, which confirms the column alignment. Mirror cell A(33,10,26) = A(33,10,7) by complementation.
- The claim covers one cell, (33,10,7), with one bound, U = 145 < 150. Nothing is bundled. The p2 quantifier "for some cell" is met by this single cell.
  The full success criterion (an explicit code beating the lower bound 72) is not claimed and not met. Only partial win p2 is at issue.

## Decision
The arithmetic is confirmed exactly and independently. The LP is the standard constant-weight Delsarte LP (Delsarte inequalities plus the AVZ
Prop 15 shell constraint). The bound is strictly below the live tabulated 150 and also below the strongest trivial neighbour bound 146.
It is a single cell. It is conditional on one published, peer-reviewed input, A(26,10,7) <= 36 (AVZ 2000, Thm 14), and that input is
load-bearing: with 37 the result would be subsumed.

confirmed_scope: An exact rational dual certificate for the Delsarte linear program of J(33,7), augmented with the single standard shell inequality a_7 <= A(26,10,7) and using the published bound A(26,10,7) <= 36 (Agrell–Vardy–Zeger 2000, printed in Brouwer's table), proves A(33,10,7) <= 145, strictly below the live tabulated upper bound 150 and below the neighbour Johnson bound 146 obtainable from the table's current A(32,10,6) = 31.

pass: true
