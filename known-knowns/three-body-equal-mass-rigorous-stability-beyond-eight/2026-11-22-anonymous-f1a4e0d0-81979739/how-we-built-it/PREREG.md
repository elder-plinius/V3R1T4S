# PREREG (frozen Sun Nov 22 19:14:45 UTC 2026)

Target: three-body-equal-mass-rigorous-stability-beyond-eight; claim aimed at partial win p1 (then p2).

Criterion (verbatim, bank p1): "A computer-assisted proof of existence and linear stability (certified ellipticity of
the reduced monodromy) for one listed solution other than the figure-eight, with no prior rigorous linear-stability
proof found by a literature search."

Pre-registered order of orbits (global row numbers in data/ics_971_100_num.txt): 2 (Intermediate-Moth region first),
then 3 (Schubart/S), 6 (Figure-8 region, first after the eight), 9 (Broucke). p2 only if all four pass.

Certificate (all in outward-rounded ball arithmetic, python-flint arb; every test strict):
C1. Krawczyk: for G(vx, vy, t) = (x2(t), y2(t), (v1(t) - v3(t)) . q1(t)) on a box X around the listed (vx, vy, T/2),
    K(X) = xhat - C G(xhat) + (I - C DG(X))(X - xhat) lies in the interior of X (C = inverse of mid DG). Taylor
    remainders bounded by Cauchy estimates from a verified complex Picard inclusion on every step.
C2. Six invariant gradients (H, L, Px, Py, Fx, Fy with F = Sum q - 2t Sum v) at x0 independent: some 6x6 minor
    certified non-zero over X.
C3. M = S A^{-1} S A (A = D phi_t enclosed over X, t in the Krawczyk time interval), p = charpoly(M), q = p/(lambda-1)^8
    by Taylor shift; with q = lambda^4 + a lambda^3 + b lambda^2 + a' lambda + 1, certify for the quadratic
    s^2 + a s + (b - 2): discriminant > 0 and both roots strictly inside (-2, 2). (Both a and a' enclosures are used:
    each must give the result.)
Consistency (not a pass criterion, reported): the certified frequencies w = arccos(s/2)/(2 pi) enclose the source's
40-digit w1, w2 for that row.
Known-positive / known-negative tests before scoring: the figure-eight row 1 must pass C1-C3 and reproduce its angles;
a row-2 box shifted by 1e-6 in vx must fail C1.

null_test: not needed because the claim is an explicit interval certificate checked deterministically (no search
or statistical inference is scored).
Novelty gate: literature search repeated by the NOVELTY skeptic before any claim.
