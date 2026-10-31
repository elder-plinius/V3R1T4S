"""fullchain.py -- certified (Arb ball arithmetic, python-flint) evaluation of the chain of REDUCTION_FULL.md.

Every number that enters the final bound is produced by a predicate that is evaluated with Arb balls; there is no floating-point
search whose result is trusted: the (c,w) tables are found by bisection on the *certified* predicates, so the value kept is by
construction one for which the predicate was certified True.  Python floats are used only as exact dyadic representations of the
numbers that are stored in the json files (every float converts to an Arb ball exactly).

Sections of REDUCTION_FULL.md that this file implements:
  a_lo      Lemma K1 closed form (section 3.1)            E2_up    Lemma V2 (section 5)
  cert_lt1  Lemma R, case R1 (section 6)                  cert_gt1 Lemma R, case R2 (section 6)
  solve_all the table rho(c,w) (section 6.4)              scheme   Claims 1,2,3 and conclusion (section 8)
Usage:   python fullchain.py build  EPSDEN QMAX   -> writes rho_cert.json
         python fullchain.py scheme EPSDEN Q      -> scans (k,u), writes scheme_best_<Q>.json
"""
import itertools, json, math, os, sys, bisect
from flint import arb, ctx

ctx.prec = 160
HERE = os.path.dirname(os.path.abspath(__file__))

PI = arb.pi()
S2 = arb(2).sqrt()
S3 = arb(3).sqrt()
TH = (arb(1) / 3).acos()                 # theta = arccos(1/3), dihedral angle of the regular tetrahedron
AL = TH / (2 * PI)                       # alpha = theta/(2 pi): surface/volume fraction of a centred wedge
KAP = arb(1) / 3                         # kappa = cos(theta)
SIN = (1 - KAP * KAP).sqrt()             # sin(theta)
K2C = 1 - KAP * KAP
HMA = arb(1) / 2 - AL                    # 1/2 - alpha
ONE_MINUS_AL = 1 - AL
FCAP = 1 - AL - S2 / (3 * PI)            # Lemma A
VCONE = (3 * TH - PI) / (4 * PI)         # solid angle fraction of a regular-tetrahedron vertex
VBT = (4 * PI / 3) / (S2 / 12)           # vol(unit ball) / vol(unit-edge regular tetrahedron)
S23 = (arb(2) / 3).sqrt()                # sqrt(2/3): height of the unit tetrahedron, and sin(edge,face)


def down(x):
    """python float <= x (x an Arb ball): exact lower end rounded down once more."""
    return math.nextafter(float(x.lower()), -math.inf)


def up(x):
    return math.nextafter(float(x.upper()), math.inf)


# ------------------------------------------------------------------ K1: closed form of a(r)
def a_lo(r):
    """Lower bound (exact Arb number) of a(r) = (1/pi)[atan(sqrt((1-r^2)/2)) - (r/sqrt3) acos(r sqrt2/sqrt(3-r^2))], 0<=r<1
    (REDUCTION_FULL.md 3.1: the area fraction of the minimising wedge; decreasing in r).  r: Arb ball.  Returns 0 if r >= 0.98."""
    if not (r.upper() < arb("0.98")):
        return arb(0)
    val = ((((1 - r * r) / 2).sqrt()).atan() - r / S3 * (r * S2 / (3 - r * r).sqrt()).acos()) / PI
    return val.lower()


def cube_root_up(x):
    """exact Arb number >= x^(1/3), x>0 Arb ball"""
    if not (x > 0):
        return arb(0)
    return (x ** (arb(1) / 3)).upper()


# ------------------------------------------------------------------ Lemma V2 (section 5)
EMAX = 0.9
NT = 36   # cells in t
NX = 48   # cells per integral


def _bracket(y):
    return PI - y.acos() + y * (1 - y * y).sqrt()


def _A2(x0, s1):                         # area of the disc slice, half plane at signed distance (s1 + kappa x0)/sin(theta)
    R2 = 1 - x0 * x0
    return R2 * _bracket((s1 + KAP * x0) / (R2.sqrt() * SIN))


def _Bl(x1):
    R2 = 1 - x1 * x1
    return R2 * _bracket(-(KAP * x1) / (R2.sqrt() * SIN))


def E2_up_exact(e):
    """Exact Arb number >= E2(e) := sup (vol(W)/vol(B) - alpha) over theta-wedges W, c not interior, edge line at distance <= e
    (e: python float treated exactly, 0 < e <= EMAX).  Cell bound of section 5."""
    e = arb(e)
    best = arb(0)
    e2 = e * e
    for i in range(NT):
        t0 = (e * (i * i) / (NT * NT)).lower()          # exact lower end of the cell in t
        t1 = (e * ((i + 1) * (i + 1)) / (NT * NT)).upper()
        dd = (K2C * (e2 - t0 * t0)).upper()
        sq = dd.sqrt().upper() if dd > 0 else arb(0)
        smax = (KAP * t1 + sq).upper()                  # >= sup of s2max(t,e) over the cell
        if smax > e.upper():
            smax = e.upper()                            # Cauchy-Schwarz: s2max <= e
        # Vslab upper bound: int_0^smax A(x;-t0) dx  (A non-increasing in t, so t0 <= t gives an upper bound)
        tot = arb(0)
        for j in range(NX):
            lo = (smax * j / NX).lower()
            hi = (smax * (j + 1) / NX).upper()
            tot += _A2(lo.union(hi), -t0).upper() * (hi - lo).upper()
        # Loss lower bound: int_0^t0 Bl, Bl decreasing: right-endpoint sum with widths rounded down
        loss = arb(0)
        if t0 > 0:
            w = (t0 / NX).lower()
            for j in range(NX):
                xi = (t0 * (j + 1) / NX).upper()
                loss += _Bl(xi).lower() * w
        val = 3 / (4 * PI) * (tot - loss)
        if not val.is_finite():
            raise ValueError("non-finite enclosure in E2 at e=%r cell %d" % (float(e), i))
        if val.upper() > best:
            best = val.upper()
    return best


E_LO, RATIO = 1e-5, 1.012
GRID = []
_E2CACHE = {}


def _grid():
    if not GRID:
        g = E_LO
        while g < EMAX:
            GRID.append(g)
            g *= RATIO
        GRID.append(EMAX)


def E_up(u):
    """Exact Arb number >= E(e) for every edge distance e <= u (u: exact Arb number): Lemma V2 table at the next grid point
    >= u (E2 is non-decreasing in e), and 1/2 - alpha (volume of a half ball) if u > EMAX."""
    _grid()
    uf = math.nextafter(float(u.upper()), math.inf)
    if uf > EMAX:
        return HMA.upper()
    i = bisect.bisect_left(GRID, uf)
    if i not in _E2CACHE:
        _E2CACHE[i] = E2_up_exact(GRID[i])
    return min(_E2CACHE[i], HMA.upper())


# ------------------------------------------------------------------ Lemma R (section 6)
def capvol_up(c):
    return arb(0) if c == 0 else (arb(1) / 2 if c == 1 else FCAP.upper())


def orderings(c, w):
    m = c + w - 1
    out = []
    for pos in itertools.combinations(range(m), c):
        sig = ['w'] * m
        for p in pos:
            sig[p] = 'c'
        out.append(tuple(sig))
    return out


def prefix_types(sig, rho):
    rh = []
    cc = ww = 0
    for x in sig:
        rh.append(rho[(cc, 1 + ww)])
        if x == 'c':
            cc += 1
        else:
            ww += 1
    return rh


def cert_lt1(c, w, T, rho):
    """R1: certifies  1 - w alpha - capvol(c) - sum_k E_up((T/rho_k)^(1/3)) - T >= 0   (T python float, exact)."""
    Ta = arb(T)
    tot = 1 - w * AL - capvol_up(c)
    for k in range(w - 1):
        rk = arb(rho[(c + w - 1 - k, 1 + k)])
        tot -= E_up(cube_root_up(Ta / rk))
    return bool(tot.lower() >= Ta)


def cert_gt1(c, w, T, rho):
    """R2: for every ordering sigma the profile with all delta_i < u_i(T) is infeasible."""
    Ta = arb(T)
    for sig in orderings(c, w):
        rh = prefix_types(sig, rho)
        cov = arb(0)
        caps = arb(0)
        nc = 0
        for x, r in zip(sig, rh):
            uu = cube_root_up(Ta / arb(r))
            if not (uu < 1):
                continue
            if x == 'c':
                cov += (1 - uu) / 2
                caps += (1 - uu) ** 2 * (2 + uu) / 4
                nc += 1
            else:
                cov += a_lo(uu)
        if not ((cov.lower() > ONE_MINUS_AL.upper()) or (nc >= 2 and caps.lower() > FCAP.upper())):
            return False
    return True


def base_rho(cmax=11):
    rho = {(0, 1): down(ONE_MINUS_AL), (1, 1): down(HMA), (0, 2): down(HMA)}
    for c in range(2, cmax + 1):
        rho[(c, 1)] = down(S2 / (3 * PI))
    return rho


def mono_close(rho):
    for k in list(rho):
        for k2 in list(rho):
            if k2[1] >= k[1] and k2[0] + k2[1] >= k[0] + k[1] and rho[k2] > rho[k]:
                rho[k] = rho[k2]


def pred(c, w, T, rho):
    t = w * float(AL) + c / 2
    return cert_lt1(c, w, T, rho) if t < 1 else cert_gt1(c, w, T, rho)


def solve_state(c, w, rho):
    """largest float T (found by bisection) for which the certified predicate holds; the lower end is always certified."""
    lo, hi = 0.0, 1.0
    for _ in range(90):
        mid = (lo + hi) / 2
        if mid > 0 and pred(c, w, mid, rho):
            lo = mid
        else:
            hi = mid
    if lo <= 0:
        raise RuntimeError("no certified T for %s" % ((c, w),))
    return lo


def build(qmax):
    rho = base_rho()
    order = sorted([(c, w) for w in range(2, 6) for c in range(0, 5) if c + w <= 5 and (c, w) != (0, 2)], key=lambda x: (x[0] + x[1], x[1]))
    for (c, w) in order:
        rho[(c, w)] = solve_state(c, w, rho)
        print("state", (c, w), "t=%.3f" % (w * float(AL) + c / 2), "CERTIFIED lower bound %.6e" % rho[(c, w)], flush=True)
        mono_close(rho)
    for w in range(6, qmax + 2):
        T = solve_state(0, w, rho)
        rho[(0, w)] = min(T, rho[(0, w - 1)])
        if w <= 10 or w % 10 == 0:
            print("state", (0, w), "CERTIFIED %.6e" % rho[(0, w)], flush=True)
    return rho


def save_rho(rho, path):
    json.dump({"%d,%d" % k: v for k, v in rho.items()}, open(path, "w"), indent=1, sort_keys=True)


def load_rho(path):
    return {tuple(map(int, k.split(','))): v for k, v in json.load(open(path)).items()}


def recertify(rho, verbose=True):
    """Independent pass: checks base values and every stored state with the certified predicates (no search)."""
    assert rho[(0, 1)] <= down(ONE_MINUS_AL) and rho[(1, 1)] <= down(HMA) and rho[(0, 2)] <= down(HMA)
    for c in range(2, 12):
        assert rho[(c, 1)] <= down(S2 / (3 * PI))
    states = sorted([k for k in rho if k[1] >= 2 and k != (0, 2)], key=lambda x: (x[0] + x[1], x[1]))
    direct = set()
    failed = []
    for k in states:
        (direct.add if pred(k[0], k[1], rho[k], rho) else failed.append)(k)
    for k in failed:
        ok = any(k2 in direct and k2[1] >= k[1] and k2[0] + k2[1] >= k[0] + k[1] and rho[k2] >= rho[k] for k2 in direct)
        assert ok, ("FAILED", k, rho[k])
    if verbose:
        print("directly certified states: %d   justified by class inclusion: %d" % (len(direct), len(failed)))
    return len(direct), len(failed)


# ------------------------------------------------------------------ Claims 1-3 (section 8)
_gam = {}


def gamma_lo(q):
    """exact float r with alpha + q a(r) > 1 certified (K2): a is decreasing, so any smaller radius works too."""
    if q in _gam:
        return _gam[q]
    lo, hi = 0.0, 0.98
    for _ in range(80):
        m = (lo + hi) / 2
        if (AL + q * a_lo(arb(m)) - 1).lower() > 0:
            lo = m
        else:
            hi = m
    _gam[q] = lo
    return lo


def qmin(delta, R1):
    """smallest q>=5 with gamma_q R1 > delta (certified)"""
    for q in range(5, 3000):
        if (arb(gamma_lo(q)) * R1 - delta).lower() > 0:
            return q
    return None


def vertex_count(rv_up, Rpp):
    a = a_lo((rv_up / Rpp).upper())
    if not (a > 0):
        return None
    val = ((1 - VCONE) / a).upper()
    return int(math.floor(up(val)))                       # integer >= floor(true upper bound): conservative


def scheme_cert(Q, k, ustr, rho, epsden):
    u = arb(ustr)
    kappa_p = S2 / 3 / (1 + arb(1) / epsden)           # K4': vertices at distance > r_v = R0/kappa_p  => wedge
    gQ = arb(gamma_lo(Q))
    R0 = u / gQ
    rv = (R0 / kappa_p).upper()
    sigma = 2 * u
    d = (1 - (k - 1) * sigma) / 2
    delta = 2 * u
    chk = {}
    chk["d>2*r_v"] = bool((d - 2 * rv).lower() > 0)
    chk["d>=2u"] = bool((d - 2 * u).lower() >= 0)
    chk["1/sqrt2>=2u"] = bool((1 / S2 - 2 * u).lower() >= 0)
    chk["R0<=sqrt(2/3)d"] = bool((S23 * d - R0).lower() >= 0)
    R1 = S23 * d - delta
    chk["R1>0"] = bool(R1.lower() > 0)
    Rpp = S23 * d - rv
    chk["0<R''<sqrt(2/3)"] = bool(Rpp.lower() > 0 and (S23 - Rpp).lower() > 0)
    chk["r_v/R''<0.98"] = bool((rv / Rpp).upper() < arb("0.98"))
    if not all(chk.values()):
        return dict(chk, ok=False)
    q = qmin(delta, R1)
    qv_old = qmin(2 * rv, S23 * d - 2 * rv)
    qv_area = vertex_count(rv, Rpp)
    if q is None or qv_area is None:
        return dict(chk, ok=False)
    qv = qv_area                                         # (the K2-based count qv_old is not needed; reported for comparison)
    mv = int(math.floor(up(2 * rv / sigma))) + 1          # m_v >= floor(2 r_v/sigma)+1 (outward rounded)
    good = 6 * k - 4 * qv * mv
    if good <= 0:
        return dict(chk, ok=False, good=good)
    rhoQ = arb(rho[(0, Q)])
    b = arb(good) / q * VBT * u ** 3 * rhoQ
    b_lo = arb(down(b))
    dl = down(b_lo / (1 + b_lo))
    return dict(chk, ok=True, Q=Q, k=k, u=ustr, gamma_Q=float(gQ), r_v=float(rv), d=float(d), q=q, qv=qv, qv_old=qv_old,
                mv=mv, good=good, rho_Q=float(rhoQ), b_lb=float(b_lo), density_deficit_lb=dl)


def scan(Q, rho, epsden, step=10):
    best = None
    for ui in range(300, 3200, step):
        ustr = "%.5f" % (ui / 1e5)
        kc = int(0.31 / (ui / 1e5))
        for k in range(max(2, kc - 40), kc + 25):
            o = scheme_cert(Q, k, ustr, rho, epsden)
            if o.get("ok") and (best is None or o["density_deficit_lb"] > best["density_deficit_lb"]):
                best = o
    return best


if __name__ == "__main__":
    cmd = sys.argv[1]
    epsden = int(sys.argv[2])
    if cmd == "build":
        rho = build(int(sys.argv[3]))
        save_rho(rho, os.path.join(HERE, "rho_cert.json"))
        print("rho_cert(0,5) = %.6e   rho_cert(0,%d) = %.6e" % (rho[(0, 5)], int(sys.argv[3]) + 1, rho[(0, int(sys.argv[3]) + 1)]))
    elif cmd == "scheme":
        Q = int(sys.argv[3])
        rho = load_rho(os.path.join(HERE, "rho_cert.json"))
        best = scan(Q, rho, epsden)
        print("Q=%d eps=1/%d best:" % (Q, epsden), json.dumps(best), flush=True)
        json.dump(best, open(os.path.join(HERE, "scheme_best_%d.json" % Q), "w"), indent=1)
