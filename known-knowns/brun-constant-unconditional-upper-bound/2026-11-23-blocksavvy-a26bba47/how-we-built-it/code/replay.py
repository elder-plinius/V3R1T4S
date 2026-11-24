"""Rigorous (arb ball arithmetic) evaluation of Dunn's Theorem 3.3 bound for Brun's constant under GRH.
z_i are chosen by a float optimiser (any choice gives a valid bound); every term of the bound is then evaluated in arb
and the upper end of the final ball is reported.
Options:
  --c1 dunn : c1 from Dunn's li_up/li_low (Dusart 7.32 + Schoenfeld), exactly as compute_B.jl
  --c1 li   : c1 from li(x) evaluated directly in arb (no Dusart, no Schoenfeld needed for this term)
  --cpi dunn: c_pi(m_i) from JS Lemma 5.1 (q <= sqrt(x) worst case)
  --cpi q   : c_pi from Grenie-Molteni Cor. 1.2 with log q <= 2 log z (moduli [d1,d2] <= z^2), lambda = min(1/2, 2 log z / log m_i)
  --bracket dunn : Dunn's search bracket [z_{i-1}, min(z_{i-1} m_{i+1}/m_i, m_i^(1/4))];  free: [z_{i-1}/10, m_i^(1/4)] grid + Brent
Tables: V lower bounds from vsieve_fx (exact fixed point), M(z) exact counts <= 1e7."""
import argparse, math, sys, time, json
import numpy as np
from flint import arb, fmpz, fmpq, ctx
from scipy.optimize import minimize_scalar
ap = argparse.ArgumentParser()
ap.add_argument("--c1", default="dunn"); ap.add_argument("--cpi", default="dunn"); ap.add_argument("--bracket", default="dunn")
ap.add_argument("--prec", type=int, default=128); ap.add_argument("--cert", default=None); ap.add_argument("--out", default=None); ap.add_argument("--c3", default="12.6244"); ap.add_argument("--vlemma", default="klyve", help="klyve: Dunn Lemma 2.1 (c3); own: V(z) >= V(1e10) + log(z/1e10)/(2 C2) - 0.0107001 (attempts/vlemma)")
ap.add_argument("--vcap", action="store_true", help="for z > 1e10 use V(z) >= V(1e10) (monotonicity only; no Klyve c3 lemma)")
a = ap.parse_args(); ctx.prec = a.prec
import os
W = os.environ.get("BRUN_WORK", "work") + "/"
D = np.memmap(W + "Vfx_dense_1e8.bin", dtype=np.float64, mode="r")                 # D[n] <= V(n), n <= 1e8
raw = np.fromfile(W + "Vfx_chunks_1e10.bin", dtype=np.uint8).reshape(-1, 24)
u = raw[:, :16].copy().view("<u8").reshape(-1, 2)                                   # S_lo(k*1e4) = lo + 2^64 hi
Cf = u[:, 1].astype(np.float64) + u[:, 0].astype(np.float64) / 2.0**64               # float copy (optimiser only)
Ms = np.memmap(W + "M_1e7.bin", dtype=np.int32, mode="r")
L1, L2, L3, STEP = 10**8, 10**10, 10**7, 10**4
TWO64 = arb(2) ** 64
def S_exact(k):  # exact rigorous lower bound V(k*1e4) as arb
    return (arb(fmpz(int(u[k - 1, 0]))) + arb(fmpz(int(u[k - 1, 1]))) * TWO64) / TWO64
PI = arb.pi(); pi2u = arb(fmpq(6601619, 10**7)); li2u = arb(fmpq(10451638, 10**7)); li2l = arb(fmpq(10451637, 10**7))
c3 = arb(fmpq(int(round(float(a.c3) * 10**4)), 10**4)); A732 = arb(fmpq(732, 100))
VL2 = S_exact(L2 // STEP); VL2f = float(Cf[-1]); c3f = float(a.c3)
# ---------- float model (for choosing z only) ----------
def Vf(t):
    if t > math.log(L2) and a.vcap: return VL2f
    if t > math.log(L2) and a.vlemma == "own": return VL2f + (t - math.log(L2)) / (2 * 0.6601619) - 0.0107001
    if t > math.log(L2): return VL2f + (t - math.log(L2)) / (2 * 0.6601619) + c3f * (3 * math.exp(-t / 2) - 9 / math.sqrt(L2))
    z = math.exp(t)
    if z > L1: return float(Cf[int(z // STEP) - 1])
    return float(D[int(z)])
def logrf(t):
    if t < math.log(L3): return math.log(int(Ms[int(math.exp(t))]))
    return t + math.log(4 / math.pi**2) + math.log1p((3.038 * math.exp(-t / 2) + 5.744 * math.exp(-0.75 * t)) * math.pi**2 / 4)
def cpif(ls, t):
    if a.cpi == "q":
        lam = min(0.5, 2 * t / ls)
        return 1 / (8 * math.pi) + (1 / (2 * math.pi) + 3 / ls) * lam + 1 / (4 * math.pi * ls) + 6 / ls**2
    return 3 / (8 * math.pi) + (6 + 1 / math.pi) / (4 * ls) + 6 / ls**2
# ---------- rigorous pieces ----------
def pi1_up(x): l = x.log(); return x / l * (1 + 1 / l + 2 / l**2 + A732 / l**3)
def pi1_low(x): l = x.log(); return x / l * (1 + 1 / l + 2 / l**2)
def Li_up(x): return pi1_up(x) + x.sqrt() * x.log() / (8 * PI) + li2u
def Li_low(x): return pi1_low(x) - x.sqrt() * x.log() / (8 * PI) - li2u
def c1(s, e):
    if a.c1 == "li":   # integral of li(t)/t^2 = [loglog t - li(t)/t]; li(t) >= li(t) - li(2), so this bounds Dunn's integrand
        return (e.log().log() - e.li() / e) - (s.log().log() - s.li() / s)
    return (e.log().log() - (Li_low(e) - li2u) / e) - (s.log().log() - (Li_up(s) - li2l) / s)
def c2(s, e): return -2 * (e.log() + 2) / e.sqrt() + 2 * (s.log() + 2) / s.sqrt()
def cpi(s, z):
    l = s.log(); tail = 6 / l**2 + li2u / (s.sqrt() * l)
    if a.cpi == "q":
        lam = 2 * z.log() / l
        lam = lam if lam < arb(fmpq(1, 2)) else arb(fmpq(1, 2))
        if not (lam <= arb(fmpq(1, 2))): lam = arb(fmpq(1, 2))
        return 1 / (8 * PI) + (1 / (2 * PI) + 3 / l) * lam + 1 / (4 * PI * l) + tail
    return 3 / (8 * PI) + (6 + 1 / PI) / (4 * l) + tail
def V_low(z):  # z: exact arb (dyadic), zf float
    zf = float(z.mid())
    if zf > L2:
        assert z > arb(L2)
        if a.vcap: return VL2
        if a.vlemma == "own": return VL2 + (z.log() - arb(L2).log()) / (2 * pi2u) - arb(fmpq(107001, 10**7))
        return VL2 + (z.log() - arb(L2).log()) / (2 * pi2u) + c3 * (3 / z.sqrt() - 9 / arb(L2).sqrt())
    n = int(math.floor(zf)); assert arb(n) <= z and z < arb(n + 1)
    if n > L1: return S_exact(n // STEP)
    return arb(float(D[n]))
def r_up(z):
    zf = float(z.mid())
    if zf < L3:
        n = int(math.floor(zf)); assert arb(n) <= z and z < arb(n + 1); return arb(int(Ms[n]))
    return 4 / PI**2 * z + arb(fmpq(3038, 1000)) * z.sqrt() + arb(fmpq(5744, 1000)) * z.sqrt().sqrt()
# ---------- midpoints: 4e18, then 10^(19 + i/5), i = 0..9905 (last 10^2000) ----------
L10 = arb(10).log()
mids = [arb(4) * arb(10)**18] + [(L10 * arb(fmpq(95 + i, 5))).exp() for i in range(9906)]
lmids = [float(m.log().mid()) for m in mids]
t0 = time.time(); total = arb(0); tprev = math.log(650.0); zs = []; contrib = []; cert = []
for i in range(len(mids) - 1):
    s, e = mids[i], mids[i + 1]; ls, le = lmids[i], lmids[i + 1]
    C1 = c1(s, e); C2 = c2(s, e); C1f = float(C1.mid()); lC2f = float(C2.log().mid())
    tmax = ls / 4 - 1e-9
    def f(t):
        x = lC2f + math.log(cpif(ls, t)) + 2 * logrf(t)
        return C1f / Vf(t) + (math.exp(x) if x < 700 else float("inf"))
    if a.bracket == "dunn":
        lo, hi = tprev, min(tprev + (le - ls), tmax)
        t = lo if hi <= lo else minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-9}).x
    else:
        lo, hi = max(math.log(3.0), tprev - math.log(10)), tmax
        grid = np.linspace(lo, hi, 400); vals = [f(g) for g in grid]; j = int(np.argmin(vals))
        g0, g1 = grid[max(j - 1, 0)], grid[min(j + 1, len(grid) - 1)]
        t = minimize_scalar(f, bounds=(g0, g1), method="bounded", options={"xatol": 1e-9}).x
        if f(t) > vals[j]: t = grid[j]
    z = arb(math.exp(t)) if t < math.log(1e12) else arb(t).exp()   # exact dyadic double, or the real exp(t) as a ball
    zrep = ["z", float.hex(math.exp(t))] if t < math.log(1e12) else ["t", float.hex(t)]
    assert z <= s.root(4) and z >= arb(1)
    term = 2 * (C1 / V_low(z) + cpi(s, z) * C2 * r_up(z)**2)
    total += term; tprev = t; zs.append(t / math.log(10)); contrib.append(float(term.upper())); cert.append([zrep[0], zrep[1], term.upper().str(20, radius=False)])
rem = 32 * pi2u / mids[-1].log() + 8 / mids[-1].sqrt()
pst = -2 * arb(fmpz(3023463123235320)) / (arb(4) * arb(10)**18)
B = total + rem + arb(fmpq(1840518, 10**6)) + pst
res = dict(vlemma=a.vlemma, vcap=a.vcap, c1=a.c1, cpi=a.cpi, bracket=a.bracket, prec=a.prec, c3=a.c3, intervals=len(mids) - 1,
           sum_upper=total.upper().str(20, radius=False), remainder_upper=rem.upper().str(12, radius=False),
           B_ball=B.str(25), B_upper=B.upper().str(20, radius=False), rad=B.rad().str(5, radius=False),
           log10z_last=zs[-1], log10z_first=zs[:3], n_z_le_1e10=sum(1 for z in zs if z <= 10), wall_s=round(time.time() - t0, 1),
           contrib_first10=sum(contrib[:10]), contrib_by_1000=[sum(contrib[k:k + 1000]) for k in range(0, len(contrib), 1000)])
print(json.dumps(res, indent=1))
if a.out:
    json.dump(res, open(a.out, "w"), indent=1); np.save(a.out.replace(".json", "_log10z.npy"), np.array(zs))
if a.cert:
    json.dump(dict(options=vars(a), note="per interval i (m_i = 4e18 for i=0, else 10^(19+(i-1)/5)): z_i as exact double ('z', hex) or z_i = exp(t_i) ('t', hex), and the sup of 2*(c1/V + c_pi c2 r^2) to 20 digits",
                   B_upper_without_pi2z=B.upper().str(20, radius=False), intervals=cert), open(a.cert, "w"), separators=(",", ":"))
