# Proof of the C1 bound (labels per kit/RULES.md rule 1)

Setting (quoted from White 2011, NTRS 20110015936): metric Eq. (1) with shape function
f(r) = [tanh(s(r+R)) - tanh(s(r-R))] / (2 tanh(sR)), s = sigma > 0, R > 0; energy density Eq. (3)
T00 = -(1/8pi) v^2 rho^2 / (4 r^2) (df/dr)^2 (G = c = 1; rho^2 = y^2 + z^2, r^2 = x^2 + y^2 + z^2 in the bubble frame);
boost gamma = cosh(0.5 ln|1 - v^2 f^2|).

**Step 1 (PROVED-HERE). f(0) = 1, f(R) = 1/(1 + tanh^2(sR)) >= 1/2, f -> 0 as r -> inf, and f is continuous.**
f(0) = 2 tanh(sR)/(2 tanh(sR)) = 1. At r = R: f(R) = tanh(2sR)/(2 tanh(sR)); with tanh(2x) = 2 tanh x/(1 + tanh^2 x),
f(R) = 1/(1 + tanh^2(sR)), and tanh^2 < 1 gives f(R) > 1/2. As r -> inf both tanh terms -> 1, so f -> 0.

**Step 2 (PROVED-HERE). max over space of gamma >= g (g > 1) iff v >= u*, where u* in (0,1) solves
(2 - u^2)/(2 sqrt(1 - u^2)) = g.**
Take v >= 0 (the sign of v only sets the direction; E depends on v^2). Write u = v f(r) >= 0. For u < 1, cosh(0.5 ln(1 - u^2)) = ((1-u^2)^(1/2) + (1-u^2)^(-1/2))/2 = (2 - u^2)/(2 sqrt(1-u^2)),
which is strictly increasing on [0,1) (with w = 1 - u^2 in (0,1], (w^(1/2) + w^(-1/2))/2 decreases in w because its
w-derivative (w^(-1/2) - w^(-3/2))/4 <= 0), equals 1 at u = 0 and diverges as u -> 1. So u* exists uniquely.
(If) If v >= u*: f is continuous from f(0) = 1 to 0 (Step 1), so some r has v f(r) = u*, where gamma = g.
(Only if) If v < u* (< 1): every point has u = v f <= v < u* (0 <= f <= 1 on r >= 0, since each tanh term difference is
bounded by the value at r = 0 ... see note), so gamma < g everywhere.
Note on 0 <= f <= 1 (PROVED-HERE): f >= 0 since tanh is increasing and r + R > r - R. f(r) <= 1: tanh(s(r+R)) -
tanh(s(r-R)) as a function of r has derivative s[sech^2(s(r+R)) - sech^2(s(r-R))] <= 0 for r >= 0 (|r+R| >= |r-R|), so it
is maximal at r = 0 where it equals 2 tanh(sR).
Numerical cross-check (NUMERICAL): u* = 0.0299002893428026 for g = 1 + 1e-7 (result/check_bound_output.txt).

**Step 3 (PROVED-HERE). Total energy (the integral of Eq. (3) over the spatial slice, as the source uses it; not an ADM mass) E = -(c^4/(12 G)) beta^2 I(s), I(s) = int_0^inf f'(r)^2 r^2 dr.**
The spatial slices of Eq. (1) at fixed t have metric dx^2 + dy^2 + dz^2 (flat), so the volume element is dx dy dz =
r^2 dr dOmega in bubble-centred spherical coordinates with rho = r sin(theta). Then int rho^2/r^2 dOmega =
int sin^2(theta) dOmega = 8pi/3, so E_geom = -(1/8pi)(v^2/4)(8pi/3) I = -(v^2/12) I. In SI, an energy density in
geometric units (m^-2) times c^4/G gives J/m^3, and v = beta (units of c): E = -(c^4/(12 G)) beta^2 I with I in metres.

**Step 4 (PROVED-HERE). I(s) >= R f(R)^2 >= R/4 for every s > 0.**
For any a > 0, since f -> 0: f(a) = -int_a^inf f'(r) dr <= int_a^inf |f'| r * r^(-1) dr
<= (int_a^inf f'^2 r^2 dr)^(1/2) (int_a^inf r^(-2) dr)^(1/2) <= I^(1/2) a^(-1/2) (Cauchy-Schwarz).
So I >= a f(a)^2; take a = R and use Step 1.

**Step 5 (PROVED-HERE). C1: if max gamma >= g then E <= -(c^4/(48 G)) u*^2 R.**
Steps 2, 3, 4: beta >= u* and I >= R/4.

**Step 6 (NUMERICAL). Values.** c = 299792458 m/s, G = 6.67430e-11, R = 5e-3 m:
u* reading: E <= -1.127084914e37 J (mass equivalent -1.25405e20 kg); slide's 0.0004c reading:
E <= -2.017092607e33 J (-2.24432e16 kg). The true minimum over s is about 2.7x larger in magnitude (result/eval3d_output.txt).

**Step 7 (PROVED-HERE). Sign.** T00 in Eq. (3) is minus a product of squares, so T00 <= 0 everywhere; for v > 0 and
any s, f' is not identically zero (f goes from 1 to 0), so E < 0 strictly. A source of "positive energy density"
cannot supply Eq. (3).

Scope: this bounds the energy the source's own equations assign to its own operating point (boost 1.0000001, 1 cm).
It says nothing about whether other metrics or other stress-energy could produce an interferometer signal.
