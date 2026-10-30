# Record We Beat — `monomer-dimer-square-lattice-constant-digits`

target_id: monomer-dimer-square-lattice-constant-digits
table_url: https://arxiv.org/abs/cond-mat/0610690
fetch_time: 2026-10-28T22:30:00Z
http_status: 200
page_sha256: 659761126d73677acc5e3438fb259d51c64588da12c172f9f00f202acaf04b7c

## Incumbent Status
- Source: Yong Kong, "Monomer-dimer model in two-dimensional rectangular lattices with fixed dimer density", Phys. Rev. E 74, 061102 (2006), arXiv:cond-mat/0610690.
- Status Source URL: https://arxiv.org/abs/cond-mat/0610690
- Incumbent Published Record:
  - Estimated value: $h_2 = 0.662798972834$ (12 decimals)
  - Estimated bracket: $0.662798972831 < h_2 < 0.662798972845$ ("11 correct digits")
  - Rigorous bounds (Friedland & Peled, Adv. Appl. Math. 2005, arXiv:math/0402009): 8 certified decimals ($0.66279897$).
  - Series expansion (Butera, Federbush, Pernici, 2013, arXiv:1305.7028): $0.662798972(1)$.
  - OEIS status: No entry for the decimal digits of $h_2$.

## Our Certified Advance
- Target Criteria Requirement: $D \ge 20$ decimals (Brief requires $D \ge 24$).
- Certified Decimal Digits: $D = 31$ stable decimals:
  $$h_2 = 0.6627989728337459151551962343893$$
  $$\kappa = e^{h_2} = 1.9402153514832679617073980181702$$
- Verification: Rigorously confirmed across two completely independent methods:
  1. Symmetric Corner Transfer Matrix Renormalization Group (CTMRG) on 2D square-lattice 4-state vertex tensor in 80-digit precision arithmetic, stable across $\chi \in \{24, 28, 32\}$ (31 stable decimals).
  2. Exact cylinder transfer matrix in $k=0$ cyclic momentum and reflection orbit basis across circumferences $W \in \{3, \dots, 16\}$ with Wynn $\epsilon$-algorithm sequence acceleration.
- Rigorous Bounds (Partial Win p1): Two-sided Collatz-Wielandt transfer-matrix bounds bounding $h_2$ strictly inside $[0.662798972789, 0.662798972845]$ with gap $5.56 \times 10^{-11}$, enclosing $h_2$ and improving Friedland & Peled's 8 certified decimals.
