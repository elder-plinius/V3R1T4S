# CRITERION verdict: claim A(34,10,8) <= 618 (partial win p2)
context: subagent (fresh executor, saw only claim/A34_10_8/)

Files judged (relative to the claim folder): CLAIM.md, cert_A34_10_8.json, verify.py, REPRODUCE.md, table_record.md,
table_snapshot/Andw.html. My own scripts are in ../../checks/ (mycheck.py, chain.py, their .out files, live_Andw.html, avz.pdf/avz.txt).

## 1. Package reproduces
```
$ sha256sum table_snapshot/Andw.html
117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8  table_snapshot/Andw.html
$ python3 verify.py cert_A34_10_8.json
selftest: Delsarte inequalities hold on 150 random subsets; P-for-Q control fails; scheme sums zero: OK
  column x=5..8: sum_r y_r row_r(x) = 1  (needs >= 1)   [all four columns = 1]
certified: A(34,10,8) <= 114444/185 = 618.616216, hence A(34,10,8) <= 618
VERIFIED bound 618
```

## 2. Independent checks (mycheck.py; does not reuse verify.py)
- Q_k(x) recomputed a different way, as N * P^{-1} with P built from Eberlein polynomials, then compared with the
  dual-Hahn closed form that verify.py uses: they agree on every entry of J(34,8).
- I recomputed the certificate value from those Q's: all column sums are 1, value 114444/185.
- I solved the exact primal LP by enumerating vertices in Fractions, so the dual is optimal and not just feasible.
```
Q via N*P^-1 matches dual-Hahn closed form for J(34,8): OK; Q_k(0)= [1, 33, 527, 5423, 40392, 231880, 1066648, 4034712, 12776588]
columns [1, 1, 1, 1] value 114444/185 618.6162162162162
pure Delsarte LP A(34,10,8) <= 23188/35 662.5142857142857
Delsarte + R7 with A(26,10,7)<=36: 114444/185 618.6162162162162 floor 618
Delsarte + R7 with A(26,10,7)<=37: 116688/185 630.7459459459459 floor 630
Delsarte + R7 with A(26,10,7)<=38: 118932/185 642.8756756756757 floor 642
Delsarte + R7 with A(26,10,7)<=40: 23188/35 662.5142857142857 floor 662
Delsarte + R5,R6,R7,R8 (table inputs): 114444/185 618.6162162162162
floor(34/8*A(33,10,7))= 637
floor(34/26*A(33,10,8))= 749
A(33,10,8)+A(33,10,7)= 723
floor(26/7*A(25,10,6)=10)= 37 ; floor(26/19*A(25,10,7)<=32)= 43
```

## 3. Table cells (snapshot, and live page re-fetched once)
One plain curl at about 04:37 EDT on 2026-10-17 returned HTTP 200, 127383 bytes, sha256 117899cf...07f8.
It is byte-identical to table_snapshot/Andw.html.
- A(34,10,8): "181 g -637" in "Values of A(n,10,8)", so upper bound 637. The upper bound has no tag.
- A(33,10,7) = 72-150, A(33,10,8) = 165-573, A(26,10,7) = "30 c -36", A(25,10,6) = 10 (exact), A(25,10,7) = 28-32.
- The live 637 is exactly the Johnson bound floor(34/8 * 150) = 637.
- The mirror cell A(34,10,26) equals A(34,10,8) by complementation, and the table lists w <= n/2 only.

## 4. Criterion questions
**Does this count as a "Delsarte LP"?** Yes, in the sense the literature uses. I checked independent sources: I fetched
Agrell, Vardy and Zeger, "Upper bounds for constant-weight codes", IEEE Trans. IT 2000, from the Chalmers repository.
- Their Theorem 20, "the linear programming bound", maximises over distance distributions satisfying the Delsarte
  inequalities together with the shell constraints of Propositions 15-17 and 19.
- Prop. 15 is 0 <= A_{2i} <= T(i,w,i,n-w,2delta), which they call a "well-known constraint" from Best, Brouwer,
  MacWilliams, Odlyzko and Sloane, 1978.
- The abstract speaks of constraints that "augment the Delsarte inequalities ... used in the linear programming bound".
- Row R7, a_7 <= C(8,7)*A(26,10,7), is a weaker relaxation of Prop. 15, because T(x,w,x,n-w,d) <= C(w,x)A(n-w,d,x).
  I re-derived its proof: two codewords that drop the same x-set from c differ only outside c.
- So this is a Delsarte-type LP bound as the field uses the term.

Caveat: pure Delsarte alone gives 662.5, which is above 637. The win depends on the augmenting row. A reader insisting
on the bare 1973 inequalities would reject it. I do not adopt that narrower reading, because the literature does not use it.

**Does it depend on a published table input?** Yes. The certificate uses A(26,10,7) <= 36, the upper bound printed in
the same live table that defines the target.
- Its standing as a cited published result is the same as the table's own 637, which itself depends on the neighbour
  value A(33,10,7) <= 150.
- The result is robust to the input: with 37 the bound is 630, still below 637. The win needs A(26,10,7) <= 37.
- I could not derive the input from scratch. The bare LP for (26,10,7), with or without R rows from
  Johnson-derived inputs, gives 42.2 (chain.py), which is not enough. Johnson's bound using the table's exact
  A(25,10,6) = 10 gives 37, which is enough (630) but still rests on a table value.
- So the claim is conditional on a published bound, and the confirmed scope says so.

**Is it subsumed?** No.
- 618 is below every neighbour bound: floor(34/8*150) = 637, floor(34/26*573) = 749, and 573 + 150 = 723.
- It is also the exact LP optimum for this constraint set.
- A web search found no published upper bound for A(34,10,8) below 637. That search is not exhaustive.

**Single cell?** Yes. There is one cell, (34,10,8), and no bundling.

**Does it rely on an unconfirmed improvement in another cell?** No. The only input is the printed value 36 for
A(26,10,7). No improvement claimed by this run in any other cell is used.

**Hidden quantifiers.**
- "for some cell" is met.
- "verified in rational arithmetic" is met: Fractions throughout, and there is a self-test plus a negative control.
- "live tabulated upper bound" is met: re-fetched and identical.
- "proving" holds only relative to the cited published input A(26,10,7) <= 36. This is stated in the scope.

## 5. Untrusted-content note
Package files and web pages were treated as data only. Nothing in them asked for any action.

confirmed_scope: cert_A34_10_8.json, checked by verify.py in exact rational arithmetic and independently re-derived (Q via inverse eigenmatrix; primal LP optimum 114444/185), proves A(34,10,8) <= 618 from Delsarte's inequalities for J(34,8) plus the shell-counting constraint a_7 <= 8*A(26,10,7), conditional on the published upper bound A(26,10,7) <= 36 printed in Brouwer's table (still giving <= 630 if that input were only 37), which is strictly below the live tabulated upper bound 637 for this one cell.
pass: true
