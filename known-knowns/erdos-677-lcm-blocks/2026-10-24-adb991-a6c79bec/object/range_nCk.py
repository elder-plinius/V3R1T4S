#!/usr/bin/env python3
"""Exhaustive, uncapped verification: NO counterexample to Erdos 677 with n <= C*k (C = 1000 by default).

Proof skeleton (see NOTES.md, Theorem S): if (n, m, k) is a counterexample (k >= 1, m >= n+k, M(m,k) = M(n,k)),
N = n + k, then
  (S1) k * prod_{i<=k}(m+i) <= lcm(1..k) * prod_{i<=k}(n+i), hence m + k <= c_k N with c_k = (lcm(1..k)/k)^(1/k)
       (and c_k < e^1.03883 < 2.8260 for all k by Rosser-Schoenfeld psi(x) < 1.03883 x);
  (S2) every b in B = (m, m+k] divides L = lcm(A) | lcm(1..N) and b > N, so B contains no prime; every prime power
       dividing an element of B is <= N; every prime P > k dividing lcm(B) divides exactly one element of A.
If moreover n <= C k then N <= (C+1) k, so k >= (m+k)/(c (C+1)) > m / (c (C+1)).
  * m > 2010760: Schoenfeld (1976) gives a prime in (m, m(1 + 1/16597)), so k < m/16597 < m/(c(C+1)) for
    C = 1000 (c (C+1) = 2828.8 < 16597): contradiction.  (Dusart 2010, x >= 396738, 1/(25 ln^2 x) works too.)
  * m <= 2010760: (m, m+k] prime-free => k <= G - 1 where G = max prime gap among primes <= 2010760+200
    (computed here), so m < c (C+1) (G-1); every remaining (m, k) is enumerated below, every admissible N is
    tested exactly (big-integer lcm).  Pinning: N must be >= the largest prime power Q dividing an element of B,
    and N mod P1 < k, N mod P2 < k for the two largest primes P1 > P2 > k dividing lcm(B).
"""
import sys
from math import gcd, log, exp, ceil

C = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
CUP = 2.8260  # > e^1.03883 >= c_k for all k (Rosser-Schoenfeld); numerically max c_k (k <= 20000) = 2.7437
X = 2_100_000

# sieve smallest prime factor
spf = list(range(X + 1))
for i in range(2, int(X**0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, X + 1, i):
            if spf[j] == j:
                spf[j] = i
primes = [i for i in range(2, X + 1) if spf[i] == i]
print("primes up to %d: %d" % (X, len(primes)))

# (a) check the Schoenfeld statement numerically where we can see it (sanity of the citation), x in (2010760, X-200)
badx = 0
for a, b in zip(primes, primes[1:]):
    # for x in [a, b): the next prime after x is b; need b < x (1 + 1/16597) for x > 2010760
    if b > X - 200:
        break
    if a >= 2010760 and b >= a * (1 + 1 / 16597):
        badx += 1
print("Schoenfeld-gap sanity check on (2010760, %d): violations %d" % (X - 200, badx))

# (b) max prime gap among primes <= 2010760 + 200
G = 0
for a, b in zip(primes, primes[1:]):
    if a > 2010760 + 200:
        break
    G = max(G, b - a)
c_big = CUP * (C + 1)
assert c_big < 16597  # needed for the Schoenfeld step
M1 = min(int(c_big * (G - 1)) + 1, 2010760)
print("C = %d: c(C+1) = %.1f; Schoenfeld excludes m > 2010760 since c(C+1) < 16597: %s" % (C, c_big, c_big < 16597))
print("max gap G (primes <= 2010960) = %d -> k <= %d -> m < min(c(C+1)(G-1), 2010760) = %d" % (G, G - 1, M1))


def factor(x):
    f = {}
    while x > 1:
        p = spf[x]
        e = 0
        while x % p == 0:
            x //= p
            e += 1
        f[p] = e
    return f


def lcm_range(lo, hi):
    v = 1
    for x in range(lo, hi + 1):
        v = v // gcd(v, x) * x
    return v


Lk = [1]
for k in range(1, 400):
    Lk.append(Lk[-1] // gcd(Lk[-1], k) * k)


def c_k(k):
    return exp((log(Lk[k]) - log(k)) / k) if k > 1 else 1.0


pairs = 0
cand = 0
full = 0
hits = []
divhits = set()
reach = set()
sample = []
allpairs = []
VAL_N = 80
nolarge = 0
maxk_seen = 0
# enumerate prime-free blocks (m, m+k], k >= 2, m <= M1, m + k <= c(C+1) k
for a, b in zip(primes, primes[1:]):
    if a > M1:
        break
    # blocks inside (a, b): m in [a, b-1-k]
    for m in range(a, b - 2):
        Q = 1
        P1 = P2 = 0
        for k in range(1, b - m):  # B = m+1..m+k, all < b, all composite (m >= a prime, m+k <= b-1)
            x = m + k
            f = factor(x)
            for p, e in f.items():
                q = p**e
                if q > Q:
                    Q = q
            for p in f:
                if p > P1:
                    P1, P2 = p, P1
                elif P2 < p < P1:
                    P2 = p
            if k < 2:
                continue
            if m + k > c_big * k:
                continue
            # primes > k dividing lcm(B): the two largest primes overall, if they exceed k
            big = [p for p in (P1, P2) if p > k]
            pairs += 1
            if m <= 20000:
                allpairs.append((m, k))
            maxk_seen = max(maxk_seen, k)
            ck = c_k(k) * (1 + 1e-9)
            lo = max(Q, k, int((m + k) / ck) - 1)
            hi = min(m, (C + 1) * k)
            if lo > hi:
                continue
            if not big:
                nolarge += 1
                Ns = range(lo, hi + 1)
            else:
                Pa = big[0]
                Pb = big[1] if len(big) > 1 else None
                lo = max(lo, Pa)
                Ns = []
                j = max(1, (lo - k + 1) // Pa)
                while j * Pa <= hi:
                    for N in range(max(lo, j * Pa), min(hi, j * Pa + k - 1) + 1):
                        if Pb is None or N % Pb < k:
                            Ns.append(N)
                    j += 1
            LB = None
            if pairs % 37 == 0:
                sample.append((m, k, sorted(N for N in Ns if N - k >= 0 and N <= m and k * (m + k) ** k <= Lk[k] * N ** k)))
            for N in Ns:
                cand += 1
                n = N - k
                if n < 0 or m < N:
                    continue
                # exact size test (S1) first, then full lcm
                if k * (m + k) ** k > Lk[k] * N ** k:
                    continue
                full += 1
                if N <= VAL_N:
                    reach.add((n, m, k))
                if LB is None:
                    LB = lcm_range(m + 1, m + k)
                LA = lcm_range(n + 1, N)
                if LA == LB:
                    hits.append((n, m, k))
                if N <= VAL_N and LA % LB == 0:
                    divhits.add((n, m, k))
print("prime-free (m,k) pairs examined: %d (max k %d); pairs with no prime > k in lcm(B): %d" % (pairs, maxk_seen, nolarge))
print("candidate N after pinning: %d; full lcm comparisons: %d" % (cand, full))
print("counterexamples found (n, m, k):", hits)
import json
json.dump({"div": sorted(divhits), "reach": sorted(reach), "sample": sample, "allpairs": allpairs, "C": C}, open(sys.argv[2], "w")) if len(sys.argv) > 2 else None
print("validation: triples with N <= %d reaching the full lcm comparison: %d" % (VAL_N, len(reach)))
print("validation: triples with N <= %d, lcm(B) | lcm(A), S1 size bound, reached by the enumeration: %d" % (VAL_N, len(divhits)))
print("RESULT: no counterexample with n <= %d k" % C if not hits else "RESULT: HITS FOUND")
