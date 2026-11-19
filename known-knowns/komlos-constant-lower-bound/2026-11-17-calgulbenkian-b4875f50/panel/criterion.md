context: Claude Code subagent, fresh context [Sonnet 5.5]

Criterion skeptic report, partial win p2 (komlos-constant-lower-bound).

Word-by-word check of p2
- "explicit matrix": object/komlos_15x15_p2.txt, SHA-256 matches the one claimed (b4875f50...5de5113). Header "15 15 10^12", then 225 integers.
- "at most 15 nonzero columns": 15 columns, all nonzero (every column has positive squared norm). OK. The number of rows is unconstrained by p2 (m = 15 here anyway), so no issue.
- "rational entries": stored as integers over the common denominator D = 10^12, i.e. exact rationals P/D. The entries like 707106781186 (approx 1/sqrt 2) and 288675134594 (approx 1/(2 sqrt 3)) are truncated decimals, but that is legitimate: the matrix claimed is the rational one as stored, not the idealised one. I recomputed every column's squared norm in exact integers: all 15 are <= D^2. Columns 5, 6 and 7 (1-indexed; indices 4, 5, 6 in 0-index) hit exactly 1 with zero slack; the others have slack. So the rounding was done inward and norms stay <= 1.
- "exact discrepancy exhaustive over all 2^n sign vectors, two independent programs": the package ships a Python file (exact Fraction branch-and-bound plus a Gray-code scan in the same file) and a separate C99 __int128 Gray-code checker. The Python file's two methods are not fully independent of each other (same parser), but the C program is a separate language and parser, so "two independently written programs" is met by the shipped files alone; the package's own claim of "three implementations" is a slight overcount (two files). I did not need to count my reproduction as the second, but I also wrote a third, plain brute-force integer check (all 2^14 sign classes with x1 = +1, exact integers, no pruning). It gives min over x of max-row-sum = 2059565086610 / 10^12 = 2.05956508661, matching the claim exactly. I did not run the shipped C program or shell script; I read the Python checker and the receipts only.
- "strictly greater than 2.006": 2.05956508661 > 2.006, checked exactly (2059565086610 > 2006 * 10^9). OK.
- Fixing x1 = +1 by symmetry is valid since the discrepancy is invariant under global sign flip.

Hidden quantifiers / stretched definitions
- p2 says "at most 15 nonzero columns", and the object has exactly 15. Fine.
- The claim says it "subsumes p1": p1 needs discrepancy >= 2 under the same rules; 2.0596 >= 2, so p2 implies p1. Correct, and it does not make a different claim.
- The claim honestly does not assert a full-criterion win (needs d > 2.41421), so no stretching there.
- The package's matrix is real data; the "How we found it" prose is labeled contributor text and is not load-bearing.

Null model
- The package's null test (1000 random unit-column Gaussian 15x15 matrices, best 0.92) is weak as a null, since random matrices are far from optimised ones, but it is irrelevant to correctness: this is an exact certificate, not a statistical finding. The real comparison baseline is Spielman's 2.005-2.006 and Kunisky's tree matrices. I take the exact check as decisive and the null as decoration.

Prior art / subsumption
- Kunisky's tree matrices first certify above 2 at 16 columns (K(16) >= 2.0607). Since this claim has 15 columns, that bound does not subsume it, and 2.0596 < 2.0607 is consistent with monotone growth in columns. The only prior n <= 15 value is Spielman's unpublished [2.005, 2.006], which the claim exceeds, with a gap of about 0.0536. The condition that nothing is subsumed by a larger-n published bound holds as stated, but I did not re-fetch arXiv or the 24a page; I relied on the criterion text, which says the reference interval is the prior record for 15 columns. I could not independently rule out a newer preprint with a 15-column value above 2.006. The package's own baseline fetch reports 0 open PRs touching 24a.

Limits
- This is not an improvement over 1 + sqrt(2) and does not claim to be.
- Rational rounding to 10^-12 is an engineering choice; it does not weaken the exactness of the certificate.

confirmed_scope: The stored rational 15x15 matrix object/komlos_15x15_p2.txt (integers over 10^12, all 15 column squared norms <= 1 exactly) has exact discrepancy 205956508661/10^11 = 2.05956508661 over all sign vectors, strictly above 2.006 and above 2, so it meets partial win p2 (and p1) but not the full criterion.
pass: true
