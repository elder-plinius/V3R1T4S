# L9: dyadic bisection with (1+eps) widening, floating-point semantics of the verifier's split_cover (verifyB.py).
#  A. deterministic split schedule (coordinate and half-width are path independent) and the depth at which the
#     sufficient exact-cover condition  h*eps' >= u(2|c| + h(1+lambda))  stops holding.
#  B. exact (integer) check of ALL 22 root splits (4,194,303 splits) with virtual-end bookkeeping for the true domain.
#  (C = l9_depth.py: certificate decode / max split depth;  D = l9_random_exact.py: random exact-cover experiment)
import numpy as np, math, struct, gzip, sys, time
from fractions import Fraction as F
INFL = 1e-11
u = 2.0**-53
lam = 1.0 + INFL                       # the double actually used
epsp = lam - 1.0                       # eps' (exact, as a double difference)
def corners5():
    n = 5; m = 2; circ = 1.0/(2.0*np.sin(np.pi*m/n)); a = 2.0*np.pi*np.arange(n)/n
    V = np.stack([circ*np.cos(a), circ*np.sin(a)], 1); return float(np.max(np.hypot(V[:, 0], V[:, 1])))
CIRC5 = corners5()
print("CIRC5 (as float in verifyB) =", repr(CIRC5), "; double(1+1e-11) - 1 =", repr(epsp))
print("=== A. split schedule ===")
h = [0.7, 0.7, np.pi/5, 0.7, 0.7]          # h3x,h3y,hrho,h5x,h5y  (root box of verifyB)
cmax = [0.7, 0.7, 2*np.pi/5, 0.7, 0.7]
def suff(hk, ck): return hk*epsp >= u*(2*ck + hk*(1+lam))
sched = []
fail_depth = None
for d in range(0, 90):
    w = [h[0], h[1], CIRC5*h[2], h[3], h[4]]; k = int(np.argmax(w)); hk = h[k]
    ok = suff(hk, cmax[k]+hk)               # |c| <= cmax (box ends) ; be generous: use c+h
    sched.append((d, k, hk, ok))
    if fail_depth is None and not ok: fail_depth = d
    h[k] = (hk*0.5)*lam
print("coordinate order for the first 30 splits:", [s[1] for s in sched[:30]])
for d in (0, 10, 22, 40, 60, 62, 64, 70, 76, 80, 89): print(f"  depth {d}: split coord {sched[d][1]}, h_split = {sched[d][2]:.4e}, sufficient condition holds: {sched[d][3]}")
print("FIRST DEPTH AT WHICH THE SUFFICIENT CONDITION FAILS:", fail_depth)
print("  threshold h* (translations, |c|+h<=0.7+h):", 2*0.7*u/(epsp-u*(1+lam)))
print("=== B. exact check of the 22 root splits with virtual domain ends ===")
SC = 2**200
def I(x): return int(math.ldexp(x, 200))        # exact for doubles with lsb >= 2^-200
def Ifl(fr): return (fr.numerator*SC)//fr.denominator
def Ice(fr): return -((-fr.numerator*SC)//fr.denominator)
# rational enclosure of pi (Machin, as in l3_f.py) -> upper bound for 2pi/5
def atan_inv(q, nt):
    s = F(0)
    for k in range(nt): s += F((-1)**k, (2*k+1)*q**(2*k+1))
    nxt = F(1, (2*nt+1)*q**(2*nt+1)); a, b = s, s + (nxt if nt % 2 == 0 else -nxt); return min(a, b), max(a, b)
a5 = atan_inv(5, 30); a239 = atan_inv(239, 12); pi_hi = 16*a5[1]-4*a239[0]; pi_lo = 16*a5[0]-4*a239[1]
vlo0 = [Ifl(F(-7, 10)), Ifl(F(-7, 10)), 0, Ifl(F(-7, 10)), Ifl(F(-7, 10))]
vhi0 = [Ice(F(7, 10)), Ice(F(7, 10)), Ice(2*pi_hi/5), Ice(F(7, 10)), Ice(F(7, 10))]
# stored root: (c,h) per coordinate as doubles
c0 = [0.0, 0.0, np.pi/5, 0.0, 0.0]; h0 = [0.7, 0.7, np.pi/5, 0.7, 0.7]
stats = dict(splits=0, minslackL=None, minslackR=None, minoverlap=None, fail=0)
def upd(key, v):
    if stats[key] is None or v < stats[key]: stats[key] = v
t0 = time.time()
stack = [(c0, h0, vlo0, vhi0, 0)]
seeds = 0
minsl = [None]*5
while stack:
    c, hh, vlo, vhi, d = stack.pop()
    if d == 22:
        seeds += 1
        for k in range(5):
            if not (I(c[k]) - I(hh[k]) <= vlo[k] and vhi[k] <= I(c[k]) + I(hh[k])): stats['fail'] += 1   # I(c)-I(h) exact? c-h computed on ints: exact
        continue
    w = (hh[0], hh[1], CIRC5*hh[2], hh[3], hh[4]); k = int(np.argmax(w))
    half = hh[k]*0.5; cl = c[k]-half; cr = c[k]+half; hc = half*lam
    L_lo, L_hi, R_lo, R_hi = I(cl)-I(hc), I(cl)+I(hc), I(cr)-I(hc), I(cr)+I(hc)
    stats['splits'] += 1
    # NOTE I(cl) is the float cl (the verifier's stored child centre), so L_lo etc. are exact reals of the stored boxes
    ok = (L_lo <= vlo[k]) and (R_hi >= vhi[k]) and (L_hi >= R_lo)
    if not ok: stats['fail'] += 1
    sl = (vlo[k]-L_lo, R_hi-vhi[k], L_hi-R_lo)
    for key, v in zip(('minslackL', 'minslackR', 'minoverlap'), sl): upd(key, v)
    m = L_hi
    for (cc, lo2, hi2) in ((cl, vlo[k], m), (cr, m, vhi[k])):
        c2 = list(c); h2 = list(hh); c2[k] = cc; h2[k] = hc
        vl = list(vlo); vh = list(vhi); vl[k] = lo2; vh[k] = hi2
        stack.append((c2, h2, vl, vh, d+1))
print(f"splits checked: {stats['splits']} (expected 2^22-1 = {2**22-1}); seeds reached: {seeds}; failures: {stats['fail']}; time {time.time()-t0:.0f}s")
print("min over splits of: (virtual lo - left child lo) =", stats['minslackL']/SC, "; (right child hi - virtual hi) =", stats['minslackR']/SC, "; (left hi - right lo) overlap =", stats['minoverlap']/SC)
assert stats['fail'] == 0 and seeds == 2**22
print("ALL 22 ROOT SPLITS COVER THE TRUE DOMAIN [-7/10,7/10]^2 x [0, 2pi/5] x [-7/10,7/10]^2 EXACTLY (virtual ends: 7/10 and Machin upper bound of 2pi/5 rounded outward)")
