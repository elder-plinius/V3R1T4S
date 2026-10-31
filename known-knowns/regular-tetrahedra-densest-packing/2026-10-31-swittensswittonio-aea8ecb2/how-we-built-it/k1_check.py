"""K1 cross-checks (NOT used as proof inputs; the proof of K1 is in REDUCTION_FULL.md section 3).
 (1) the elementary closed form a(e) = (1/pi)[atan(sqrt((1-e^2)/2)) - (e/sqrt3) acos(e sqrt2/sqrt(3-e^2))] (derived in 3.1 by one integration by parts)
     against Arb quadrature of the defining integral  A_away(e) = (1/2pi) int_{-theta/2}^{theta/2} G(e,cos phi) dphi,
     G(e,c) = sqrt(1-e^2) - e c acos(e c / sqrt(1-e^2+e^2c^2));
 (2) the same closed form against the Gauss-Bonnet closed form used in earlier versions and against Monte-Carlo area of the 'away' wedge.
Run with the venv python (python-flint)."""
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flint import arb, acb, ctx
import fullchain as F
ctx.prec = 120
th = F.TH
def Gacb(e, c):
    """G(e,c) for complex c on a small neighbourhood of the real segment; returns NaN-ball if analyticity cannot be guaranteed"""
    k2 = 1 - e * e + (e * c) ** 2
    if not (k2.real > 0):
        return acb(float('nan'))
    w = e * c / k2.sqrt()
    one_minus = 1 - w * w
    if not (one_minus.real > 0):
        return acb(float('nan'))
    return acb((1 - e * e).sqrt()) - e * c * w.acos()
print("e      | (1/2pi)int G (Arb)  - closed form (enclosure of the difference)")
worst = 0
for e in [0.01, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.95, 0.97]:
    ea = arb(e)
    I = acb.integral(lambda x, an: Gacb(ea, x.cos()), acb(-th / 2), acb(th / 2)) / (2 * arb.pi())
    cf = (((1 - ea * ea) / 2).sqrt().atan() - ea / F.S3 * (ea * F.S2 / (3 - ea * ea).sqrt()).acos()) / arb.pi()
    diff = I.real - cf
    print("%.2f   | %s" % (e, diff.str(5)))
    worst = max(worst, abs(float(diff.mid())) + float(diff.rad()))
print("max |difference| + radius over the grid: %.3e" % worst)
# Gauss-Bonnet closed form of the earlier reductions
def a_gb(r):
    h2 = r * r / 3; h = r / math.sqrt(3)
    phi = math.acos((1 / 3 + h2) / (1 - h2)); psi = 2 * math.asin(math.sqrt(1 - r * r) / math.sqrt(1 - h2))
    return (2 * phi - 2 * h * psi) / (4 * math.pi)
def a_new(e):
    return (math.atan(math.sqrt((1 - e * e) / 2)) - e / math.sqrt(3) * math.acos(e * math.sqrt(2) / math.sqrt(3 - e * e))) / math.pi
print("max |a_new - a_GB| over 2000 points of [0,0.99]:", max(abs(a_new(i / 2000 * 0.99) - a_gb(i / 2000 * 0.99)) for i in range(2001)))
# Monte Carlo: area fraction of the away wedge (edge direction z, apex (e,0), opening toward +x, half-angle theta/2) on the unit sphere
import numpy as np
rng = np.random.default_rng(12345)
N = 4_000_000
P = rng.normal(size=(N, 3)); P /= np.linalg.norm(P, axis=1)[:, None]
thv = math.acos(1 / 3)
for e in [0.0, 0.2, 0.5, 0.8, 0.9]:
    ang = np.arctan2(P[:, 1], P[:, 0] - e)
    inside = np.abs(ang) <= thv / 2
    # points with x<e-ish handled by the angle test (apex at (e,0))
    print("e=%.1f  MC away-wedge fraction %.5f  +- %.5f   closed form %.5f" % (e, inside.mean(), math.sqrt(inside.mean() * (1 - inside.mean()) / N), a_new(e)))
