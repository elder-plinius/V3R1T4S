# PREREG
# Frozen 2026-11-13T07:16:35Z from `date -u` before any attack output on CW(208,81) is scored.

criterion: Success means a first row w in {-1,0,1}^n with exactly k nonzeros, zero periodic autocorrelation at every nonzero shift (so W W^T = kI), that is proper (its support is not contained in a coset of a proper subgroup of Z_n), verified by two independent programs, for an (n,k) whose status is 'Open' in the live La Jolla repository (https://dmgordon.org/circulant-weighing-matrices/ and the latest cwm.json on GitHub dmgordo/circulant-weighing-matrices or Zenodo, re-fetched live immediately before claiming) and that is not settled in the literature (not among the non-existence results of Tan, arXiv:2608.18468, and with no existence or non-existence result found by a fresh arXiv search for that CW(n,k)).

partial_win_p1: A non-existence proof for a CW(n,k) that is 'Open' in the live cwm.json and not already settled in the literature (e.g. not one of the eight cases of Tan, arXiv:2608.18468), delivered as a checkable certificate (an exhaustive search with a DRAT/LRAT-verified UNSAT proof, or an explicit multiplier/field-descent argument whose computational part a skeptic re-runs).

cell: CW(208,81), repository key CW(208,9), n=208, s=9, k=81.
plus_count: 45
minus_count: 36
zero_count: 127

statistic: two independent exact checkers. Checker A is periodic autocorrelation by direct sum. Checker B is the coefficient of x^t in w(x) * w(x^{-1}) modulo x^n-1. Both are integer arithmetic. A candidate passes only if both agree, C(0)=81, C(t)=0 for t=1..207, the sign counts are 45 and 36, entries are in {-1,0,1}, and the support is proper.

threshold: a win is a proper first row that both checkers accept, still Open in a refetch of cwm.json, and not settled by Tan arXiv:2608.18468 or a later paper found in the fresh search. Partial win p1 is a finished exhaustive search of every sequence constant on the orbits of multiplication by 3 on Z/208Z, with 45 pluses and 36 minuses, that finds no autocorrelation-zero row, together with the multiplier theorem (Tan, arXiv:2608.18468v2, Result 2.3: if a CW(v, p^{2e}) exists and gcd(v,p)=1, then a translate is fixed by p). gcd(208,3)=1 and 81=3^4, so that family is the whole existence question. A capped or unfinished search is not p1. An improper row is not a win.

null_test: not needed because an explicit object checked by a deterministic checker against a table value, or an exhaustive multiplier-orbit argument a skeptic re-runs. No search-performance or beats-chance claim.

baseline: not applicable. This is not an empirical score on data.

families_frozen_before_scoring:
- F1: every sequence constant on the orbits of <3> acting by multiplication on Z/208Z, with exactly 45 entries +1 and 36 entries -1. This is the forced family.
- F2: product and inflation constructions from published rows whose orders multiply to 208 and whose s-parameters multiply to 9. Checked by the same two checkers.
- F3: integer contractions ICW_d(208/d, 81) for d in {2,4,8,16}, entries bounded by d, sum of squares 81, sum ±9, autocorrelation 0. A divisor with no such contraction forbids the cell. A nonempty contraction does not.

No threshold above will be edited after scores. A changed plan is a new PREREG.v2.md.
