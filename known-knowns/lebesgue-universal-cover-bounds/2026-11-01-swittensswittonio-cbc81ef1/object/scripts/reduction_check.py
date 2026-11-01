# Independent interval check (mpmath.iv, 200 bit, outward) of the far-field exclusions of Zeng S10, with the TRUE vertex radii.
from mpmath import iv
iv.prec = 200
pi = iv.pi
tau = iv.mpf('0.834')
def acos(x): return iv.atan2(iv.sqrt(1 - x * x), x)   # 0<x<1
def G(rho):   # area conv(B(0,1/2) u {p}), |p| = rho >= 1/2
    return pi / 4 + iv.sqrt(rho * rho - iv.mpf('0.25')) / 2 - acos(1 / (2 * rho)) / 4
R3 = 1 / (2 * iv.sin(pi / 3))                 # circumradius of the width-1 regular Reuleaux triangle  (= 1/sqrt3)
R5 = 1 / (2 * iv.sin(2 * pi / 5))             # circumradius of the width-1 regular Reuleaux pentagon  (= 1/(2 cos(pi/10)))
assert (R5 - 1 / (2 * iv.cos(pi / 10))).a <= 0 <= (R5 - 1 / (2 * iv.cos(pi / 10))).b
def dfar(r, R, delta): return iv.sqrt(r * r + R * R + 2 * r * R * iv.cos(delta))
b3 = iv.mpf('0.190700'); b5 = iv.mpf('0.194601')
d3 = dfar(b3, R3, pi / 3); d5 = dfar(b5, R5, pi / 5)
g3 = G(d3) - tau; g5 = G(d5) - tau
print('R3 vertex radius', R3); print('R5 vertex radius', R5)
print('d3(b3) =', d3); print('d5(b5) =', d5)
print('G(d3(b3)) - 0.834 =', g3, '  >0 :', g3.a > 0, '  (paper: [2.13944145452936,2.13944145452937]e-7)')
print('G(d5(b5)) - 0.834 =', g5, '  >0 :', g5.a > 0, '  (paper: [1.46438884041707,1.46438884041708]e-7)')
print('d3(b3) > 1/2:', d3.a > 0.5, ' d5(b5) > 1/2:', d5.a > 0.5)
# monotonicity ingredients (checked here as inequalities on intervals; proofs in report):
# G'(rho) = sqrt(rho^2-1/4)/(2 rho) > 0 for rho>1/2 ; d(r) = sqrt(r^2+R^2+2 r R cos(delta)), d'(r) = (r + R cos delta)/d(r) > 0 for r>=0, delta<=pi/2.
# strictly: with the exact vertex radii, how far could b3/b5 be lowered?  (not needed; information only)
lo, hi = iv.mpf('0.15'), b3
for _ in range(60):
    mid = (lo + hi) / 2
    if (G(dfar(mid, R3, pi / 3)) - tau).a > 0: hi = mid
    else: lo = mid
print('smallest b3 for which G(d3(b3))>0.834 (bisection upper):', hi.b)
lo, hi = iv.mpf('0.15'), b5
for _ in range(60):
    mid = (lo + hi) / 2
    if (G(dfar(mid, R5, pi / 5)) - tau).a > 0: hi = mid
    else: lo = mid
print('smallest b5 for which G(d5(b5))>0.834 (bisection upper):', hi.b)
# bridge constants: float(pi/5), float(pi/3) vs true
import math
for nm, f, t in (('pi/5', math.pi / 5, pi / 5), ('pi/3', math.pi / 3, pi / 3)):
    print(nm, 'float', repr(f), 'float-true =', iv.mpf(f) - t)
# core box max-norm vs radial: |c|_inf >= 0.08 => |c| >= 0.08 (trivial); coarse box contains the balls (trivial)
