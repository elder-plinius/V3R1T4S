#!/usr/bin/env python3
"""Numerical sanity check for physlib-clifford-dirac-iso (kernel-first lens).

Rebuilds the four gamma matrices exactly as Physlib defines them (chiral-basis matrices from
Fermion.Dirac.gamma_toMatrix, conjugated by endEquivMatrix's P and P^-1), checks the Clifford relations for
signature (+,-,-,-), forms the 16 ordered products gamma_A (A a subset of {0,1,2,3}, increasing order) and
computes their rank over R (as vectors in R^32 = real and imaginary parts of the 16 entries).
Also prints, for each product, its support pattern, to pick entry functionals for the Lean proof.
Standard library only (exact arithmetic with Gaussian rationals via fractions).
"""
from fractions import Fraction as F
from itertools import combinations

I = complex(0, 1)

def mat(rows):
    return [[complex(x) for x in r] for r in rows]

def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

def add(A, B):
    return [[A[i][j] + B[i][j] for j in range(4)] for i in range(4)]

def smul(c, A):
    return [[c * A[i][j] for j in range(4)] for i in range(4)]

ONE = mat([[1 if i == j else 0 for j in range(4)] for i in range(4)])

# Fermion.Dirac.gamma_toMatrix (chiral basis), indices inl 0, inr 0, inr 1, inr 2
chiral = [
    mat([[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]),
    mat([[0, 0, 0, 1], [0, 0, 1, 0], [0, -1, 0, 0], [-1, 0, 0, 0]]),
    mat([[0, 0, 0, -I], [0, 0, I, 0], [0, I, 0, 0], [-I, 0, 0, 0]]),
    mat([[0, 0, 1, 0], [0, 0, 0, -1], [-1, 0, 0, 0], [0, 1, 0, 0]]),
]
# Fermion.Dirac.endEquivMatrix_apply: P * M * ((1/2) * Q)
P = mat([[1, 0, 1, 0], [0, 1, 0, 1], [-1, 0, 1, 0], [0, -1, 0, 1]])
Q = smul(0.5, mat([[1, 0, -1, 0], [0, 1, 0, -1], [1, 0, 1, 0], [0, 1, 0, 1]]))
assert all(abs(x - y) < 1e-12 for r1, r2 in zip(mul(P, Q), ONE) for x, y in zip(r1, r2)), "P*Q != 1"
dirac = [mul(mul(P, M), Q) for M in chiral]

def show(M):
    def f(z):
        z = complex(round(z.real, 9), round(z.imag, 9))
        if z.imag == 0:
            return "%g" % z.real
        if z.real == 0:
            return "%gI" % z.imag
        return str(z)
    return "; ".join(", ".join(f(z) for z in r) for r in M)

eta = [1, -1, -1, -1]
ok = True
for mu in range(4):
    for nu in range(4):
        ac = add(mul(dirac[mu], dirac[nu]), mul(dirac[nu], dirac[mu]))
        target = smul(2 * eta[mu] if mu == nu else 0, ONE)
        if any(abs(ac[i][j] - target[i][j]) > 1e-12 for i in range(4) for j in range(4)):
            ok = False
print("Clifford relations {g_mu, g_nu} = 2 eta_mu_nu (+,-,-,-):", "OK" if ok else "FAIL")
for k, M in enumerate(dirac):
    print("dirac gamma%d = !![%s]" % (k, show(M)))

def products(gs):
    out = []
    for r in range(5):
        for A in combinations(range(4), r):
            M = ONE
            for a in A:
                M = mul(M, gs[a])
            out.append((A, M))
    return out

def realvec(M):
    return [M[i][j].real for i in range(4) for j in range(4)] + [M[i][j].imag for i in range(4) for j in range(4)]

def rank(rows):
    rows = [[F(round(x * 2) , 2) for x in r] for r in rows]  # entries are half-integers at worst
    rk = 0
    ncol = len(rows[0])
    for c in range(ncol):
        piv = None
        for r in range(rk, len(rows)):
            if rows[r][c] != 0:
                piv = r
                break
        if piv is None:
            continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        for r in range(len(rows)):
            if r != rk and rows[r][c] != 0:
                f = rows[r][c] / rows[rk][c]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[rk])]
        rk += 1
    return rk

for name, gs in (("dirac", dirac), ("chiral", chiral)):
    ps = products(gs)
    print("%s: number of products = %d, real rank of the products = %d" % (name, len(ps), rank([realvec(M) for _, M in ps])))
    for A, M in ps:
        print("  %s A=%s : !![%s]" % (name, A, show(M)))
# the real algebra generated: closure under products of the R-span; rank of all products of length <= 6 words
ps = []
import itertools
words = [()]
for L in range(1, 7):
    words += list(itertools.product(range(4), repeat=L))
allm = []
for w in words:
    M = ONE
    for a in w:
        M = mul(M, dirac[a])
    allm.append(realvec(M))
print("real rank of all words of length <= 6 in the dirac gammas:", rank(allm))
