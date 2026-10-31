"""Profile-aware multi-scale recursion for rho_hat(c,w), CERTIFIED with Arb ball arithmetic (python-flint).
Run with the venv python:  venv\\Scripts\\python.exe code\\rig_dp.py   (from attempts/formalist-3).
Writes code/rho_cert.json (certified lower bounds, floats rounded DOWN) and prints every number.

Logic (all labelled in REDUCTION.md):
  state (c,w): config in the unit ball with <= c caps, <= w wedges (one centred wedge W0), r=infinity.
  t = w*alpha + c/2.
  t<1 : rho_hat = smallest T with  T = 1 - w*al - capvol(c) - sum_k E(u_k(T)),  u_k = (T/rho_hat(c+w-1-k, 1+k))^(1/3)
  t>1 : rho_hat = min over orderings sigma of the object types of the smallest T with
        sum_i A_{sigma_i}(u_i(T)) <= 1-alpha (and cap-volume <= FCAP if >=2 caps),  u_i = (T/rho_hat(type of first i objects))^(1/3)
Certification: at the reported T_lo the *violated* inequality is checked with outward-rounded balls (see cert_* below)."""
import itertools, json, math, sys, os
from flint import arb, ctx
ctx.prec = 160
PI = arb.pi(); S2 = arb(2).sqrt(); S3 = arb(3).sqrt()
COSTH = arb(1) / 3
TH = COSTH.acos(); AL = TH / (2 * PI)
COT = arb(1) / (2 * S2)                       # cot(theta) = 1/(2 sqrt 2)
HMA = arb(1) / 2 - AL                         # 1/2 - alpha
FCAP = 1 - AL - S2 / (3 * PI)                 # Lemma A: total volume of >=2 disjoint caps (disjoint from W0) <= FCAP
ONE_MINUS_AL = 1 - AL
al_f = float(AL)

def down(x):   # python float <= arb lower end
    f = float(x.lower()); return math.nextafter(f, -math.inf)
def up(x):
    f = float(x.upper()); return math.nextafter(f, math.inf)

# ---------------- float versions (search only; NOT used for certification) ----------------
_gl_x, _gl_w = None, None
def _gl():
    global _gl_x, _gl_w
    if _gl_x is None:
        import numpy as np
        _gl_x, _gl_w = np.polynomial.legendre.leggauss(24)
    return _gl_x, _gl_w
cot_f = 1 / (2 * math.sqrt(2))
def A_f(x):
    R2 = 1 - x * x; y = x * cot_f / math.sqrt(R2)
    return R2 * (math.pi - math.acos(y) + y * math.sqrt(1 - y * y))
def E_f(e):
    if e >= 0.9: return 0.5 - al_f
    gx, gw = _gl()
    s = 0.0
    for xi, wi in zip(gx, gw):
        s += wi * A_f(e * (xi + 1) / 2)
    return min(3 / (4 * math.pi) * s * e / 2, 0.5 - al_f)
def a_f(r):
    if r >= 0.999: return 0.0
    h2 = r * r / 3; h = r / math.sqrt(3)
    phi = math.acos((1 / 3 + h2) / (1 - h2)); psi = 2 * math.asin(math.sqrt(1 - r * r) / math.sqrt(1 - h2))
    return (2 * phi - 2 * h * psi) / (4 * math.pi)
def capvol_f(d): return (1 - d) ** 2 * (2 + d) / 4
FCAP_f = float(FCAP)

# ---------------- certified (arb) ingredients ----------------
def A_ball(X):
    R2 = 1 - X * X
    y = X * COT / R2.sqrt()
    return R2 * (PI - y.acos() + y * (1 - y * y).sqrt())
NCELL = 160
def E_up(u):
    """certified upper bound of sup volume-fraction excess of a theta-wedge with c not interior, edge distance <= u
       (REDUCTION.md Lemma V):  E(u) <= (3/4pi) * int_0^u A(x) dx, capped by 1/2-alpha."""
    uu = arb(float(u.upper()))
    if float(uu) >= 0.9: return up(HMA)
    tot = arb(0)
    for i in range(NCELL):
        x0 = uu * i / NCELL; x1 = uu * (i + 1) / NCELL
        X = (x0 + x1) / 2; X = arb(X.mid(), (x1 - x0).upper() / 2 + X.rad())
        tot += A_ball(X).upper() * (x1 - x0)
    val = 3 / (4 * PI) * tot
    return min(up(val), up(HMA))
def a_lo(uu):
    """certified lower bound of the exact wedge-area fraction a(uu) (decreasing in uu)."""
    if float(uu) >= 0.98: return arb(0)
    r = uu
    h2 = r * r / 3; h = r / S3
    phi = ((arb(1) / 3 + h2) / (1 - h2)).acos()
    psi = 2 * ((1 - r * r).sqrt() / (1 - h2).sqrt()).asin()
    return arb(down((2 * phi - 2 * h * psi) / (4 * PI)))

def cube_root_up(x):   # upper end of x^(1/3), x arb positive
    return arb(up((x.log() / 3).exp()))

# ---------------- states ----------------
rho = {}      # certified (python floats, rounded down)
rho_f = {}    # float search values
rho[(0, 1)] = down(ONE_MINUS_AL); rho[(1, 1)] = down(HMA); rho[(0, 2)] = down(HMA)
for c in range(2, 12): rho[(c, 1)] = down(S2 / (3 * PI))
rho_f.update(rho)

def capvol_total_f(c): return c / 2 if c <= 1 else FCAP_f
def capvol_total_up(c): return arb(0) if c == 0 else (arb(1) / 2 if c == 1 else arb(up(FCAP)))

def search_lt1(c, w, R):
    rk = [R[(c + w - 1 - k, 1 + k)] for k in range(w - 1)]
    def g(T):
        return 1 - w * al_f - capvol_total_f(c) - sum(E_f((T / r) ** (1 / 3)) for r in rk) - T
    lo, hi = 0.0, 1.0
    for _ in range(200):
        m = (lo + hi) / 2
        if g(m) > 0: lo = m
        else: hi = m
    return lo
def orderings(c, w):
    m = c + w - 1; out = []
    for pos in itertools.combinations(range(m), c):
        sig = ['w'] * m
        for p in pos: sig[p] = 'c'
        out.append(tuple(sig))
    return out
def prefix_types(sig, R):
    rh = []; cc = ww = 0
    for x in sig:
        rh.append(R[(cc, 1 + ww)])
        if x == 'c': cc += 1
        else: ww += 1
    return rh
def search_gt1(c, w, R):
    best = None
    for sig in orderings(c, w):
        rh = prefix_types(sig, R)
        def ok(T):
            tot = 0.0; caps = 0.0; nc = 0
            for x, r in zip(sig, rh):
                u = (T / r) ** (1 / 3)
                if u >= 1: continue
                if x == 'c': tot += (1 - u) / 2; caps += capvol_f(u); nc += 1
                else: tot += a_f(u)
            return tot <= 1 - al_f and not (nc >= 2 and caps > FCAP_f)
        lo, hi = 0.0, max(rh)
        if ok(lo): T = lo
        else:
            for _ in range(200):
                m = (lo + hi) / 2
                if ok(m): hi = m
                else: lo = m
            T = hi
        best = T if best is None else min(best, T)
    return best

def cert_lt1(c, w, T):
    Ta = arb(T); tot = 1 - w * AL - capvol_total_up(c)
    for k in range(w - 1):
        rk = arb(rho[(c + w - 1 - k, 1 + k)])
        tot -= E_up(cube_root_up(Ta / rk))
    return float((tot - Ta).lower()) >= 0
def cert_gt1(c, w, T):
    Ta = arb(T)
    for sig in orderings(c, w):
        rh = prefix_types(sig, rho)
        cov = arb(0); caps = arb(0); nc = 0
        for x, r in zip(sig, rh):
            uu = cube_root_up(Ta / arb(r))
            if float(uu) >= 1: continue
            if x == 'c':
                cov += (1 - uu) / 2; caps += (1 - uu) ** 2 * (2 + uu) / 4; nc += 1
            else:
                cov += a_lo(uu)
        infeasible = float(cov.lower()) > float(ONE_MINUS_AL.upper()) or (nc >= 2 and float(caps.lower()) > float(FCAP.upper()))
        if not infeasible: return False
    return True

def mono_close(R, table):
    for k in list(table):
        for k2 in list(table):
            if k2[1] >= k[1] and k2[0] + k2[1] >= k[0] + k[1] and table[k2] > table[k]:
                table[k] = table[k2]

def solve_state(c, w, qmax_log):
    t = w * al_f + c / 2
    if t < 1: Tf = search_lt1(c, w, rho)
    else: Tf = search_gt1(c, w, rho)
    rho_f[(c, w)] = Tf
    T = Tf * (1 - 1e-6)
    for _ in range(60):
        okc = cert_lt1(c, w, T) if t < 1 else cert_gt1(c, w, T)
        if okc: break
        T *= (1 - 1e-4)
    else:
        raise RuntimeError("certification failed %s" % ((c, w),))
    rho[(c, w)] = T
    return Tf, T, t

if __name__ == "__main__":
    NMAX = 5
    QMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    order = sorted([(c, w) for w in range(2, 6) for c in range(0, 5) if c + w <= NMAX and (c, w) != (0, 2)], key=lambda x: (x[0] + x[1], x[1]))
    for (c, w) in order:
        Tf, T, t = solve_state(c, w, None)
        print("state", (c, w), "t=%.3f" % t, "float %.6e  CERTIFIED lower bound %.6e" % (Tf, T), flush=True)
        mono_close(rho, rho)
    # pure-wedge states (0,w), w = 6..QMAX+... (single ordering)
    for w in range(6, QMAX + 2):
        Tf, T, t = solve_state(0, w, None)
        rho[(0, w)] = min(T, rho[(0, w - 1)])
        if w <= 10 or w % 10 == 0: print("state", (0, w), "t=%.3f" % t, "float %.6e  CERTIFIED %.6e" % (Tf, rho[(0, w)]), flush=True)
    out = {"%d,%d" % k: v for k, v in rho.items()}
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rho_cert.json"), "w"), indent=1, sort_keys=True)
    print("rho_cert(0,5) =", rho[(0, 5)], " rho_cert(0,%d) =" % (QMAX + 1), rho[(0, QMAX + 1)])
