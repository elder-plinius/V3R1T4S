#!/usr/bin/env python3
"""Machine-check every hypothesis of a theorem-based proof that the EAQECC
in an object JSON (a Construction X code over GF(9) from Hermitian-curve AG codes with a divisor on a DEGREE-4 place)
has d_EA >= d_X, with no minimum-distance computation. Degree-4 generalization of an earlier goppa_x.py (degree-3
places; not shipped here). Written with its own field tower GF(6561) = GF(9)[u]/(quartic) (the builder's deg4.py uses
GF(3)[z]/(degree-8 primitive) instead) and its own GF(3)/GF(9) linear algebra and Riemann-Roch spaces; it shares no
code with the claim's checkers, its builder or deg4.py. Proof steps L1-L8: see ../NOTES.md (not shipped; HOW_WE_FOUND_IT.md gives the proof in four steps).
Usage: goppa_x4.py object.json a b witness_word
   a, b: C1 = C_L(D_28, aQ + bP_inf), C2 = C_L(D_28, (a-1)Q + bP_inf), tried for every degree-4 place Q;
   witness_word: n comma-separated GF(9) codes (a + 3b) of a word of C claimed to have weight d_X."""
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

# ---------- GF(6561) = GF(9)[u]/(u^4 + m3 u^3 + m2 u^2 + m1 u + m0), elements (c0..c3) coded c0 + 9c1 + 81c2 + 729c3 ----------
NE = 6561
def enc(c): return c[0] + 9 * c[1] + 81 * c[2] + 729 * c[3]
def dec(u): return (u % 9, (u // 9) % 9, (u // 81) % 9, u // 729)
def pmul_mod(a, b, MQ):
    r = [0] * 7
    for i in range(4):
        if a[i]:
            for j in range(4): r[i + j] = ADD9[r[i + j]][MUL9[a[i]][b[j]]]
    for k in (6, 5, 4):                               # u^4 = -(m3 u^3 + m2 u^2 + m1 u + m0)
        c = r[k]; r[k] = 0
        if c:
            for t, mt in enumerate(MQ): r[k - 4 + t] = ADD9[r[k - 4 + t]][NEG9[MUL9[c][mt]]]
    return r[:4]
def find_quartic():
    """first u^4 + m3 u^3 + m2 u^2 + m1 u + m0 over GF(9) for which u has multiplicative order 6560 (so the quotient is
    the field GF(6561) and u is primitive)."""
    for m0, m1, m2, m3 in itertools.product(range(9), repeat=4):
        if m0 == 0: continue
        MQ = (m0, m1, m2, m3); one = (1, 0, 0, 0); x = (0, 1, 0, 0); order = None
        for k in range(1, NE):
            if list(x) == list(one): order = k; break
            x = tuple(pmul_mod(x, (0, 1, 0, 0), MQ))
        if order == NE - 1:
            return MQ
MQ = find_quartic()
EXP = [0] * (2 * (NE - 1)); LOG = [None] * NE
xx = (1, 0, 0, 0)
for k in range(NE - 1):
    u = enc(xx); EXP[k] = EXP[k + NE - 1] = u; LOG[u] = k
    xx = tuple(pmul_mod(xx, (0, 1, 0, 0), MQ))
assert all(LOG[u] is not None for u in range(1, NE))
A81 = [[a9(x % 9, y % 9) + 9 * a9(x // 9, y // 9) for y in range(81)] for x in range(81)]
def ADD(u, v): return A81[u % 81][v % 81] + 81 * A81[u // 81][v // 81]
def NEG(u): return enc([NEG9[c] for c in dec(u)])
def MUL(u, v): return 0 if (u == 0 or v == 0) else EXP[LOG[u] + LOG[v]]
def pw(u, e):
    if u == 0: return 0 if e else 1
    return EXP[(LOG[u] * e) % (NE - 1)]
# GF(9) sits inside as (c, 0, 0, 0) = c; check that the embedding is a ring map
assert all(MUL(x, y) == MUL9[x][y] and ADD(x, y) == ADD9[x][y] for x in range(9) for y in range(9))
def frob(u): return pw(u, 9)
assert all(frob(c) == c for c in range(9)) and sum(1 for u in range(NE) if frob(u) == u) == 9

# ---------- the curve y^3 + y = x^4 and its degree-4 places ----------
I9 = next(c for c in range(9) if MUL9[c][c] == NEG9[1])          # i^2 = -1
ART = {}
for y in range(NE): ART.setdefault(ADD(pw(y, 3), y), []).append(y)
aff = sorted((x, y) for x in range(9) for y in range(9) if ADD9[MUL9[MUL9[y][y]][y]][y] == MUL9[MUL9[x][x]][MUL9[x][x]])
assert len(aff) == 27
def deg_over9(u):
    v, k = frob(u), 1
    while v != u: v, k = frob(v), k + 1
    return k
pts = [(x, y) for x in range(NE) for y in ART.get(pw(x, 4), [])]
assert len(pts) + 1 == 6076, len(pts)                              # #C(GF(9^4)) = 9^4 + 1 - 6 * 81, P_inf included
pts4 = [P for P in pts if deg_over9(P[0]) == 4]
assert len(pts4) == 6048 and all(deg_over9(P[1]) in (1, 2, 4) for P in pts4)
places, seen = [], set()
for P in sorted(pts4):
    if P in seen: continue
    orb = [P]
    for _ in range(3): orb.append((frob(orb[-1][0]), frob(orb[-1][1])))
    assert len(set(orb)) == 4 and (frob(orb[-1][0]), frob(orb[-1][1])) == P
    seen.update(orb); places.append(P)
assert len(places) == 1512

def series_at(x0, y1, A):
    """power series (mod t^A) of x and y at the point (x0, y1): x = x0 + t, y = y1 + s, s + s^3 = (x0 + t)^4 - x0^4."""
    def mul(p, q):
        r = [0] * A
        for i, a in enumerate(p):
            if a:
                for j in range(A - i): r[i + j] = ADD(r[i + j], MUL(a, q[j]))
        return r
    X = ([x0, 1] + [0] * (A - 2)) if A >= 2 else [x0]
    R = mul(mul(X, X), mul(X, X)); R[0] = ADD(R[0], NEG(pw(x0, 4)))
    s = [0] * A
    for _ in range(A + 1): s = [ADD(r, NEG(c)) for r, c in zip(R, mul(mul(s, s), s))]
    chk = [ADD(a, b) for a, b in zip(s, mul(mul(s, s), s))]
    assert chk == R, "series"
    Y = s[:]; Y[0] = ADD(Y[0], y1)
    return X, Y, mul

def riemann_roch(P, a, b):
    """evaluation basis of C_L(D_28, aQ + bP_inf), Q the degree-4 place of the point P = (x0, y0): rows over GF(9), 28
    columns (27 affine points in 'aff' order, then P_inf as the coefficient of the monomial of pole order 12a + b of
    g = f p^a, p the minimal polynomial of x0 over GF(9)). div p = Q + Q' + Q'' - 12 P_inf with Q', Q'' the places of
    (x0, y0 +- i), so f in L(aQ + bP_inf) <=> g in L((12a + b)P_inf) vanishing to order a at (x0, y0 +- i)."""
    x0, y0 = P; M = 12 * a + b
    mons = [(i, j) for j in range(3) for i in range(M // 3 + 1) if 3 * i + 4 * j <= M]
    eqs = []
    if a > 0:
        for y1 in (ADD(y0, I9), ADD(y0, NEG(I9))):             # the other two points over x0, not on Q
            assert (x0, y1) in set(pts) and ADD(pw(y1, 3), y1) == pw(x0, 4)
            X, Y, mul = series_at(x0, y1, a)
            cols = []
            for (i, j) in mons:
                v = [1] + [0] * (a - 1)
                for _ in range(i): v = mul(v, X)
                for _ in range(j): v = mul(v, Y)
                cols.append(v)
            for k in range(a):
                for comp in range(4): eqs.append([dec(cols[m][k])[comp] for m in range(len(mons))])
    G = null9(eqs, len(mons)) if eqs else [[int(m == r) for m in range(len(mons))] for r in range(len(mons))]
    p = [1]
    for r in (x0, frob(x0), frob(frob(x0)), frob(frob(frob(x0)))):
        q = [0] * (len(p) + 1)
        for k, c in enumerate(p): q[k + 1] = ADD(q[k + 1], c); q[k] = ADD(q[k], NEG(MUL(r, c)))
        p = q
    assert all(c < 9 for c in p) and len(p) == 5                # p(x) in GF(9)[x], monic of degree 4
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
            pa = 1
            for _ in range(a): pa = MUL9[pa][px]
            row.append(MUL9[val][INV9[pa]])
        row.append(g[top]); rows.append(row)
    return rows, len(mons)

def main():
    obj = json.load(open(sys.argv[1])); a, b = int(sys.argv[2]), int(sys.argv[3])
    wit = [int(x) for x in sys.argv[4].split(",")]
    G9, S = obj["G9"], [[x % 3 for x in r] for r in obj["S"]]
    K, n = len(G9), len(G9[0]); h = 28; m = n - h
    eps = obj["construction"].split("columns marked '-' in ")[1].split()[0]
    assert len(eps) == n and len(wit) == n
    print("GF(6561) modulus u^4 + %d u^3 + %d u^2 + %d u + %d over GF(9); i = %d; 27 affine points; %d points over GF(6561); "
          "%d degree-4 places" % (MQ[3], MQ[2], MQ[1], MQ[0], I9, len(pts) + 1, len(places)))
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
    rH, rT = rank9(H, h), rank9(T, m)
    lam = null9([[T[i][c] for i in range(K)] for c in range(m)], K)   # lam . T = 0
    Z = [[0] * h for _ in lam]
    for z, l in zip(Z, lam):
        for i, c in enumerate(l):
            if c:
                for t in range(h): z[t] = ADD9[z[t]][MUL9[c][H[i][t]]]
    rZ = rank9(Z, h)
    print("L3: K = %d, rank(head) = %d (injective: %s), dim zero-tail subcode = %d, rank(tail) = %d, K - dim zero-tail = %d"
          % (K, rH, rH == K, rZ, rT, K - rZ))
    # L4
    hits = []
    for idx, P in enumerate(places):
        B1, m1 = riemann_roch(P, a, b)
        if rank9(B1, h) != rH or rank9(B1 + H, h) != rH: continue
        B2, m2 = riemann_roch(P, a - 1, b)
        ok2 = rank9(B2, h) == rZ and rank9(B2 + Z, h) == rZ
        hits.append((idx, P, len(B1), len(B2), ok2))
    for idx, P, d1, d2, ok2 in hits:
        print("L4: place #%d (point x0 = %d, y0 = %d in this GF(6561) coding): head code = C_L(D_28, %dQ + %dP_inf) "
              "(dim %d), zero-tail code = C_L(D_28, %dQ + %dP_inf) (dim %d): %s" % (idx, P[0], P[1], a, b, d1, a - 1, b, d2, ok2))
    good = [x for x in hits if x[4]]
    print("L4: %d of %d places identify both codes" % (len(good), len(places)))
    # L5 / L6 / L7
    g1, g2 = 28 - (4 * a + b), 28 - (4 * (a - 1) + b)
    tb = []
    for r in T:
        if rank9(tb + [r], m) > len(tb): tb.append(r)
    kt = len(tb)
    mds = kt > 0 and all(det9([[tb[i][c] for c in cols] for i in range(kt)]) for cols in itertools.combinations(range(m), kt))
    dA = m - kt + 1 if mds else None
    print("L5: Goppa bounds d(head code) >= 28 - %d = %d, d(zero-tail code) >= 28 - %d = %d" % (4 * a + b, g1, 4 * (a - 1) + b, g2))
    print("L6: tail code dimension %d (= K - dim zero-tail: %s), all %d maximal minors nonzero: %s -> d(tail) = %s"
          % (kt, kt == K - rZ, len(list(itertools.combinations(range(m), kt))), mds, dA))
    dX = min(g2, g1 + dA) if (good and mds and rH == K and kt == K - rZ) else None
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
