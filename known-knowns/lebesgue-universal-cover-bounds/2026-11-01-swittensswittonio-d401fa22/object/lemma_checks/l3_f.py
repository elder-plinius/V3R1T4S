# L3: f(d) = area conv(D(0,1/2), p), |p|=d>=1/2.  (a) mp.iv enclosure of f(0.7) (b) exact-rational enclosure
# (c) sympy exact: Green-theorem area == closed form; f' = (1/2) sqrt(1-1/(4d^2)) > 0 (d) random break test.
import numpy as np, sympy as sp
from mpmath import mp, iv
from fractions import Fraction as F
from math import isqrt

def IACOS(x): return iv.atan2(iv.sqrt(1-x*x), x)   # arccos x = atan2(sqrt(1-x^2), x), x in (0,1)
print("=== (a) mpmath interval arithmetic (mp.iv, outward rounding) ===")
for dps in (30, 60, 100):
    iv.dps = dps
    d = iv.mpf('0.7')            # interval enclosing the decimal 0.7 (not the binary double)
    half = iv.mpf(1)/2
    # arccos via atan2: arccos(x)=atan2(sqrt(1-x^2),x); mp.iv has acos
    fd = (iv.pi - IACOS(half/d))/4 + iv.sqrt(d*d - iv.mpf(1)/4)/2
    print(f"dps={dps}: f(0.7) in {fd}")
    assert fd.a > iv.mpf('0.836548794').b, "fails 0.836548794"
    assert fd.a > iv.mpf('0.8344').b
    print("   lower end > 0.836548794 and > 0.8344 : OK ;  lower end - 0.8344 =", fd.a - iv.mpf('0.8344').b)
iv.dps = 30
# also the double 0.7 and the point d* where f=0.8344 (root bracket by interval bisection)
lo, hi = iv.mpf('0.69'), iv.mpf('0.70')
def ff(x): return (iv.pi - IACOS(iv.mpf(1)/2/x))/4 + iv.sqrt(x*x - iv.mpf(1)/4)/2
for _ in range(60):
    mid = (lo.a + hi.b)/2; mid = iv.mpf(mid)
    if ff(mid).b < iv.mpf('0.8344').a: lo = mid
    else: hi = mid
print("root of f(d)=0.8344 bracketed by interval bisection:", lo.a, hi.b, "(f increasing, so f(d)>0.8344 for d>=0.7 > hi)")

print("=== (b) exact rational enclosure, no floating point, no library for pi/atan ===")
def atan_inv(q, nterms):   # atan(1/q) series bounds, q int>=2 : returns (lo,hi) Fractions
    s = F(0); 
    for k in range(nterms):
        s += F((-1)**k, (2*k+1)*q**(2*k+1))
    nxt = F(1, (2*nterms+1)*q**(2*nterms+1))
    # alternating decreasing: true value between s and s + (-1)^nterms * nxt
    a, b = s, s + (nxt if nterms % 2 == 0 else -nxt)
    return (min(a, b), max(a, b))
a5 = atan_inv(5, 30); a239 = atan_inv(239, 12)
pi_lo = 16*a5[0] - 4*a239[1]; pi_hi = 16*a5[1] - 4*a239[0]       # Machin
print("pi in [", float(pi_lo), ",", float(pi_hi), "] width", float(pi_hi-pi_lo))
PI50=F('3.14159265358979323846264338327950288419716939937510'); assert pi_lo<PI50<pi_hi; print('Machin enclosure contains the textbook 50-digit pi: OK')
# sqrt(6) bounds
def sqrt_bounds(x, scale=10**30):
    r = isqrt(x.numerator*scale*scale//x.denominator); return F(r, scale), F(r+1, scale)
s6 = sqrt_bounds(F(6)); s024 = sqrt_bounds(F(24, 100))
# arccos(5/7) = 2 atan(1/sqrt6)   [tan(x/2)=sqrt((1-c)/(1+c))=sqrt((2/7)/(12/7))=1/sqrt6]
# atan(z)=z*sum (-1)^k z^(2k)/(2k+1) with z^2=1/6 exactly, z=1/sqrt6 in [1/s6hi, 1/s6lo]
def atan_z(z, N=40):      # z Fraction in (0,1): bounds of atan(z) with z rational
    s = F(0)
    for k in range(N): s += F((-1)**k, 2*k+1)*z**(2*k+1)
    nxt = z**(2*N+1)/(2*N+1)
    return (s, s+nxt) if N % 2 == 0 else (s-nxt, s)
zlo, zhi = 1/s6[1], 1/s6[0]
acos_hi = 2*atan_z(zhi)[1]; acos_lo = 2*atan_z(zlo)[0]
print("arccos(5/7) in [", float(acos_lo), ",", float(acos_hi), "]")
f_lo = (pi_lo - acos_hi)/4 + s024[0]/2
print("exact-rational lower bound of f(7/10) =", float(f_lo), " (Fraction numerator/denominator digits:", len(str(f_lo.numerator)), ")")
assert f_lo > F(8344, 10000) and f_lo > F(836548794, 10**9)
print("exact rational check: f(7/10) >= %s > 0.836548794 > 0.8344 : OK" % float(f_lo))

print("=== (c) sympy exact identities ===")
d, r, th, b = sp.symbols('d r theta beta', positive=True)
r_ = sp.Rational(1, 2)
beta = sp.acos(r/d)
# Green: boundary = segment p->T1, arc T1->T2 (far side, angle from beta to 2pi-beta, centre 0 radius r), segment T2->p
# put p=(d,0); T1=(r cos beta, r sin beta), T2=(r cos beta, -r sin beta); counter-clockwise: p -> T1 -> arc -> T2 -> p
t = sp.symbols('t', real=True)
def seg(P, Q):  # integral of (x dy - y dx)/2 on segment
    return sp.Rational(1, 2)*(P[0]*Q[1]-P[1]*Q[0])
p = (d, 0); T1 = (r*sp.cos(beta), r*sp.sin(beta)); T2 = (r*sp.cos(beta), -r*sp.sin(beta))
arc = sp.Rational(1, 2)*r**2*((2*sp.pi - beta) - beta)     # int (x dy - y dx)/2 = r^2 dtheta/2
area = seg(p, T1) + arc + seg(T2, p)
area = sp.simplify(area.subs(sp.sin(beta), sp.sqrt(1-(r/d)**2)))
target = r*sp.sqrt(d**2-r**2) + r**2*(sp.pi-beta)
diff = sp.simplify(sp.expand(area - target))
print("Green-theorem area minus [r sqrt(d^2-r^2) + r^2 (pi - acos(r/d))] =", diff)
assert diff == 0
fexpr = (sp.pi - sp.acos(1/(2*d)))/4 + sp.sqrt(d**2 - sp.Rational(1, 4))/2
print("closed form at r=1/2 equals paper's f:", sp.simplify(target.subs(r, r_) - fexpr) == 0)
fp = sp.simplify(sp.diff(fexpr, d))
print("f'(d) =", fp)
print("f'(d) - (1/2) sqrt(1 - 1/(4 d^2)) simplifies to", sp.simplify(fp - sp.sqrt(1-1/(4*d**2))/2))
print("f(1/2) =", sp.simplify(fexpr.subs(d, sp.Rational(1, 2))), "= pi/4 = area(D)")
# alternative independent derivation: support-function formula  A = (1/2) int (h^2 - h'^2) dtheta,  h = max(1/2, d cos theta)
h1 = d*sp.cos(th); 
beta2 = sp.acos(1/(2*d))
A_sf = sp.Rational(1, 2)*( 2*sp.integrate(h1**2 - sp.diff(h1, th)**2, (th, 0, beta2)) + (2*sp.pi-2*beta2)*sp.Rational(1, 4) )
A_sf = sp.simplify(A_sf)
print("support-function area formula minus f(d) =", sp.simplify(A_sf - fexpr))

print("=== (d) numerical break attempts ===")
import sys; sys.path.insert(0, '.')
from common import f as ff64, disc_points, hull_area
rng = np.random.default_rng(5)
worst = 0
for dd in rng.uniform(0.5, 1.6, 300):
    P = np.vstack([disc_points(20000), [[dd, 0.0]]])
    worst = max(worst, abs(hull_area(P) - float(ff64(dd))))
print("max |area conv(20000-gon inscribed + point) - f(d)| over 300 random d in [0.5,1.6]:", worst, "(inscribed polygon is inner: expected ~ r^2 pi^2/(N^2) ~ 1e-9)")
ds = np.linspace(0.5, 3, 200001); fv = ff64(ds)
print("min of f(d+) - f(d) over grid (strict increase):", np.diff(fv).min())
print("f(0.7) float64 =", float(ff64(0.7)), " d*: f=0.8344 at", float(np.interp(0.8344, fv, ds)))
