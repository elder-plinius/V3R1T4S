#!/usr/bin/env python3
"""AG codes on the Hermitian curve y^3 + y = x^4 over GF(9), evaluated at all 28 rational points (27 affine + P_inf),
with divisor G = a Q + b P_inf, Q a place of degree 3.
This is the family codetables.de uses for its [28,13,13]_9 ("AlgebraicGeometricCode ... based on 1 divisors of
degree [3]") and its [33,13,16]_9 (Construction X on two of them).

Method. Q has a representative point (x0, y0) over GF(729) with x0 not in GF(9). p(x) = prod (x - x0^(9^t)), t = 0..2,
is in GF(9)[x]; div p(x) = Q + Q' + Q'' - 9 P_inf, where Q', Q'' are the places of (x0, y0 + i), (x0, y0 - i)
(i^2 = -1 in GF(9); the fibre of x0 is {y0, y0 + i, y0 - i}). So
   f in L(aQ + bP_inf)  <=>  g = f p(x)^a in L((9a + b) P_inf) and v_Q'(g) >= a, v_Q''(g) >= a.
Basis of L(M P_inf): x^i y^j, j <= 2, 3i + 4j <= M (distinct pole orders). x - x0 is a local parameter at every
affine point (dF/dy = 3y^2 + 1 = 1); y = y0' + s(t) with s + s^3 = (x0 + t)^4 - x0^4 solved as a power series.
Vanishing conditions are GF(729)-linear in the GF(9) coefficients of g; each is split into 6 GF(3) equations.
Coordinates: f(P) = g(P) / p(x_P)^a at the 27 affine points (p has no GF(9) roots), and at P_inf the coefficient of
g's basis monomial of pole order 9a + b (the generalized evaluation (t^b f)(P_inf); p(x)^a has leading term of pole
order 9a with coefficient 1). Goppa bound d >= 28 - (3a + b); dim = 3a + b - 2 when 3a + b >= 5.
Usage: deg3.py list                         -> all degree-3 places (representatives) with an index
       deg3.py code IDX a b out.code         -> write "K n" + rows (GF(9) as a + 3b, w^2 = w + 1)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---------- GF(3)-vector arithmetic for GF(729) = GF(3)[z]/(f), elements 0..728 as base-3 digit vectors ----------
def digits(u):
    d = []
    for _ in range(6):
        d.append(u % 3); u //= 3
    return d
def undigits(d):
    u = 0
    for k in reversed(range(6)):
        u = 3 * u + d[k] % 3
    return u
POW3 = [3 ** k for k in range(6)]
def add729(u, v):
    r = 0
    for k in range(6):
        r += ((u // POW3[k] + v // POW3[k]) % 3) * POW3[k]
    return r
def neg729(u):
    return undigits([(-x) % 3 for x in digits(u)])
def polymulmod(a, b, f):
    # a, b digit lists (deg < 6), f monic degree-6 digit list of length 7
    r = [0] * 11
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] = (r[i + j] + x * y) % 3
    for k in range(10, 5, -1):
        c = r[k]
        if c:
            for t in range(7):
                r[k - 6 + t] = (r[k - 6 + t] - c * f[t]) % 3
    return r[:6]
def find_primitive():
    import itertools
    for tail in itertools.product(range(3), repeat=6):
        f = list(tail) + [1]
        if f[0] == 0:
            continue
        # order of z must be 728
        e = [0, 1, 0, 0, 0, 0]; x = [1, 0, 0, 0, 0, 0]; seen = 0
        for k in range(1, 729):
            x = polymulmod(x, e, f)
            if x == [1, 0, 0, 0, 0, 0]:
                seen = k; break
        if seen == 728:
            return f
F6 = find_primitive()
EXP = [0] * 1456; LOG = [None] * 729
x = [1, 0, 0, 0, 0, 0]
for k in range(728):
    u = undigits(x); EXP[k] = u; EXP[k + 728] = u; LOG[u] = k
    x = polymulmod(x, [0, 1, 0, 0, 0, 0], F6)
def mul729(u, v):
    if u == 0 or v == 0:
        return 0
    return EXP[LOG[u] + LOG[v]]
def pow729(u, e):
    if u == 0:
        return 0 if e else 1
    return EXP[(LOG[u] * e) % 728]
ADDT = [[add729(u, v) for v in range(729)] for u in range(729)]
NEGT = [neg729(u) for u in range(729)]

# ---------- GF(9) inside GF(729): W with W^2 = W + 1 ----------
SUB9 = [u for u in range(729) if pow729(u, 9) == u]
W = next(u for u in SUB9 if mul729(u, u) == ADDT[u][1] and u not in (0, 1))
def emb(e9):                     # GF(9) code a + 3b -> a + b W in GF(729)
    a, b = e9 % 3, e9 // 3
    r = 0
    for _ in range(a):
        r = ADDT[r][1]
    for _ in range(b):
        r = ADDT[r][W]
    return r
EMB = [emb(e) for e in range(9)]
BACK = {EMB[e]: e for e in range(9)}
I9 = next(e for e in range(9) if mul729(EMB[e], EMB[e]) == NEGT[1])

from gf9lib import ADD, MUL, NEG, INV, CONJ, rref9

# ---------- points and places ----------
T = {}
for y in range(729):
    T.setdefault(ADDT[pow729(y, 3)][y], []).append(y)
def frob(u):
    return pow729(u, 9)
def places():
    seen = set(); reps = []
    for x0 in range(729):
        if x0 in BACK:
            continue
        for y0 in T.get(pow729(x0, 4), []):
            if (x0, y0) in seen:
                continue
            orb = [(x0, y0), (frob(x0), frob(y0)), (frob(frob(x0)), frob(frob(y0)))]
            assert frob(orb[2][0]) == x0 and frob(orb[2][1]) == y0
            for p in orb:
                seen.add(p)
            reps.append((x0, y0))
    return reps
PLACES = places()

def pw9(x, e):
    r = 1
    for _ in range(e):
        r = MUL[r][x]
    return r
PTS = [(x, y) for x in range(9) for y in range(9) if ADD[pw9(y, 3)][y] == pw9(x, 4)]
assert len(PTS) == 27

def series_mul(p, q, cut):
    r = [0] * cut
    for i in range(cut):
        if p[i]:
            for j in range(cut - i):
                if q[j]:
                    r[i + j] = ADDT[r[i + j]][mul729(p[i], q[j])]
    return r
def series_pow(p, e, cut):
    r = [1] + [0] * (cut - 1)
    for _ in range(e):
        r = series_mul(r, p, cut)
    return r
def local_xy(x0, y0, cut):
    """x = x0 + t, y = y0 + s(t) with s + s^3 = (x0 + t)^4 - x0^4, mod t^cut."""
    X = [x0, 1] + [0] * (cut - 2) if cut >= 2 else [x0]
    X = X[:cut]
    rhs = series_pow(X, 4, cut); rhs[0] = ADDT[rhs[0]][NEGT[pow729(x0, 4)]]
    s = [0] * cut
    for _ in range(cut + 1):
        s3 = [0] * cut
        for k in range(cut):
            if s[k] and 3 * k < cut:
                s3[3 * k] = pow729(s[k], 3)
        s = [ADDT[rhs[k]][NEGT[s3[k]]] for k in range(cut)]
    Y = s[:]; Y[0] = ADDT[Y[0]][y0]
    # check
    chk = ADDT_series(series_pow(Y, 3, cut), Y)
    assert chk == series_pow(X, 4, cut), "local expansion failed"
    return X, Y
def ADDT_series(p, q):
    return [ADDT[a][b] for a, b in zip(p, q)]

def nullspace3(rows, ncol):
    A = [r[:] for r in rows]; piv = []; r = 0
    for c in range(ncol):
        p = next((i for i in range(r, len(A)) if A[i][c] % 3), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        if A[r][c] % 3 == 2:
            A[r] = [(2 * v) % 3 for v in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] % 3:
                f = A[i][c]
                A[i] = [(u - f * v) % 3 for u, v in zip(A[i], A[r])]
        piv.append(c); r += 1
    basis = []
    for fcol in [c for c in range(ncol) if c not in piv]:
        v = [0] * ncol; v[fcol] = 1
        for i, pc in enumerate(piv):
            v[pc] = (-A[i][fcol]) % 3
        basis.append(v)
    return basis

def code(idx, a, b):
    x0, y0 = PLACES[idx]
    M = 9 * a + b
    mons = sorted([(i, j) for j in range(3) for i in range(M // 3 + 1) if 3 * i + 4 * j <= M], key=lambda t: 3 * t[0] + 4 * t[1])
    top = [m for m in mons if 3 * m[0] + 4 * m[1] == M]
    assert len(top) == 1, "pole order M not a pole number"
    nm = len(mons)
    conds = []                                   # GF(729) vectors over the monomials
    for u in (EMB[I9], NEGT[EMB[I9]]):
        yq = ADDT[y0][u]
        assert pow729(x0, 4) == ADDT[pow729(yq, 3)][yq]
        X, Y = local_xy(x0, yq, max(a, 1))
        ex = [series_mul(series_pow(X, i, a), series_pow(Y, j, a), a) for i, j in mons]
        for k in range(a):
            conds.append([e[k] for e in ex])
    rows3 = []                                   # unknowns: alpha_m (GF(3)), beta_m (GF(3)); c_m = alpha + beta w
    for cv in conds:
        dA = [digits(e) for e in cv]
        dB = [digits(mul729(W, e)) for e in cv]
        for dd in range(6):
            rows3.append([dA[m][dd] for m in range(nm)] + [dB[m][dd] for m in range(nm)])
    sol3 = nullspace3(rows3, 2 * nm) if rows3 else [[1 if k == l else 0 for k in range(2 * nm)] for l in range(2 * nm)]
    vecs9 = [[v[m] + 3 * v[nm + m] for m in range(nm)] for v in sol3]
    B, _ = rref9(vecs9)
    assert 2 * len(B) == len(sol3), "solution space not GF(9)-linear"
    # p(x) over GF(9)
    p = [1]
    for t in range(3):
        r = pow729(x0, 9 ** t)
        q = [0] * (len(p) + 1)
        for k, cf in enumerate(p):
            q[k + 1] = ADDT[q[k + 1]][cf]
            q[k] = ADDT[q[k]][NEGT[mul729(cf, r)]]
        p = q
    assert all(cf in BACK for cf in p), "p(x) not over GF(9)"
    p9 = [BACK[cf] for cf in p]
    def peval(xv):
        s = 0
        for k, cf in enumerate(p9):
            s = ADD[s][MUL[cf][pw9(xv, k)]]
        return s
    rows = []
    ti = mons.index(top[0])
    for v in B:
        r = []
        for xv, yv in PTS:
            s = 0
            for cf, (i, j) in zip(v, mons):
                if cf:
                    s = ADD[s][MUL[cf][MUL[pw9(xv, i)][pw9(yv, j)]]]
            pv = peval(xv); assert pv
            s = MUL[s][INV[pw9(pv, a)]]
            r.append(s)
        r.append(v[ti])
        rows.append(r)
    R, _ = rref9(rows)
    assert len(R) == len(rows), "evaluation not injective"
    return R, p9

def hull(G):
    K = len(G); H = []
    for gi in G:
        H.append([0] * K)
    for i, gi in enumerate(G):
        for j, gj in enumerate(G):
            s = 0
            for u, v in zip(gi, gj):
                s = ADD[s][MUL[u][CONJ[v]]]
            H[i][j] = s
    return K - len(rref9(H)[0])

if __name__ == "__main__":
    if sys.argv[1] == "orbits":
        pass
    elif sys.argv[1] == "list":
        print("GF(729) modulus digits (z^0..z^6):", F6, " W =", W, " i =", I9)
        print("degree-3 places:", len(PLACES))
        for k, (x0, y0) in enumerate(PLACES):
            print(k, x0, y0)
    else:
        idx, a, b, out = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
        G, p9 = code(idx, a, b)
        K, n = len(G), len(G[0])
        with open(out, "w") as fh:
            fh.write("%d %d\n" % (K, n))
            for r in G:
                fh.write(" ".join(map(str, r)) + "\n")
        print("place %d a=%d b=%d deg=%d: [%d,%d] (expected K=%d), p(x)=%s, natural hull=%d, Goppa d>=%d" % (
            idx, a, b, 3 * a + b, n, K, 3 * a + b - 2, p9, hull(G), 28 - 3 * a - b))

def orbits():
    """Orbits of the degree-3 places under the 216 automorphisms fixing P_inf: x -> A x + B, y -> A^4 y + A B^3 x + C
    (A in GF(9)*, C^3 + C = B^4), and under the Frobenius x -> x^3, y -> y^3 (codes from conjugate places are
    conjugate, with the same d and hull dimension)."""
    pl = {}
    for k, (x0, y0) in enumerate(PLACES):
        for t in range(3):
            pl[(pow729(x0, 9 ** t), pow729(y0, 9 ** t))] = k
    grp = [(EMB[A], EMB[B], EMB[C]) for A in range(1, 9) for B in range(9) for C in range(9)
           if ADD[pw9(C, 3)][C] == pw9(B, 4)]
    assert len(grp) == 216
    parent = list(range(len(PLACES)))
    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]; u = parent[u]
        return u
    for k, (x0, y0) in enumerate(PLACES):
        imgs = [(pow729(x0, 3), pow729(y0, 3))]
        for A, B, C in grp:
            x1 = ADDT[mul729(A, x0)][B]
            y1 = ADDT[ADDT[mul729(pow729(A, 4), y0)][mul729(mul729(A, pow729(B, 3)), x0)]][C]
            imgs.append((x1, y1))
        for im in imgs:
            parent[find(k)] = find(pl[im])
    cls = {}
    for k in range(len(PLACES)):
        cls.setdefault(find(k), []).append(k)
    return sorted(cls.values(), key=lambda c: c[0])

if __name__ == "__main__" and sys.argv[1] == "orbits":
    for c in orbits():
        print("rep %d size %d" % (c[0], len(c)))
