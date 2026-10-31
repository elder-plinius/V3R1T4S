"""CERTIFIED (Arb) counting scheme v2 (REDUCTION2.md section 2): fractional (multiplicity) packing of deficit balls
+ area-based count of bad centres at a vertex.  Uses rho_hat(0,Q) from rig_dp.py (rho_cert.json, unchanged chain).
Run:  python code/scheme2.py 40 [150]    (scans k,u for each Q; writes scheme2_best_<Q>.json)"""
import json, math, os, sys
from flint import arb, ctx
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rig_dp as R
ctx.prec = 160
AL, PI, S2, S3 = R.AL, R.PI, R.S2, R.S3
here = os.path.dirname(os.path.abspath(__file__))
RHO_FILE = os.environ.get('RHO_FILE', 'rho_cert2.json')   # rho_cert2.json: chain with Lemma V2 (rig2.py); rho_cert.json: chain of the previous run (rig_dp.py)
RHO = {tuple(map(int, k.split(','))): v for k, v in json.load(open(os.path.join(here, RHO_FILE))).items()}
VBT = (4 * PI / 3) / (S2 / 12)          # vol(unit ball)/vol(unit-edge regular tetrahedron)
KAP = S2 / 3
S23 = (arb(2) / 3).sqrt()
E_EDGES, G_VERT = 6, 4
# solid angle of a regular-tetrahedron vertex, as a fraction of the sphere: (3 theta - pi)/(4 pi), theta = arccos(1/3)
VCONE = (3 * R.TH - PI) / (4 * PI)

_gam = {}
def gamma_lo(q):
    """r with alpha + q a(r) > 1 certified (Cor 3.4 / K2 with exact area function a)."""
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

def qmin(delta, R1):
    """smallest q (>=5) with gamma_q * R1 > delta certified (then at most q objects incl. the centred one meet B(c,delta))."""
    for q in range(5, 2000):
        if float((arb(gamma_lo(q)) * R1 - delta).lower()) > 0: return q
    return None

def vertex_count(rv_up, Rpp):
    """|S| <= floor((1 - vertex-cone fraction)/a(rv/R'')): tets with a centre within r_v of a vertex w, other than T_w.
    Caller checks R'' < sqrt(2/3) so that T_w cap B(w,R'') is the vertex cone."""
    ratio = rv_up / Rpp
    ratio_up = arb(float(ratio.upper()) * (1 + 1e-12))
    a = R.a_lo(ratio_up)
    if float(a.lower()) <= 0: return None
    val = ((1 - VCONE) / a).upper()
    return int(math.floor(float(val)))

def cert(Q, k, ustr, use_area_vertex=True):
    u = arb(ustr)
    gQ = arb(gamma_lo(Q))
    rv = u / (gQ * KAP); rv_up = arb(float(rv.upper()) * (1 + 1e-12))
    sigma = 2 * u                                   # pearl spacing sigma = 2u (same-edge centres >= 2u apart)
    d = (1 - (k - 1) * sigma) / 2
    delta = 2 * u
    chk = {}
    chk["d>2*r_v"] = float((d - 2 * rv_up).lower()) > 0
    chk["d>=2u"] = float((d - 2 * u).lower()) >= 0
    R1 = S23 * d - delta
    chk["R1>0"] = float(R1.lower()) > 0
    Rpp = S23 * d - rv_up
    chk["0<R''<sqrt(2/3)"] = float(Rpp.lower()) > 0 and float((S23 - Rpp).lower()) > 0
    if not all(chk.values()): return dict(chk, ok=False)
    q = qmin(delta, R1)
    qv_old = qmin(2 * rv_up, S23 * d - 2 * rv_up)
    qv_area = vertex_count(rv_up, Rpp)
    if q is None or qv_old is None or qv_area is None: return dict(chk, ok=False, q=q)
    qv = min(qv_old, qv_area) if use_area_vertex else qv_old
    # m_v: centres of one tet within closed r_v of w lie on one edge: <= floor(2 r_v / sigma) + 1
    mv = int(math.floor(float((2 * rv_up / sigma).upper()))) + 1
    good = E_EDGES * k - G_VERT * qv * mv
    if good <= 0: return dict(chk, ok=False, good=good)
    rhoQ = arb(RHO[(0, Q)])
    b = arb(good) / q * VBT * u ** 3 * rhoQ
    b_lo = arb(R.down(b))
    dl = R.down(b_lo / (1 + b_lo))
    return dict(chk, ok=True, Q=Q, k=k, u=ustr, gamma_Q=float(gQ), r_v=float(rv_up), d=float(d), q=q, qv=qv, qv_old=qv_old,
                qv_area=qv_area, mv=mv, good=good, rho_Q=float(rhoQ), b_lb=float(b_lo), density_deficit_lb=dl)

if __name__ == "__main__":
    Qs = [int(x) for x in sys.argv[1:]] or [40]
    for Q in Qs:
        best = None
        for ui in range(100, 3200, int(os.environ.get('SCAN_STEP', '10'))):
            ustr = "%.5f" % (ui / 1e5)
            kc = int(0.31 / (ui / 1e5))
            for k in range(max(2, kc - 40), kc + 25):
                o = cert(Q, k, ustr)
                if o.get("ok") and (best is None or o["density_deficit_lb"] > best["density_deficit_lb"]): best = o
        print("Q=%d best:" % Q, json.dumps(best), flush=True)
        json.dump(best, open(os.path.join(here, "scheme2_best_%d.json" % Q), "w"), indent=1)
