# Record We Beat — `guts-weenie-rule-strong-equilibrium`

target_id: guts-weenie-rule-strong-equilibrium
table_url: https://arxiv.org/abs/2208.02788
fetch_time: 2026-10-29T04:46:30Z
http_status: 200
page_sha256: 98bc226513106104ff0b2ee9800c900a8a350746a79b967402854f7efc737b17

## Published Incumbent Status
- Primary Reference: Kevin Buck, Jae Hwan Lee, Jacob Platnick, Aric Wheeler, Kevin Zumbrun, "Continuous Guts Poker and Numerical Optimization of Generalized Recursive Games", arXiv:2208.02788v3 [math.OC] (2022), Appendix B.
- Status Source: arXiv:2208.02788v3 page retrieved 2026-10-29T04:46:30Z (HTTP 200).
- Published Record:
  - Proposition 6.1: Proved symmetric threshold equilibrium resistance for n=2.
  - Proposition 6.2: Proved symmetric threshold equilibrium resistance for n=3.
  - Appendix B.3 explicitly states: "We conjecture that this property holds for general n ≥ 2."
  - Numerical evaluations were performed for n=3, 4, 5, but no proof or exact nonnegativity certificates existed for n >= 4.
- Open Gap: The conjecture min_{t in [0,1]^{n-1}} alpha(3^{-1/(n-1)}, t) >= 0 remained unproven for all n >= 4.
- Resolution: This package establishes exact global algebraic nonnegativity certificates over Q[a] for n=4 (partial win p1) and n=5 (partial win p2), resolving both cases with machine-checkable certificates across all ordering chambers and boundaries.
