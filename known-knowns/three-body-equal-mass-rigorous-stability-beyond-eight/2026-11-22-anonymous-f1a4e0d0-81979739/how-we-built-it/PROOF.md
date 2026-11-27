# What the certificate proves and why (all steps are checked by code in code/)

Setting (source Sect. 2.2): unit masses, G = 1, state x = (q1, q2, q3, v1, v2, v3) in R^12, x' = f(x).
Euler half-twist data x0(vx, vy) = ((-1,0), (0,0), (1,0), (vx,vy), (-2vx,-2vy), (vx,vy)).

1. Reversor. S(q1,q2,q3,v1,v2,v3) = (-q3, -q2, -q1, v3, v2, v1) satisfies f(Sx) = -S f(x), S^2 = I, S^T J S = -J
   (code/lemmas.py, exact sympy). x0 in Fix(S); P = COM = L = 0 at x0, hence along the orbit.
2. Square system. G(vx, vy, t) = (x2(t), y2(t), (v1(t) - v3(t)).q1(t)). If G = 0: q2 = 0, COM = 0 gives q3 = -q1,
   P = 0 gives v2 = -(v1 + v3), L = q1 x (v1 - v3) = 0 and (v1 - v3).q1 = 0 with q1 != 0 give v1 = v3: x(t) in Fix(S).
   Reversible-systems lemma: phi_t(Sy) = S phi_{-t}(y), so phi_2t(x0) = phi_t(x(t)) = phi_t(S x(t)) = S phi_{-t}(x(t))
   = S x0 = x0: periodic with period T = 2t. (q1 != 0 holds because the enclosure is collision-free.)
3. C1 (existence). Krawczyk operator on the box X = (vx, vy, t)_listed + [-1e-55, 1e-55]^3:
   K(X) = xhat - C G(xhat) + (I - C DG(X))(X - xhat) is inside X strictly, so G has a unique zero in X.
   G(xhat) and DG(X) come from validated Taylor integration (code/vt3b.py): coefficients in arb ball arithmetic over the
   current ball; tails bounded by Cauchy estimates from a complex Picard inclusion Z + D_rho f(B) in B on each step,
   with Re(r_ij^2) > 0 on B (so the principal branch of s^(-3/2) is holomorphic there); |x_k| <= sup_B|x - c| / rho^k,
   tail <= sup|x - c| kappa^N / (1 - kappa) at |h| <= kappa rho. DG columns: d/dvx, d/dvy from the variational
   equations, d/dt = grad G . f.
4. Monodromy. A = D phi_t(x0) enclosed over X (12 tangent directions); A^-1 = -J A^T J (A symplectic; canonical
   coordinates, unit masses); D phi_t at x(t) equals S A^-1 S by step 1; M = S A^-1 S A.
5. Trivial block (C2 + structure). U = span(e_x, e_y, b_x, b_y, f(x0), R x0) (translations, Galilei boosts, vector
   field, infinitesimal rotation): M e = e, M b = b + T e, M f = f, M R x0 = R x0 (equivariances; lemmas.py checks
   Df e = 0, Df b = e, Df Rx = R f). C2 certifies dim U = 6 (a 6x6 minor of [U] non-zero). omega(f, .) = dH and
   omega(Rx0, .) = dL vanish on U (lemmas.py), so f, Rx0 lie in U^omega (dim 6), which is M-invariant. Hence
   det(lambda I - M) = (lambda - 1)^6 (lambda - 1)^2 q_red(lambda), where q_red is the characteristic polynomial of the
   map M induces on the 4-dim quotient U^omega / span(f, Rx0): the reduced monodromy.
6. C3' (ellipticity). z1..z4 in U^omega by an explicit continuous formula in x0 (COM-free vectors corrected so
   dH(z) = dL(z) = 0); coordinates of M z_j in the basis [z1..z4, f, Rx0, e_x, e_y, b_x, b_y, g1, g2] by a certified
   ball solve; the 4x4 block's charpoly lambda^4 + a3 lambda^3 + a2 lambda^2 + a1 lambda + a0 is palindromic for the
   true matrix (symplectic), so its roots are lambda with lambda + 1/lambda = s, s^2 + a s + (a2 - 2) = 0. Certified:
   discriminant > 0 and both s strictly in (-2, 2), separately with a = a3 and a = a1. So the four non-trivial
   multipliers are e^{+-i theta1}, e^{+-i theta2}, theta1 != theta2, none equal to +-1: distinct and on the unit circle.
   (C3, the 12x12 charpoly divided by (lambda-1)^8 via an exact Taylor shift, is reported as a second route.)
Not claimed: non-resonance and twist (KAM). Labels: steps 1, 2, 4, 5 PROVED-HERE (symbolic identities) / KNOWN
(reversibility lemma, Cauchy estimates, Krawczyk theorem); steps 3, 6 PROVED-HERE by the interval computation.
