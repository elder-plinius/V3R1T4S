"""Validated Taylor integration of the planar equal-mass three-body problem (G = 1, m = 1) with
variational (tangent) equations, in python-flint ball arithmetic.

State order: [x1, y1, x2, y2, x3, y3, vx1, vy1, vx2, vy2, vx3, vy3] (bodies numbered as in
Hristov-Hristova-Tanikawa, arXiv:2510.22802: body 2 is the middle body at t = 0).

Rigour:
 * Taylor coefficients 0..N-1 are computed by the standard automatic-differentiation recurrences in arb
   ball arithmetic over the current state ball (so they enclose the coefficients of every solution that
   starts in the ball).
 * The tail sum_{k>=N} x_k h^k is bounded with Cauchy estimates: a complex a priori enclosure B (acb boxes)
   with Z + D_rho * f(B) contained in B (Z = current state balls, D_rho the complex square of half-side rho)
   shows, ray by ray, that every solution starting in Z is holomorphic on |tau| <= rho with values in B.
   Hence |x_k| <= sup_B |x - c| / rho^k for k >= 1 and the tail at |h| <= kappa*rho is at most
   sup|x - c| * kappa^N / (1 - kappa).  The branch of s^(-3/2) is the principal one; the code requires
   Re(s) > 0 on every a priori box, so f is holomorphic on a neighbourhood of B.
 * The same is done for the tangent (variational) components, which form a holomorphic linear system
   together with the state.
"""
from flint import arb, acb, ctx

PAIRS = [(0, 1), (0, 2), (1, 2)]


def _zero_like(x):
    return x * 0


def taylor(X0, T0, N):
    """Taylor coefficients 0..N-1 of the state (12 lists) and tangents (len(T0) x 12 lists).
    Works for arb or acb entries."""
    nt = len(T0)
    Q = [[X0[c]] for c in range(6)]
    V = [[X0[6 + c]] for c in range(6)]
    dQ = [[[T0[p][c]] for c in range(6)] for p in range(nt)]
    dV = [[[T0[p][6 + c]] for c in range(6)] for p in range(nt)]
    z = _zero_like(X0[0])
    st = []
    for (i, j) in PAIRS:
        st.append(dict(dx=[], dy=[], s=[], w3=[], w5=[],
                       ddx=[[] for _ in range(nt)], ddy=[[] for _ in range(nt)],
                       ds=[[] for _ in range(nt)], dw3=[[] for _ in range(nt)]))
    for k in range(N - 1):
        acc = [z] * 6
        dacc = [[z] * 6 for _ in range(nt)]
        for pi, (i, j) in enumerate(PAIRS):
            P = st[pi]
            dx, dy, s, w3, w5 = P['dx'], P['dy'], P['s'], P['w3'], P['w5']
            dx.append(Q[2 * j][k] - Q[2 * i][k])
            dy.append(Q[2 * j + 1][k] - Q[2 * i + 1][k])
            sk = z
            for m in range(k + 1):
                sk = sk + dx[m] * dx[k - m] + dy[m] * dy[k - m]
            s.append(sk)
            if k == 0:
                if isinstance(sk, acb):
                    w3.append(sk ** arb(-1.5))
                else:
                    w3.append(1 / (sk * sk.sqrt()))
                w5.append(w3[0] / sk)
            else:
                a3 = z
                a5 = z
                for m in range(1, k + 1):
                    a3 = a3 + (arb(-m - 2 * k) / 2) * s[m] * w3[k - m]
                    a5 = a5 + (arb(-3 * m - 2 * k) / 2) * s[m] * w5[k - m]
                w3.append(a3 / (k * s[0]))
                w5.append(a5 / (k * s[0]))
            ax = z
            ay = z
            for m in range(k + 1):
                ax = ax + dx[m] * w3[k - m]
                ay = ay + dy[m] * w3[k - m]
            acc[2 * i] = acc[2 * i] + ax
            acc[2 * i + 1] = acc[2 * i + 1] + ay
            acc[2 * j] = acc[2 * j] - ax
            acc[2 * j + 1] = acc[2 * j + 1] - ay
            for p in range(nt):
                ddx, ddy, ds, dw3 = P['ddx'][p], P['ddy'][p], P['ds'][p], P['dw3'][p]
                ddx.append(dQ[p][2 * j][k] - dQ[p][2 * i][k])
                ddy.append(dQ[p][2 * j + 1][k] - dQ[p][2 * i + 1][k])
                t = z
                for m in range(k + 1):
                    t = t + dx[m] * ddx[k - m] + dy[m] * ddy[k - m]
                ds.append(2 * t)
                t = z
                for m in range(k + 1):
                    t = t + w5[m] * ds[k - m]
                dw3.append(arb(-1.5) * t)
                bx = z
                by = z
                for m in range(k + 1):
                    bx = bx + ddx[m] * w3[k - m] + dx[m] * dw3[k - m]
                    by = by + ddy[m] * w3[k - m] + dy[m] * dw3[k - m]
                da = dacc[p]
                da[2 * i] = da[2 * i] + bx
                da[2 * i + 1] = da[2 * i + 1] + by
                da[2 * j] = da[2 * j] - bx
                da[2 * j + 1] = da[2 * j + 1] - by
        for c in range(6):
            Q[c].append(V[c][k] / (k + 1))
            V[c].append(acc[c] / (k + 1))
            for p in range(nt):
                dQ[p][c].append(dV[p][c][k] / (k + 1))
                dV[p][c].append(dacc[p][c] / (k + 1))
    X = Q + V
    TT = [dQ[p] + dV[p] for p in range(nt)]
    return X, TT


def rhs(X, T):
    """Vector field of the combined state + tangent system (coefficient 1 of the Taylor series)."""
    Xc, Tc = taylor(X, T, 2)
    return [x[1] for x in Xc], [[t[1] for t in tp] for tp in Tc]


def _disk(rho):
    return acb(arb(0, rho), arb(0, rho))


def _pair_re_s_positive(B):
    for (i, j) in PAIRS:
        dx = B[2 * j] - B[2 * i]
        dy = B[2 * j + 1] - B[2 * i + 1]
        s = dx * dx + dy * dy
        if not (s.real > 0):
            return False
    return True


def apriori(X0, T0, rho, iters=6):
    """Complex a priori enclosure on the time disc of half-side rho. Returns list of acb boxes or None."""
    Z = [acb(x) for x in X0]
    TZ = [[acb(x) for x in tp] for tp in T0]
    D = _disk(rho)
    F, FT = rhs(Z, TZ)
    B = [Z[c] + D * F[c] * 2 for c in range(12)]
    BT = [[TZ[p][c] + D * FT[p][c] * 2 for c in range(12)] for p in range(len(T0))]
    for _ in range(iters):
        if not _pair_re_s_positive(B):
            return None
        FB, FBT = rhs(B, BT)
        new = [Z[c] + D * FB[c] for c in range(12)]
        newT = [[TZ[p][c] + D * FBT[p][c] for c in range(12)] for p in range(len(T0))]
        ok = all(B[c].contains(new[c]) for c in range(12)) and \
            all(BT[p][c].contains(newT[p][c]) for p in range(len(T0)) for c in range(12))
        if ok:
            return new, newT
        B = [_inflate(x) for x in new]
        BT = [[_inflate(x) for x in tp] for tp in newT]
    return None


def _inflate(x):
    r = x.rad() if hasattr(x, 'rad') else None
    re, im = x.real, x.imag
    e = arb(0, (re.rad() + im.rad()) * arb('0.5') + arb('1e-40'))
    return acb(re + e, im + e)


def _supdev(B, X0):
    m = arb(0)
    for b, x in zip(B, X0):
        d = (b - acb(x.mid())).abs_upper()
        if d > m:
            m = d
    return arb(m.upper())


def step(X0, T0, h, rho, B, BT, N, kappa):
    """Advance by h (arb, possibly an interval with |h| <= kappa*rho). Returns new state and tangents."""
    X, TT = taylor(X0, T0, N)
    dev = _supdev(B, X0)
    for tp, t0 in zip(BT, T0):
        d = _supdev(tp, t0)
        if d > dev:
            dev = d
    tail = dev * arb(kappa) ** N / (1 - arb(kappa))
    tail = arb(0, tail.upper())
    out = []
    for c in range(12):
        acc = X[c][N - 1]
        for k in range(N - 2, -1, -1):
            acc = acc * h + X[c][k]
        out.append(acc + tail)
    outT = []
    for tp in TT:
        row = []
        for c in range(12):
            acc = tp[c][N - 1]
            for k in range(N - 2, -1, -1):
                acc = acc * h + tp[c][k]
            row.append(acc + tail)
        outT.append(row)
    return out, outT


def min_dist(X):
    m = None
    for (i, j) in PAIRS:
        dx = X[2 * j] - X[2 * i]
        dy = X[2 * j + 1] - X[2 * i + 1]
        r = (dx * dx + dy * dy).sqrt()
        m = r if m is None else (r if r.mid() < m.mid() else m)
    return m


def max_speed(X):
    m = arb(0)
    for b in range(3):
        v = (X[6 + 2 * b] ** 2 + X[7 + 2 * b] ** 2).sqrt()
        if v.upper() > m:
            m = arb(v.upper())
    return m


def integrate(X0, T0, t_end, N=60, kappa=1 / 8.0, rho_fac=0.25, log=None, t_end_interval=None):
    """Integrate from t = 0 to t_end (exact arb point). If t_end_interval = (lo_offset, hi_offset) is given,
    the final step lands on the interval [t_end + lo_offset, t_end + hi_offset] instead."""
    t = arb(0)
    X, T = list(X0), [list(tp) for tp in T0]
    nsteps = 0
    kappa_a = arb(kappa)
    while True:
        rem = t_end - t
        rho = rho_fac * float(min_dist(X).mid()) / (1.0 + float(max_speed(X).mid()))
        res = None
        while res is None:
            res = apriori(X, T, arb(rho))
            if res is None:
                rho *= 0.5
                if rho < 1e-12:
                    raise RuntimeError('a priori enclosure failed at t=%s' % t)
        B, BT = res
        hmax = kappa * rho
        last = rem.upper() <= hmax * 0.999 and (t_end_interval is None or
                                                 (rem + t_end_interval[1]).upper() <= hmax * 0.999)
        if last:
            if t_end_interval is None:
                h = rem
            else:
                lo, hi = t_end_interval
                h = (rem + lo).union(rem + hi)
            X, T = step(X, T, h, rho, B, BT, N, kappa)
            nsteps += 1
            t = t + h
            break
        h = arb(float(hmax * 0.999))
        X, T = step(X, T, h, rho, B, BT, N, kappa)
        t = t + h
        nsteps += 1
        if log is not None and nsteps % 50 == 0:
            log('step %d t=%.6f rho=%.3e maxrad=%.3e' % (nsteps, float(t.mid()), rho,
                                                       max(float(x.rad()) for x in X)))
    return X, T, nsteps
