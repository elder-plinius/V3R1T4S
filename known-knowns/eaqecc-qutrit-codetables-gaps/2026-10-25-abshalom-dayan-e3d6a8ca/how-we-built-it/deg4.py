#!/usr/bin/env python3
"""AG codes on the Hermitian curve y^3 + y = x^4 over GF(9), evaluated at all 28 rational points (27 affine + P_inf),
with divisor G = a Q + b P_inf, Q a place of degree 4 (a generalization of an earlier
deg3.py, not shipped here, from GF(729) to GF(6561) = GF(9^4)).

Method. Q has a representative point (x0, y0) over GF(6561) with x0 of degree 4 over GF(9) (a degree-4 place cannot
have x0 in GF(81): the curve has no degree-2 places, and a fibre over GF(81) \\ GF(9) would hold 6 points of degree 4).
p(x) = prod (x - x0^(9^t)), t = 0..3, is in GF(9)[x]; div p(x) = Q + Q' + Q'' - 12 P_inf, where Q', Q'' are the places of
(x0, y0 + i), (x0, y0 - i) (i^2 = -1 in GF(9)). So
   f in L(aQ + bP_inf)  <=>  g = f p(x)^a in L((12a + b) P_inf) and v_Q'(g) >= a, v_Q''(g) >= a.
Basis of L(M P_inf): x^i y^j, j <= 2, 3i + 4j <= M. x - x0 is a local parameter at every affine point; y = y0' + s(t)
with s + s^3 = (x0 + t)^4 - x0^4 as a power series. Vanishing conditions are GF(6561)-linear in the GF(9) coefficients
of g; each is split into 8 GF(3) equations. Coordinates: f(P) = g(P) / p(x_P)^a at the 27 affine points, and at P_inf
the coefficient of g's monomial of pole order 12a + b (the generalized evaluation up to one fixed constant).
Goppa bound d >= 28 - (4a + b); dim = 4a + b - 2 when 5 <= 4a + b < 28.
Usage: deg4.py list | orbits | code IDX a b out.code | pair IDX a b out.xin   (pair: C1 = L(aQ+bP), C2 = L((a-1)Q+bP))"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf9lib import ADD, MUL, NEG, INV, CONJ, rref9

ND = 8; Q = 3 ** ND; QM = Q - 1
def digits(u):
    d = []
    for _ in range(ND):
        d.append(u % 3); u //= 3
    return d
def undigits(d):
    u = 0
    for k in reversed(range(ND)):
        u = 3 * u + d[k] % 3
    return u
A81 = [[undigits([(a + b) % 3 for a, b in zip(digits(x)[:4], digits(y)[:4])] + [0] * 4) for y in range(81)] for x in range(81)]
def add(u, v):
    return A81[u % 81][v % 81] + 81 * A81[u // 81][v // 81]
N81 = [undigits([(-a) % 3 for a in digits(x)[:4]] + [0] * 4) for x in range(81)]
def neg(u):
    return N81[u % 81] + 81 * N81[u // 81]
def polymulmod(a, b, f):
    r = [0] * (2 * ND - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] = (r[i + j] + x * y) % 3
    for k in range(2 * ND - 2, ND - 1, -1):
        c = r[k]
        if c:
            for t in range(ND + 1):
                r[k - ND + t] = (r[k - ND + t] - c * f[t]) % 3
    return r[:ND]
def find_primitive():
    one = [1] + [0] * (ND - 1); z = [0, 1] + [0] * (ND - 2)
    for tail in itertools.product(range(3), repeat=ND):
        f = list(tail) + [1]
        if f[0] == 0:
            continue
        x = one[:]; order = 0
        for k in range(1, Q):
            x = polymulmod(x, z, f)
            if x == one:
                order = k; break
        if order == QM:
            return f
F8 = find_primitive()
EXP = [0] * (2 * QM); LOG = [None] * Q
x = [1] + [0] * (ND - 1)
for k in range(QM):
    u = undigits(x); EXP[k] = u; EXP[k + QM] = u; LOG[u] = k
    x = polymulmod(x, [0, 1] + [0] * (ND - 2), F8)
def mul(u, v):
    if u == 0 or v == 0:
        return 0
    return EXP[LOG[u] + LOG[v]]
def pw(u, e):
    if u == 0:
        return 0 if e else 1
    return EXP[(LOG[u] * e) % QM]

SUB9 = [u for u in range(Q) if pw(u, 9) == u]
assert len(SUB9) == 9
W = next(u for u in SUB9 if u not in (0, 1) and mul(u, u) == add(u, 1))
def emb(e9):
    a, b = e9 % 3, e9 // 3
    r = 0
    for _ in range(a):
        r = add(r, 1)
    for _ in range(b):
        r = add(r, W)
    return r
EMB = [emb(e) for e in range(9)]
BACK = {EMB[e]: e for e in range(9)}
assert all(BACK[mul(EMB[a], EMB[b])] == MUL[a][b] and BACK[add(EMB[a], EMB[b])] == ADD[a][b] for a in range(9) for b in range(9))
I9 = next(e for e in range(9) if mul(EMB[e], EMB[e]) == neg(1))

T = {}
for y in range(Q):
    T.setdefault(add(pw(y, 3), y), []).append(y)
def frob(u):
    return pw(u, 9)
def places():
    seen = set(); reps = []
    for x0 in range(Q):
        if pw(x0, 81) == x0:            # x0 in GF(81): no degree-4 place lies over it
            continue
        for y0 in T.get(pw(x0, 4), []):
            if (x0, y0) in seen:
                continue
            orb = [(x0, y0)]
            for _ in range(3):
                orb.append((frob(orb[-1][0]), frob(orb[-1][1])))
            assert frob(orb[3][0]) == x0 and frob(orb[3][1]) == y0
            for pt in orb:
                seen.add(pt)
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
                    r[i + j] = add(r[i + j], mul(p[i], q[j]))
    return r
def series_pow(p, e, cut):
    r = [1] + [0] * (cut - 1)
    for _ in range(e):
        r = series_mul(r, p, cut)
    return r
def local_xy(x0, y0, cut):
    X = ([x0, 1] + [0] * cut)[:cut]
    rhs = series_pow(X, 4, cut); rhs[0] = add(rhs[0], neg(pw(x0, 4)))
    s = [0] * cut
    for _ in range(cut + 1):
        s3 = [0] * cut
        for k in range(cut):
            if s[k] and 3 * k < cut:
                s3[3 * k] = pw(s[k], 3)
        s = [add(rhs[k], neg(s3[k])) for k in range(cut)]
    Y = s[:]; Y[0] = add(Y[0], y0)
    chk = [add(a, b) for a, b in zip(series_pow(Y, 3, cut), Y)]
    assert chk == series_pow(X, 4, cut), "local expansion failed"
    return X, Y

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
    M = 12 * a + b
    mons = sorted([(i, j) for j in range(3) for i in range(M // 3 + 1) if 3 * i + 4 * j <= M], key=lambda t: 3 * t[0] + 4 * t[1])
    top = [m for m in mons if 3 * m[0] + 4 * m[1] == M]
    assert len(top) == 1, "pole order M not a pole number"
    nm = len(mons)
    conds = []
    if a > 0:
        for u in (EMB[I9], neg(EMB[I9])):
            yq = add(y0, u)
            assert pw(x0, 4) == add(pw(yq, 3), yq)
            X, Y = local_xy(x0, yq, a)
            ex = [series_mul(series_pow(X, i, a), series_pow(Y, j, a), a) for i, j in mons]
            for k in range(a):
                conds.append([e[k] for e in ex])
    rows3 = []
    for cv in conds:
        dA = [digits(e) for e in cv]
        dB = [digits(mul(W, e)) for e in cv]
        for dd in range(ND):
            rows3.append([dA[m][dd] for m in range(nm)] + [dB[m][dd] for m in range(nm)])
    sol3 = nullspace3(rows3, 2 * nm) if rows3 else [[1 if k == l else 0 for k in range(2 * nm)] for l in range(2 * nm)]
    vecs9 = [[v[m] + 3 * v[nm + m] for m in range(nm)] for v in sol3]
    B, _ = rref9(vecs9)
    assert 2 * len(B) == len(sol3), "solution space not GF(9)-linear"
    p = [1]
    for t in range(4):
        r = pw(x0, 9 ** t)
        q = [0] * (len(p) + 1)
        for k, cf in enumerate(p):
            q[k + 1] = add(q[k + 1], cf)
            q[k] = add(q[k], neg(mul(cf, r)))
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
    K = len(G)
    H = [[0] * K for _ in G]
    for i, gi in enumerate(G):
        for j, gj in enumerate(G):
            s = 0
            for u, v in zip(gi, gj):
                s = ADD[s][MUL[u][CONJ[v]]]
            H[i][j] = s
    return K - len(rref9(H)[0])

def orbits():
    """Orbits of the degree-4 places under the 216 automorphisms fixing P_inf (x -> A x + B, y -> A^4 y + A B^3 x + C,
    A in GF(9)*, C^3 + C = B^4) and the Frobenius x -> x^3, y -> y^3."""
    pl = {}
    for k, (x0, y0) in enumerate(PLACES):
        for t in range(4):
            pl[(pw(x0, 9 ** t), pw(y0, 9 ** t))] = k
    grp = [(EMB[A], EMB[B], EMB[C]) for A in range(1, 9) for B in range(9) for C in range(9) if ADD[pw9(C, 3)][C] == pw9(B, 4)]
    assert len(grp) == 216
    parent = list(range(len(PLACES)))
    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]; u = parent[u]
        return u
    for k, (x0, y0) in enumerate(PLACES):
        imgs = [(pw(x0, 3), pw(y0, 3))]
        for A, B, C in grp:
            x1 = add(mul(A, x0), B)
            y1 = add(add(mul(pw(A, 4), y0), mul(mul(A, pw(B, 3)), x0)), C)
            imgs.append((x1, y1))
        for im in imgs:
            parent[find(k)] = find(pl[im])
    cls = {}
    for k in range(len(PLACES)):
        cls.setdefault(find(k), []).append(k)
    return sorted(cls.values(), key=lambda c: c[0])

def contains(G1, G2):
    R1, _ = rref9(G1)
    return len(rref9(R1 + G2)[0]) == len(R1)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "list":
        print("GF(6561) modulus digits (z^0..z^8):", F8, " W =", W, " i =", I9)
        print("degree-4 places:", len(PLACES))
    elif cmd == "orbits":
        print("degree-4 places:", len(PLACES))
        for c in orbits():
            print("rep %d size %d" % (c[0], len(c)))
    elif cmd == "code":
        idx, a, b, out = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
        G, p9 = code(idx, a, b)
        with open(out, "w") as fh:
            fh.write("%d %d\n" % (len(G), len(G[0])))
            for r in G:
                fh.write(" ".join(map(str, r)) + "\n")
        print("place %d a=%d b=%d deg=%d: [%d,%d] (expected K=%d), p(x)=%s, natural hull=%d, Goppa d>=%d" % (
            idx, a, b, 4 * a + b, len(G[0]), len(G), 4 * a + b - 2, p9, hull(G), 28 - 4 * a - b))
    elif cmd == "pair":
        idx, a, b, out = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
        G1, _ = code(idx, a, b); G2, _ = code(idx, a - 1, b)
        assert contains(G1, G2), "C2 not inside C1"
        rows = [r[:] for r in G2]
        for r in G1:
            if len(rref9(rows + [r])[0]) > len(rows):
                rows.append(r)
        assert len(rows) == len(G1)
        with open(out, "w") as fh:
            fh.write("%d %d %d\n" % (len(G1), len(G2), len(G1[0])))
            for r in rows:
                fh.write(" ".join(map(str, r)) + "\n")
        for nm_, G in (("C1", G1), ("C2", G2)):
            with open(out.replace(".xin", "_%s.code" % nm_), "w") as fh:
                fh.write("%d %d\n" % (len(G), len(G[0])))
                for r in G:
                    fh.write(" ".join(map(str, r)) + "\n")
        print("pair place %d: C1 = L(%dQ + %dP) [28,%d], C2 = L(%dQ + %dP) [28,%d], natural hulls %d, %d" % (
            idx, a, b, len(G1), a - 1, b, len(G2), hull(G1), hull(G2)))
