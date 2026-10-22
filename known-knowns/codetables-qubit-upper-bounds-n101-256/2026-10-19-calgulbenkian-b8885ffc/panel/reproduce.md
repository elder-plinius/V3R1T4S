context: Claude Code subagent, fresh context [claude-sonnet-5-5]
cell: qubit-ub-n112-k4-d36   role: reproduce

The contributor's hash list: 13 files listed, 0 not OK (checked from inside the package folder).

## Definition (quoted)
Criterion (verbatim, the part that can be checked mechanically): "a proof that no [[n,k,d]] stabilizer code exists for d equal to the live table upper bound ..., thereby lowering it by at least 1 ..., where the proof is an exact rational infeasibility certificate (Farkas dual) of the quantum weight-enumerator LP (stabilizer and normalizer enumerators linked by the quaternary MacWilliams identity, A_i <= B_i, A_i = B_i for 0 < i < d, nonnegativity, plus shadow-enumerator nonnegativity where used), checked in exact integer arithmetic by an independent script; and the new bound is NOT already implied by applying the standard propagation rules (d(n,k) <= d(n,k-1) for k >= 2, d(n,k) <= d(n+1,k), d(n,k) <= d(n-1,k+1)+1 ...) to other live cells."
My LP, from the literature definition: variables A_0..A_n (stabilizer weight enumerator, A_0 = 1, sum A_i = 2^(n-k)); B_j = 2^-(n-k) sum_i K_j(i) A_i with K_j(i) the quaternary Krawtchouk polynomial (generating function (1+3z)^(n-i) (1-z)^i); A_i >= 0; B_j >= A_j for all j; B_j = A_j for 0 < j < D; shadow Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i >= 0. A Farkas certificate: integer multipliers (free for equalities, nonnegative for inequalities) such that every column (coefficient of each A_i) of the combination is at most 0 while the combined right-hand side is positive.

## Disclosure on order
For this family the object's multiplier names (u_E0, u_E1, u_Q, v_G, v_H) have no meaning without the author's key, so I opened qubit_cert_check.py before writing my checker, and used its header only to map the multiplier families to LP rows (E0: A_0 = 1; E1: sum A = 2^(n-k); Q_j, 1 <= j <= D-1: B_j - A_j = 0; G_j, D <= j <= n: B_j - A_j >= 0; H_j: shadow >= 0). My checker (written from scratch, not shipped in this package) was then written from the definition above, with its own Krawtchouk matrix (polynomial multiplication of generating-function factors, not the explicit sum the author uses), and its own self-test: on the [[5,1,3]] code (A = 1,0,0,0,15,0) it recovers B = 1,0,0,30,15,18 (sum 2^6), shadows all nonnegative, and the symmetry C(n,i) 3^i K_j(i) = C(n,j) 3^j K_i(j). (I also checked the Steane code [[7,1,3]] by hand: B = 1,0,0,21,21,126,42,45 and shadows nonnegative.) The Farkas logic was re-derived: if the equalities hold, G and H rows are nonnegative, and A >= 0, the weighted sum gives (sum over i of column_i * A_i) >= right-hand side > 0, contradicting column_i <= 0.

## Command and real output
    (own checker, run on object/*.json with excluded distance 37)
self-test OK ([[5,1,3]]: B= [1, 0, 0, 30, 15, 18] , shadow>=0)
n,k,D = 112 4 37 | multipliers: Q 36 G 2 H 34
rhs (u_E0+u_E1*S) > 0 : True  (digits 651 )
max column coefficient <= 0 : True  (columns 113 , #zero 1 , #neg 112 )
PASS: infeasible => no qubit stabilizer code [[112,4,d]] with d>=37

## Not-implied-by-propagation check (own script, not shipped in this package)
I rebuilt the closure of the three rules from the full live table extract (33152 cells), took the minimum with the 56 merged and open PR values in the-record-we-beat/pr_claims.csv, removed this cell's own value (so it is derived only from other cells) and iterated to a fixed point; the output lines show two variants:
[[112,4]] live ub 37 claimed 36 | live+PRs+otherBatch: implied by others = 37 | claimed < implied: True
[[112,4]] live ub 37 claimed 36 | live+PRs only: implied by others = 37 | claimed < implied: True
(The "live+PRs only" line gives the same.) The folder's own three neighbour rows (neighbours.csv) agree: the best one-step bound is 37.

## Author's checker, run only after mine
== qubit_cert_check.py (exact integers, excluded distance D = live upper bound 37) and propagation neighbours
PASS [[112,4]] no code with d >= 37 (shadow=True): value has 651 digits; 36 Q, 2 G, 34 H multipliers; all 113 columns <= 0
{"n": 112, "k": 4, "d": 37, "VALID": true}
PASS certificate excludes d >= 37 = live upper bound; new upper bound 36; one-step bound implied by live neighbours and merged/open PR values = 37 (>= 37: True); triage closure of everything else (all rules iterated, live table + 56 merged/open PR values + other cells of the batch) = 37
== negative control: all shadow multipliers removed (must be rejected) (must be rejected)
PASS (negative control rejected)
ALL CHECKS PASS
Agreement: PASS, same verdict, all 113 columns at most 0, right-hand side positive. No mismatch.

## Notes
Open question 1 (does the checker's constraint set equal the criterion's LP, and does it exclude impure codes): the rows are exactly the ones the criterion lists (MacWilliams link, A_i <= B_i, equality below d, nonnegativity, shadow); B_j = A_j below D and B_j >= A_j above are the correct conditions for impure codes too (the test is on N(S) minus S, so low-weight stabilizer elements are allowed). Open question 4: a second Krawtchouk implementation is supplied by this report. Open question 2: the closure includes open PR values as above; deeper cells beyond the extracted table were not available. Whether open unmerged PR values should count as known is a ruling, not judged here.
Scope: this role confirms the certificate is exact and valid for the LP as defined; the shadow inequalities are the standard Rains shadow inequalities for stabilizer codes (not re-proved here).

pass: true
