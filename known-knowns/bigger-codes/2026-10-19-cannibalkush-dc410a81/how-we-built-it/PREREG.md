# Frozen 2026-10-19T06:16:15Z
Success means an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER (direction: max) than the lower bound shown at verification time in the (n,d,w) cell of https://aeb.win.tue.nl/codes/Andw.html (also checking the mirror cell A(n,d,n-w)), and also strictly greater than any value for that cell in arXiv:2608.13906 (Echols, 124 improved cells), arXiv:2607.19550 (Lysenstoen) or any newer arXiv paper. M must not exceed the tabulated upper bound; exceeding it means a bug.
[
  {
    "id": "p1",
    "statement": "A first explicit certificate: for a cell whose live lower bound has no surviving explicit code listing (a bare 1990-era citation), an explicit code of size equal to the tabulated lower bound, verified exactly. The skeptic confirms on the live page and in arXiv:2607.19550 / 2608.13906 that no explicit code for that cell is already published."
  },
  {
    "id": "p2",
    "statement": "An improved upper bound: an exact rational dual certificate (Delsarte LP or Schrijver-type SDP, verified in rational arithmetic) proving A(n,d,w) <= U for U strictly below the live tabulated upper bound for some cell."
  }
]
Statistic: explicit code cardinality or floor of exact feasible dual objective. Threshold: strictly improve the strongest live table, publication and pending-PR value including Johnson propagation and complement symmetry. Numeric optimization only discovers candidates; exact rational validation decides validity.
null_test: not needed because claims are explicit objects or deterministic exact rational certificates compared with published bounds, not statistical or beats-chance claims.
