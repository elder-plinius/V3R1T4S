# PREREG (frozen 2026-11-02T04:01:02Z per date -u; the A364417(20) run started 04:00:20Z and has produced no result yet)

Target: benzel-stones-and-bones-next-terms. Cells: A364417(20) = T113(20,37) (primary aim) and, if compute allows,
A364416(21) = T113(21,38).

Criterion (bank, verbatim): The exact next term A364416(21) or A364417(20), not in the DATA when re-fetched
immediately before claiming. It must come from two independent runs that agree exactly, and the same code must
reproduce every published term of A364416 and A364417.

Statistic / checker:
- Program A = attempts/search-engineer/code/benzZQ.c (row sweep along lines i = const, frontier DP, 64-bit state,
  u64 counts with every addition overflow-checked - any overflow aborts the run and voids it; sound zone pruning
  that removes a state only when an exhaustive MRV exact-cover search proves the next K rows cannot be covered).
  Must reproduce every published term: A364416(3..20) and A364417(3..19), exactly.
- Program B = an independently written second program (different source file, different sweep direction / cell
  order, different pruning code, exact 128-bit or multi-modulus arithmetic). It must reproduce the published terms
  it can reach and produce the same new term.
- Independent geometric checker attempts/contrarian/code/indep_check.py (Propp's complex-plane definition, memoized
  exact cover) for small n (3..11) of A364416, A364417, A364418, A364438.
- Claim only if A(new) == B(new) exactly, both runs overflow-free, A reproduces all published terms, and the OEIS
  DATA re-fetched right before claiming still lacks the term. Any disagreement or missing reproduction = no claim.
Thresholds: exact integer equality; no tolerance.

null_test: not needed because the claim is an exact integer from deterministic exhaustive counting programs checked
against published terms, not a search score or a "beats chance" statistic.
