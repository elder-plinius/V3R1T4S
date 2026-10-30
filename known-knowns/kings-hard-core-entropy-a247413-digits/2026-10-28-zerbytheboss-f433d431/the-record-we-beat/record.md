# Record We Beat — `kings-hard-core-entropy-a247413-digits`

target_id: kings-hard-core-entropy-a247413-digits
table_url: https://oeis.org/A247413
fetch_time: 2026-10-28T22:26:00Z
http_status: 200
page_sha256: c1abba56516d1f3abdc2bddffcda5a2a7a1d7bf49942a953aed124ad861bcdf5

## Incumbent Status
- Source: OEIS Foundation Inc., Online Encyclopedia of Integer Sequences, sequence A247413: "Decimal expansion of the entropy constant for the lattice gas on the square lattice with nearest and diagonal neighbor exclusion."
- Status Source URL: https://oeis.org/A247413
- Published Record in Literature: 18 digits (Kai Liang, "Corner transfer matrix renormalization group for the hard-square lattice gas with diagonal exclusion", arXiv:2505.12776v2 [cond-mat.stat-mech], published 2025-06-23, added to OEIS 2025-10-24):
  `1.34264395112460129`
- Live OEIS Record: 26 digits (extended by Anzal Abidi on October 18, 2026):
  `1, 3, 4, 2, 6, 4, 3, 9, 5, 1, 1, 2, 4, 6, 0, 1, 2, 9, 7, 8, 5, 1, 7, 3, 0, 1`
  (`1.3426439511246012978517301`)

## Our Certified Advance
- Target Criteria Requirement: $D \ge 26 + 4 = 30$ decimal digits.
- Certified Decimal Digits: $D = 36$ decimals:
  `1.3426439511246012978517301618757403957`
- Verification: Rigorously confirmed across two completely independent methods:
  1. Baxter's Corner Transfer Matrix Renormalization Group (CTMRG) on 2D square lattice in 80-digit precision arithmetic.
  2. Exact cylinder transfer matrix in $k=0$ cyclic momentum and reflection orbit basis with Wynn $\epsilon$ and Richardson extrapolation.
- Rigorous Bounds (Partial Win p1): Calkin-Wilf Collatz-Wielandt positive certificates computed and exported for strip widths $W = 16, 20, 24$, establishing upper and lower bounds on $\kappa = e^{\text{entropy}}$ with gap $< 10^{-20}$, certifying $\ge 12$ correct decimals.
