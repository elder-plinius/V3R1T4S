#!/usr/bin/env python3
"""Exact slice-and-absorb engine for matrix multiplication schemes over Q.

Scheme: (n1, n2, n3, terms); term = [u, v, w], each a dict index -> Fraction.
Convention (as LITA): m_k = <u_k, A> <v_k, B>, C = sum_k w_k m_k, with u index i*n2+j, v index j*n3+l, w index i*n3+l.

Slice along an axis with a direction pair (e, f), <e, f> != 0 (a generalised one-slice restriction):
  axis 0 (i):  U' = E^T U, W' = F^T W     kills terms with U = e x^T or W = f y^T
  axis 1 (j):  U' = U E,   V' = F^T V     kills terms with U = x e^T or V = f y^T
  axis 2 (l):  V' = V E,   W' = W F       kills terms with V = x e^T or W = y f^T
where col(E) = e^perp, col(F) = f^perp and E^T F = I.

Absorption (2-reduction): if sum_t c_t X_t (x) Y_t = 0 for a pairing (X, Y) of two factor types, then
Z_t -> Z_t - c_t Z_q removes term q (c_q = 1). Kernels are found modulo two 62-bit primes on a random
projection, lifted by CRT and rational reconstruction, and verified exactly before use.
"""
import json, random, sys, time
from fractions import Fraction
from math import gcd, isqrt
import flint

P1 = 4611686018427387847  # primes below 2^62
P2 = 4611686018427387817

# ---------------------------------------------------------------- io
def load_json(path):
    s = json.load(open(path))
    n1, n2, n3 = s["format"]
    terms = []
    for t in s["terms"]:
        tt = []
        for ax in "uvw":
            d = {}
            for idx, c in t[ax]:
                c = Fraction(c)
                if c:
                    d[int(idx)] = d.get(int(idx), 0) + c
            tt.append({k: v for k, v in d.items() if v})
        terms.append(tt)
    return clean((n1, n2, n3, terms))

def save_json(S, path, note=""):
    n1, n2, n3, terms = S
    out = {"format": [n1, n2, n3], "rank": len(terms), "ring": "Q",
           "convention": "m_k=(sum u_k[i*n2+j]A[i][j])*(sum v_k[j*n3+l]B[j][l]); C[i][l]=sum_k w_k[i*n3+l] m_k",
           "note": note,
           "terms": [{ax: [[k, str(c)] for k, c in sorted(f.items())] for ax, f in zip("uvw", t)} for t in terms]}
    json.dump(out, open(path, "w"))

def clean(S):
    n1, n2, n3, terms = S
    return (n1, n2, n3, [t for t in terms if all(len(f) for f in t)])

def dims(S, ax):
    """(rows, cols) of the u, v, w factor matrices."""
    n1, n2, n3 = S[:3]
    return {"u": (n1, n2), "v": (n2, n3), "w": (n1, n3)}[ax]

# ---------------------------------------------------------------- linear algebra helpers
def normalize(vec):
    """Scale so the first nonzero entry is 1; return a tuple of Fractions."""
    for x in vec:
        if x:
            return tuple(Fraction(y) / x for y in vec)
    return None

def rank1(f, rows, cols):
    """If the factor (dict over rows x cols) is rank one, return (left, right) normalised vectors, else None."""
    if not f:
        return None
    M = {}
    for idx, c in f.items():
        r, cc = divmod(idx, cols)
        M.setdefault(r, {})[cc] = c
    rs = sorted(M)
    r0 = rs[0]
    base = M[r0]
    c0 = min(base)
    for r in rs[1:]:
        row = M[r]
        if set(row) != set(base):
            return None
        lam = row[c0] / base[c0]
        for cc, x in row.items():
            if x != lam * base[cc]:
                return None
    left = [Fraction(0)] * rows
    for r in rs:
        left[r] = M[r][c0] / base[c0]
    right = [Fraction(0)] * cols
    for cc, x in base.items():
        right[cc] = x
    return normalize(left), normalize(right)

def perp_basis(e):
    """Columns spanning e^perp: for q != p, unit_q - (e_q/e_p) unit_p, p the first nonzero index of e."""
    n = len(e)
    p = next(i for i, x in enumerate(e) if x)
    cols = []
    for q in range(n):
        if q == p:
            continue
        col = [Fraction(0)] * n
        col[q] = Fraction(1)
        col[p] = -Fraction(e[q]) / e[p]
        cols.append(col)
    return cols  # list of n-1 columns, each length n

def mat_inv(G):
    n = len(G)
    A = [list(map(Fraction, row)) + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(G)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c])
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c]:
                fct = A[r][c]
                A[r] = [x - fct * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]

def slice_maps(e, f):
    """E (n x n-1) with col(E)=e^perp, F (n x n-1) with col(F)=f^perp and E^T F = I. Returned as column lists."""
    e = [Fraction(x) for x in e]; f = [Fraction(x) for x in f]
    if sum(a * b for a, b in zip(e, f)) == 0:
        raise ValueError("<e,f> = 0")
    Ec = perp_basis(e)
    F0 = perp_basis(f)
    m = len(Ec)
    G = [[sum(Ec[a][i] * F0[b][i] for i in range(len(e))) for b in range(m)] for a in range(m)]  # E^T F0
    Gi = mat_inv(G)  # F = F0 Gi  =>  E^T F = G Gi = I
    Fc = [[sum(F0[b][i] * Gi[b][a] for b in range(m)) for i in range(len(e))] for a in range(m)]
    return Ec, Fc

def apply_left(f, rows, cols, M):
    """f is rows x cols; return M^T f where M is given as a list of columns (each length rows): new rows = len(M)."""
    out = {}
    byrow = {}
    for idx, c in f.items():
        r, cc = divmod(idx, cols)
        byrow.setdefault(r, []).append((cc, c))
    for a, col in enumerate(M):
        for r, items in byrow.items():
            m = col[r]
            if m:
                for cc, c in items:
                    k = a * cols + cc
                    out[k] = out.get(k, 0) + m * c
    return {k: v for k, v in out.items() if v}

def apply_right(f, rows, cols, M):
    """f is rows x cols; return f M where M is a list of columns (each length cols): new cols = len(M)."""
    out = {}
    nc = len(M)
    bycol = {}
    for idx, c in f.items():
        r, cc = divmod(idx, cols)
        bycol.setdefault(cc, []).append((r, c))
    for a, col in enumerate(M):
        for cc, items in bycol.items():
            m = col[cc]
            if m:
                for r, c in items:
                    k = r * nc + a
                    out[k] = out.get(k, 0) + c * m
    return {k: v for k, v in out.items() if v}

def restrict(S, axis, e, f):
    n1, n2, n3, terms = S
    Ec, Fc = slice_maps(e, f)
    new = []
    for u, v, w in terms:
        if axis == 0:
            u2 = apply_left(u, n1, n2, Ec); w2 = apply_left(w, n1, n3, Fc); v2 = v
        elif axis == 1:
            u2 = apply_right(u, n1, n2, Ec); v2 = apply_left(v, n2, n3, Fc); w2 = w
        else:
            v2 = apply_right(v, n2, n3, Ec); w2 = apply_right(w, n1, n3, Fc); u2 = u
        new.append([u2, v2, w2])
    nd = [n1, n2, n3]
    nd[axis] -= 1
    return clean((nd[0], nd[1], nd[2], new))

def kill_groups(S, axis):
    """Map normalised direction -> set of terms it kills, for the e side and the f side of a slice on this axis."""
    n1, n2, n3, terms = S
    ge, gf = {}, {}
    for k, (u, v, w) in enumerate(terms):
        if axis == 0:
            ru = rank1(u, n1, n2); rw = rank1(w, n1, n3)
            de = ru[0] if ru else None; df = rw[0] if rw else None
        elif axis == 1:
            ru = rank1(u, n1, n2); rv = rank1(v, n2, n3)
            de = ru[1] if ru else None; df = rv[0] if rv else None
        else:
            rv = rank1(v, n2, n3); rw = rank1(w, n1, n3)
            de = rv[1] if rv else None; df = rw[1] if rw else None
        if de is not None:
            ge.setdefault(de, set()).add(k)
        if df is not None:
            gf.setdefault(df, set()).add(k)
    return ge, gf

def best_pairs(S, axis, top=20, extra_dirs=()):
    """Candidate (e, f, kills) for a slice on this axis, sorted by direct kill count."""
    ge, gf = kill_groups(S, axis)
    n = S[axis]
    es = sorted(ge.items(), key=lambda x: -len(x[1]))[:top]
    fs = sorted(gf.items(), key=lambda x: -len(x[1]))[:top]
    units = [tuple(Fraction(int(i == j)) for j in range(n)) for i in range(n)]
    es += [(d, ge.get(d, set())) for d in list(extra_dirs) + units if d not in dict(es)]
    fs += [(d, gf.get(d, set())) for d in list(extra_dirs) + units if d not in dict(fs)]
    out = []
    for e, ke in es:
        for f, kf in fs:
            if sum(a * b for a, b in zip(e, f)) != 0:
                out.append((len(ke | kf), e, f))
    out.sort(key=lambda x: -x[0])
    return out

# ---------------------------------------------------------------- absorption
def _mod_val(c, p):
    return (c.numerator % p) * pow(c.denominator % p, -1, p) % p

def ratrecon(a, m):
    """Rational reconstruction of a mod m with |num|, den <= sqrt(m/2)."""
    a %= m
    bound = isqrt(m // 2)
    r0, r1 = m, a
    s0, s1 = 0, 1
    while r1 > bound:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if s1 == 0 or abs(s1) > bound:
        return None
    return Fraction(r1, s1) if s1 > 0 else Fraction(-r1, -s1)

def kernel_rref(S, pair, order, p, nproj, seed):
    """RREF mod p of the projected pairing map; columns in the given term order. Returns (rref rows, pivots, rank)."""
    n1, n2, n3, terms = S
    X, Y = pair  # factor slots 0,1,2 (u, v, w)
    sz = {0: n1 * n2, 1: n2 * n3, 2: n1 * n3}
    rnd = random.Random(seed)
    ys = [[rnd.randrange(p) for _ in range(sz[Y])] for _ in range(nproj)]
    R = len(order)
    nrows = nproj * sz[X]
    M = flint.nmod_mat(nrows, R, p)
    for col, t in enumerate(order):
        fx = terms[t][X]; fy = terms[t][Y]
        for s in range(nproj):
            y = ys[s]
            dot = 0
            for idx, c in fy.items():
                dot += _mod_val(c, p) * y[idx]
            dot %= p
            if dot == 0:
                continue
            base = s * sz[X]
            for idx, c in fx.items():
                M[base + idx, col] = _mod_val(c, p) * dot % p
    Rr, rank = M.rref()
    return Rr, rank

def find_kernel(S, pair, order=None, nproj=None, seed=1):
    """Exact kernel vectors {term: Fraction} of c -> sum c_t X_t (x) Y_t, one per free column, in RREF form."""
    n1, n2, n3, terms = S
    R = len(terms)
    if order is None:
        order = list(range(R))
    X = pair[0]
    szx = {0: n1 * n2, 1: n2 * n3, 2: n1 * n3}[X]
    if nproj is None:
        nproj = max(2, -(-(R + R // 8 + 16) // szx))
    res = []
    for p in (P1, P2):
        Rr, rank = kernel_rref(S, pair, order, p, nproj, seed)
        res.append((Rr, rank))
    (R1, rk1), (R2, rk2) = res
    if rk1 != rk2:
        return None
    rank = rk1
    # pivot columns
    piv = []
    row = 0
    for col in range(R):
        if row < rank and int(R1[row, col]) != 0:
            piv.append(col); row += 1
    free = [c for c in range(R) if c not in set(piv)]
    m = P1 * P2
    kers = []
    for q in free:
        vec = {order[q]: Fraction(1)}
        ok = True
        for r, pc in enumerate(piv):
            a1 = int(R1[r, q]); a2 = int(R2[r, q])
            if a1 == 0 and a2 == 0:
                continue
            # value of pivot coordinate is -rref[r, q]
            x = (a1 * P2 * pow(P2, -1, P1) + a2 * P1 * pow(P1, -1, P2)) % m
            fr = ratrecon((-x) % m, m)
            if fr is None:
                ok = False; break
            if fr:
                vec[order[pc]] = fr
        if ok:
            kers.append(vec)
    return kers

def verify_kernel(S, pair, vec):
    n1, n2, n3, terms = S
    X, Y = pair
    acc = {}
    for t, c in vec.items():
        fx = terms[t][X]; fy = terms[t][Y]
        for ix, cx in fx.items():
            cc = c * cx
            for iy, cy in fy.items():
                key = (ix, iy)
                acc[key] = acc.get(key, 0) + cc * cy
    return all(v == 0 for v in acc.values())

def absorb_once(S, pair, order=None, seed=1):
    """Remove one term per verified kernel vector (free column). Returns (new scheme, removed count)."""
    kers = find_kernel(S, pair, order=order, seed=seed)
    if not kers:
        return S, 0
    n1, n2, n3, terms = S
    Z = 3 - pair[0] - pair[1]
    terms = [[dict(f) for f in t] for t in terms]
    removed = 0
    Sx = (n1, n2, n3, terms)
    for vec in kers:
        if not verify_kernel(Sx, pair, vec):
            continue
        q = next(iter(vec))  # the free column, coefficient exactly 1 (first key inserted)
        zq = dict(terms[q][Z])
        if not zq:
            continue
        for t, c in vec.items():
            if t == q:
                continue
            zt = terms[t][Z]
            for idx, x in zq.items():
                val = zt.get(idx, 0) - c * x
                if val:
                    zt[idx] = val
                else:
                    zt.pop(idx, None)
        terms[q][Z] = {}
        removed += 1
    return clean((n1, n2, n3, terms)), removed

PAIRS = [(0, 1), (0, 2), (1, 2)]

def absorb_all(S, max_rounds=50, seed=1, log=None, order_fn=None):
    quiet = 0
    rounds = 0
    total = 0
    pi = 0
    while quiet < 3 and rounds < max_rounds:
        pair = PAIRS[pi % 3]
        order = order_fn(S, pair) if order_fn else None
        S2, k = absorb_once(S, pair, order=order, seed=seed + rounds)
        if k:
            S = S2; total += k; quiet = 0
            if log:
                log("  absorb pair %s removed %d -> rank %d" % (pair, k, len(S[3])))
        else:
            quiet += 1
        pi += 1
        rounds += 1
    return S, total

# ---------------------------------------------------------------- branching absorption
def remove_with(S, pair, vec, q):
    """Use kernel vector vec (sum c_t X_t (x) Y_t = 0) to remove term q (vec[q] != 0) by shifting the free factors."""
    n1, n2, n3, terms = S
    Z = 3 - pair[0] - pair[1]
    terms = [[dict(f) for f in t] for t in terms]
    cq = vec[q]
    zq = dict(terms[q][Z])
    for t, c in vec.items():
        if t == q:
            continue
        zt = terms[t][Z]
        r = c / cq
        for idx, x in zq.items():
            val = zt.get(idx, 0) - r * x
            if val:
                zt[idx] = val
            else:
                zt.pop(idx, None)
    terms[q][Z] = {}
    return clean((n1, n2, n3, terms))

def all_kernels(S):
    out = []
    for pair in PAIRS:
        ks = find_kernel(S, pair) or []
        for v in ks:
            if verify_kernel(S, pair, v):
                out.append((pair, v))
    return out

def branch_absorb(S, depth=3, width=8, log=print, seen=None):
    """Depth-limited search over which term each kernel vector removes. Returns the best scheme found."""
    best = S
    ks = all_kernels(S)
    if not ks or depth == 0:
        return best
    tried = 0
    for pair, vec in ks:
        for q in list(vec)[:width]:
            S2 = remove_with(S, pair, vec, q)
            tried += 1
            r = branch_absorb(S2, depth - 1, width, log)
            if len(r[3]) < len(best[3]):
                best = r
                log("    branch: pair %s remove %d -> %d (best %d)" % (pair, q, len(S2[3]), len(best[3])))
    return best

# ---------------------------------------------------------------- flip-then-merge
def fkey(f):
    """Projective key of a factor: entries divided by the first nonzero entry."""
    if not f:
        return None
    items = sorted(f.items())
    c0 = items[0][1]
    return tuple((k, v / c0) for k, v in items)

def in_span2(y, a, b):
    """Return (alpha, beta) with y = alpha*a + beta*b exactly, or None (dict vectors)."""
    keys = sorted(set(y) | set(a) | set(b))
    # solve with two pivot coordinates
    rows = [(a.get(k, 0), b.get(k, 0), y.get(k, 0)) for k in keys]
    # Gaussian elimination on a 2-unknown system
    piv = None
    for r in rows:
        if r[0] or r[1]:
            piv = r; break
    if piv is None:
        return None
    sol = None
    for r in rows:
        det = piv[0] * r[1] - piv[1] * r[0]
        if det:
            al = (piv[2] * r[1] - piv[1] * r[2]) / det
            be = (piv[0] * r[2] - piv[2] * r[0]) / det
            sol = (al, be); break
    if sol is None:
        # a and b parallel on all coordinates: y must be a multiple of the pivot direction
        return None
    al, be = sol
    for (x1, x2, yy) in rows:
        if al * x1 + be * x2 != yy:
            return None
    return sol

def flip_merge_moves(S):
    """All (a, b, c, X, Y) such that a, b share slot X, c shares slot Z with a, and Y_c in span(Y_a, Y_b) with a
    nonzero Y_a coefficient: flipping (a, b) by mu = beta/alpha makes a and c share Y and Z, so they merge."""
    n1, n2, n3, terms = S
    groups = [{}, {}, {}]
    for t, tt in enumerate(terms):
        for s in range(3):
            groups[s].setdefault(fkey(tt[s]), []).append(t)
    moves = []
    for X in range(3):
        for g in groups[X].values():
            if len(g) < 2:
                continue
            for a in g:
                for b in g:
                    if a == b:
                        continue
                    for Y in range(3):
                        if Y == X:
                            continue
                        Z = 3 - X - Y
                        for c in groups[Z][fkey(terms[a][Z])]:
                            if c in (a, b):
                                continue
                            sol = in_span2(terms[c][Y], terms[a][Y], terms[b][Y])
                            if sol and sol[0] != 0:
                                moves.append((a, b, c, X, Y, sol))
    return moves

def apply_flip_merge(S, move):
    """Flip (a, b) on shared slot X: Y_a += mu*Y_b (scaled to the X-proportionality), Z_b -= mu*lam*Z_a; then merge a into c."""
    n1, n2, n3, terms = S
    a, b, c, X, Y, (al, be) = move
    Z = 3 - X - Y
    terms = [[dict(f) for f in t] for t in terms]
    # X_b = lam * X_a
    ka = min(terms[a][X]); lam = terms[b][X][ka] / terms[a][X][ka]
    # a(X_a, Y_a, Z_a) + b(lam X_a, Y_b, Z_b) = a(X_a, Y_a + mu Y_b, Z_a) + b(lam X_a, Y_b, Z_b - (mu/lam) Z_a)
    mu = be / al
    for k, x in terms[b][Y].items():
        terms[a][Y][k] = terms[a][Y].get(k, 0) + mu * x
    terms[a][Y] = {k: v for k, v in terms[a][Y].items() if v}
    for k, x in terms[a][Z].items():
        terms[b][Z][k] = terms[b][Z].get(k, 0) - (mu / lam) * x
    terms[b][Z] = {k: v for k, v in terms[b][Z].items() if v}
    # now Y_a' = Y_c / al, Z_a = rho Z_c: term a = (X_a, Y_c/al, rho Z_c); fold into c's X factor
    kz = min(terms[c][Z]); rho = terms[a][Z][kz] / terms[c][Z][kz]
    for k, x in terms[a][X].items():
        terms[c][X][k] = terms[c][X].get(k, 0) + (rho / al) * x
    terms[c][X] = {k: v for k, v in terms[c][X].items() if v}
    terms[a] = [{}, {}, {}]
    return clean((n1, n2, n3, terms))
