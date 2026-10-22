# Criterion skeptic report: ub-35-14-14-837

context: Claude Code subagent, fresh context [Claude Sonnet 5.5]

Scope: judged only the package folder of this cell, plus one fetch of https://aeb.win.tue.nl/codes/Andw.html (fetched 2026-10-18T17:54:53Z, HTTP 200, sha256 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349, identical to the page hash recorded in the claim). The contributor's hash list: every file verified OK.

## Criterion applied
Partial win p2 (verbatim): "An improved upper bound: an exact rational dual certificate (Delsarte LP or Schrijver-type SDP, verified in rational arithmetic) proving A(n,d,w) <= U for U strictly below the live tabulated upper bound for some cell."
Bar used for "live tabulated upper bound": the table-implied bound (printed bounds plus both Johnson rules applied recursively), per the maintainer's ruling (PR #350).

## Clause by clause
1. Exact rational dual certificate, Delsarte LP: met. I wrote my own check (written from scratch, not shipped in this package) in Fraction arithmetic: Eberlein eigenvalues of the Johnson scheme J(35,14) with an exact orthogonality test, Q_k(x) = m_k E_x(k) / v_x, all y_k nonnegative with indices 1..14, and min over Johnson distance x = 7..14 of sum_k y_k(-Q_k(x)) >= 1. My output line: (35, 14, 14) min_x sum_k y_k(-Q_k(x)) = 1.0 ge1: True objective 837.3134328358209 floor 837 claimed 837 OK. This is a feasible dual, so A(35,14,14) <= floor(objective) = 837.
2. "U strictly below": met against the table-implied bound. I recomputed the implied bound with my own parser of the page and my own Johnson recursion (also written from scratch, not shipped in this package): (35, 14, 14) lb/ub printed: None None implied 1143. It is the same with or without the merged V3R1T4S extra bounds, so it does not depend on them. Margin 1143 - 837 = 306, direction min, strictly below.
3. "live tabulated upper bound": cannot be decided literally. The live cell reads 163 (lower-bound-only subtable "Lower bounds for A(n,14,14)") and prints no upper bound, so there is no printed number to be strictly below. The page states "For n > 28 unmarked upper bounds are from the Johnson bound", and the cell is unmarked, so the implied Johnson-recursion value is the page's own convention for it. Under the PR #350 ruling this is the bar and it is cleared; read with only printed numbers the clause is vacuous.
4. Non-subsumed by propagation: met. The certificate is a pure Delsarte LP with no table inputs, and its value is below the full Johnson-recursion bound, so it is not a consequence of table values by the two Johnson rules. I did not check unmarked-cell LP or SDP values in the literature beyond the page's own references (Schrijver 2005, Kim-Toan, Polak 2017 cover n <= 28 on the page); that part is left to the novelty role.
5. Mirror cell A(n,d,n-w): the page lists this cell with no printed upper bound; checked in the fetched table that the mirror column carries none.
6. Format: certificate is a JSON with key "y" of rationals as strings; INDEX.csv value 837, table value 1143, matches my numbers. The JSON field table_cell_as_printed is author bookkeeping and is not trusted (for the 29-row cells it records an older lower bound than the live page, which does not affect an upper bound).
7. Lower-bound clauses of the main criterion (M strictly greater, explicit code, Echols and Lysenstoen): not applicable to p2; no code is claimed.

confirmed_scope: The exact rational Delsarte dual certificate in object/cert_A35_14_14.json proves A(35,14,14) <= 837, which is strictly below the table-implied upper bound 1143 (margin 306; the live cell prints no upper bound) as of the Andw.html page with sha256 15b15c8d...3349 fetched 2026-10-18; it is an upper-bound certificate only (enumerated partial win p2 under the PR #350 table-implied reading) and says nothing about any lower bound or code.

pass: true
