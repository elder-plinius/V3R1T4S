#!/usr/bin/env python3
"""formalist lens (adapted from onepoint_check.py of an earlier run, not shipped): a no-search proof that the
object's distance is >= 28 - m - r for E_m with r coordinates deleted and some columns multiplied by w.
It shares only the GF(9) tables of gf9lib.py with the builder; no builder or checker code.
1. From S alone: rank S over GF(3), c = rank(S J S^T)/2, k = n - s + c (own elimination).
2. Build E = the extended one-point code of the Hermitian curve y^3 + y = x^4 over GF(9) with pole order m (monomials
   x^i y^j, j <= 2, 3i + 4j <= m, at the 27 affine points ordered by x then y in the encoding; 28th coordinate = the
   coefficient of the unique monomial of pole order m), with its own point list and monomial evaluation; delete the
   given coordinates and multiply the given columns of the result by w (encoded 3).
3. Check phi(E') (rows (a|b) of r and w r) is symplectically orthogonal to every row of S and has dimension
   2n - rank S, so span(S)^perp = phi(E') and symplectic weight on span(S)^perp is Hamming weight on E'.
4. Bound, proved here: d(E_m) >= 28 - m (a nonzero f in L(m P_inf) with nonzero top coefficient has pole order exactly
   m, so at most m zeros, all affine: weight >= 27 - m + 1; with zero top coefficient its pole order is <= m - 1, so
   at most m - 1 affine zeros and weight >= 27 - (m - 1) = 28 - m). Deleting r coordinates removes at most r nonzero
   entries of each word, and multiplying columns by w != 0 changes no weight: d(E') >= 28 - m - r. As 28 - m > r, no
   nonzero word dies, so E' keeps the GF(9) dimension of E_m. Hence d_EA >= 28 - m - r on all of span(S)^perp (the
   isotropic part removed can only raise it).
5. A witness word (GF(9) codes a + 3b) checked in E', outside span(S), with its weight.
Usage: punct_check.py object.json m deleted_cols scaled_cols witness_word"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf9lib import ADD, MUL, NEG
def rank3(rows, ncol):
    A = [r[:] for r in rows]; r = 0
    for c in range(ncol):
        p = next((i for i in range(r, len(A)) if A[i][c] % 3), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        inv = 1 if A[r][c] % 3 == 1 else 2
        A[r] = [(inv * v) % 3 for v in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] % 3:
                f = A[i][c]; A[i] = [(u - f * v) % 3 for u, v in zip(A[i], A[r])]
        r += 1
    return r
obj = json.load(open(sys.argv[1])); m = int(sys.argv[2])
dele = [int(t) for t in sys.argv[3].split(",") if t]; scl = set(int(t) for t in sys.argv[4].split(",") if t)
wit = [int(t) for t in sys.argv[5].split(",")]
S = [[v % 3 for v in r] for r in obj["S"]]; n = len(S[0]) // 2
def symp(u, v): return (sum(u[i] * v[n + i] - u[n + i] * v[i] for i in range(n))) % 3
s = rank3(S, 2 * n)
J = [[symp(a, b) for b in S] for a in S]
c2 = rank3(J, len(S)); c = c2 // 2; k = n - s + c
print("1. n=%d rank S=%d rank(S J S^T)=%d c=%d k=%d" % (n, s, c2, c, k))
def p9(x, e):
    r = 1
    for _ in range(e): r = MUL[r][x]
    return r
pts = [(x, y) for x in range(9) for y in range(9) if ADD[p9(y, 3)][y] == p9(x, 4)]
mons = [(i, j) for j in range(3) for i in range(m // 3 + 1) if 3 * i + 4 * j <= m]
top = [t for t in mons if 3 * t[0] + 4 * t[1] == m]
assert len(pts) == 27 and len(top) == 1
E = [[MUL[p9(x, i)][p9(y, j)] for x, y in pts] + [1 if (i, j) == top[0] else 0] for i, j in mons]
keep = [t for t in range(28) if t not in dele]
E = [[r[t] for t in keep] for r in E]
E = [[MUL[3][v] if t in scl else v for t, v in enumerate(r)] for r in E]
assert len(E[0]) == n
r = len(dele)
print("2. E_%d: %d monomials (pole orders %s), top monomial %s; deleted coordinates %s (affine points %s); columns %s of the result times w"
      % (m, len(mons), sorted(3 * i + 4 * j for i, j in mons), top[0], dele, [pts[t] for t in dele if t < 27], sorted(scl)))
def phi(r):
    out = []
    for sc in (1, 3):
        v = [MUL[sc][x] for x in r]
        out.append([x % 3 for x in v] + [x // 3 for x in v])
    return out
PE = [v for row in E for v in phi(row)]
orth = all(symp(u, srow) == 0 for u in PE for srow in S)
dE = rank3(PE, 2 * n)
print("3. phi(E') orthogonal to every row of S: %s; dim_GF(3) phi(E') = %d; 2n - rank S = %d; span(S)^perp = phi(E'): %s" % (orth, dE, 2 * n - s, orth and dE == 2 * n - s))
print("   GF(9) dimension of E' = %d (E_%d has %d monomials)" % (dE // 2, m, len(mons)))
print("4. bound (proved in the docstring): d(E') >= 28 - %d - %d = %d, so d_EA >= %d" % (m, r, 28 - m - r, 28 - m - r))
PW = phi(wit)
inN = rank3(PE + PW, 2 * n) == dE
inS = rank3(S + PW[:1], 2 * n) == s
wt = sum(1 for x in wit if x)
print("5. witness weight %d, in E': %s, phi(witness) in span(S): %s -> d_EA <= %d" % (wt, inN, inS, wt))
ok = orth and dE == 2 * n - s and dE // 2 == len(mons) and inN and not inS and wt == 28 - m - r
print("RESULT: d_EA = %d exactly (no distance search): %s" % (28 - m - r, ok))
