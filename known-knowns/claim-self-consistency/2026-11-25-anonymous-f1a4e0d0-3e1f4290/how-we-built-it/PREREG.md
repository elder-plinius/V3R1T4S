# PREREG (frozen 2026-11-25T19:11:58Z, before any energy is computed)

Criterion (verbatim, charter claim-self-consistency Shape): "counterexample (an explicit parameter set quoted from the
source under which its own equations contradict its conclusion) or bound (a certified lower bound on the power, energy
or field the claimed effect requires)."

null_test: not needed because the claim is a deterministic bound (a proof plus quadrature of a stated formula by two
methods), not a search, detection or "beats chance" statistic.
Step 3c (baseline): not applicable (no benchmark score).

## Claim to be tested (C1, bound)
Source operating point: bubble diameter 1 cm (R = 5.000e-3 m), boost gamma_target = 1 + 1e-7 ("on the order of
1.0000001"). Source equations: Eq. (1), f(r), Eq. (3), gamma = cosh(0.5 ln|1 - v^2 f^2|).
C1: for every sigma > 0 and every v_s for which max over space of gamma >= gamma_target, the total energy
E = integral of T00 over the spatial slice (SI: T00_SI = (c^4/G) T00_geom) satisfies
  E <= -(c^4 / (48 G)) * u*^2 * R,
where u* solves (2 - u^2) / (2 sqrt(1 - u^2)) = gamma_target, u* < 1 (the source's own gamma formula).
Also reported, same bound with the slide's own "~0.0004c" (u = 4e-4) in place of u*.
Conclusion contradicted: "something as simple as a very high-voltage capacitor ring" / "toroidal-ring of positive
energy density" generating the boost: (i) sign: Eq. (3) is <= 0 everywhere and its integral strictly negative for
v_s > 0; (ii) magnitude: the bound in kg (E/c^2).

C1 holds only if all of these hold:
(a) Proof (formalist), every step labelled: (1) max gamma >= gamma_target iff v_s >= u*; (2) angular integral gives
    E = -(c^4/(12 G)) beta^2 * I(sigma), I = integral_0^inf f'(r)^2 r^2 dr; (3) I >= R f(R)^2 >= R/4 for all sigma.
(b) Numerical certificate (evaluator): Method A: I(sigma) by mpmath quad at 30 digits on [0, inf) split at R;
    Method B: E from a direct 3D Cartesian midpoint integration of Eq. (3) itself (not the reduced 1D form) on a
    grid, at 3 resolutions. Thresholds: (i) A and B agree within 1e-3 relative at sigma R in {0.5, 1, 2, 5} at the
    finest grid; (ii) Method A minimum over sigma (golden-section on log sigma, bracket sigma R in [1e-3, 1e3], plus a
    log grid of 601 points) satisfies E_min <= closed-form bound (i.e. |E_min| >= bound) and the bound <= -1e30 J for
    both u readings; (iii) known-case tests: v = 0 gives 0; at sigma R = 50, A matches the thin-wall asymptote
    -(c^4/G) beta^2 R^2 sigma / 36 within 5 %.
Constants: c = 299792458 m/s (exact), G = 6.67430e-11 m^3 kg^-1 s^-2 (CODATA 2018).

## Side results (reported, not part of C1)
S1 quarter-wave check: fractional optical path change needed for lambda/4 at 633 nm over 1 cm (single and double
pass) vs 1e-7. S2 boost-100 example vs Eq. (1) ship coordinate velocity v_s + v_i. S3 Casimir comparison (steelman).
