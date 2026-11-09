# Criterion skeptic report

context: subagent (Claude Agent tool, model claude-sonnet-5-5), given only claim/

Scope of what I read: everything under claim/ (CLAIM.md, REPRODUCE.md, object/, checkers/, rebuild/, table/). Nothing else
under runs/. My own scripts and outputs are in panel/work-criterion/ (crit_check.py / crit_check.out,
table_neighbors.py / table_neighbors.out, ag_sanity.py / ag_sanity.out). No network was used. I scanned the claim files for
text addressed to reviewers (grep for "ignore previous", "pass: true", "verdict" and similar): none found.

## 1. Condition-by-condition table

| # | Condition in the criterion | What shows it | Status |
|---|---|---|---|
| 1 | Explicit EAQECC [[n,k,d;c]]_3 | object has n=28, k=5, d=15, c=11, field GF(3) symplectic | met (n, k, c recomputed by me; d see row 9) |
| 2 | c >= 1 | c = 11 (my computation); no c = 0 case anywhere | met |
| 3 | Exact generator matrix over GF(3), symplectic, 2n columns, or over GF(9) trace-Hermitian | S is 34 x 56 over GF(3) with entries in {0,1,2} and 2n = 56; G9 (11 x 28) and D9 (17 x 28) over GF(9) also given | met (S is the matrix I computed from) |
| 4 | Cell of the qutrit table at https://eaqecc.codetables.de/qutrit.php | the saved page lists exactly one cell `[[28,5,13-22;11]]<sub>3</sub>`, no duplicate (n,k,c) keys among 3888 parsed cells | met, as a listed cell, not an implied one |
| 5 | Table re-fetched live immediately before claiming | table/RECORD.md: three plain GETs, HTTP 200, same sha256 each time, last at 2026-10-24T10:36:29Z; table/qutrit.headers.txt carries the server header `date: Sat, 24 Oct 2026 10:36:29 GMT`, which matches. My own clock at check time: Sat Oct 24 11:30:04 UTC 2026, so the copy is about 54 minutes old now | met as of 10:36:29Z; cannot be re-done by me (no network). The claimer must re-fetch at the moment of claiming and compare sha256 37bbf731...936c; see section 3 |
| 6 | s = number of independent generators on Alice's n qutrits | rank_GF(3)(S) = 34 = number of rows | met (my output below) |
| 7 | c = rank(S J S^T)/2 | rank(S J S^T) = 22, Gram matrix antisymmetric, so c = 11 | met |
| 8 | k = n - s + c | 28 - 34 + 11 = 5 | met |
| 9 | d = exact min weight of vectors in the symplectic dual of span(S) that are NOT in span(S) ∩ span(S)^perp, strictly greater than d_lower | table d_lower = 13 for (28,5,11); claimed d = 15. Checker A (S only, GF(3), enumerates all 3^22 vectors of span(S)^perp) computes exactly "min symplectic weight over span(S)^perp minus the hull", plus the pure distance separately; Checker B does the same over GF(9) (min over C minus the Hermitian hull). I read both and the definition matches the criterion (see below). I did NOT rerun the 3^22 enumeration; the exact d = 15 rests on the author's checkers and the other skeptic's enumeration | 15 > 13, no tie. d >= 15 independently supported by my own argument (section 2.3); exact d = 15 rests on the enumerations |
| 10 | d <= d_upper | d_upper = 22 in the cell; 15 <= 22 | met |
| 11 | Exclusion of c = 0 | c = 11 | met |
| 12 | "Table's d_lower for that (n,k,c)": order of n, k, c | cell text is `[[28,5,13-22;11]]` and the page legend states the format [[n, k, d_lower-d_upper; c]]; the object has n=28, k=5, c=11 | met, right cell, right order |

Checker definitions, read line by line. Checker A: `s = rank(S)`; `G[i][j] = x_i.z_j - z_i.x_j`; `c = rank(G)//2`; `k = n - s + c`;
`perp` = nullspace of the system (z_i | -x_i).v = 0, i.e. the symplectic dual, dimension asserted to be 2n - s; the
isotropic part is built as span(S) ∩ perp from the dependencies between S and the perp basis; the basis of perp is
ordered with the hull basis first, and a vector counts as "not in the hull" iff some logical coefficient is nonzero; `d` is
the minimum symplectic weight (position counted when x or z is nonzero) over those, and `d_pure` is reported separately.
It is not the pure distance and it does not use the classical code. Checker B: enumerates all 9^11 codewords of C, tests
the Hermitian hull via the inner products with the generators, and takes the minimum weight over C minus the hull
(`d_ea`), also reporting `d_all`. One more point I checked: in rebuild/build_claim.py the JSON field "d" is taken from a
command-line argument (not computed); k and c in the JSON are computed. So "d" in the JSON is a claim, verified only by the checkers.

## 2. My own computation (panel/work-criterion/crit_check.py, output in crit_check.out)

Command: `python3 -I crit_check.py <claim/object/eaqecc_28_5_15_11.json>` (standard library only). Output, verbatim:

```
sha256 83602b9ae21bd9ab3d1872f4bb244f452a689cb88254e0cc398a75df2e9fd434
claimed n,k,c,d = 28 5 11 15
S shape: 34 x {56}  entries: [0, 1, 2]
s = rank(S) = 34
Gram antisymmetric: True ; rank(S J S^T) = 22 (even: True )
c = rank/2 = 11
k = n - s + c = 28 - 34 + 11 = 5
dim span(S)^perp = 2n - s = 22 ; hull dim = s - 2c = 12
MATCH claimed (n,k,c): True
c >= 1: True ; rows independent (s == len(S)): True
w^2-w-1 roots in GF(3): []
G9 11 x {28}  D9 17 x {28}
D9 Hermitian-orthogonal to G9: True
w encoded as 3 ; S rows == phi(r), phi(w r) of D9 rows in order: True
affine points of y^3+y=x^4 over GF(9): 27
monomials (i,j), pole order 3i+4j: [((0, 0), 0), ((1, 0), 3), ((2, 0), 6), ((3, 0), 9), ((4, 0), 12), ((0, 1), 4), ((1, 1), 7), ((2, 1), 10), ((3, 1), 13), ((0, 2), 8), ((1, 2), 11)]
pole orders distinct: True count 11
rebuilt rows == G9 rows (as a set): True ; rebuilt rank 11 ; rank(G9) 11 ; rank(G9 + rebuilt) = 11
rank(D9) = 17 ; rank over GF(9) of G9 = 11 ; 11 + 17 = 28: True
Hermitian Gram rank of G9 = 5 ; hull l = 6 ; k = kappa - l = 5 ; c = n - kappa - l = 11
```

The file hash also agrees with the sha256 in CLAIM.md and with `shasum -a 256` of the file. The GF(3) route (S only) and
the GF(9) route (G9 only) give the same (k, c) = (5, 11), and the hull has dimension 12 over GF(3) = 6 over GF(9).

### 2.1 Duality check (panel/work-criterion/ag_sanity.out)

```
symplectic <S_i, phi(C basis)> all zero: True ; #phi(C basis) vectors: 22
rank of the 22 vectors over GF(3): 22 ; rank of [S; them] = 44 (34 + hull overlap)
```

So span(S)^perp (dimension 22) is exactly phi(C) with C = rowspace(G9): S is symplectically orthogonal to these 22
independent vectors, and 44 = 34 + 22 - 12 matches the hull dimension 12. The code that Checker B enumerates (9^11 = 3^22 words)
is the same set that Checker A enumerates.

### 2.2 Table neighbours (panel/work-criterion/table_neighbors.out)

```
cells parsed: 3888 duplicate keys: 0
(28,5,11) -> (13, 22)
all listed c for (28,5): [(0, (9, 11)), (3, (10, 14)), (5, (12, 19)), (11, (13, 22)), (12, (14, 22)), (13, (16, 22)), (15, (17, 22)), (17, (18, 23)), (19, (19, 23)), (21, (20, 23)), (23, (21, 24))]
lengthening  [[27,5,d;11]] -> [[28,5,d;11]]: source cell (27, 5, 11) = (13, 21); implied d_lower for (28,5,11) = 13
puncturing   [[29,5,d;11]] -> [[28,5,d-1;11]]: source cell (29, 5, 11) = (13, 22); implied d_lower for (28,5,11) = 12
subcode      [[28,6,d;11]] -> [[28,5,d;11]]: source cell (28, 6, 11) = (13, 20); implied d_lower for (28,5,11) = 13
incr. dim.   [[28,4,d;10]] -> [[28,5,d;11]]: source cell (28, 4, 10) = None; ...
q. shortening [[29,4,d;11]] -> [[28,5,d-1;11]]: source cell (29, 4, 11) = None; ...
len. reduction [[29,5,d;10]] -> [[28,5,d;11]]: source cell (29, 5, 10) = None; ...
any (28,5,c<=11) with d_lower>=15: []
(n<=28,5,c<=11) with d_lower>=15: []
```

So the page's own legend rules do not already give d >= 15 at (28,5,11), and no listed code with k = 5, n <= 28, c <= 11 has
d_lower >= 15. The result is not subsumed by another listed cell. The table itself shows the cell as a "lengthening of
[[27,5,13;11]]" (arXiv:2207.05647 source), a derived bound of 13, and the next-higher c rows are 14 (c=12) and 16 (c=13).

### 2.3 Why I believe d >= 15 independently of the enumeration (my argument, partly computed)

G9 equals (as a set of rows, checked) the extended one-point code of the Hermitian curve y^3 + y = x^4 over GF(9): the 11
monomials x^i y^j (j <= 2, 3i + 4j <= 13) evaluated at the 27 affine points, with last coordinate = coefficient of the
unique monomial of pole order 13. The pole orders are distinct (0,3,4,6,7,8,9,10,11,12,13), so a nonzero codeword comes
from f with top pole order m' <= 13. A function with pole divisor m'·P_inf has at most m' affine zeros, so the weight on
the 27 affine coordinates is >= 27 - m'. If m' = 13 the last coordinate is nonzero (+1); if m' <= 12 the affine part is
already >= 15. Hence every nonzero codeword of C has weight >= 15, so the minimum over the smaller set C minus the hull is also >= 15
(and "strictly greater than 13" needs only d >= 14). I tested the 27 - m' bound exhaustively for all words with top
pole order <= 10 (8 monomials, every word):

```
top pole order  0: min affine weight over all words with that top monomial = 27; Goppa bound 27 - m = 27; OK=True
top pole order  3: ... = 24; bound 24; OK=True        top pole order  4: ... = 23; bound 23; OK=True
top pole order  6: ... = 21; bound 21; OK=True        top pole order  7: ... = 20; bound 20; OK=True
top pole order  8: ... = 19; bound 19; OK=True        top pole order  9: ... = 18; bound 18; OK=True
top pole order 10: ... = 17; bound 17; OK=True
```

The bound is attained exactly at each tested order, which is consistent with exact d = 15 at order 13 (14 affine + 1 at infinity).
The orders 11, 12, 13 (the part of the space needing 9^9 to 9^11 words) I did not enumerate; that is what the author's
Checker A/B and the other skeptic cover. This is a supporting argument, not a replacement.
The author's expected output (REPRODUCE.md) reports d = 15 with 71280 non-hull minimum-weight words and 1008 minimum-weight
words inside the hull (72288 - 71280); I did not run it.

## 3. Hidden quantifiers, stretched definitions, and other findings

- Is the cell listed or implied? Listed: `<TD ... title="lengthening of [[27,5,13;11]] subcode of [[27,8,13;11]] from arXiv:2207.05647">[[28,5,13-22;11]]<sub>3</sub></TD>`. I read n, k, c from the cell text itself (the page's nested table layout lists one block of cells per (n, k)); I did not rely on the visual grid position.
- Strictly greater, not a tie: 15 vs 13. Even the neighbouring listed c = 12 (14) and c = 13 (16) are not the cell claimed.
- Order of (n, k, c): cell text is [[n,k,d_l-d_u;c]]; read as n = 28, k = 5, c = 11, d_l = 13, d_u = 22. The object has the same n, k, c.
- One cell only; the claim does not bundle cells. The claim sentence says "strictly above d_lower = 13 for the cell (28,5,11)", which matches what the object shows.
- k = 0 or c = 0 passed off? No: k = 5, c = 11.
- Pure distance vs EAQECC distance: d (hull excluded) and d_pure are both reported by Checker A; the lower bound I derived is for all nonzero words, so it does not depend on hull handling. The criterion's definition is met by the checker as written.
- Weight convention: symplectic weight on the n = 28 Alice qutrits (position counted if (x_i, z_i) != (0,0)), equal to the GF(9) Hamming weight because a + b w = 0 iff (a, b) = (0, 0). No weight on Bob's side.
- s = 34 > n = 28 is allowed here (k = n - s + c with c = 11).
- Staleness of the table copy: the copy is the author's own saved GET (sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c, 628039 bytes, "Last change: 10.07.2025", server Date 10:36:29 GMT). Three fetches over about 71 minutes gave the same hash, so the page was stable, but I cannot authenticate the copy against the live site and cannot re-fetch. The criterion says re-fetch "immediately before claiming"; that final re-fetch (same URL, compare the hash; if it differs, re-read the (28,5,11) cell) is a step for the claimer at the time of the claim, not for this panel. If the hash differs and d_lower for (28,5,11) has risen to 15 or more, this result no longer meets the criterion.
- The "d" field in the JSON is an input to build_claim.py, not an output; the numbers in the claim depend on the checkers, which I read and found to match the criterion's definition.
- Partial wins p1 and p2: not claimed, not relevant.

## 4. Null models

A null/permutation test does not apply. The claim is an exact combinatorial and algebraic statement about one explicit finite object
(a rank computation over GF(3) and a minimum weight over a finite set of 3^22 vectors), compared with a number printed in a table.
There is no statistical estimate, sample, p-value or random baseline, so nothing for a null model to calibrate. The relevant
guards are the exact recomputation of (s, c, k), the checker's definition of d, and the table-cell comparison, covered above. (The
analogue of a null check here is the sanity run in 2.3, where the bound is attained exactly at every tested order.)

## 5. Verdict

confirmed_scope: claim/object/eaqecc_28_5_15_11.json (sha256 83602b9ae21bd9ab3d1872f4bb244f452a689cb88254e0cc398a75df2e9fd434) holds a 34 x 56 GF(3) symplectic matrix S with n = 28, s = rank(S) = 34, c = rank(S J S^T)/2 = 11 >= 1 and k = n - s + c = 5 (recomputed by me), whose minimum symplectic weight over span(S)^perp minus span(S) ∩ span(S)^perp is at least 15 (I derived d >= 15 from the Hermitian one-point code structure, verified G9 against it, and tested the zero-count bound exhaustively for top pole order <= 10; d is exactly 15 per the author's checkers, which I read but did not rerun), which is strictly greater than d_lower = 13 and at most d_upper = 22 in the listed cell [[28,5,13-22;11]]_3 of claim/table/qutrit.php (sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c, server date 2026-10-24T10:36:29Z), with no neighbouring cell or legend rule on that saved page giving d_lower >= 15 for (28,5,11); a fresh live re-fetch at the moment of claiming is still owed by the claimer and was not done by me.

pass: true
