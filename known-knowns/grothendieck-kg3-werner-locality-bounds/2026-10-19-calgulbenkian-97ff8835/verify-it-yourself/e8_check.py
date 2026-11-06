#!/usr/bin/env python3
"""Standard-library checker for the E8 Grothendieck instance (d = 8, 120 x 120).

Notation: ip(x, y) is the Euclidean inner product.
Claim checked: for the 120 x 120 integer matrix A stored in the MATLAB file (A = 3 G - 13 I, G the
Gram matrix of the 120 positive roots of E8 in some order and with arbitrary signs),
  (1) L = max over a, b in {-1,+1}^120 of a^T A b equals 6104 exactly, and
  (2) Q = sum_ij A_ij ip(u_i, u_j) = 9240 for the unit vectors u_i = r_i / sqrt(2),
hence K_G(8) >= Q / L = 9240 / 6104 = 165/109.

Everything is exact integer or Fraction arithmetic; nothing is read from the contributor's
certificate. Phases:
  A  extract the matrix from the MATLAB 7.3 file and check its integer structure;
  B  identify its 120 lines with the 120 positive roots of E8 (explicit base search, root
     coordinates in the simple-root basis, entrywise reconstruction of the Gram matrix);
  C  Q = (A.A + 13 trace A) / 6;
  D  lower bound: an explicit sign vector b with ||A b||_1 = 6104 (a = sign(A b));
  E  upper bound: enumerate every dominant w = 2v (v a dominant weight with |v|^2 <= |rho|^2) and
     check a rational Lagrange-dual certificate for each, so that every b in {-1,1}^120 has
     ||A b||_1 <= 6104.

Upper-bound argument (see UPPER_BOUND.md in this folder for the full text):
  max_a a^T A b = ||A b||_1. Put w = sum_j b_j r_j. Then (A b)_i = 3 ip(r_i, w) - 13 b_i.
  The Weyl group permutes the roots up to sign, so replacing b by the transformed sign vector
  leaves ||A b||_1 unchanged and moves w to a dominant w. w lies in the zonotope
  sum_j [-1,1] r_j, whose vertices are the Weyl images of 2 rho, so |w|^2 <= |2 rho|^2; and
  w = 2 rho mod 2 (root lattice) puts w in 2 (root lattice) (E8 is unimodular), i.e. w = 2v with v
  a dominant weight, v = sum_k c_k omega_k, c_k >= 0 integers, |v|^2 <= |rho|^2.
  For fixed w, any mu gives  ||A b||_1 <= D_w(mu) = -ip(w,mu) + sum_i max_{s=+-1} ( |3 x_i - 13 s| + s ip(r_i, mu) ),
  x_i = ip(r_i, w), valid for every b in {-1,1}^120 with sum_j b_j r_j = w (add ip(mu, sum b_j r_j - w) = 0).
  A certificate is a rational mu with D_w(mu) <= 6104; when no such b exists mu may be arbitrarily large.
"""
import sys, array, itertools, time
from fractions import Fraction

M = 120
TARGET = 6104

# E8 Cartan matrix, Bourbaki labelling: chain 1-3-4-5-6-7-8 with node 2 attached to node 4
EDGES = [(1, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (2, 4)]


def cartan():
    C = [[0] * 8 for _ in range(8)]
    for i in range(8):
        C[i][i] = 2
    for a, b in EDGES:
        C[a - 1][b - 1] = C[b - 1][a - 1] = -1
    return C


def inverse_fraction(C):
    n = len(C)
    A = [[Fraction(C[i][j]) for j in range(n)] + [Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = next(r for r in range(col, n) if A[r][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [x / pv for x in A[col]]
        for r in range(n):
            if r != col and A[r][col] != 0:
                f = A[r][col]
                A[r] = [x - f * y for x, y in zip(A[r], A[col])]
    return [row[n:] for row in A]


def load_matrix(path):
    b = open(path, 'rb').read()
    for off in range(8):
        n = (len(b) - off) // 8
        a = array.array('q')
        a.frombytes(b[off:off + 8 * n])
        if sys.byteorder == 'big':
            a.byteswap()
        for k in range(n - M * M + 1):
            if a[k] == -7 and a[k + M + 1] == -7 and a[k + M * M - 1] == -7:
                blk = a[k:k + M * M]
                if all(blk[i * M + i] == -7 for i in range(M)) and all(blk[i * M + j] == blk[j * M + i] for i in range(M) for j in range(i)):
                    return [[blk[i * M + j] for j in range(M)] for i in range(M)], (off, k)
    raise SystemExit("matrix block not found")


def identify(A):
    """Return (P, S, G): P[j] = positive-root coordinates (simple-root basis) of line j, S[j] = sign
    with raw_j = S[j] * P[j], Gram G of the raw vectors (= (A + 13 I)/3)."""
    m = M
    G = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            v = A[i][j] + (13 if i == j else 0)
            assert v % 3 == 0
            G[i][j] = v // 3
    C = cartan()
    Ci = inverse_fraction(C)
    assert all(x.denominator == 1 for r in Ci for x in r)
    Ci = [[int(x) for x in r] for r in Ci]
    order = [1, 3, 4, 2, 5, 6, 7, 8]            # each node adjacent to an earlier one
    placed = {}                                  # node -> (line, sign)

    def rec(t):
        if t == 8:
            return True
        node = order[t]
        for j in range(m):
            if any(j == v[0] for v in placed.values()):
                continue
            for s in ((1,) if t == 0 else (1, -1)):
                ok = True
                for other, (lj, sj) in placed.items():
                    if s * sj * G[j][lj] != C[node - 1][other - 1]:
                        ok = False
                        break
                if ok:
                    placed[node] = (j, s)
                    if rec(t + 1):
                        return True
                    del placed[node]
        return False

    if not rec(0):
        raise SystemExit("no E8 base found among the lines")
    base = [placed[k] for k in range(1, 9)]       # base[k-1] = (line, sign) for simple root k
    raw = []
    for j in range(m):
        g = [base[k][1] * G[base[k][0]][j] for k in range(8)]     # ip(alpha_k, r_j)
        n = [sum(Ci[a][b] * g[b] for b in range(8)) for a in range(8)]
        raw.append(n)
    P, S = [], []
    for n in raw:
        if all(x >= 0 for x in n):
            P.append(n); S.append(1)
        elif all(x <= 0 for x in n):
            P.append([-x for x in n]); S.append(-1)
        else:
            raise SystemExit("line is not a root: mixed signs")
    return P, S, G, C, Ci, base


def form(C, x, y):
    return sum(x[i] * C[i][j] * y[j] for i in range(8) for j in range(8))


def enumerate_dominant(Ci, bound):
    """all integer c >= 0 with c^T Ci c <= bound (Ci has non-negative entries, so partial sums prune)."""
    out = []
    c = [0] * 8

    def q(cv):
        return sum(cv[i] * Ci[i][j] * cv[j] for i in range(8) for j in range(8))

    def rec(k):
        if k == 8:
            out.append(tuple(c))
            return
        v = 0
        while True:
            c[k] = v
            if q(c) > bound:
                break
            rec(k + 1)
            v += 1
        c[k] = 0

    rec(0)
    return out


def dual_times_q(P, xs, nw, Mvec, q):
    """q * D_w(mu) for mu = Mvec / q expressed through m_k = ip(alpha_k, mu)."""
    tot = -sum(a * b for a, b in zip(nw, Mvec))
    for n, x in zip(P, xs):
        dot = n[0] * Mvec[0] + n[1] * Mvec[1] + n[2] * Mvec[2] + n[3] * Mvec[3] + n[4] * Mvec[4] + n[5] * Mvec[5] + n[6] * Mvec[6] + n[7] * Mvec[7]
        v1 = q * abs(3 * x - 13) + dot
        v2 = q * abs(3 * x + 13) - dot
        tot += v1 if v1 > v2 else v2
    return tot


def main():
    import os
    mat, certpath, witpath = sys.argv[1], sys.argv[2], sys.argv[3]
    t0 = time.time()
    ok = True
    print("== Phase A: matrix from the MATLAB file")
    A, loc = load_matrix(mat)
    ent = sorted({x for r in A for x in r})
    print("matrix found (byte offset %d, element %d): 120 x 120, symmetric, diagonal all -7, entries %s" % (loc[0], loc[1], ent))
    assert set(ent) <= {-7, -3, 0, 3}
    rows3 = {sum(1 for x in r if abs(x) == 3) for r in A}
    rows0 = {sum(1 for x in r if x == 0) for r in A}
    print("per row: number of entries +-3 = %s, number of zeros = %s" % (sorted(rows3), sorted(rows0)))
    print("== Phase B: identification with the positive roots of E8")
    try:
        P, S, G, C, Ci, base = identify(A)
        if len({tuple(p) for p in P}) != 120 or not all(form(C, p, p) == 2 for p in P):
            raise SystemExit("the 120 lines do not give 120 distinct norm-2 root vectors")
    except SystemExit as e:
        print("Phase B FAILED: %s" % e)
        print("RESULT FAIL")
        sys.exit(1)
    print("base of simple roots found among the lines (Bourbaki labelling), lines %s" % [b[0] for b in base])
    # entrywise reconstruction of the Gram matrix from the root coordinates
    bad = 0
    for i in range(M):
        for j in range(M):
            if S[i] * S[j] * form(C, P[i], P[j]) != G[i][j]:
                bad += 1
    print("Gram entries not reproduced by root coordinates: %d of %d" % (bad, M * M))
    ok &= (bad == 0)
    two_rho = [sum(p[k] for p in P) for k in range(8)]
    norm_2rho = form(C, two_rho, two_rho)
    print("120 distinct positive roots with all coordinates >= 0 and norm 2; |2 rho|^2 = %d (so |rho|^2 = %d)" % (norm_2rho, norm_2rho // 4))
    print("A = D (3 G' - 13 I) D with D = diag(signs) and G' the Gram matrix of the 120 positive roots; L and Q are unchanged by D.")
    # identity used in the upper bound: (A b)_i = 3 ip(r_i, w) - 13 b_i with w = sum_j b_j r_j, checked on pseudo-random sign vectors
    import random
    rng = random.Random(1)
    bad_id = 0
    for _ in range(40):
        bb = [rng.choice((-1, 1)) for _ in range(M)]
        Abb = [sum(A[i][j] * bb[j] for j in range(M)) for i in range(M)]
        nwv = [sum(S[j] * bb[j] * P[j][k] for j in range(M)) for k in range(8)]
        for i in range(M):
            xi = sum(P[i][k] * sum(C[k][l] * nwv[l] for l in range(8)) for k in range(8)) * S[i]
            if Abb[i] != 3 * xi - 13 * bb[i]:
                bad_id += 1
    print("identity (A b)_i = 3 ip(r_i, w) - 13 b_i on 40 pseudo-random sign vectors: %d violations" % bad_id)
    ok &= (bad_id == 0)
    print("== Phase C: Q")
    AA = sum(x * x for r in A for x in r)
    tr = sum(A[i][i] for i in range(M))
    num = AA + 13 * tr
    print("A.A = %d, trace A = %d, Q = (A.A + 13 trace A)/6 = %s" % (AA, tr, Fraction(num, 6)))
    Q = Fraction(num, 6)
    ok &= (Q == 9240)
    print("== Phase D: lower bound L >= 6104")
    wit = {}
    for line in open(witpath):
        t = line.split()
        if len(t) == 9:
            wit[tuple(int(x) for x in t[:8])] = int(t[8])
    assert len(wit) == 120 and set(wit) == {tuple(p) for p in P}, "witness does not cover the 120 roots"
    b = [S[j] * wit[tuple(P[j])] for j in range(M)]
    assert all(x in (-1, 1) for x in b)
    Ab = [sum(A[i][j] * b[j] for j in range(M)) for i in range(M)]
    val = sum(abs(x) for x in Ab)
    a = [1 if x >= 0 else -1 for x in Ab]
    aAb = sum(a[i] * Ab[i] for i in range(M))
    print("witness b has %d entries +1 and %d entries -1; a = sign(A b); a^T A b = %d ; ||A b||_1 = %d" % (b.count(1), b.count(-1), aAb, val))
    ok &= (aAb == val == TARGET)
    print("== Phase E: upper bound L <= 6104")
    bound = norm_2rho // 4
    cs = enumerate_dominant(Ci, bound)
    print("dominant w = 2v with v = sum c_k omega_k, |v|^2 <= %d: %d vectors" % (bound, len(cs)))
    cert = {}
    parts = [certpath] if os.path.exists(certpath) else []
    k = 1
    while os.path.exists("%s.part%02d" % (certpath, k)):
        parts.append("%s.part%02d" % (certpath, k)); k += 1
    for pth in parts:
        for line in open(pth):
            t = line.split()
            if len(t) == 17:
                cert[tuple(int(x) for x in t[:8])] = ([int(x) for x in t[8:16]], int(t[16]))
    print("certificate lines read: %d" % len(cert))
    worst = None
    n_tight = 0
    missing = 0
    fail = 0
    for c in cs:
        if c not in cert:
            missing += 1
            continue
        Mv, q = cert[c]
        nv = [sum(Ci[a_][b_] * c[b_] for b_ in range(8)) for a_ in range(8)]
        nw = [2 * x for x in nv]
        xs = [2 * sum(p[k_] * c[k_] for k_ in range(8)) for p in P]
        d = dual_times_q(P, xs, nw, Mv, q)
        if q <= 0 or d > TARGET * q:
            fail += 1
        if d == TARGET * q:
            n_tight += 1
        gap = Fraction(d, q)
        if worst is None or gap > worst[0]:
            worst = (gap, c)
    print("dominant vectors without a certificate: %d; certificates with dual value above 6104: %d; with dual value exactly 6104: %d" % (missing, fail, n_tight))
    print("largest certified dual value: %s at c = %s" % (worst[0], worst[1]))
    ok &= (missing == 0 and fail == 0)
    print("elapsed %.1f s" % (time.time() - t0))
    if ok:
        print("RESULT PASS: L = 6104, Q = 9240, Q/L = %s = %.16f" % (Fraction(9240, 6104), 9240 / 6104))
    else:
        print("RESULT FAIL")
        sys.exit(1)


if __name__ == '__main__':
    main()
