"""Own replacement for the Klyve/Dunn Lemma 2.1 constant (proof in ../vlemma/PROOF_vlemma.md):
   for z > L >= 1:  V(z) >= V(L) + log(z/L)/(2 C2) - A(L),   A(L) <= (kappa + 4 + 8) L^-s S(s)  (valid when kappa+4 >= 1/(2s)),
   S(s) = prod_{p>2} (1 + (2 p^s + p^(2s)) / (p (p-2))),  0 < s < 1/2,  kappa = (gamma + log 2)/2.
   S(s) bounded rigorously: exact arb product over odd p <= P, tail via sum_{p>P} p^-b <= 1.25506 b P^(1-b) / ((b-1) log P)
   (pi(x) <= 1.25506 x / log x for x > 1), with log(1+a) <= a.
   Also checks numerically |eps(t)| <= 4/t, eps(t) = sum_{m<=t, m odd} 1/m - log(t)/2 - kappa, for t <= 1e6."""
import math, numpy as np
from flint import arb, fmpq, ctx
ctx.prec = 128
P = 10**7
sv = np.ones(P + 1, dtype=bool); sv[:2] = False; sv[4::2] = False
for i in range(3, int(P**0.5) + 1, 2):
    if sv[i]: sv[i*i::2*i] = False
primes = [int(p) for p in np.nonzero(sv)[0] if p > 2]
gamma = arb.const_euler(); kappa = (gamma + arb(2).log()) / 2
def S_upper(s):
    logS = arb(0)
    for p in primes:
        pa = arb(p); logS += (1 + (2 * pa**s + pa**(2 * s)) / (pa * (pa - 2))).log()
    fac = arb(P + 1) / arb(P - 1)          # p/(p-2) <= (P+1)/(P-1) for p >= P+1
    def tail(b):  # sum_{p>P} p^-b
        return arb(fmpq(125506, 100000)) * b * arb(P)**(1 - b) / ((b - 1) * arb(P).log())
    logS += fac * (2 * tail(2 - s) + tail(2 - 2 * s))
    return logS.exp()
L = arb(10)**10
for s in ("0.40", "0.44", "0.46", "0.48"):
    sa = arb(fmpq(int(s[2:]), 100)); S = S_upper(sa)
    c = kappa + 4; assert c > 1 / (2 * sa)
    A = (c + 8) * L**(-sa) * S
    print("s=%s  S(s) <= %s   A(1e10) <= %s" % (s, S.upper().str(8, radius=False), A.upper().str(8, radius=False)), flush=True)
k = float(kappa.mid()); worst = 0.0; O = 0.0
for n in range(1, 10**6 + 1):
    if n % 2 == 1: O += 1.0 / n
    for t in (n, n + 1 - 1e-9):
        worst = max(worst, abs(O - 0.5 * math.log(t) - k) * t)
print("max_t<=1e6 t*|eps(t)| =", worst, "(claimed <= 4)")
