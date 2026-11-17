# PREREG (frozen Sat Oct 31 14:32:51 UTC 2026)

Disclosure up front: one exploratory run of attempts/backwards-object/code/gvgreedy4 (seed 1) at about
14:31 UTC produced candidate nets for base 4 (m,s,t) = (13,21,6) and (13,22,6) before this file was written; the
(13,22,6) file passed code/netcheck.py. That output is exploratory and is NOT the claim object. Any claim object is
regenerated after this file with seeds fixed below and judged only by the rule below.

## Criterion (verbatim, bank mint-digital-nets-lower-t)
See target.md (copied verbatim from repo/bank/targets.json). Main criterion: explicit C_1..C_s over F_b forming a
digital (t,m,s)-net (exhaustive composition rank check), t strictly below MinT 'Constructive and digital', t >= MinT
digital lower bound, no paper/preprint/table already giving a digital (t,m,s)-net over F_b with that t, two
independent rank checkers agree. Partial win p1: first explicit construction reaching MinT's 'Digital'
(existence) value in a base 3/4/5 cell where it is strictly below 'Constructive and digital'.

## Statistic and checker
- The object is judged by an exact, deterministic checker: for every composition (d_1..d_s) of k = m - t into s
  non-negative parts, rank over F_b of the stacked first d_i rows of C_i equals k. Exhaustive, no sampling.
- Checker A: code/netcheck.py (pure Python, field tables, Gaussian elimination). Checker B: an independent C
  program written separately (code/netcheck_b.c), different representation. Both must print PASS on the same file.
  Both checkers are validated on fixtures first: a positive (identity/anti-identity (0,m,2)-net) and a negative
  (duplicated matrix), and checker A against the point-counting definition (code/pointcheck.py) on small nets.
- F_4 model: F_2[w]/(w^2+w+1), symbols 0,1,2=w,3=w+1.

## Thresholds
- p1 claim (one cell): t equal to MinT 'Digital' value and strictly below MinT 'Constructive and digital' value
  for that (b,m,s), read live on MinT query.php for that cell; b in {3,4,5}.
- Main-criterion claim (one cell): t strictly below MinT's 'Digital' (existence) value as well as below
  'Constructive and digital', and >= MinT digital lower bound; plus a literature search since 2008.
- A tie with any listed value is not a win. One cell per claim; if several cells are reached, the claim carries the
  single strongest one (largest s at given b,m,t, which implies smaller s by s-reduction), others are listed as
  by-products only.
- Seeds for the claim objects: 101, 102, 103 (first one that passes both checkers is the carrier).

null_test: not needed because the claim is an explicit object checked exhaustively by a deterministic exact checker against a table value (no search statistic, no 'beats chance' claim).
