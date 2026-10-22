# PREREG: monomer-dimer entropy h2 digits (written before any digit-bearing run)

Written 2026-10-18 (agent clock shows 2026-10-19 in FETCHLOG), BEFORE any width >= 13 transfer-matrix run and before any CTM run.
Quantity: h2 = ln(kappa), kappa = lim Z(n,n)^(1/n^2), Z = number of matchings (monomer-dimer coverings, unit weights) of the grid.

## Disclosures (what was seen before this file)
- Friedland-Peled (arXiv math/0402009) Table 1: log beta(m)/m for periodic widths m = 4..16 (upper bounds), and Kong's bracket
  0.662798972831 < h2 < 0.662798972845.  From these I know the periodic raw sequence converges by about a factor 15 per +2 in width.
- Method knowledge (not data) from ../kings/ (CTM code ctmgen2.py structure, Wynn recipe PREREG_B.md).
- No monomer-dimer computation of my own had been run when this file was written.

## Method A (corner transfer matrix), headline estimator
- Model: bond-occupancy vertex model, one tensor per lattice site, legs = bond occupation 0/1 (dimension 2), tensor = 1 iff
  (left+right+up+down) <= 1.  kappa = Z per site.  (Adapted from ../kings/ctmgen2.py: same CTM scheme, new tensor.)
- Four distinct corners and four distinct edge tensors, float64 SVD for the projector, Newton-Schulz exact re-orthonormalisation,
  all contractions in 256-bit arb (python-flint).  kappa read off as N11*N00/(N10*N01) from closed contractions.
- Ladder: chi = 12, 16, 20, 24, 28, 32, 36, 40, ... (step 4), each warm-started from the previous chi; each stage runs until
  |dkappa| < 1e-36 on three consecutive iterations or 400 iterations.  Stop the ladder at the first chi_k (k >= 4 rungs) at which the
  last four rungs agree on >= 28 decimals, or at chi = 64, whichever comes first.
- Headline digits D_A = number of leading decimals of h2 = ln(kappa) common to the LAST FOUR rungs of the ladder (three increases).

## Method B (exact periodic-cylinder transfer matrices + Wynn extrapolation), headline estimator
- Data: L_m = ln beta(m), beta(m) = largest eigenvalue of the exact transfer matrix of the cylinder of circumference m (periodic row
  of m sites, free along the length), even m = 4, 6, ..., M; computed in unsigned 128-bit fixed point, eigenvalue from
  ||Tx||^2/||x||^2 after power iteration, converged to < 1e-45.  No CTM value is used anywhere in B.
- Sequence: d_m = (L_m - L_{m-2})/2 for even m = 6, 8, ..., mmax (start width m0 = 6, i.e. first term uses L_4).
- Extrapolation: Wynn epsilon algorithm on d_6, d_8, ..., d_mmax at 60 digits.  E(mmax) = last entry of the highest even-index column.
  No other column, no averaging, no selection.
- Ladder (truncation parameter): mmax = 16, 18, 20, 22, 24, 26 (and 28 if it completes within the memory/time budget).
- Headline digits D_B = number of leading decimals common to E(mmax) for the LAST FOUR consecutive mmax of the ladder (three increases).
- Other variants (open strips, other start widths, other columns) are context only, labelled as such, and never used for the headline.

## Joint claim rule
- Reported digits D = min(D_A, D_B, number of decimals on which E_B(last) and kappa_A(last) agree), must be >= 20 and the value must lie
  inside Kong's bracket and inside my own rigorous enclosure (see REPORT.md).  Anything chosen after seeing data is listed in REPORT.md
  under "post-hoc choices".

## Rigorous part (separate; not subject to the ladder rule)
- Upper bounds: h2 <= (1/m) ln beta(m), m even, m >= 4.  Lower bounds: p*h2 >= ln beta(p+2q) - ln beta(2q), q >= 2.
  Each beta bounded by Collatz-Wielandt ratios of exact-integer test vectors (cross-multiplied in >= 256-bit integers).
  Proofs are written in REPORT.md from the definitions.
