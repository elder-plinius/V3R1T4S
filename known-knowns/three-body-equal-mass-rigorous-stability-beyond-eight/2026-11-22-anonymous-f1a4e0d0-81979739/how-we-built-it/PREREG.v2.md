# PREREG.v2 (frozen Sun Nov 22 19:16:53 UTC 2026); replaces C2 of PREREG.md only

Why: PREREG.md C2 used F = Sum q - T Sum v as a phi_T-invariant; it is not (F(phi_T x) = Sum q(0)), so that check
would not justify the trivial block. Changed before any certificate (C1-C3) was computed on any orbit; the only output
so far is a point integration of the figure-eight (known-positive test of the integrator, G enclosed to 1e-48).
Everything else in PREREG.md (criterion, orbit order, C1, C3, consistency check, known-positive/negative tests,
null_test line) stands unchanged.

C2 (new). Let U = span(e_x, e_y, b_x, b_y, f(x0), R x0), where e = COM translations (dq_i = e), b = boosts (dv_i = e),
f the vector field, R x0 = (J q_i, J v_i) the infinitesimal rotation. Exactly: M e = e, (M - I) b = T e, M f = f,
M R x0 = R x0 (translation, Galilei, time and rotation equivariance), so U lies in the generalized eigenspace E_1 of M
for eigenvalue 1; E_1 is symplectic; omega(f, .) = dH and omega(Rx0, .) = dL vanish on U at x0 (P = 0, COM = 0,
H and L invariant under translations/rotations), so f, R x0 span a 2-dim radical of omega|U. Hence dim E_1 >= 6 + 2 = 8
and (lambda - 1)^8 divides det(lambda I - M). The certificate checks, in ball arithmetic over the box, that the 12 x 6
matrix [e_x e_y b_x b_y f(x0) R x0] has a 6 x 6 minor certified non-zero. Pass only if it does.
