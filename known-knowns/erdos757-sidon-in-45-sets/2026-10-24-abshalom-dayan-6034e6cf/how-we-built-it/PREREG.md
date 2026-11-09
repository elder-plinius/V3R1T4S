# PREREG (frozen 2026-10-24T10:33:26Z, before any attack output is scored)

## Criterion (verbatim from repo/bank/targets.json)
Success means a finite set A of distinct integers with all of the following. (1) Every 4-subset has at least 5 distinct absolute differences, checked exhaustively. (2) The exact maximum Sidon subset size s(A) is certified by two independent exact methods (bitmask branch-and-bound and an ILP that forbids every a+b=c+d, including a=b, i.e. 3-APs). (3) The ratio s/|A|, compared in fractions.Fraction, is STRICTLY SMALLER (direction: min) than the best upper bound on c* shown at verification time at https://www.erdosproblems.com/757, on the EinsteinArena 'Sidon Subsets of (4,5)-Sets' leaderboard and in any newer arXiv paper (context: 4/7 on 2026-10-03; a ratio exactly equal to the live best is not a success). (4) s/|A| >= 9/17; a ratio below 9/17 contradicts a theorem and means a bug, never a claim. (5) The verifier confirms in arXiv:2602.23282 the lemma that a finite witness bounds c* (the blow-up lemma or the inf-formula), or else re-derives it. (6) The checker reproduces s=8 on the Ma-Tang 14-set as a calibration test.

## Statistic and checker
- Object: a finite set A of distinct integers (exact; rationals are scaled to integers by checker.to_ints).
- (4,5): two methods must agree: (a) the literal C(n,4) check of distinct absolute differences (stdlib),
  (b) the pair-sum characterisation (no additive quadruple with distinct elements, linear 3-AP hypergraph).
- h(A): two independent exact methods must agree: (a) CP-SAT optimal with best bound = value, model forbidding
  every a+b = c+d with distinct pairs (a <= b, c <= d), including a = b; (b) a branch-and-bound written separately
  (bitmask B&B on the 3-AP hypergraph after (b) above; or a SAT cardinality refutation of h+1 with pysat if the
  B&B times out; the report says which).
- Ratio r = Fraction(h, |A|).

## Thresholds
- Win (full success): r < 5/9 strictly (the live community bound, below the literal sources' 4/7), with r >= 9/17.
  A ratio r in [5/9, 4/7) is NOT claimed (already beaten by the 5/9 family; reported as not novel).
- Partial p1 candidate: r == 5/9 exactly with |A| not a multiple of 14 (a finite set attaining the live limit);
  the CRITERION skeptic decides whether that meets p1 literally.
- r < 9/17 means a bug: stop and debug, never claim.
- Calibration (must pass before any claim): Ma-Tang 14-set gives (4,5) True, h = 8; reader's S_6 gives 65 points,
  h = 37.

null_test: not needed because every claim is an explicit finite object checked by deterministic exact checkers against a fixed table value (no search statistic or beats-chance claim)
