# CRITERION verdict: A(31,10,7) <= 106 (claimed partial win p2)

context: subagent (fresh executor, saw only claim/A31_10_7/)

Files are named relative to the claim folder (claim/A31_10_7/). My own scripts are in ../../checks/ (lp.py, checks2.py). The pages I fetched once each are saved there too: live_Andw.html, sph.pdf/sph.txt, arx_*.html.

## What p2 asks for, read literally
p2: "An improved upper bound: an exact rational dual certificate (Delsarte LP or Schrijver-type SDP, verified in rational arithmetic) proving A(n,d,w) <= U for U strictly below the live tabulated upper bound for some cell."
Conditions: (a) an exact rational dual certificate, (b) of the Delsarte LP or Schrijver SDP type, (c) checked in rational arithmetic, (d) proving A(n,d,w) <= U, (e) with U strictly below the LIVE tabulated upper bound, (f) for one cell. The claim is A(31,10,7) <= 106 against a printed 109.

## (a,c,d) The certificate checks out exactly
Running `python3 verify.py cert_A31_10_7.json` gives:
```
selftest: Delsarte inequalities hold on 150 random subsets; P-for-Q control fails; scheme sums zero: OK
  column x=5: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=6: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=7: sum_r y_r row_r(x) = 1  (needs >= 1)
certified: A(31,10,7) <= 2015/19 = 106.052632, hence A(31,10,7) <= 106
VERIFIED bound 106
```
I also checked it with my own code. ../../checks/lp.py computes Q_k by a different route: Q_k(x) = m_k E_x(k)/v_x with Eberlein polynomials, and I checked the orthogonality relations exactly for J(31,7). It then solves the LP exactly by enumerating every vertex in rational arithmetic:
```
orthogonality of Q for J(31,7): OK
pure Delsarte: A(31,10,7) <= 775/7 = 110.7143  a=['84', '0', '180/7']
Delsarte + a7<=24: A(31,10,7) <= 2015/19 = 106.0526  a=['1512/19', '28/19', '24']
Delsarte + a7<=25: A(31,10,7) <= 6200/57 = 108.7719  a=['1561/19', '35/57', '25']
Delsarte + a7<=26: A(31,10,7) <= 775/7 = 110.7143  a=['84', '0', '180/7']
```
The value 2015/19 is the true LP optimum: the primal vertex reaches it. ../../checks/checks2.py re-checks the cert's duals with my own Q:
`(1) columns ['1', '1', '1'] all>=1: True  value 2015/19 106.05263157894737`.

Null model: the pure Delsarte LP gives 110, which is worse than the table's 109. So the whole improvement comes from the row R7: a_7 <= A(24,10,7). The bound stands or falls with that input.

## (b) Does "Delsarte LP + a_x <= C(w,x)A(n-w,d,x)" count as "Delsarte LP"?
Only R7 (x = w = 7, C(7,7) = 1) is used, i.e. a_w <= A(n-w,d,w): the codewords disjoint from a fixed c form an (n-w,d,w) code. The inequality is elementary and correct. I brute-force sanity-checked it on small codes (checks2.py (5): `A(6,4,3) = 4 ; codewords disjoint from any c in 200 random (9,4,3) codes never exceed it: True`).

Independent literature: Agrell–Vardy–Zeger, ISIT 2000, "Constant-Weight Code Bounds from Spherical Code Bounds" (sph.txt, Sec. III), says: "The linear programming bound for a constant-weight code with w <= n/2 is A(n,2δ,w) <= 1 + max sum A_2i, where the maximum is taken over all {A_i} that satisfy certain well-known constraints [2]" ([2] = Best et al. 1978). It then adds further constraints as an "Improved Linear Programming Bound". So in the standard literature the "LP bound" for constant-weight codes means Delsarte's inequalities plus extra valid linear constraints on the distance distribution. Brouwer's table also labels KKT ("Improved linear programming bounds") this way. I could not retrieve the full AVZ 2000 Trans. IT paper (the Zeger PDF link timed out; I did not retry), so I could not confirm from its text that this particular constraint is among the "well-known constraints". That does not matter here: it is an elementary, proven-valid linear constraint, and the certificate is a rational LP dual. I judge (b) satisfied without stretching the definition.

## The crux: is the input A(24,10,7) <= 24 justified?
Snapshot, raw HTML of the d=10 table, row n=24 (my own grep):
`<th>24</th><td>9</td>` `<td><a href="cwc/d10/i24.7">24</a><sup>c</sup></td>` `<td>...39</a><sup>E</sup>-60</td>` ...
The cell shows a single value 24 (lower-bound source "c", explicit code link). There is no lo-hi range.

Page legend, read literally: "The tables below give the best known lower (and upper) bounds" and "Unmarked upper bounds (for n ≤ 28) are taken from AVZ". The d=4 section alone says "For now, lower bounds only. Optimum values are indicated by a dot." The d=10 section has no such disclaimer. The page's own note "[BSSS] showed A(21,10,8) ≥ 21, but the period indicating equality may have been a mistake. However, equality follows from [AVZ] (26)." concerns a cell also printed as the single value "21". It shows that a single value in these sections is maintained as an equality, with the upper bound sourced. The legend does not say "single value = exact" in so many words, so on the page alone this reading is a strong but implicit convention.

Independent source (decisive): the AVZ ISIT 2000 paper (sph.txt, Theorem 1) says: "Let b = δ − w(n − w)/n. Then A(n,2δ,w) ≤ ⌊δ/b⌋ if b ≥ δ/n; A(n,2δ,w) ≤ n if 0 < b ≤ δ/n ..." It then lists "previously unknown exact values ... A(24,10,7) = 24".

I re-proved this myself (checks2.py (2),(3)):
```
(2) A(24,10,7): b=1/24, delta/n=5/24, s_max=-1/119  => 0<b<=delta/n => <= n = 24 (Rankin: pairwise-negative vectors in R^(n-1) number <= n)
(3) embedding: normalized inner product = 1 - D n/(2w(n-w)), vectors in sum-zero hyperplane: OK (2000 pairs)
```
Argument: map 0→+1 and 1→−1, then subtract the mean vector. Weight-7 words of length 24 become vectors of equal norm in the 23-dim sum-zero hyperplane, with normalized inner product 1 − Dn/(2w(n−w)) <= 1 − 120/119 = −1/119 < 0 for D >= 10. Any set of vectors in R^23 with pairwise strictly negative inner products has at most 24 members (Rankin). So A(24,10,7) <= 24 holds unconditionally. This also settles the weaker requirement A(24,10,7) <= 25 (needed for any improvement; with 25 the LP gives 108.77 -> 108). The input is proved, not just read off the table, so the claim is unconditional.

## (e) Live table value, mirror, non-subsumption
- I fetched https://aeb.win.tue.nl/codes/Andw.html once at 2026-10-17 08:44 UTC (04:44 EDT): HTTP 200, 127383 bytes, sha256 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8. It is byte-identical to table_snapshot/Andw.html (`cmp` → IDENTICAL). The live cell is row 31, w=7: `62c-109`. The secondary "Values of A(n,10,7)" table also shows 62c-109 at n=31. The legend says "For n > 28 unmarked upper bounds are from the Johnson bound." 109 is unmarked.
- Mirror A(31,10,24) = A(31,10,7) by complementation; the table lists w <= n/2 only. No separate cell holds a smaller bound.
- Johnson bounds from the current neighbours (checks2.py (4)): from A(30,10,6) = 25 -> 110; from A(30,10,7) <= 85 -> 109; monotonicity from A(32,10,7) <= 139 -> 139. Theorem 1 does not apply to (31,10,7) itself (b = −13/31 < 0). Pure Delsarte gives 110. Nothing printed or directly implied gets to 106, so 106 is not subsumed.
- Literature: the two arXiv papers named in the bank (2608.13906 and 2607.19550, abstracts fetched once each) are about lower bounds only. A web search for "A(31,10,7)" found no published upper bound below 109. This search is not exhaustive. The narrower claim I can confirm is "strictly below the live tabulated upper bound", which is exactly what p2 asks.
- Hidden quantifiers: the claim covers one cell, one U. "Live" is met by today's fetch. The bound is unconditional (the input was re-proved above). It is not an asymptotic, average, or family statement.

## Caveat (does not block a pass)
The table's 109 for n > 28 is only a Johnson bound, so this is a modest improvement (109 -> 106) of a weakly tabulated cell. p2 asks literally for "strictly below the live tabulated upper bound", and that is met.

confirmed_scope: An exact rational Delsarte-LP dual certificate (Delsarte inequalities k=1,2 for J(31,7) plus the elementary constraint a_7 <= A(24,10,7) <= 24, the latter proved independently via the Agrell–Vardy–Zeger/Rankin spherical-code bound) proves A(31,10,7) <= 106, strictly below the upper bound 109 printed for this cell in Brouwer's Andw.html as fetched 2026-10-17 08:44 UTC.

pass: true
