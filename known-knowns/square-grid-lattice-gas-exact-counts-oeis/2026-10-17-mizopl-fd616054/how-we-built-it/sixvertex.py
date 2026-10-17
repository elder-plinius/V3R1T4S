#!/usr/bin/env python3
"""
A054759: Eulerian orientations of the n x n torus = six-vertex model at the ice point.

Convention / derivation (pinned, see NOTES.md):
  Vertical edge below vertex j carries bit d_j (1 = arrow points UP = "in" to vertex j).
  Vertical edge above vertex j carries bit u_j (1 = UP).
  Horizontal edge h_j to the left of vertex j: 1 = arrow points RIGHT.
  Ice rule at vertex j (in-degree = out-degree = 2):
        d_j + (1-u_j) + h_j + (1-h_{j+1}) = 2
    =>  h_{j+1} = h_j + d_j - u_j      (must stay in {0,1})
  Around the periodic ring h_n = h_0  =>  sum_j d_j = sum_j u_j  (up-arrow count conserved
  => transfer matrix T is block-diagonal by number of up vertical arrows = "sector").

  T[d][u] = number of valid starting values h_0 in {0,1} so that h_j = h_0 + Q_j stays in {0,1}
  for all j, where Q_j = sum_{i<j} (d_i - u_i) is the prefix sum (Q_0 = 0, j = 0..n-1).
  With m = min_j Q_j (<=0), M = max_j Q_j (>=0):
        valid h_0 in [ -m , 1-M ] intersected with {0,1}
        count = max(0, min(1,1-M) - max(0,-m) + 1)   -> value in {0,1,2}.

  a(n) = Tr(T^n) on the n x n torus = sum over sectors k of Tr(T_k^n).

Modular arithmetic: float64 BLAS matmul is EXACT because entries < p < 2^20 and the
contracted dimension k <= C(15,7)=6435, so sum of products < 6435 * (2^20)^2 < 2^53.
Reduce mod p via int64 after each matmul. CRT across several primes to get the exact integer.
"""
import sys
import numpy as np
from itertools import combinations
from functools import reduce


def primes_below(bound, count, start=None):
    """Return `count` primes just below `bound` (descending from bound)."""
    def is_prime(x):
        if x < 2:
            return False
        if x % 2 == 0:
            return x == 2
        i = 3
        while i * i <= x:
            if x % i == 0:
                return False
            i += 2
        return True
    out = []
    x = (start if start is not None else bound) - 1
    while len(out) < count and x > 2:
        if is_prime(x):
            out.append(x)
        x -= 1
    return out


def sector_states(n, k):
    """All n-bit patterns with exactly k ones. Return (Ns, bits array int8 [Ns,n])."""
    combs = list(combinations(range(n), k))
    Ns = len(combs)
    bits = np.zeros((Ns, n), dtype=np.int8)
    for idx, c in enumerate(combs):
        for pos in c:
            bits[idx, pos] = 1
    return Ns, bits


def build_sector_matrix(n, bits):
    """Build the T_k matrix (float64) for a sector given its [Ns,n] bit patterns.

    T[a,b] for d = bits[a], u = bits[b]. Entry depends on min/max of prefix sums of (d-u).
    Prefix Q_j = sum_{i<j} s_i, j=0..n-1 (Q_0 = 0). We track Q over j=0..n-1, i.e. add
    s_0..s_{n-2} (we must NOT add s_{n-1}, which would be Q_n and is enforced =0 by sector).
    """
    Ns = bits.shape[0]
    # s_j[a,b] = bits[a,j] - bits[b,j]
    cur = np.zeros((Ns, Ns), dtype=np.int16)   # Q_0 = 0
    mn = np.zeros((Ns, Ns), dtype=np.int16)
    mx = np.zeros((Ns, Ns), dtype=np.int16)
    for j in range(n - 1):                      # add s_0 .. s_{n-2}
        sj = bits[:, j][:, None].astype(np.int16) - bits[:, j][None, :].astype(np.int16)
        cur += sj
        np.minimum(mn, cur, out=mn)
        np.maximum(mx, cur, out=mx)
    # count = max(0, min(1, 1-M) - max(0, -m) + 1)
    lo = np.maximum(0, -mn)
    hi = np.minimum(1, 1 - mx)
    cnt = hi - lo + 1
    cnt[cnt < 0] = 0
    return cnt.astype(np.float64)


def build_sector_matrix_explicit(n, bits):
    """INDEPENDENT entry computation: explicitly simulate the horizontal walk for both
    starting values h_0 in {0,1} and count the ones that stay in {0,1}. Vectorized but a
    different code path from the min/max closed form (cross-check guard)."""
    Ns = bits.shape[0]
    bi = bits.astype(np.int16)
    entry = np.zeros((Ns, Ns), dtype=np.float64)
    for h0 in (0, 1):
        cur = np.full((Ns, Ns), h0, dtype=np.int16)          # h_0
        valid = np.ones((Ns, Ns), dtype=bool)                # h_0 in {0,1} always
        for j in range(n - 1):                               # produce h_1..h_{n-1}
            sj = bi[:, j][:, None] - bi[:, j][None, :]
            cur = cur + sj
            valid &= (cur >= 0) & (cur <= 1)
        entry += valid
    return entry


def matpow_mod(A, e, p):
    """A^e mod p using float64 BLAS matmul + int64 reduction (exact for p<2^20, k<2^13)."""
    n = A.shape[0]
    # identity
    R = np.eye(n, dtype=np.float64)
    B = (A.astype(np.int64) % p).astype(np.float64)
    first = True
    while e > 0:
        if e & 1:
            if first:
                R = B.copy()
                first = False
            else:
                C = R @ B
                R = (C.astype(np.int64) % p).astype(np.float64)
        e >>= 1
        if e > 0:
            C = B @ B
            B = (C.astype(np.int64) % p).astype(np.float64)
    if first:  # e was 0
        return R
    return R


def trace_Tn_mod(n, p, reverse=False, builder=build_sector_matrix):
    """Compute a(n) = Tr(T^n) mod p by summing Tr(T_k^n) over sectors k=0..n."""
    total = 0
    for k in range(n + 1):
        Ns, bits = sector_states(n, k)
        if reverse:
            bits = bits[:, ::-1].copy()   # alternate encoding: reverse vertex order
        if Ns == 0:
            continue
        T = builder(n, bits)
        Tn = matpow_mod(T, n, p)
        total = (total + int(np.trace(Tn)) ) % p
    return total % p


def crt(residues, moduli):
    """Chinese remainder. Return x in [0, prod)."""
    M = reduce(lambda a, b: a * b, moduli)
    x = 0
    for r, m in zip(residues, moduli):
        Mi = M // m
        inv = pow(Mi % m, -1, m)
        x = (x + r * Mi * inv) % M
    return x, M


def compute_a(n, primes, reverse=False, builder=build_sector_matrix, verbose=False):
    res = []
    for p in primes:
        r = trace_Tn_mod(n, p, reverse=reverse, builder=builder)
        res.append(r)
        if verbose:
            print(f"    n={n} p={p} -> {r}", flush=True)
    val, M = crt(res, primes)
    return val, M, res


if __name__ == "__main__":
    # smoke test
    primes = primes_below(1 << 20, 8)
    for n in range(1, 5):
        v, M, res = compute_a(n, primes)
        print(f"a({n}) = {v}")
