"""CERTIFIED (Arb) evaluation of the decoupled pearl/deficit-ball counting scheme (REDUCTION.md section E),
using the certified rho_hat(0,Q) from rig_dp.py.  Scans (Q,k,u) with float screening, then certifies the best candidates.
Run:  venv\\Scripts\\python.exe code\\scheme.py        (from attempts/formalist-3)"""
import json, math, os, sys
from fractions import Fraction as Fr
from flint import arb, ctx
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rig_dp as R
ctx.prec = 160
AL, PI, S2, S3 = R.AL, R.PI, R.S2, R.S3
here = os.path.dirname(os.path.abspath(__file__))
RHO = {tuple(map(int, k.split(','))): v for k, v in json.load(open(os.path.join(here, 'rho_cert.json'))).items()}
VBT = (4 * PI / 3) / (S2 / 12)          # vol(unit ball) / vol(unit-edge regular tetrahedron)
KAP = S2 / 3                             # kappa = sqrt(2)/3   (Lemma 3.5 constant, GEK)
S23 = (arb(2) / 3).sqrt()
E_EDGES, G_VERT = 6, 4

_gam = {}
def gamma_lo(q):
    """largest (certified) r with alpha + q a(r) > 1  (Cor 3.4 with the exact area function)."""
    if q in _gam: return _gam[q]
    lo, hi = 0.0, 1.0
    for _ in range(80):
        m = (lo + hi) / 2
        if R.al_f + q * R.a_f(m) > 1: lo = m
        else: hi = m
    r = lo * (1 - 1e-7)
    for _ in range(200):
        if float((AL + q * R.a_lo(arb(r)) - 1).lower()) > 0: break
        r *= (1 - 1e-6)
    _gam[q] = r
    return r

def cert(Q, k, ustr, verbose=False):
    u = arb(ustr); uF = Fr(ustr)
    gQ = arb(gamma_lo(Q))
    rv = u / (gQ * KAP); rv_up = arb(float(rv.upper()))
    sigma = 2 * u                                   # spacing sigma = 2u exactly
    d = (1 - (k - 1) * sigma) / 2
    delta = 2 * u
    chk = {}
    chk["d>2*r_v"] = float((d - 2 * rv_up).lower()) > 0
    chk["d>=4u (d>=2*delta)"] = float((d - 4 * u).lower()) >= 0
    chk["R1>0"] = float((S23 * d - delta).lower()) > 0
    if not all(chk.values()): return dict(chk, ok=False)
    def qmin(dl, R1):
        for q in range(5, 1500):
            if float((arb(gamma_lo(q)) * R1 - dl).lower()) > 0: return q
        return None
    q = qmin(delta, S23 * d - delta); qv = qmin(2 * rv_up, S23 * d - 2 * rv_up)
    if q is None or qv is None: return dict(chk, ok=False, q=q, qv=qv)
    m = 2                                            # open interval of length 2*delta=2*sigma holds <=2 progression points
    mv = int(math.floor(float((2 * rv_up / sigma).upper()))) + 1
    good = E_EDGES * k - G_VERT * qv * mv
    if good <= 0: return dict(chk, ok=False, good=good)
    Delta = m * (q - 1)
    rhoQ = arb(RHO[(0, Q)])                          # config in B(c,u) has at most Q tets (incl. T): class K(0,Q)
    b = arb(good) / (Delta + 1) * VBT * u ** 3 * rhoQ
    b_lo = arb(R.down(b))
    dl = R.down(b_lo / (1 + b_lo))
    return dict(chk, ok=True, Q=Q, k=k, u=ustr, gamma_Q=float(gQ), r_v=float(rv_up), d=float(d), q=q, qv=qv, m=m, mv=mv,
                good=good, Delta=Delta, rho_Q=float(rhoQ), b_lb=float(b_lo), density_deficit_lb=dl)

if __name__ == "__main__":
    Qs = [int(x) for x in sys.argv[1:]] or [5, 8, 12, 20, 30]
    best_all = None
    for Q in Qs:
        if (0, Q) not in RHO: continue
        best = None
        for ui in range(100, 3200, 20):
            ustr = "%.5f" % (ui / 1e5)
            kc = int(0.31 / (ui / 1e5))
            for k in range(max(2, kc - 14), kc + 15):
                o = cert(Q, k, ustr)
                if o.get("ok") and (best is None or o["density_deficit_lb"] > best["density_deficit_lb"]): best = o
        print("Q=%d best:" % Q, json.dumps(best), flush=True)
        if best and (best_all is None or best["density_deficit_lb"] > best_all["density_deficit_lb"]): best_all = best
    print("BEST:", json.dumps(best_all))
    json.dump(best_all, open(os.path.join(here, "scheme_best.json"), "w"), indent=1)
