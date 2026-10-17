# PREREG frozen 2026-10-16T16:33:32Z (before any attack output is scored)
target: group-testing-separable-designs; A054961 n=10..27 and A290492 n=13.
criterion: target.md (quoted from OEIS).
statistic: checker/check_union.py: number of distinct vectors m, and whether all C(m,2) pairwise ORs (A054961) or C(m,3) triple ORs (A290492) are distinct.
threshold: PROMISING iff check passes and m > the live OEIS lower bound for that n (data/*.txt; re-fetched once before any claim).
null_test: not needed because every claim would be an explicit object checked by a deterministic checker against a published value.
lenses: search-engineer (min-conflicts local search in C, all n), constructor (cyclic/structured families), swimmer (collective moves: flip a bit column across many vectors), contrarian (is the OEIS bound already beaten elsewhere?).
