# PREREG (frozen 2026-10-17T08:04:55Z, before any attack output)

criterion (verbatim, from target.md / bank): see target.md "Success criterion" and partial wins p1, p2, copied verbatim.

## Lens obstruction (partial win p2)
- statistic: for each cell (n,d,w) of the live table (data/Andw.html, fetched 2026-10-17T08:02:33Z), the optimum L of a linear
  program over the inner distribution a_x (x = Johnson distance) with: Delsarte inequalities, the shortening second-moment
  inequalities M_{t,s} (t<=2), and per-distance bounds a_x <= B_x derived from smaller cells. Every smaller-cell bound used
  must be a numeric upper bound read from the same live table, or an exact elementary bound (Johnson recursion, trivial cells).
- checker: float LP (HiGHS) only to locate candidates; a candidate counts only after an exact rational dual certificate is
  verified in Python Fractions (dual feasibility checked exactly) giving U = floor(certified value).
- threshold: p2 candidate iff U < the live numeric upper bound of that cell (strictly). A cell with no numeric upper bound
  ("...") is not a p2 candidate. Equal = nothing.
## Lens structured (main criterion)
- statistic: size M of an explicit code that is a union of orbits of a permutation group (AGL(1,p) subgroups, with fixed points).
- checker: tools/check.py (pairwise popcount) on the explicit word list.
- threshold: M strictly greater than the live lower bound (and of the mirror cell), and M <= live upper bound. Tie = nothing.

null_test: not needed because every claim here is an explicit object (code word list or rational LP dual certificate) checked by a deterministic exact checker against a table value; no statistical or search-score claim is made.
