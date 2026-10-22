"""Up-sets of {0,1}^m and domination of Bernoulli(q)^m by Strassen's theorem.

A law P on {0,1}^m stochastically dominates Q = Bernoulli(q)^m (a monotone coupling with X >= Y exists) iff
P(A) >= Q(A) for every up-set A (Strassen 1965; for a finite poset this is max-flow/min-cut).
Patterns are integers x in [0, 2^m); bit i is child i. An up-set is a frozenset of patterns closed upward.
"""
from fractions import Fraction

import numpy as np


def upsets(m):
    """All up-sets of {0,1}^m (Dedekind numbers: m = 5 gives 7581), as sorted tuples of patterns."""
    if m == 0:
        return [(), (0,)]
    res = []
    lower = upsets(m - 1)
    top = 1 << (m - 1)
    S = [set(u) for u in lower]
    for i, A0 in enumerate(S):          # patterns with bit m-1 = 0
        for A1 in S:                    # patterns with bit m-1 = 1 (shifted)
            if A0 <= A1:                # x in A0 implies x + top in A: closed upward needs A0 subset of A1
                res.append(tuple(sorted(A0 | {x | top for x in A1})))
    return res


def matrix(m):
    U = upsets(m)
    M = np.zeros((len(U), 1 << m), bool)
    for i, A in enumerate(U):
        M[i, list(A)] = True
    return U, M


def q_law(q, m):
    return np.array([q ** bin(x).count("1") * (1 - q) ** (m - bin(x).count("1")) for x in range(1 << m)])


def q_law_exact(q, m):
    q = Fraction(q)
    return [q ** bin(x).count("1") * (1 - q) ** (m - bin(x).count("1")) for x in range(1 << m)]


def max_q(laws, m, tol=1e-6):
    """For each law (rows of an array, each summing to 1), the largest q it dominates (float guide)."""
    U, M = matrix(m)
    P = laws @ M.T.astype(float)            # (nlaws, nupsets)
    lo = np.zeros(len(laws))
    hi = np.ones(len(laws))
    Mf = M.astype(float)
    while (hi - lo).max() > tol:
        mid = (lo + hi) / 2
        Q = np.stack([q_law(t, m) for t in mid]) @ Mf.T
        ok = (P >= Q - 1e-15).all(axis=1)
        lo = np.where(ok, mid, lo)
        hi = np.where(ok, hi, mid)
    return lo


if __name__ == "__main__":
    for m in range(6):
        print(m, len(upsets(m)))
