#!/usr/bin/env python3
"""Machine-check every hypothesis of a theorem-based proof that the EAQECC in an
object JSON (a Construction X code over GF(9) from Hermitian-curve AG codes) has d_EA >= d_X, with no minimum-distance
computation. Written fresh: own GF(9), GF(729) = GF(9)[u]/(cubic), GF(3)/GF(9) linear algebra and Riemann-Roch
spaces (shares no code with the claim's checkers, its builder or deg3.py). Proof steps L1-L8: see ../NOTES.md (not shipped; HOW_WE_FOUND_IT.md gives the proof in four steps).
Usage: goppa_x.py object.json a b witness_word
   a, b: C1 = C_L(D_28, aQ + bP_inf), C2 = C_L(D_28, (a-1)Q + bP_inf), tried for every degree-3 place Q;
   witness_word: 33 comma-separated GF(9) codes (a + 3b) of a word of C claimed to have weight d_X."""
import sys, json, itertools

# ---------- GF(9) = GF(3)[w]/(w^2 - w - 1), element a + b w coded a + 3b ----------
def m9(x, y):
    a1, b1, a2, b2 = x % 3, x // 3, y % 3, y // 3
    return (a1 * a2 + b1 * b2) % 3 + 3 * ((a1 * b2 + a2 * b1 + b1 * b2) % 3)
def a9(x, y): return (x % 3 + y % 3) % 3 + 3 * ((x // 3 + y // 3) % 3)
def n9(x): return (-(x % 3)) % 3 + 3 * ((-(x // 3)) % 3)
MUL9 = [[m9(x, y) for y in range(9)] for x in range(9)]
ADD9 = [[a9(x, y) for y in range(9)] for x in range(9)]
NEG9 = [n9(x) for x in range(9)]
INV9 = [None] + [next(y for y in range(1, 9) if MUL9[x][y] == 1) for x in range(1, 9)]
W = 3
assert MUL9[W][W] == ADD9[W][1]                      # w^2 = w + 1

def rank9(rows, ncols):
    A = [list(r) for r in rows]; r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(A)) if A[i][c]), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]; iv = INV9[A[r][c]]; A[r] = [MUL9[iv][x] for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                f = A[i][c]; A[i] = [ADD9[x][NEG9[MUL9[f][y]]] for x, y in zip(A[i], A[r])]
        r += 1
    return r
def null9(rows, ncols):
    """basis of {v in GF(9)^ncols : rows . v = 0}"""
    A = [list(r) for r in rows]; piv = []; r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(A)) if A[i][c]), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]; iv = INV9[A[r][c]]; A[r] = [MUL9[iv][x] for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                f = A[i][c]; A[i] = [ADD9[x][NEG9[MUL9[f][y]]] for x, y in zip(A[i], A[r])]
        piv.append(c); r += 1
    free = [c for c in range(ncols) if c not in piv]; B = []
    for fc in free:
        v = [0] * ncols; v[fc] = 1
        for i, pc in enumerate(piv): v[pc] = NEG9[A[i][fc]]
        B.append(v)
    return B
def det9(M):
    return 0 if rank9(M, len(M)) < len(M) else 1      # only nonzero-ness is needed

# ---------- GF(3) linear algebra ----------
def rank3(rows, ncols):
    A = [list(r) for r in rows]; r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(A)) if A[i][c] % 3), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        if A[r][c] % 3 == 2: A[r] = [(2 * x) % 3 for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] % 3:
                f = A[i][c]; A[i] = [(x - f * y) % 3 for x, y in zip(A[i], A[r])]
        r += 1
    return r

# ---------- GF(729) = GF(9)[u]/(u^3 + m2 u^2 + m1 u + m0), elements (c0, c1, c2) coded c0 + 9 c1 + 81 c2 ----------
def find_cubic():
    for m0, m1, m2 in itertools.product(range(9), repeat=3):
        if m0 == 0: continue
        if all(ADD9[ADD9[MUL9[MUL9[x][x]][x]][MUL9[m2][MUL9[x][x]]]][ADD9[MUL9[m1][x]][m0]] for x in range(9)):
            return (m0, m1, m2)
MC = find_cubic()
def enc(c): return c[0] + 9 * c[1] + 81 * c[2]
def dec(u): return (u % 9, (u // 9) % 9, u // 81)
def pmul(u, v):
    a, b = dec(u), dec(v); r = [0] * 5
    for i in range(3):
        for j in range(3): r[i + j] = ADD9[r[i + j]][MUL9[a[i]][b[j]]]
    for k in (4, 3):                                  # u^3 = -(m2 u^2 + m1 u + m0)
        c = r[k]; r[k] = 0
        if c:
            for t, mt in enumerate(MC): r[k - 3 + t] = ADD9[r[k - 3 + t]][NEG9[MUL9[c][mt]]]
    return enc(r[:3])
def padd(u, v): a, b = dec(u), dec(v); return enc([ADD9[x][y] for x, y in zip(a, b)])
def pneg(u): return enc([NEG9[x] for x in dec(u)])
MUL = [[0] * 729 for _ in range(729)]
for u in range(729):
    for v in range(u, 729): MUL[u][v] = MUL[v][u] = pmul(u, v)
ADD = [[padd(u, v) for v in range(729)] for u in range(729)]
NEG = [pneg(u) for u in range(729)]
def pw(u, e):
    r = 1
    for _ in range(e): r = MUL[r][u]
    return r
F9 = list(range(9))                                    # GF(9) inside GF(729): (c, 0, 0) = c
def frob(u): return pw(u, 9)
assert all(frob(c) == c for c in F9) and sum(1 for u in range(729) if frob(u) == u) == 9

# ---------- the curve ----------
I9 = next(c for c in F9 if MUL9[c][c] == NEG9[1])       # i^2 = -1
CUBE = {}
for y in range(729): CUBE.setdefault(ADD[pw(y, 3)][y], []).append(y)
aff = sorted((x, y) for x in F9 for y in F9 if ADD9[MUL9[MUL9[y][y]][y]][y] == MUL9[MUL9[x][x]][MUL9[x][x]])
assert len(aff) == 27
pts3 = [(x, y) for x in range(729) if frob(x) != x for y in CUBE.get(pw(x, 4), [])]
places, seen = [], set()
for P in sorted(pts3):
    if P in seen: continue
    orb = [P, (frob(P[0]), frob(P[1])), (frob(frob(P[0])), frob(frob(P[1])))]
    assert len(set(orb)) == 3
    seen.update(orb); places.append(P)

def series_at(x0, y1, A):
    """power series (mod t^A) of x and y at the point (x0, y1): x = x0 + t, y = y1 + s, s + s^3 = (x0 + t)^4 - x0^4."""
    def mul(p, q):
        r = [0] * A
        for i, a in enumerate(p):
            if a:
                for j in range(A - i): r[i + j] = ADD[r[i + j]][MUL[a][q[j]]]
        return r
    X = [x0, 1] + [0] * (A - 2) if A >= 2 else [x0]
    R = mul(mul(X, X), mul(X, X)); R[0] = ADD[R[0]][NEG[pw(x0, 4)]]
    s = [0] * A
    for _ in range(A + 1): s = [ADD[r][NEG[c]] for r, c in zip(R, mul(mul(s, s), s))]
    chk = [ADD[a][b] for a, b in zip(s, mul(mul(s, s), s))]
    assert chk == R, "series"
    Y = s[:]; Y[0] = ADD[Y[0]][y1]
    return X, Y, mul

def riemann_roch(P, a, b):
    """evaluation basis of C_L(D_28, aQ + bP_inf), Q the place of the point P = (x0, y0): rows over GF(9), 28 columns
    (27 affine points in 'aff' order, then P_inf as the coefficient of the monomial of pole order 9a + b of g = f p^a)."""
    x0, y0 = P; M = 9 * a + b
    mons = [(i, j) for j in range(3) for i in range(M // 3 + 1) if 3 * i + 4 * j <= M]
    eqs = []
    if a > 0:
        for y1 in (ADD[y0][I9], ADD[y0][NEG[I9]]):           # the points over x0 not on Q
            X, Y, mul = series_at(x0, y1, a)
            cols = []
            for (i, j) in mons:
                v = [1] + [0] * (a - 1)
                for _ in range(i): v = mul(v, X)
                for _ in range(j): v = mul(v, Y)
                cols.append(v)
            for k in range(a):
                for comp in range(3): eqs.append([dec(cols[m][k])[comp] for m in range(len(mons))])
    G = null9(eqs, len(mons)) if eqs else [[int(m == r) for m in range(len(mons))] for r in range(len(mons))]
    # p(x) = (x - x0)(x - x0^9)(x - x0^81), coefficients in GF(9)
    p = [1]
    for r in (x0, frob(x0), frob(frob(x0))):
        q = [0] * (len(p) + 1)
        for k, c in enumerate(p): q[k + 1] = ADD[q[k + 1]][c]; q[k] = ADD[q[k]][NEG[MUL[r][c]]]
        p = q
    assert all(c < 9 for c in p)
    top = mons.index(next(m for m in mons if 3 * m[0] + 4 * m[1] == M))
    rows = []
    for g in G:
        row = []
        for (xp, yp) in aff:
            val = 0
            for c, (i, j) in zip(g, mons):
                if c:
                    t = c
                    for _ in range(i): t = MUL9[t][xp]
                    for _ in range(j): t = MUL9[t][yp]
                    val = ADD9[val][t]
            px = 0
            for k in reversed(range(len(p))): px = ADD9[MUL9[px][xp]][p[k]]
            assert px != 0
            row.append(MUL9[val][INV9[pw(px, a) if a else 1]] if a else val)
        row.append(g[top]); rows.append(row)
    return rows, len(mons)

def main():
    obj = json.load(open(sys.argv[1])); a, b = int(sys.argv[2]), int(sys.argv[3])
    wit = [int(x) for x in sys.argv[4].split(",")]
    G9, S = obj["G9"], [[x % 3 for x in r] for r in obj["S"]]
    K, n = len(G9), len(G9[0]); h = n - 5
    eps = obj["construction"].split("columns marked '-' in ")[1].split()[0]
    assert len(eps) == n
    print("GF(729) modulus u^3 + %d u^2 + %d u + %d over GF(9); i = %d; 27 affine points; %d degree-3 places"
          % (MC[2], MC[1], MC[0], I9, len(places)))
    # L1
    def phi(v): return [x % 3 for x in v] + [x // 3 for x in v]
    def sp(u, v): return sum(u[t] * v[n + t] - u[n + t] * v[t] for t in range(n)) % 3
    vecs = [phi(r) for r in G9] + [phi([MUL9[W][x] for x in r]) for r in G9]
    orth = all(sp(u, s) == 0 for u in vecs for s in S)
    rS, rV = rank3(S, 2 * n), rank3(vecs, 2 * n)
    print("L1: rank S = %d, dim phi(C) = %d, 2n - rank S = %d, phi(C) orthogonal to S: %s -> span(S)^perp = phi(C): %s"
          % (rS, rV, 2 * n - rS, orth, orth and rV == 2 * n - rS))
    # L2
    winv = INV9[W]
    U = [[MUL9[winv][x] if eps[t] == '-' else x for t, x in enumerate(r)] for r in G9]
    print("L2: %d columns unscaled by w^-1 (pattern %s)" % (eps.count('-'), eps))
    # L3
    H = [r[:h] for r in U]; T = [r[h:] for r in U]
    rH, rT = rank9(H, h), rank9(T, 5)
    lam = null9([[T[i][c] for i in range(K)] for c in range(5)], K)   # lam . T = 0
    Z = [[0] * h for _ in lam]
    for z, l in zip(Z, lam):
        for i, c in enumerate(l):
            if c:
                for t in range(h): z[t] = ADD9[z[t]][MUL9[c][H[i][t]]]
    rZ = rank9(Z, h)
    print("L3: K = %d, rank(head) = %d (injective: %s), dim zero-tail subcode = %d, rank(tail) = %d"
          % (K, rH, rH == K, rZ, rT))
    # L4
    hits = []
    for idx, P in enumerate(places):
        B1, m1 = riemann_roch(P, a, b)
        if rank9(B1, h) != rH or rank9(B1 + H, h) != rH: continue
        B2, m2 = riemann_roch(P, a - 1, b)
        ok2 = rank9(B2, h) == rZ and rank9(B2 + Z, h) == rZ
        hits.append((idx, P, len(B1), len(B2), ok2))
    for idx, P, d1, d2, ok2 in hits:
        print("L4: place #%d (point x0 = %d, y0 = %d in this GF(729) coding): head code = C_L(D_28, %dQ + %dP_inf) "
              "(dim %d), zero-tail code = C_L(D_28, %dQ + %dP_inf) (dim %d): %s" % (idx, P[0], P[1], a, b, d1, a - 1, b, d2, ok2))
    good = [x for x in hits if x[4]]
    print("L4: %d of %d places identify both codes" % (len(good), len(places)))
    # L5 / L6 / L7
    g1, g2 = 28 - (3 * a + b), 28 - (3 * (a - 1) + b)
    basisT = [T[i] for i in range(K)]
    # a 3 x 5 basis of the tail code
    tb = []
    for r in basisT:
        if rank9(tb + [r], 5) > len(tb): tb.append(r)
    mds = all(det9([[tb[i][c] for c in cols] for i in range(3)]) for cols in itertools.combinations(range(5), 3))
    dA = 5 - len(tb) + 1 if mds else None
    print("L5: Goppa bounds d(head code) >= 28 - %d = %d, d(zero-tail code) >= 28 - %d = %d" % (3 * a + b, g1, 3 * (a - 1) + b, g2))
    print("L6: tail code dimension %d, all %d maximal minors nonzero: %s -> d(tail) = %s"
          % (len(tb), len(list(itertools.combinations(range(5), 3))), mds, dA))
    dX = min(g2, g1 + dA) if (good and mds and rH == K) else None
    print("L7: d(C) >= min(%d, %d + %s) = %s, so d_EA >= %s" % (g2, g1, dA, dX, dX))
    # L8
    wt = sum(1 for x in wit if x)
    inC = rank9(G9 + [wit], n) == rank9(G9, n)
    outS = rank3(S + [phi(wit)], 2 * n) == rS + 1
    print("L8: witness weight %d, in C: %s, phi(witness) orthogonal to S: %s, outside span(S): %s"
          % (wt, inC, all(sp(phi(wit), s) == 0 for s in S), outS))
    ok = dX is not None and inC and outS and wt == dX and orth and rV == 2 * n - rS
    print("RESULT: d_EA = %s exactly (theorem-based; no distance search): %s" % (dX, ok))

main()
