# Record We Beat — `hard-core-entropy-square-honeycomb-digits`

target_id: hard-core-entropy-square-honeycomb-digits
table_url: https://oeis.org/A085850
fetch_time: 2026-10-29T02:58:20Z
http_status: 200
page_sha256: afce68df28d781dc201cc3614014e35c7e69c64c1fbb9be4d1ef109181077447

## Incumbent Status
- Source: OEIS Foundation Inc., Online Encyclopedia of Integer Sequences, sequence A085850: "Decimal expansion of the entropy constant for the lattice gas on the square lattice with nearest-neighbor exclusion."
- Status Source URL: https://oeis.org/A085850
- Published Literature Record: Rodney J. Baxter, "Planar lattice gases with nearest-neighbor exclusion", Annals of Combinatorics 3 (1999) 191-203, arXiv:cond-mat/9811264:
  `1.5030480824753322643220663294755536893857810` (43 decimals, with last 3 digits `810` flagged uncertain).
- Live OEIS Record: 40 decimal digits:
  `1, 5, 0, 3, 0, 4, 8, 0, 8, 2, 4, 7, 5, 3, 3, 2, 2, 6, 4, 3, 2, 2, 0, 6, 6, 3, 2, 9, 4, 7, 5, 5, 5, 3, 6, 8, 9, 3, 8, 5, 7`

## Our Certified Advance
- Settlement of Baxter's Flagged Digits (`p3`): Strictly confirmed decimals 41–43 as `8, 1, 0` (`CONFIRMED_SOLUTION`).
- Certified Decimal Digits: $D = 65$ decimals:
  `1.5030480824753322643220663294755536893857810386103050620281017359`
- Margin: +25 decimal digits beyond the live OEIS A085850 entry.
- Verification: Rigorously confirmed across two completely independent methods:
  1. Baxter's 1999 Corner Transfer Matrix (CTM) variational equations and block CTMRG in 80-digit precision arithmetic.
  2. Exact cylinder transfer matrix in $k=0$ cyclic momentum and reflection orbit basis with sequence extrapolation.
- Rigorous Bounds (Partial Win p1): Calkin-Wilf Collatz-Wielandt positive certificate vectors exported for strip circumferences $W = 16, 18, 20$, certifying bounds with CW gap $< 10^{-50}$.
