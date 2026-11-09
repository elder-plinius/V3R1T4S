# PREREG: site-percolation-2-uniform-lattices-thresholds

frozen: 2026-10-16T05:22:16Z (date -u), before any percolation measurement on a two-uniform lattice.
Already run before this freeze (calibration only, no two-uniform lattice): the transfer-matrix code on the square,
triangular, kagome, honeycomb and (3,12^2) lattices (n <= 4), and two 40,000-sample Monte Carlo benchmarks on kagome
(L = 32) and square (L = 64).

null_test: not needed because the claim is a measured constant (a deterministic transfer-matrix root sequence plus a Monte Carlo estimate with a stated error bar), not a detection or beats-chance claim; the controls are calibration lattices with exactly known thresholds and published high-precision sequences that the same code must reproduce (listed below)

## Criterion (verbatim from the bank)

> Success means, for at least one of the 20 two-uniform lattices in the live Wikipedia table (re-fetched immediately before claiming), a site percolation threshold with stated one-sigma uncertainty at most 2e-6 (100 times smaller than the table's), such that (a) two independent methods agree within three combined sigma (for example Newman-Ziff wrapping-probability finite-size scaling on tori up to L >= 2048 unit cells, and the Jacobsen-Scullard critical-polynomial root sequence P_B(p) = 0 for growing bases), (b) the value is within 3 sigma of the table value or the discrepancy is explained, (c) the same code reproduces the published BOND threshold of that lattice to at least 6 digits and the site threshold of the (3,12^2) or kagome Archimedean lattice to at least 6 digits, and (d) a literature search finds no published site value for that lattice with uncertainty below 2e-6. Direction: smaller uncertainty.

Partial wins (verbatim):
- **p1:** All 20 two-uniform site thresholds to uncertainty at most 2e-5 each, same two-method and reproduction rules, published as a table with code.
- **p2:** An independent determination, to at least 7 digits, of a 'citation needed' bond threshold in the same Wikipedia table, either confirming it or showing a discrepancy larger than its stated error bar.

## Cells (one claim per lattice)

The four "row" lattices of the Wikipedia table, built by `attempts/evaluator-first/code/lattices.py` (`rows()`):
#23 = rows SSST, #22 = rows SST, #21 = rows STT, #20 = rows STTT (S = row of unit squares, T = row of triangles).
Identity rule: `check_tiling()` must report unit edges, regular faces, Euler V-E+F = 0, no edge crossings, exactly
2 vertex orbits, and vertex-type fractions and zbar equal to the Wikipedia row. Other two-uniform lattices may be added
only through a new, timestamped PREREG.v2.md.

## Method A: transfer matrix (exact-polynomial lens), `attempts/exact-polynomial/code/tmcrit.c`

- Statistic: p_c(n), the root of Lambda_open(p) = Lambda_closed(p) on the n x infinity cylinder of circumference n a1
  (a1 = (1,0), along the rows), Jacobsen arXiv:1507.03027 eq. (13), for n = 1..n_max (n_max as large as memory allows).
- Regression net that must pass before and after the target runs: square site n <= 8 equal to Jacobsen's Table 2 to
  1e-12; kagome bond n <= 5 equal to Table 3 to 1e-12; triangular site 1/2, kagome site 1 - 2 sin(pi/18),
  (3,12^2) site sqrt(1 - 2 sin(pi/18)), square bond 1/2, triangular bond 2 sin(pi/18), honeycomb bond 1 - 2 sin(pi/18),
  each for n = 1..4 to 1e-12.
- Extrapolation (frozen): ansatz p_c(n) = p_c + sum_{k=1..K} A_k n^(-e_k). Exponent family: e_k = 2(k+1) (4, 6, 8, ...;
  Jacobsen 2015 eq. 34) if the local exponent from the three largest n is within 0.5 of an even integer >= 4;
  otherwise e_k = e_1 + (k-1) with e_1 = that local exponent rounded to the nearest integer. Fit family: K = 1..4,
  each solved exactly on the K+1+j largest available n, j = 0, 1, 2, using only n >= 4. p_TM = median of the family;
  sigma_TM = max |estimate - p_TM| over the family (convergence spread, never the last difference alone).
- Claim requirement for method A: sigma_TM <= 2e-7.

## Method B: Monte Carlo (timeline-aligner lens), `attempts/evaluator-first/code/nzwrap.c`

- Newman-Ziff site (or bond) addition in random order on L1 x L2 tori of unit cells, union-find with unwrapped
  displacements. Per sample n1 (first non-contractible cycle) and n2 (first cluster with rank-2 winding).
  R_0D(n) = P(n < n1), R_2D(n) = P(n >= n2), canonical curves by binomial convolution.
- Estimator per size: p_L = root of R_2D(p) - R_0D(p) = 0 from the pooled histograms; sigma_L = jackknife over at least
  20 independent blocks (distinct seeds or consecutive blocks of one xoshiro256** stream).
- Fixed aspect ratios (near-square tori): #23 L2 = L1/4; #22 L2 = L1/3; #21 L2 = 3 L1/8; #20 L2 = 2 L1/7;
  kagome L2 = L1. Sizes L2 in {8, 12, 16, 24, 32, 48, 64, 128}, plus one low-statistics torus with L1 >= 2048 cells.
- FSS fit (primary): weighted least squares p_L = p_MC + A L2^(-4) over the sizes with L2 >= 16; sigma_MC from the fit
  covariance, multiplied by sqrt(chi2/dof) when chi2/dof > 1. Stability (kill criterion 2): the same fit restricted
  to L2 >= 24 must agree with the primary within one sigma_MC; otherwise the MC line is dead until a new prereg.
  A free-exponent fit is reported as a check, not used for the value.
- Claim requirement for method B: sigma_MC <= 2e-6.

## Decision rules

- (a) agreement: |p_TM - p_MC| <= 3 sqrt(sigma_TM^2 + sigma_MC^2).
- (b) |p_TM - p_table| <= 3 sqrt(sigma_TM^2 + (2e-4)^2) with the live Wikipedia site value, or the discrepancy explained.
- (c) "reproduces to at least 6 digits" means |ours - published| < 1e-6 with our sigma <= 1e-7.
  Transfer matrix: the lattice's Wikipedia bond value (tmcrit bond mode, same extrapolation rule), and kagome and
  (3,12^2) site (exact). Monte Carlo: kagome site within 3 sigma with sigma <= 2e-6, and the lattice's Wikipedia bond
  value within 3 sigma with sigma <= 2e-6 (a 2e-6-level calibration of the second method; the 6-digit reproductions
  are by the code that produces the claimed value, the transfer matrix).
- (d) a literature search (arXiv, web, this repo's TROPHY_CASE.md and open PRs) right before claiming finds no
  site value for that lattice with uncertainty below 2e-6.
- The claimed value is p_TM +- sigma_TM; the claim states sigma_MC and the agreement separately.
- Live table re-fetched right before claiming; if the cell changed, the comparison is redone.

## Partial win p2 (bond, 'citation needed'), frozen the same way

For each of the four lattices: p_bond,TM with sigma <= 1e-8 by the rule above. Confirmed if |p_bond,TM - wiki| <= 3
sqrt(sigma_TM^2 + sigma_wiki^2) with sigma_wiki the table's own error, a discrepancy if larger. The MC bond value
(sigma <= 2e-6) must agree with p_bond,TM within 3 combined sigma, as a sanity check of the independent determination.

## Dead-line rules

- Any regression-net failure: the transfer-matrix line stops until fixed.
- sigma_TM > 2e-7 at the largest feasible n: no full claim from method A for that lattice.
- MC kagome calibration off by more than 3 sigma: the whole MC pipeline stops until fixed (kill criterion 5).
