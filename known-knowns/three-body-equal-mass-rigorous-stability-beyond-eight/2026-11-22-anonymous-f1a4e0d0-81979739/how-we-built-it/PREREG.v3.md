# PREREG.v3 (frozen Sun Nov 22 19:44:01 UTC 2026); adds an equivalent route C3' for C3 and resets box sizes

Why: on row 2 (first run, box 1e-30) C1 passed but C3 failed only from width (12x12 charpoly and Taylor shift amplified
a 6e-5 monodromy width to 1e16). Runs with box 1e-55/1e-70 on rows 2, 3, 6, 9 were stopped before reaching C1-C3:
their centre enclosures (rows 3, 6, 9) were wider than the boxes, so C1 could not pass; nothing was scored.
Unchanged: criterion (bank p1, verbatim in PREREG.md), orbit order (2, 3, 6, 9), C1, C2 (PREREG.v2), known tests,
null_test line.

C3' (new, equivalent route; the claim passes C3 if C3 or C3' certifies). U = span(e_x, e_y, b_x, b_y, f(x0), R x0) is
M-invariant (M e = e, M b = b + T e, M f = f, M R x0 = R x0), so U^omega (dim 6) is M-invariant, contains
span(f, R x0), and det(lambda I - M) = (lambda - 1)^6 [U] x (lambda - 1)^2 [span(f, R x0)] x q_red(lambda), where q_red is
the characteristic polynomial of the map M induces on the 4-dim quotient U^omega / span(f, R x0) (the reduced
monodromy). The certificate builds z1..z4 in U^omega by an explicit formula in x0 (fixed COM-free vectors corrected along
two fixed COM-free vectors so that dH(z) = dL(z) = 0; P- and COM-conditions hold by construction), solves
B y = M z_i with B = [z1..z4, f, R x0, e_x, e_y, b_x, b_y, g1, g2] (B certified invertible by the ball solve), and takes the
4x4 block. Pass: for q_red = lambda^4 + a3 lambda^3 + a2 lambda^2 + a1 lambda + a0, with a = a3 and with a = a1 separately,
s^2 + a s + (a2 - 2) has certified positive discriminant and both roots strictly inside (-2, 2).
Box sizes are chosen per row so that the centre enclosure of G is narrower than the box; any row may be retried with a
larger precision or order (each attempt is logged; a deterministic certificate that passes is not a search statistic).
