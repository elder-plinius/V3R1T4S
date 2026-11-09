# How the finite hypotheses are certified

The table V is an arbitrary array of binary64 numbers. How it was built does not matter (`build_V.py`: dynamic programming, then Gaussian smoothing in phi). Only the checks below count.

Notation: T = 501/1000, b = 35/10000, rho in [rho_-, rho_+] = [1/sqrt2 - b, 1/sqrt2 + b], beta = -(85/100) i, gamma = 1/2 + (866/1000) i, L = 8, Lam0 = 5, Lam1 = 10, alpha = 6/5, p(x) = Lam1 x^alpha, x = e^tau. Grid: tau_i = -8 + i/200, i = 0..1600, phi_j = 2 pi j/2514. V is bilinear on each cell.

Define, for (y,w) with y in the band and |y - w| <= T, on a cell C with bilinear function V_C:

    G_C(tau,phi; y,w) = d_tau V_C + (Im w/y) d_phi V_C + |w| V_C - T|w + beta x y| + 2 y x Re(gamma beta e^{i phi}) + p(x) e(w,y),
    e(w,y) = mu(y) + Re w - y|w| = ((|w|-y^2)^2 + T^2 - |y-w|^2)/(2y).

(HJB) says G_C >= kappa on the whole disc. The check proves this with kappa = 1e-6, in four reductions.

## Reduction 1: from the disc to the circle (ray lemma)

Fix C, (tau,phi), y. Since T < rho_- <= y, the origin is outside the disc D = {w: |y-w| <= T}. Take any ray {t u: t >= 0}, |u| = 1, meeting D. D is convex, so the ray meets D in a segment whose ends lie on the circle |y-w| = T. On the ray, |w| = t and Re w, Im w are linear in t, so e(w,y) = mu(y) + Re w - y|w| and every term of G_C other than -T|w + beta x y| are affine in t. The term -T|t u + beta x y| is concave in t. So G_C is concave on the segment and takes its minimum at an end. This holds for every real value of V_C, d_tau V_C, d_phi V_C and p. Hence the minimum of G_C over D is attained on the circle, where w = y - T e^{i psi} and e = (W - y^2)^2/(2y), W = |w|.

The same argument applies to the TERM expression Re(gamma(y - w - beta y)) + Lam0 e(w,y) on the half disc D+ = D intersected with {Im w >= 0}: a ray in the closed upper half plane meets D+ in a segment with both ends on the circle, or on the real axis, where the ray is the real axis itself and the ends are y - T and y + T, again on the circle. So the minimum on D+ is on the arc psi in [pi, 2 pi].

## Reduction 2: from the cell to its corners

Fix (y,psi). The V part d_tau V_C + (Im w/y) d_phi V_C + W V_C is bilinear in (tau,phi), since d_tau V_C is affine in phi, d_phi V_C is affine in tau, and V_C is bilinear. Let Y(tau,phi) be the remaining terms. Writing I for bilinear interpolation at the four corners,

    G_C = I[V part + Y] + (Y - I[Y]) >= min over corners of G_C - E_ab,

where E_ab bounds I[Y] - Y from above: Y - I[Y] >= -(d^2/8) K_tau - (dphi^2/8) K_phi if Y_tautau <= K_tau and Y_phiphi <= K_phi on the cell. With x_hi = e^{tau_{i+1}}:

- -T|w + beta x y| is concave in x, and x = e^tau, so its tau second derivative is at most its x-Lipschitz constant times x, at most T|beta| y x.
- 2 y x Re(gamma beta e^{i phi}) has tau and phi second derivatives at most 2 y x |beta|, using |gamma| <= 1.
- p(x) e has tau second derivative Lam1 alpha^2 x^alpha e, with e <= e_max = u_max^2/(2 rho_-), u_max = rho_+ + T + rho_+^2, because |W - y^2| <= W + y^2 <= y + T + y^2.

So K_tau = rho_+ x_hi |beta| (T + 2) + Lam1 alpha^2 x_hi^alpha e_max, K_phi = 2 rho_+ x_hi |beta|.

## Reduction 3: from all rho to a grid of 9 values

Fix a corner and psi. In y (with psi fixed), the second derivatives are:

- (-T sin psi/y) V_phi: at most 2T|V_phi|/rho_-^3.
- W V: W_yy = T^2 sin^2 psi/W^3 is at most 1/W, because W >= T|sin psi|, and at most 1/(rho_- - T) because W >= y - T. So at most |V|/(rho_- - T).
- -T|y(1 + beta x) - T e^{i psi}|: the inside is affine in y, so this is concave and contributes nothing to an upper bound.
- 2 y x Re(...): linear.
- p e with e = u^2/(2y), u = W - y^2, |u_y| <= 1 + 2 rho_+ (since |W_y| <= 1), |u_yy| <= 1/(rho_- - T) + 2: e_yy = (u_y^2 + u u_yy)/y - 2 u u_y/y^2 + u^2/y^3, so e_yy <= e_rr := (u_y,max^2 + u_max u_yy,max)/rho_- + 2 u_max u_y,max/rho_-^2 + u_max^2/rho_-^3.

If f'' <= K on an interval of length dl, then f >= chord of f - K dl^2/8, which is the bound used throughout. It gives G >= min over the nine rho of G - E_r, with E_r = (dr^2/8)(p e_rr + 2T max|V_phi|/rho_-^3 + max|V|/(rho_- - T)), dr = 2b/8.

## Reduction 4: from all psi to an adaptive grid

Fix a corner and rho = y. In psi:

- (-T sin psi/y) V_phi: at most T|V_phi|/y.
- W(psi) = |y - T e^{i psi}|: from W^2 = y^2 + T^2 - 2 y T cos psi, one gets W'' = T y (y cos psi - T)(y - T cos psi)/W^3. Both factors have modulus at most W, because W^2 = (y cos psi - T)^2 + y^2 sin^2 psi = (y - T cos psi)^2 + T^2 sin^2 psi. So |W''| <= T y/W <= T rho_+/(rho_- - T) =: Wpp. Also |W'| = T y |sin psi|/W <= T because W >= y|sin psi|.
- e = u^2/(2y), u = W - y^2: e'' = (W'^2 + u W'')/y <= epp := (T^2 + u_max Wpp)/rho_-.
- f(psi) = |a - T e^{i psi}| with a = y(1 + beta x), |a| > T: the same formula gives |f''| <= T|a|/f <= T|a|/(|a| - T). So -T f'' <= T^2 |a|/(|a| - T). The code asserts |a| > T.

So K_psi = T|V_phi|/y + |V| Wpp + p epp + T^2 |a|/(|a| - T). Each cell starts with 64 intervals of psi; an interval whose chord bound is too low is split into 4, down to depth 6, and the cell counts as failing if a bound is still below the requirement at the last depth.

## TERM and INIT

TERM: on psi in [pi, 2 pi], 65536 intervals, chord bound with K = T|gamma| + Lam0 epp, plus (dr^2/8) Lam0 e_rr for rho. The value used is m = that minimum minus the table entry V[1600][0].

INIT: V[0][j] >= T + (T + 2)|beta| e^{-8} at all nodes; V(-8,·) is linear between nodes, so the nodes suffice.

## Rounding

`check_hjb.py` uses binary64 numpy. The requirement carries a pad of 1e-10 per bound. G is a sum of at most about 15 terms, each of modulus below 1000 (differences of the table divided by d or dphi are below 1 in modulus, see the Lipschitz report), each from a few operations with relative error below 4 ulps, so the accumulated error is far below 1e-10. This is a pad argument, not interval arithmetic. `code/check2.c` is a separate C program with outward-rounded interval arithmetic and adaptive subdivision, reported as written separately from `check_hjb.py`. It widens every floating operation by one ulp and each result of sin, cos and exp by 4 ulps, and builds with `-ffp-contract=off`. So it assumes that Apple libm is within 4 ulps and that the machine rounds to nearest, without flush to zero. These are assumptions, not proved. It uses no corner argument: every box goes through interval jets. Its log files, with the rows each one covers, are listed in `verify-it-yourself/RECEIPTS.md`.
