#!/usr/bin/env python3
"""Exact rational check of Walsh-Fourier moments M_k = (1/8) sum_x (x^T G x)^k
using standard-library fractions + numpy exact linear algebra on sample matrices."""
from fractions import Fraction
import numpy as np

# Check M_1, M_2, M_3 exact identities in terms of t2 = tr(G^2) and t3 = tr(G^3)
# Let's verify on 50 random symmetric matrices with unit diagonal!
rng = np.random.default_rng(1)
signs = np.array([[1, s2, s3, s4] for s2 in (-1, 1) for s3 in (-1, 1) for s4 in (-1, 1)], dtype=float)

X2, Y2 = [], []
X3, Y3 = [], []
X4, Y4 = [], []
for _ in range(50):
    A = rng.uniform(-1, 1, size=(4, 4))
    G = 0.5*(A + A.T)
    np.fill_diagonal(G, 1.0)
    qs = np.array([s @ G @ s for s in signs])
    t2 = np.trace(G @ G)
    t3 = np.trace(G @ G @ G)
    t4 = np.trace(G @ G @ G @ G)
    detG = np.linalg.det(G)
    s4_off = sum(G[i,j]**4 for i in range(4) for j in range(i+1, 4))
    X2.append([1.0, t2]); Y2.append(np.mean(qs**2))
    X3.append([1.0, t2, t3]); Y3.append(np.mean(qs**3))
    X4.append([1.0, t2, t2**2, t3, t4, detG, s4_off]); Y4.append(np.mean(qs**4))

c2, res2, _, _ = np.linalg.lstsq(X2, Y2, rcond=None)
c3, res3, _, _ = np.linalg.lstsq(X3, Y3, rcond=None)
c4, res4, _, _ = np.linalg.lstsq(X4, Y4, rcond=None)
print("M_2 = [1, tr(G^2)] @", [Fraction(x).limit_denominator(1000) for x in c2], "residual:", res2)
print("M_3 = [1, tr(G^2), tr(G^3)] @", [Fraction(x).limit_denominator(1000) for x in c3], "residual:", res3)
print("M_4 = [1, t2, t2^2, t3, t4, detG, sum_{i<j} g_ij^4] @", [Fraction(x).limit_denominator(1000) for x in c4], "residual:", res4)
