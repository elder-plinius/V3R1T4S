#!/usr/bin/env python3
"""Cubic/d-regular unlabeled graph counting via Burnside over vertex cycle types.

Method A (m1): histogram recurrence (Cheng-Xu Thm 3.2/4.1) eliminating one cycle
  at a time; global memo cache over histogram states. Fast; used for large N.
Method B (m2): direct coefficient extraction from Eq (2.6), state = residual-degree
  vector of all cycles; feasible only for few-part partitions. Independent per-type
  cross-check.

Outer loop: U_d(N) = sum_lambda F_d(lambda)/z_lambda; connected C_d via inverse
Euler transform (Eq 6.1-6.4). All exact big integers.
"""
import sys
from math import gcd, comb, factorial
from functools import lru_cache

D = 3


def set_degree(d):
    global D
    D = d
    Ia_cache.clear()
    Phi.cache_clear()
    class_options.cache_clear()


Ia_cache = {}

def Ia(a):
    """list I_a[u], u=0..D : # internal edge-orbit choices giving internal degree u.
    P_a(x) = (1+x^2)^floor((a-1)/2) (1+x)^[a even]."""
    key = (a, D)
    if key in Ia_cache:
        return Ia_cache[key]
    poly = [1]
    def mul(p, q):
        r = [0] * (len(p) + len(q) - 1)
        for i, ci in enumerate(p):
            if ci:
                for j, cj in enumerate(q):
                    r[i + j] += ci * cj
        return r
    for _ in range((a - 1) // 2):
        poly = mul(poly, [1, 0, 1])
    if a % 2 == 0:
        poly = mul(poly, [1, 1])
    res = [poly[u] if u < len(poly) else 0 for u in range(D + 1)]
    Ia_cache[key] = res
    return res


# ---- class-allocation options: distributing pivot joining-orbits to one class ----
# For a pivot of length pa and a target class (b, s) with h cycles:
#   g=gcd(pa,b); alpha=b/g edges to pivot per orbit; beta=pa/g to target per orbit.
#   choose nu_k = #cycles getting k orbits (k=0..K); weight = multinomial * C(g,k)^nu_k
# Returns list of (consumed, weight, moves) where moves = tuple of (b, new_s, cnt).

@lru_cache(maxsize=None)
def class_options(pa, b, s, h):
    g = gcd(pa, b)
    alpha = b // g
    beta = pa // g
    Kmax = min(g, D // alpha if alpha else 0, s // beta if beta else 0)
    opts = []
    # enumerate nu = (nu_1..nu_Kmax); nu_0 = h - sum
    def rec(k, remaining, consumed, weight, moves):
        if k > Kmax:
            # remaining cycles keep residual s (nu_0 of them) -> stay in class (b,s)
            mv = list(moves)
            if remaining > 0:
                mv.append((b, s, remaining))
            opts.append((consumed, weight, tuple(mv)))
            return
        new_s = s - k * beta
        ck = comb(g, k)
        for nu in range(0, remaining + 1):
            if nu == 0:
                rec(k + 1, remaining, consumed, weight, moves)
            else:
                if new_s < 0:
                    break
                # incremental multinomial: multiply by C(remaining, nu) to pick which
                w = weight * comb(remaining, nu) * (ck ** nu)
                mv = list(moves)
                if new_s > 0:
                    mv.append((b, new_s, nu))
                rec(k + 1, remaining - nu, consumed + alpha * k * nu, w, mv)
    rec(1, h, 0, 1, [])
    return opts


PHI = {}  # explicit memo (picklable for worker checkpoints)

class _PhiCache:
    def cache_clear(self):
        PHI.clear()
    def cache_info(self):
        import types
        return types.SimpleNamespace(currsize=len(PHI))


def Phi(H):
    """H: sorted-desc tuple of (a, r, count), r in 1..3, count>0."""
    v = PHI.get(H)
    if v is not None:
        return v
    r = _Phi(H)
    PHI[H] = r
    return r
Phi.cache_clear = _PhiCache().cache_clear
Phi.cache_info = _PhiCache().cache_info


def _Phi(H):
    if not H:
        return 1
    pa, pr, pc = H[0]
    rest = []
    if pc - 1 > 0:
        rest.append((pa, pr, pc - 1))
    rest.extend(H[1:])
    rest = tuple(rest)
    Iav = Ia(pa)
    total = 0
    for u in range(0, pr + 1):
        iu = Iav[u]
        if iu == 0:
            continue
        budget = pr - u
        for w, newH in _distribute(pa, rest, 0, budget):
            if w:
                total += iu * w * Phi(newH)
    return total


def _distribute(pa, classes, idx, budget):
    """Allocate pivot (length pa) joining-orbits to classes[idx:], consuming exactly
    `budget`.  Return list of (weight, new_histogram_tuple)."""
    if idx == len(classes):
        return [(1, ())] if budget == 0 else []
    b, s, h = classes[idx]
    out = []
    tails_cache = {}
    for consumed, weight, moves in class_options(pa, b, s, h):
        if consumed > budget:
            continue
        rem = budget - consumed
        if rem not in tails_cache:
            tails_cache[rem] = _distribute(pa, classes, idx + 1, rem)
        for w2, tailmoves in tails_cache[rem]:
            out.append((weight * w2, _merge(moves, tailmoves)))
    return out


def _merge(moves, tail):
    d = {}
    for (a, r, c) in tail:
        d[(a, r)] = d.get((a, r), 0) + c
    for (a, r, c) in moves:
        d[(a, r)] = d.get((a, r), 0) + c
    return tuple(sorted(((a, r, c) for (a, r), c in d.items() if c > 0), reverse=True))


def F_A(lam):
    """Method A fixed count for cycle type lam (tuple of cycle lengths)."""
    from collections import Counter
    cnt = Counter(lam)
    H = tuple(sorted(((a, D, m) for a, m in cnt.items()), reverse=True))
    return Phi(H)


# ================= Method B: direct Eq (2.6) coefficient extraction =================
def F_B(lam):
    """Independent: multiply out prod_i P_{a_i}(x_i) prod_{i<j}(1+x_i^p x_j^q)^g and
    read [x_1^D..x_t^D].  State = tuple of degrees so far. Feasible for small t."""
    t = len(lam)
    if t == 0:
        return 1
    # start: internal factors
    from collections import defaultdict
    state = {tuple([0] * t): 1}
    for i, a in enumerate(lam):
        Iav = Ia(a)
        nxt = defaultdict(int)
        for deg, c in state.items():
            for u in range(0, D + 1):
                iu = Iav[u]
                if iu and deg[i] + u <= D:
                    nd = list(deg); nd[i] += u
                    nxt[tuple(nd)] += c * iu
        state = nxt
    # pair factors
    for i in range(t):
        for j in range(i + 1, t):
            g = gcd(lam[i], lam[j])
            p = lam[j] // g   # exponent on x_i
            q = lam[i] // g   # exponent on x_j
            nxt = defaultdict(int)
            for deg, c in state.items():
                Kmax = min(g, (D - deg[i]) // p if p else g, (D - deg[j]) // q if q else g)
                for k in range(0, Kmax + 1):
                    nd = list(deg); nd[i] += k * p; nd[j] += k * q
                    nxt[tuple(nd)] += c * comb(g, k)
            state = nxt
    return state.get(tuple([D] * t), 0)


# ================= outer loop: Burnside + inverse Euler =================
def partitions(n, maxpart=None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield ()
        return
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - k, k):
            yield (k,) + rest


def z_lambda(lam):
    from collections import Counter
    cnt = Counter(lam)
    z = 1
    for a, m in cnt.items():
        z *= (a ** m) * factorial(m)
    return z


def U_counts(Nmax, method=F_A, verbose=False):
    """Return dict N -> U_d(N) (all unlabeled d-regular, incl. disconnected), even N."""
    U = {}
    for N in range(2, Nmax + 1):
        if (D * N) % 2 != 0:
            U[N] = 0
            continue
        B = 0
        for lam in partitions(N):
            f = method(lam)
            if f:
                B += (factorial(N) // z_lambda(lam)) * f
        assert B % factorial(N) == 0, "Burnside sum not divisible by N! at N=%d" % N
        U[N] = B // factorial(N)
        if verbose:
            sys.stderr.write("N=%d U=%d\n" % (N, U[N]))
    return U


def connected_from_U(U, Nmax):
    """Inverse Euler transform (Cheng-Xu 6.1-6.4). U defined on even N (odd ->0)."""
    # work over all n=1..Nmax with U[n]=0 for odd/missing
    Uf = {n: U.get(n, 0) for n in range(1, Nmax + 1)}
    b = {}
    C = {}
    for n in range(1, Nmax + 1):
        bn = n * Uf[n] - sum(b[j] * Uf[n - j] for j in range(1, n))
        b[n] = bn
        s = sum(j * C[j] for j in range(1, n) if n % j == 0 and j in C)
        num = bn - s
        assert num % n == 0, "connected division not exact at n=%d" % n
        C[n] = num // n
    return C
