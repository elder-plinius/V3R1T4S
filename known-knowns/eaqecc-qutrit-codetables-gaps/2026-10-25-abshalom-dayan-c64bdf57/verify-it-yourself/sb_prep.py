#!/usr/bin/env python3
"""Self-break check, written from the bank definition only, no earlier checker code:
from the stabilizer matrix S (rows (x|z) over GF(3), 2n columns) compute
  s = rank S, c = rank(S J S^T)/2, k = n - s + c,
  a GF(3) basis of N = span(S)^perp (symplectic dual: <u,v> = u_x.v_z - u_z.v_x = 0 for every row of S),
  dim of the isotropic part I = span(S) ∩ N,
and write "n dimN" followed by the dimN basis rows of N (2n trits each) for sb_enum.c, which enumerates all of N.
Usage: sb_prep.py object.json out.txt"""
import json, sys

def rref(rows, ncol):
    A = [[v % 3 for v in r] for r in rows]; piv = []; r = 0
    for c in range(ncol):
        p = next((i for i in range(r, len(A)) if A[i][c]), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        if A[r][c] == 2:
            A[r] = [(2 * v) % 3 for v in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                f = A[i][c]; A[i] = [(u - f * v) % 3 for u, v in zip(A[i], A[r])]
        piv.append(c); r += 1
    return A[:r], piv

def nullspace(rows, ncol):
    R, piv = rref(rows, ncol); free = [c for c in range(ncol) if c not in piv]; out = []
    for f in free:
        v = [0] * ncol; v[f] = 1
        for i, p in enumerate(piv):
            v[p] = (-R[i][f]) % 3
        out.append(v)
    return out

obj = json.load(open(sys.argv[1])); S = [[v % 3 for v in r] for r in obj["S"]]; n = len(S[0]) // 2
def symp(u, v):
    return (sum(u[i] * v[n + i] - u[n + i] * v[i] for i in range(n))) % 3
s = len(rref(S, 2 * n)[0])
G = [[symp(a, b) for b in S] for a in S]
c2 = len(rref(G, len(S))[0]); assert c2 % 2 == 0
c = c2 // 2; k = n - s + c
# v in N  <=>  for each row r: r_x . v_z - r_z . v_x = 0  <=>  v . (-r_z | r_x) = 0
M = [[(-x) % 3 for x in r[n:]] + r[:n] for r in S]
N = nullspace(M, 2 * n)
assert all(symp(r, v) == 0 for r in S for v in N)
assert len(N) == 2 * n - s
dimI = len(N) + s - len(rref(N + S, 2 * n)[0])
print("n=%d s=%d rank(SJS^T)=%d c=%d k=%d dimN=%d dimI=%d (claimed n=%s k=%s c=%s d=%s)"
      % (n, s, c2, c, k, len(N), dimI, obj.get("n"), obj.get("k"), obj.get("c"), obj.get("d")))
with open(sys.argv[2], "w") as f:
    f.write("%d %d\n" % (n, len(N)))
    for v in N:
        f.write(" ".join(map(str, v)) + "\n")
