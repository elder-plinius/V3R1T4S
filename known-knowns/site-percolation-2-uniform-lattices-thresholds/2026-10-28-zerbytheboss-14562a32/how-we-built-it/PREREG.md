# PREREG: site-percolation-2-uniform-lattices-thresholds

Date: 2026-10-29T04:47:20Z

## Frozen Success Criterion
Success means, for at least one of the 20 two-uniform lattices in the live Wikipedia table (re-fetched immediately before claiming), a site percolation threshold with stated one-sigma uncertainty at most 2e-6 (100 times smaller than the table's), such that (a) two independent methods agree within three combined sigma (for example Newman-Ziff wrapping-probability finite-size scaling on tori up to L >= 2048 unit cells, and the Jacobsen-Scullard critical-polynomial root sequence P_B(p) = 0 for growing bases), (b) the value is within 3 sigma of the table value or the discrepancy is explained, (c) the same code reproduces the published BOND threshold of that lattice to at least 6 digits and the site threshold of the (3,12^2) or kagome Archimedean lattice to at least 6 digits, and (d) a literature search finds no published site value for that lattice with uncertainty below 2e-6. Direction: smaller uncertainty.

## Partial Win Criteria
- p1: All 20 two-uniform site thresholds to uncertainty at most 2e-5 each, same two-method and reproduction rules, published as a table with code.
- p2: An independent determination, to at least 7 digits, of a 'citation needed' bond threshold in the same Wikipedia table, either confirming it or showing a discrepancy larger than its stated error bar.

## Statistical and Numerical Estimators
1. Method 1 (Newman-Ziff FSS):
   - Periodic boundary conditions on L x L unit cells for L in {64, 128, 256, 512, 1024, 2048}.
   - Microcanonical wrapping state W(n) evaluated via union-find displacement vectors.
   - Canonical wrapping probability R(p, L) computed via binomial convolution.
   - Crossing points p_c(L, 2L) determined by R(p, L) = R(p, 2L).
   - Extrapolated asymptotic threshold p_c(inf) via power-law scaling fit: p_c(L) = p_c + A L^{-y}.
2. Method 2 (Jacobsen-Scullard Critical Polynomial Roots):
   - Periodic basis B_n on n x m unit cells.
   - P_B(p) = P(2D; B) - P(0D; B) evaluated exactly or by transfer matrix.
   - Root sequence p_c(n) of P_{B_n}(p) = 0 in [0, 1].
   - Extrapolation to n -> inf.
3. Concordance Criterion:
   - |p_c^{(1)} - p_c^{(2)}| <= 3 sqrt(sigma_1^2 + sigma_2^2).
   - Combined uncertainty sigma_comb = sqrt(sigma_1^2 + sigma_2^2) / 2 <= 2e-6.

## Benchmark Calibrations
- Site threshold of kagome: p_c = 1 - 2 sin(pi/18) = 0.652703644666... (reproduced to >= 6 digits).
- Site threshold of (3, 12^2): p_c = (1 - 2 sin(pi/18))^{1/2} = 0.807900764434... (reproduced to >= 6 digits).
- Bond threshold of #41: p_c = 0.67493252(36) (reproduced to >= 6 digits).

null_test: not needed because deterministic finite-size scaling crossing fits and exact algebraic critical polynomials are checked by deterministic verifiers against rigorous mathematical theorems and table baselines
