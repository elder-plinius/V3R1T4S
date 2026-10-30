#!/usr/bin/env python3
"""Exact EAQECC parameters from a qutrit stabilizer matrix S alone (written from the bank
definition; shares no code with earlier runs' checkers or builders).

S rows are (x|z) over GF(3), 2n columns, symplectic form <(x|z),(x'|z')> = x.z' - z.x'.
  s = rank(S), c = rank(S J S^T)/2, k = n - s + c,
  N = span(S)^perp (symplectic dual), I = span(S) ∩ N (isotropic part), d = min symplectic weight on N \\ I.
For the GF(9) route, N must be closed under M(x|z) = (z | x+z) (multiplication by w, w^2 = w + 1); then
N = phi(C) for the GF(9)-linear code C = {x + w z}, symplectic weight = Hamming weight over GF(9), and
d >= d(C). infoset.c then decides d(C) >= delta exactly from a generator matrix of C.

Usage:
  gf9info.py prep object.json G9.txt        parameters, M-invariance, writes "kappa n" + kappa rows (a+3b codes)
  gf9info.py witness object.json p1,p2,...  the GF(9) codeword of C vanishing on the given positions (if unique
                                            up to scalars), its weight, membership in N and in I
  gf9info.py claimed object.json            prints the claimed n k c d fields
"""
import json, sys

# ---------- GF(3) ----------
def rref3(rows, ncols):
    A = [[v % 3 for v in r] for r in rows]
    piv, r = [], 0
    for col in range(ncols):
        p = next((i for i in range(r, len(A)) if A[i][col]), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        if A[r][col] == 2:
            A[r] = [(2 * v) % 3 for v in A[r]]
        for i in range(len(A)):
            if i != r and A[i][col]:
                f = A[i][col]
                A[i] = [(a - f * b) % 3 for a, b in zip(A[i], A[r])]
        piv.append(col)
        r += 1
        if r == len(A):
            break
    return A[:r], piv

def rank3(rows, ncols):
    return len(rref3(rows, ncols)[1]) if rows else 0

def null3(rows, ncols):
    """Basis of {v : row . v = 0 for all rows}."""
    R, piv = rref3(rows, ncols)
    basis = []
    for f in (j for j in range(ncols) if j not in piv):
        v = [0] * ncols
        v[f] = 1
        for i, pc in enumerate(piv):
            v[pc] = (-R[i][f]) % 3
        basis.append(v)
    return basis

def symp(u, v, n):
    return (sum(u[i] * v[n + i] - u[n + i] * v[i] for i in range(n))) % 3

def Mw(v, n):
    x, z = v[:n], v[n:]
    return z + [(a + b) % 3 for a, b in zip(x, z)]

# ---------- GF(9) = GF(3)[w]/(w^2 - w - 1), a + b w <-> a + 3b ----------
def f9(a, b):
    return (a % 3) + 3 * (b % 3)

def mul9(u, v):
    a, b, c, d = u % 3, u // 3, v % 3, v // 3
    return f9(a * c + b * d, a * d + b * c + b * d)

def add9(u, v):
    return f9(u % 3 + v % 3, u // 3 + v // 3)

def neg9(u):
    return f9(-(u % 3), -(u // 3))

INV9 = {u: next(v for v in range(1, 9) if mul9(u, v) == 1) for u in range(1, 9)}

def rref9(rows, ncols):
    A = [list(r) for r in rows]
    piv, r = [], 0
    for col in range(ncols):
        p = next((i for i in range(r, len(A)) if A[i][col]), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = INV9[A[r][col]]
        A[r] = [mul9(inv, v) for v in A[r]]
        for i in range(len(A)):
            if i != r and A[i][col]:
                f = neg9(A[i][col])
                A[i] = [add9(a, mul9(f, b)) for a, b in zip(A[i], A[r])]
        piv.append(col)
        r += 1
        if r == len(A):
            break
    return A[:r], piv

def null9(rows, ncols):
    R, piv = rref9(rows, ncols)
    basis = []
    for f in (j for j in range(ncols) if j not in piv):
        v = [0] * ncols
        v[f] = 1
        for i, pc in enumerate(piv):
            v[pc] = neg9(R[i][f])
        basis.append(v)
    return basis

# ---------- analysis ----------
def analyze(S):
    n = len(S[0]) // 2
    S = [[v % 3 for v in r] for r in S]
    s = rank3(S, 2 * n)
    K = [[symp(u, v, n) for v in S] for u in S]
    rK = rank3(K, len(S))
    assert rK % 2 == 0, "commutation matrix of odd rank"
    c = rK // 2
    k = n - s + c
    # N = span(S)^perp: <s_i, v> = x_i . v_z - z_i . v_x, coefficient vector (-z_i | x_i)
    coeff = [[(-v) % 3 for v in r[n:]] + r[:n] for r in S]
    N = null3(coeff, 2 * n)
    assert all(symp(u, v, n) == 0 for u in S for v in N)
    # I = span(S) ∩ N = { a S : a K = 0 } (K antisymmetric; a K = 0 <=> K^T a = 0)
    KT = [list(col) for col in zip(*K)]
    A = null3(KT, len(S))
    Ivecs = []
    for a in A:
        w = [0] * (2 * n)
        for ai, r in zip(a, S):
            if ai:
                w = [(x + ai * y) % 3 for x, y in zip(w, r)]
        Ivecs.append(w)
    Ib, _ = rref3(Ivecs, 2 * n) if Ivecs else ([], [])
    dimI = len(Ib)
    assert all(symp(u, v, n) == 0 for u in S for v in Ib)
    rN = rank3(N, 2 * n)
    assert rank3(N + Ib, 2 * n) == rN, "I not inside N"
    Minv = rank3(N + [Mw(v, n) for v in N], 2 * n) == rN
    return dict(n=n, s=s, c=c, k=k, N=N, I=Ib, dimN=rN, dimI=dimI, M_invariant=Minv)

def gf9_code(N, n):
    rows9 = [[f9(v[i], v[n + i]) for i in range(n)] for v in N]
    G, piv = rref9(rows9, n)
    return G

def load(path):
    return json.load(open(path))

def main():
    cmd, path = sys.argv[1], sys.argv[2]
    obj = load(path)
    if cmd == "claimed":
        print("claimed n=%s k=%s c=%s d=%s" % (obj.get("n"), obj.get("k"), obj.get("c"), obj.get("d")))
        return
    info = analyze(obj["S"])
    n = info["n"]
    print("n=%d s=%d c=%d k=%d dim_N=%d dim_I=%d N_closed_under_w=%s" % (
        n, info["s"], info["c"], info["k"], info["dimN"], info["dimI"], info["M_invariant"]))
    if not info["M_invariant"]:
        print("N is not GF(9)-linear; the GF(9) route does not apply")
        sys.exit(2)
    G = gf9_code(info["N"], n)
    kappa = len(G)
    print("kappa=%d (2*kappa == dim_N: %s)" % (kappa, 2 * kappa == info["dimN"]))
    assert 2 * kappa == info["dimN"]
    if cmd == "prep":
        with open(sys.argv[3], "w") as f:
            f.write("%d %d\n" % (kappa, n))
            for r in G:
                f.write(" ".join(map(str, r)) + "\n")
        print("wrote", sys.argv[3])
    elif cmd == "witness":
        zero = [int(t) for t in sys.argv[3].split(",") if t != ""]
        # messages m with (m G)_j = 0 for j in zero: null space of the transposed columns
        cols = [[G[i][j] for i in range(kappa)] for j in zero]
        msgs = null9(cols, kappa)
        print("codewords of C vanishing on the %d given positions: GF(9)-dimension %d" % (len(zero), len(msgs)))
        for m in msgs[:1]:
            cw = [0] * n
            for mi, r in zip(m, G):
                if mi:
                    cw = [add9(a, mul9(mi, b)) for a, b in zip(cw, r)]
            v = [x % 3 for x in cw] + [x // 3 for x in cw]
            wt = sum(1 for x in cw if x)
            inN = rank3(info["N"] + [v], 2 * n) == info["dimN"]
            inI = rank3(info["I"] + [v], 2 * n) == info["dimI"]
            orthS = all(symp(r, v, n) == 0 for r in obj["S"])
            print("codeword (a+3b):", " ".join(map(str, cw)))
            print("weight=%d in_N=%s orthogonal_to_all_rows_of_S=%s in_isotropic_part=%s" % (wt, inN, orthS, inI))

if __name__ == "__main__":
    main()
