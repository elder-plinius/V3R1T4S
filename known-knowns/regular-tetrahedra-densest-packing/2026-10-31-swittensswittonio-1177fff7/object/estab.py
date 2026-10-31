"""Lemma V2 (REDUCTION2.md section 1): sharper single-wedge excess  E2(e) = sup over wedges W (dihedral theta, c not interior,
edge line at distance <= e from c) of  vol(W)/vol(B) - alpha,  using BOTH face offsets (s1 = -t <= 0, s2 >= 0):
     vol(W) = alpha + Vslab(s1,s2) - Loss(t)      (exact identity, see REDUCTION2.md 1.1)
     Vslab = int_0^{s2} A(x0; -t) dx0 ,  A(x0;s1) = R^2 (pi - arccos y + y sqrt(1-y^2)),  R^2 = 1-x0^2,  y = (s1 + kappa x0)/(R sin theta)
     Loss(t) = int_0^t B(x1) dx1 ,      B(x1)    = R^2 (pi - arccos y + y sqrt(1-y^2)),  R^2 = 1-x1^2,  y = -kappa x1/(R sin theta)
     edge-distance constraint:  s2 <= s2max(t,e) = kappa t + sqrt((1-kappa^2)(e^2 - t^2)),  0 <= t <= e.
All evaluated with Arb balls: per t-cell [t0,t1]: upper bound  Vslab_up(t0, sup s2max over cell) - Loss_lo(t0).
Valid for e <= EMAX = 0.5 (needs |y|<1 in the integrals; checked by Arb acos domain); for larger e the old Lemma V bound E_up is used."""
import math, bisect
from flint import arb, ctx
import rig_dp as R
ctx.prec = 160
PI = R.PI; KAP = arb(1) / 3; SIN = (1 - KAP * KAP).sqrt(); K2 = 1 - KAP * KAP
EMAX = 0.9
NT = 36        # t cells
NX = 48        # x cells per integral

def _bracket(y):
    return PI - y.acos() + y * (1 - y * y).sqrt()

def A2(x0, s1):
    R2 = 1 - x0 * x0
    y = (s1 + KAP * x0) / (R2.sqrt() * SIN)
    return R2 * _bracket(y)

def Bl(x1):
    R2 = 1 - x1 * x1
    y = -(KAP * x1) / (R2.sqrt() * SIN)
    return R2 * _bracket(y)

def _cell_ball(a, b):
    """arb ball containing [a,b] for arb endpoints a<=b (uses uppers/lowers)."""
    lo = a.lower(); hi = b.upper()
    return arb((lo + hi) / 2, (hi - lo) / 2)

def _sq_up(d):
    """upper bound of sqrt(max(d,0)) for arb d."""
    return arb(max(0.0, float(d.upper())) * (1 + 1e-15) + 0.0).sqrt() if float(d.upper()) > 0 else arb(0)

def _s2max_up(t, e):
    """upper bound of kappa t + sqrt((1-kappa^2)(e^2-t^2)) at arb t (|t|<=e up to rounding)."""
    return KAP * t + _sq_up(K2 * (e * e - t * t))

def E2_up_exact(e):
    """certified upper bound (python float) of E2 at edge distance e (float, treated exactly)."""
    e = arb(e)
    best = arb(0)
    tstar = KAP * e
    # t cells: t_i = e (i/NT)^2
    for i in range(NT):
        t0 = e * arb(i * i) / (NT * NT); t1 = e * arb((i + 1) * (i + 1)) / (NT * NT)
        # sup over the cell of kappa t + sqrt(K2 (e^2 - t^2)) <= kappa t1 + sqrt(K2 (e^2 - t0^2)) and <= e (global max)
        S2 = KAP * t1 + _sq_up(K2 * (e * e - t0 * t0))
        if float(S2.upper()) > float(e.upper()): S2 = e
        S2 = arb(R.up(S2))
        # Vslab upper: int_0^{S2} A2(x0; -t0) dx0 via per-cell ball enclosures
        tot = arb(0); h = S2 / NX
        for j in range(NX):
            xb = arb(((2 * j + 1) * h / 2).mid(), (h / 2).upper())
            tot += A2(xb, -t0).upper() * h
        # Loss lower: int_0^{t0} B (decreasing) with right endpoints
        loss = arb(0)
        if float(t0.upper()) > 0:
            hh = t0 / NX
            for j in range(NX):
                loss += Bl(hh * (j + 1)).lower() * hh
        val = 3 / (4 * PI) * (tot - loss)
        if not val.is_finite(): raise ValueError('non-finite enclosure in E2 (domain of acos?) at e=%r cell %d' % (float(e), i))
        if float(val.upper()) > float(best.upper()): best = arb(val.upper())
    return R.up(best)

def up_pos(x):
    return arb(max(0.0, float(x.upper())))

# ---- certified table on a geometric grid; E_up(u) = table value at the next grid point >= u (monotone => valid) ----
E_LO, RATIO = 1e-5, 1.012
GRID = []; TAB = []
def _build():
    if GRID: return
    e = E_LO
    while e < EMAX * (1 + 1e-12):
        GRID.append(e); e *= RATIO
    GRID.append(EMAX)
    for g in GRID:
        # the grid value is rounded to a float, the bound is for exactly that float
        TAB.append(E2_up_exact(g))
    # make the table monotone (running max) -- the true sup is non-decreasing in e, so this keeps validity
    for i in range(1, len(TAB)):
        if TAB[i] < TAB[i - 1]: TAB[i] = TAB[i - 1]

def E2_table(e_up):
    """certified upper bound of E2 for any edge distance <= e_up (python float), e_up <= EMAX."""
    _build()
    i = bisect.bisect_left(GRID, e_up)
    return TAB[i] if i < len(GRID) else None

_old_E_up = R.E_up
_old_E_f = R.E_f
def E_up_combined(u):
    """certified: min(old Lemma V bound, Lemma V2 bound)."""
    uu = float(u.upper())
    old = _old_E_up(u)
    if uu <= EMAX:
        new = E2_table(math.nextafter(uu, math.inf))
        if new is not None: return min(old, new)
    return old

def E_f_table(e):
    """float (search only)."""
    if e <= EMAX:
        _build()
        i = bisect.bisect_left(GRID, e)
        if i < len(GRID): return min(_old_E_f(e), TAB[i])
    return _old_E_f(e)

if __name__ == "__main__":
    import time
    t0 = time.time()
    for e in (1e-4, 1e-3, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5):
        old = float(_old_E_up(arb(e)))
        new = E2_up_exact(e)
        print("e=%-8g old E_up=%.6e   E2_up=%.6e   ratio=%.4f   old/e=%.4f new/e=%.4f" % (e, old, new, new / old, old / e, new / e), flush=True)
    print("time", time.time() - t0)
