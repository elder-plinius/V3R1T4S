"""Flat (consensus) absorption on engine.py schemes, re-implemented from the method described in the contributors'
ca.py (known-knowns/faster-matrix-multiplication/2026-10-15-anonymous-c6d1e0ab-4b68518a/how-we-built-it/opus_step/).

For a pairing (X, Y) with an exact, verified kernel basis c^(1..k) of c -> sum_t c_t X_t (x) Y_t, and ell_t in Q^k the
coordinates of term t, every linear Phi: Q^k -> Q^m gives an equal tensor with Z_t -> Z_t + Phi(ell_t). Term t dies
iff the point y_t = (ell_t, Z_t) lies in the graph {(l, -Phi(l))}, a k-dimensional subspace transverse to {0} x Q^m.
We grow a subspace H point by point (a whole quotient-direction group joins at once), keeping the ell parts
independent, choosing the heaviest group (random among ties: 'rflat'), several restarts; the search runs modulo
2^31-1 on three random projections of Z. Phi is then solved exactly over Q from the chosen points and applied
exactly; kills are recounted exactly (the mod-p prediction is only a guide).
Library: flat_once(S, pair, rng, restarts), flat_all(S, rng, restarts, max_rounds)."""
import os, sys, random
from fractions import Fraction
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import find_kernel, verify_kernel, clean, PAIRS

P = 2147483647
NPROJ = 3


def modp(x):
    return (x.numerator % P) * pow(x.denominator % P, P - 2, P) % P


class Kern:
    def __init__(self, S, pair, kers, rng):
        n1, n2, n3, terms = S
        self.Z = Z = 3 - pair[0] - pair[1]
        self.k = k = len(kers)
        self.sup = sorted(set().union(*[set(v) for v in kers]))
        self.ell = {t: [kers[s].get(t, Fraction(0)) for s in range(k)] for t in self.sup}
        cl, keys = {}, []
        for t in self.sup:
            lt = self.ell[t]
            nz = next(x for x in lt if x != 0)
            key = (tuple(x / nz for x in lt), tuple(sorted((a, x / nz) for a, x in terms[t][Z].items())))
            if key not in cl:
                cl[key] = []
                keys.append(key)
            cl[key].append(t)
        self.keys = keys
        self.members = [cl[q] for q in keys]
        self.weight = np.array([len(m) for m in self.members], dtype=np.int64)
        m = {0: n1 * n2, 1: n2 * n3, 2: n1 * n3}[Z]
        g = [[rng.randrange(1, P) for _ in range(m)] for _ in range(NPROJ)]
        Y = np.zeros((len(keys), k + NPROJ), dtype=np.int64)
        for c, (ray, val) in enumerate(keys):
            for j, x in enumerate(ray):
                Y[c, j] = modp(x)
            for q in range(NPROJ):
                s = 0
                for a, x in val:
                    s = (s + modp(x) * g[q][a]) % P
                Y[c, k + q] = s
        self.Y = Y


def _norm_key(row):
    nzi = np.flatnonzero(row)
    if len(nzi) == 0:
        return None, None
    inv = pow(int(row[nzi[0]]), P - 2, P)
    return int(nzi[0]), ((row * inv) % P).tobytes()


def rflat(kern, rng, mode="rflat"):
    """Grow H; returns (predicted kill weight, chosen cluster indices)."""
    k = kern.k
    R = kern.Y.copy()            # rows reduced modulo the current H
    closed = np.zeros(len(kern.keys), dtype=bool)
    chosen = []
    for _ in range(k):
        idx = np.flatnonzero(~closed)
        if len(idx) == 0:
            break
        groups = {}
        for c in idx:
            piv, key = _norm_key(R[c])
            if key is None:
                closed[c] = True
                continue
            if piv >= k:          # ell part already in the span: would break transversality
                continue
            g = groups.setdefault(key, [0, []])
            g[0] += int(kern.weight[c])
            g[1].append(int(c))
        if not groups:
            break
        gl = sorted(groups.values(), key=lambda g: (-g[0], g[1][0]))
        top = gl[0][0]
        if mode == "rflat":
            ties = [g for g in gl if g[0] == top]
            pick = ties[rng.randrange(len(ties))]
        elif mode == "noisy":
            pick = max(gl[:12], key=lambda g: g[0] * (1 + 0.6 * rng.random()))
        else:
            pick = gl[0]
        rep = pick[1][0]
        chosen.append(rep)
        # add rep's reduced row as a new pivot row and reduce every row by it
        row = R[rep].copy()
        piv = int(np.flatnonzero(row)[0])
        row = (row * pow(int(row[piv]), P - 2, P)) % P
        col = R[:, piv].copy()
        nzm = col != 0
        R[nzm] = (R[nzm] - (col[nzm, None] * row[None, :]) % P) % P
        closed |= ~R.any(axis=1)
    return int(kern.weight[closed].sum()), chosen


def _groups(kern, R, closed):
    k = kern.k
    groups = {}
    for c in np.flatnonzero(~closed):
        piv, key = _norm_key(R[c])
        if key is None or piv >= k:
            continue
        g = groups.setdefault(key, [0, []])
        g[0] += int(kern.weight[c])
        g[1].append(int(c))
    return sorted(groups.values(), key=lambda g: (-g[0], g[1][0]))


def _add(R, rep):
    R = R.copy()
    row = R[rep].copy()
    piv = int(np.flatnonzero(row)[0])
    row = (row * pow(int(row[piv]), P - 2, P)) % P
    col = R[:, piv].copy()
    nzm = col != 0
    R[nzm] = (R[nzm] - (col[nzm, None] * row[None, :]) % P) % P
    return R


def beam(kern, width=6, branch=3):
    """Beam search over the growth of H (states deduplicated by their closed set)."""
    k = kern.k
    R0 = kern.Y.copy()
    st = [(R0, ~R0.any(axis=1), [])]
    best = (0, [])
    for _ in range(k):
        cand = []
        for R, closed, ch in st:
            for w, mem in _groups(kern, R, closed)[:branch]:
                R2 = _add(R, mem[0])
                cl2 = ~R2.any(axis=1)
                cand.append((int(kern.weight[cl2].sum()), R2, cl2, ch + [mem[0]]))
        if not cand:
            break
        cand.sort(key=lambda x: -x[0])
        seen, nst = set(), []
        for w, R2, cl2, ch in cand:
            key = np.flatnonzero(cl2).tobytes()
            if key in seen:
                continue
            seen.add(key)
            if w > best[0]:
                best = (w, ch)
            nst.append((R2, cl2, ch))
            if len(nst) >= width:
                break
        st = nst
    return best


def solve_phi(kern, terms, chosen):
    """Exact Phi as k dicts phi_s (Z index -> Fraction) with sum_s ell_c[s] phi_s = -Z_c for every chosen c."""
    k = kern.k
    rows = [list(kern.keys[c][0]) for c in chosen]                       # d x k
    rhs = [{a: -x for a, x in kern.keys[c][1]} for c in chosen]          # d dicts
    d = len(rows)
    A = [r[:] for r in rows]
    B = [dict(b) for b in rhs]
    pivcols = []
    r = 0
    for col in range(k):
        sel = next((i for i in range(r, d) if A[i][col] != 0), None)
        if sel is None:
            continue
        A[r], A[sel] = A[sel], A[r]
        B[r], B[sel] = B[sel], B[r]
        inv = 1 / A[r][col]
        A[r] = [x * inv for x in A[r]]
        B[r] = {a: x * inv for a, x in B[r].items()}
        for i in range(d):
            if i != r and A[i][col] != 0:
                f = A[i][col]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
                bi = B[i]
                for a, x in B[r].items():
                    v = bi.get(a, 0) - f * x
                    if v:
                        bi[a] = v
                    else:
                        bi.pop(a, None)
        pivcols.append(col)
        r += 1
        if r == d:
            break
    assert r == d, "chosen rays not independent"
    phi = [dict() for _ in range(k)]
    for i, col in enumerate(pivcols):     # non-pivot phi_s = 0; RREF gives phi_pivot = B row
        phi[col] = B[i]
    return phi


def apply_phi(S, kern, phi):
    n1, n2, n3, terms = S
    Z = kern.Z
    new = [[dict(f) for f in t] for t in terms]
    for t in kern.sup:
        z = new[t][Z]
        for s, l in enumerate(kern.ell[t]):
            if l:
                for a, x in phi[s].items():
                    v = z.get(a, 0) + l * x
                    if v:
                        z[a] = v
                    else:
                        z.pop(a, None)
    S2 = clean((n1, n2, n3, new))
    return S2, len(terms) - len(S2[3])


def flat_once(S, pair, rng, restarts=8, mode="rflat", seed=1):
    kers = find_kernel(S, pair, seed=seed)
    if not kers:
        return S, 0, 0
    kers = [v for v in kers if verify_kernel(S, pair, v)]
    if not kers:
        return S, 0, 0
    kern = Kern(S, pair, kers, rng)
    best = None
    if mode == "beam":
        best = beam(kern)
    for i in range(max(1, restarts)):
        w, ch = rflat(kern, rng, mode="greedy" if (i == 0 and mode not in ("noisy", "beam")) else
                      ("rflat" if mode == "beam" else mode))
        if best is None or w > best[0]:
            best = (w, ch)
    w, ch = best
    if not ch:
        return S, 0, kern.k
    phi = solve_phi(kern, S[3], ch)
    S2, kills = apply_phi(S, kern, phi)
    if kills < w:      # projection collision: the exact step still is a valid scheme, only fewer kills
        print("    note: exact kills %d below mod-p prediction %d" % (kills, w), flush=True)
    return S2, kills, kern.k


def flat_all(S, rng=None, restarts=8, max_rounds=60, mode="rflat", log=None, start=0):
    rng = rng or random.Random(1)
    quiet, total, pi = 0, 0, start
    for rnd in range(max_rounds):
        pair = PAIRS[pi % 3]
        S2, kills, k = flat_once(S, pair, rng, restarts=restarts, mode=mode, seed=1 + rnd)
        if kills:
            S, total, quiet = S2, total + kills, 0
            if log:
                log("  flat pair %s k=%d removed %d -> rank %d" % (pair, k, kills, len(S[3])))
        else:
            quiet += 1
            if quiet >= 3:
                break
        pi += 1
    return S, total
