#!/usr/bin/env python3
"""Checks the two corrected expectations behind the truncation compensation of SSZ N_rho^T
(eq. (7)/(22) and eq. (28)). Standard library, plus numpy for the exact last-exit series (part 4).

Setting (SSZ Prop. 3 proof): state (a, h) with honest lead d = h - a > 0; the attacker only waits.
Each block: attacker w.p. alpha (d -> d-1), honest w.p. 1-alpha (d -> d+1).  'Return' = d hits 0,
probability q^d, q = alpha/(1-alpha).  At the return the state is (a0, a0) with a0 = h + U, U = number of
honest blocks during the excursion.  Claim: E[U | return] = alpha d/(1-2 alpha), so
    E[a0 | return] = h + alpha (h-a)/(1-2 alpha),
while the printed value (h-a)/(1-2 alpha) equals E[duration N | return] (a time, not a position).
1. exact: G(d) = q^d * alpha d/(1-2alpha) solves G(d) = alpha G(d-1) + (1-alpha)(G(d+1) + q^(d+1)), G(0)=0, G -> 0,
   where G(d) = E[U ; return]  (Fractions, d = 1..60).
2. Monte Carlo (fixed seed; a walk whose lead reaches d+50 is counted as non-returning, return
   probability from there (9/11)^50 ~ 4e-5): conditional means of U, N and a0 for a few (a, h).
3. Monte Carlo of E[last(a,h)] for a >= h (the T = a compensation, eq. (22)/(27)/(7)).
4. Deterministic series: E[psi] = sum_t P(psi > t) = sum_t E[phi(D_t)], phi(k>=1)=1, phi(0)=2 alpha,
   phi(-k)=q^k, with the law of D_t propagated exactly in floating point (t < 40000, |D| <= 3000).
   Corrected Lemma 13: E[last(a,h)] = 2K + ((a-h)/(1-2a) + a + h)/2, K = a(1-a)/(1-2a)^2 (printed: K + ...).
"""
import random
from fractions import Fraction as F

def exact_identity(alpha, dmax=60):
    q = alpha / (1 - alpha); c = alpha / (1 - 2 * alpha)
    G = lambda d: q ** d * c * d
    ok = all(G(d) == alpha * G(d - 1) + (1 - alpha) * (G(d + 1) + q ** (d + 1)) for d in range(1, dmax + 1))
    return ok and G(0) == 0

def mc_return(alpha, a, h, n, rng, extra=50):
    d0 = h - a; cap = d0 + extra; sU = sN = ret = 0
    for _ in range(n):
        d, U, N = d0, 0, 0
        while 0 < d < cap:
            N += 1
            if rng.random() < alpha: d -= 1
            else: d += 1; U += 1
        if d == 0: ret += 1; sU += U; sN += N
    return ret / n, sU / ret, sN / ret

def mc_last(alpha, a, h, n, rng, horizon=6000):
    tot = 0
    for _ in range(n):
        x, y, last = a, h, a if a == h else None
        # walk until honest lead exceeds a safe margin (returns w.p. (9/11)^60 ~ 6e-6; tiny bias)
        lead = y - x
        while lead < 60 and (x + y) < horizon:
            if rng.random() < alpha: x += 1
            else: y += 1
            lead = y - x
            if x == y: last = x
        if last is None: last = x  # cannot happen for a >= h: starting in Low-Triangle the walk visits the diagonal
        tot += last
    return tot / n

if __name__ == '__main__':
    for al in (F(9, 20), F(19, 40)):
        print('alpha', al, 'exact identity E[U;return] = q^d*alpha*d/(1-2alpha) for d=1..60:', exact_identity(al))
    rng = random.Random(20261127)
    al = 0.45
    for a, h in ((249, 250), (245, 250), (240, 250)):
        d = h - a; pr, EU, EN = mc_return(al, a, h, 40000, rng)
        print('alpha .45 (a,h)=(%d,%d): P(return) mc %.5f exact %.5f | E[N|ret] mc %.3f (printed formula (h-a)/(1-2a) = %.3f)'
              ' | E[a0|ret] mc %.3f corrected h+a(h-a)/(1-2a) = %.3f'
              % (a, h, pr, (al / (1 - al)) ** d, EN, d / (1 - 2 * al), h + EU, h + al * d / (1 - 2 * al)))
    K = al * (1 - al) / (1 - 2 * al) ** 2
    for a, h in ((0, 0), (3, 1), (10, 10)):
        m = mc_last(al, a, h, 100000, rng)
        print('alpha .45 E[last(%d,%d)] mc %.3f  printed eq.(22) %.3f  corrected %.3f'
              % (a, h, m, K + 0.5 * ((a - h) / (1 - 2 * al) + a + h), 2 * K + 0.5 * ((a - h) / (1 - 2 * al) + a + h)))
    import numpy as np
    q = al / (1 - al)
    def Epsi(d0, steps=40000, M=3000):
        p = np.zeros(2 * M + 1); p[d0 + M] = 1.0
        D = np.arange(-M, M + 1)
        phi = np.ones(2 * M + 1); phi[D == 0] = 2 * al; phi[D < 0] = q ** (-D[D < 0].astype(float))
        tot = 0.0
        for t in range(steps):
            tot += p @ phi
            n = np.zeros_like(p); n[1:] += al * p[:-1]; n[:-1] += (1 - al) * p[1:]; p = n
        return tot
    for a, h in ((0, 0), (3, 1), (10, 10), (5, 0)):
        E = Epsi(a - h); last = 0.5 * (E + a + h)
        print('alpha .45 series (a,h)=(%d,%d): E[psi]=%.6f E[last]=%.6f  printed eq.(22) %.6f  corrected %.6f'
              % (a, h, E, last, K + 0.5 * ((a - h) / (1 - 2 * al) + a + h), 2 * K + 0.5 * ((a - h) / (1 - 2 * al) + a + h)))
