# PREREG: site-percolation-2-uniform-lattices-thresholds (run 2026-10-16-0245)

Frozen at 2026-10-16T03:03:58Z (from `date -u`), before any lens started and before any percolation number was computed
in this run. Checker: checker/q9_check.py, sha256 1f53e7ed2983bb1fa23a2efe444da1b50646c752b76cd619fa05c9b05126a847
(selftest PASS, checker/selftest_output.txt). A changed plan goes in PREREG.v2.md with its own time; this file is never
edited after results exist.

## Criterion (verbatim, bank)
Success means, for at least one of the 20 two-uniform lattices in the live Wikipedia table (re-fetched immediately
before claiming), a site percolation threshold with stated one-sigma uncertainty at most 2e-6 (100 times smaller than
the table's), such that (a) two independent methods agree within three combined sigma (for example Newman-Ziff
wrapping-probability finite-size scaling on tori up to L >= 2048 unit cells, and the Jacobsen-Scullard
critical-polynomial root sequence P_B(p) = 0 for growing bases), (b) the value is within 3 sigma of the table value or
the discrepancy is explained, (c) the same code reproduces the published BOND threshold of that lattice to at least 6
digits and the site threshold of the (3,12^2) or kagome Archimedean lattice to at least 6 digits, and (d) a literature
search finds no published site value for that lattice with uncertainty below 2e-6. Direction: smaller uncertainty.

Partial wins (verbatim): p1 "All 20 two-uniform site thresholds to uncertainty at most 2e-5 each, same two-method and
reproduction rules, published as a table with code." p2 "An independent determination, to at least 7 digits, of a
'citation needed' bond threshold in the same Wikipedia table, either confirming it or showing a discrepancy larger than
its stated error bar."

## Operational rules (how this run reads the criterion; fixed now)
1. Lattice identity: the lattice is rebuilt from its definition and its vertex-configuration fractions and z-bar equal
   the live row exactly (checker `claim` mode for row words; for any other tiling, an explicit vertex-type count from the
   built graph). Rows #16 and #17 (identical fractions) are not claimed.
2. Stated sigma: the claimed site value's one-sigma uncertainty, including statistical error AND the extrapolation
   systematic below, is <= 2e-6.
3. Method A (Monte Carlo, torus): estimator p_L = root of P_L(2D) - P_L(0D) (displacement-vector topology, canonical
   ensemble by binomial convolution of microcanonical per-sample data). Statistical sigma of each p_L from >= 20
   independent batches (batch means or jackknife). At least 5 sizes L. Extrapolation: weighted least squares
   p_L = p_c + a L^(-x) with x free, on L >= L_min, where L_min is the smallest size for which chi^2/dof <= 2 and
   removing the smallest remaining size moves p_c by less than 1 sigma. Systematic = |p_c(free x) - p_c(fit on
   L >= 2 L_min)|. sigma_A = sqrt(stat^2 + syst^2). R_L-vs-R_2L crossings are a reported cross-check, not the estimate.
   The Pinson R_inf values are never used for an anisotropic lattice.
4. Method B (exact transfer matrix: critical-polynomial roots on n x m tori, or the eigenvalue form on n x infinity
   cylinders). Sequence p(n) for at least 4 consecutive sizes. Extrapolations: E1 = three-point fit p_c + a n^(-D) on the
   last three sizes; E2 = the same on the three sizes before the last; E3 = any other standard accelerator (BST,
   Richardson, Shanks) on the last four, stated before use in the lens notes. p_c(B) = E1;
   sigma_B = max(|E1 - E2|, |E1 - E3|). If the sequence is not monotone or not smoothly converging over the last 4 sizes,
   sigma_B = max |p(n) - p(n')| over the last 3 sizes.
5. (a) |p_A - p_B| <= 3 sqrt(sigma_A^2 + sigma_B^2). The claimed value is the inverse-variance weighted mean of A and B;
   its sigma is that of the weighted mean, but never less than min(sigma_A, sigma_B).
   Both methods' codes are independent implementations (no shared source file).
6. (b) |p - table| <= 3 sqrt(sigma^2 + sigma_table^2); otherwise the discrepancy must be explained in the claim.
7. (c) "reproduces ... to at least 6 digits": |value - reference| <= 1e-6 and the code's own stated sigma <= 1e-6, for
   (i) the table bond value of the same lattice and (ii) kagome site (1 - 2 sin(pi/18)) or (3,12^2) site
   ((1 - 2 sin(pi/18))^(1/2)). Each method whose value enters the claim reports its own reproduction; if only one method
   reaches 6 digits, the claim says so and the CRITERION skeptic decides whether "the same code" is met.
8. (d) NOVELTY skeptic's literature search; a published site value for that lattice with sigma < 2e-6 kills the claim.
9. p2: a bond value of a 'citation needed' row with stated sigma <= 5e-8 by rule 4 (or by rule 3), plus the code's
   reproduction of the elongated triangular (TS) bond 0.41964035886369(2) or kagome bond 0.524404999167439(4) to
   <= 5e-8. Verdict: "confirms" if |delta| <= 3 sqrt(sigma^2 + sigma_table^2), "discrepancy" otherwise.
10. One lattice (one table cell) per claim.

## Calibration gate (the control for this target; fixed now)
Before any 2-uniform value is believed, each method's code must recover, blind to nothing but by its fixed pipeline:
square site 0.59274605079210 and triangular site 1/2 (within 3 of its sigmas), and kagome site exact; a bond code must
recover square bond 1/2 and the elongated triangular bond 0.41964035886369 within 3 of its sigmas. A method that misses
any of these by more than 3 sigma is dead for the claim until repaired (kill criterion 1).

null_test: not needed because the claim is a numerical estimate of a physical constant judged by two independent methods and by recovery of exactly known thresholds (the calibration gate above), not a search, key, period, language or beats-chance claim.
