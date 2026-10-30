#!/usr/bin/env python3
"""From a symplectic stabilizer matrix S over GF(3) (rows (x|z), 2n columns), compute exactly:
s = rank(S), c = rank(S J S^T)/2, k = n - s + c, a basis of N = span(S)^perp (symplectic dual) and of the
isotropic part I = span(S) ∩ N. Writes a text file for subset_ea.c: "n dimI dimN" then dimN rows of 2n entries,
the first dimI rows spanning I. Written from the bank definition; shares no code with the
builders. Usage: gf3prep.py object.json out.txt   (or gf3prep.py --text S.txt out.txt with "n s" + s rows)."""
import json, sys

P = 3

def rref(rows, ncols):
    """Reduced row echelon form mod 3. Returns (rows_rref, pivot_cols)."""
    A = [list(r) for r in rows]
    piv = []
    r = 0
    for col in range(ncols):
        p = next((i for i in range(r, len(A)) if A[i][col] % P), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 if A[r][col] == 1 else 2          # 2*2 = 4 = 1 mod 3
        A[r] = [(v * inv) % P for v in A[r]]
        for i in range(len(A)):
            if i != r and A[i][col]:
                f = A[i][col]
                A[i] = [(a - f * b) % P for a, b in zip(A[i], A[r])]
        piv.append(col)
        r += 1
        if r == len(A):
            break
    return A[:r], piv

def rank(rows, ncols):
    return len(rref(rows, ncols)[1])

def nullspace(rows, ncols):
    """Basis of {v : A v = 0} mod 3."""
    R, piv = rref(rows, ncols)
    free = [j for j in range(ncols) if j not in piv]
    basis = []
    for f in free:
        v = [0] * ncols
        v[f] = 1
        for i, pc in enumerate(piv):
            v[pc] = (-R[i][f]) % P
        basis.append(v)
    return basis

def symp(u, v, n):
    return (sum(u[i] * v[n + i] for i in range(n)) - sum(u[n + i] * v[i] for i in range(n))) % P

def vecmat(u, M):
    out = [0] * len(M[0])
    for a, row in zip(u, M):
        if a:
            out = [(o + a * r) % P for o, r in zip(out, row)]
    return out

def analyze(S, n):
    S = [[x % P for x in r] for r in S]
    assert all(len(r) == 2 * n for r in S)
    s = rank(S, 2 * n)
    M = [[symp(a, b, n) for b in S] for a in S]
    rM = rank(M, len(S))
    assert rM % 2 == 0
    c = rM // 2
    k = n - s + c
    F = [[(-r[n + i]) % P for i in range(n)] + [r[i] for i in range(n)] for r in S]   # <r, v> = F_r . v
    N = nullspace(F, 2 * n)
    U = nullspace(M, len(S))                     # u with M u = 0  ->  uS in N
    I = rref([vecmat(u, S) for u in U], 2 * n)[0] if U else []
    # basis of N starting with I
    basis = list(I)
    for v in N:
        if rank(basis + [v], 2 * n) > len(basis):
            basis.append(v)
    assert len(basis) == len(N) == 2 * n - s
    for v in basis:                                # every basis vector really is in N
        assert all(symp(r, v, n) == 0 for r in S)
    for v in I:                                    # and I really is in span(S)
        assert rank(S + [v], 2 * n) == s
    return dict(n=n, s=s, c=c, k=k, dimI=len(I), dimN=len(basis)), basis

def load(argv):
    if argv[1] == "--text":
        lines = open(argv[2]).read().split("\n")
        n, m = map(int, lines[0].split())
        S = [list(map(int, l.split())) for l in lines[1:1 + m]]
        return n, S, argv[3]
    obj = json.load(open(argv[1]))
    return obj["n"], obj["S"], argv[2]

if __name__ == "__main__":
    n, S, out = load(sys.argv)
    info, basis = analyze(S, n)
    print("n=%(n)d s=%(s)d c=%(c)d k=%(k)d dim_isotropic=%(dimI)d dim_dual=%(dimN)d" % info)
    with open(out, "w") as f:
        f.write("%d %d %d\n" % (n, info["dimI"], info["dimN"]))
        for v in basis:
            f.write(" ".join(map(str, v)) + "\n")
