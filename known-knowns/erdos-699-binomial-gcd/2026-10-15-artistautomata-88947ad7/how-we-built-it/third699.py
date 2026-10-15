"""Third implementation for Erdos #699 at single n, written separately from the C programs.
For each i in [1, n/2) such that no prime lies in [n-i+1, n] (deterministic Miller-Rabin), P(n,i) = primes p >= i with
v_p(C(n,i)) > 0 (prime factors of n-k, k < i, by trial division; v_p by Legendre's formula, checked for every p).
Candidates j in (i, n/2]: all j whose base-q digits are <= n's, for the q in P(n,i) with the fewest such j (counted
exactly); each is kept only if v_p(C(n,j)) = 0 (Legendre) for every p in P(n,i). Prints per n: cases, candidates.
Usage: python3 third699.py SEED COUNT LO HI   (n = random.Random(SEED).randrange(LO, HI), COUNT times)"""
import random, sys
def mr(n):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0: return n == p
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True
def factors(m):
    out, d = set(), 2
    while d * d <= m:
        if m % d == 0:
            out.add(d)
            while m % d == 0: m //= d
        d += 1 if d == 2 else 2
    if m > 1: out.add(m)
    return out
def vf(m, p):
    v = 0
    while m: m //= p; v += m
    return v
def vbin(n, k, p): return vf(n, p) - vf(k, p) - vf(n - k, p)
def digits(n, q):
    d = []
    while n: d.append(n % q); n //= q
    return d
def count_dom(n, q, hi):
    c = 1
    for x in digits(n, q): c *= x + 1
    return c   # upper bound on dominated j <= n (exact count of j <= n)
def dominated(n, q, lo, hi):
    ds = digits(n, q); out = [0]
    pw = 1
    for x in ds:
        out = [v + t * pw for v in out for t in range(x + 1) if v + t * pw <= hi]
        pw *= q
    return [v for v in out if lo < v <= hi]
def one(n, strict=False):
    half = n // 2; cases = cands = 0; fac = {}
    for i in range(1, half):
        if mr(n - (i - 1)): break
        cases += 1
        for k in range(i):
            if n - k not in fac: fac[n - k] = factors(n - k)
        P = sorted({p for k in range(i) for p in fac[n - k] if p > i})
        assert all(vbin(n, i, p) > 0 for p in P)
        if not strict and mr(i) and vbin(n, i, i) > 0: P.append(i)
        assert P, (n, i)
        q = min(P, key=lambda p: count_dom(n, p, half))
        assert count_dom(n, q, half) <= 5 * 10**7, ('too many', n, i, q)
        for j in dominated(n, q, i, half):
            if all(vbin(n, j, p) == 0 for p in P): cands += 1
    return cases, cands
if __name__ == '__main__':
    seed, cnt, lo, hi = map(int, sys.argv[1:5]); rng = random.Random(seed)
    for _ in range(cnt):
        n = rng.randrange(lo, hi); c, k = one(n); print('n=%d cases=%d candidates=%d' % (n, c, k), flush=True)
