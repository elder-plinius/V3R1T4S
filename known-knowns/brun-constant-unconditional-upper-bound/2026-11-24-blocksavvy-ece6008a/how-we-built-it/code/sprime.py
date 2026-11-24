"""Rigorous upper bounds for S'(s) = prod_{p>2} (1 + (2/(p-2)) p^-s + (p/(p-2)) p^-2s), 1/2 < s < 1  (arb).
Exact product over odd p <= P = 1e7; tail via log(1+a) <= a and, for p > P, p/(p-2) <= (P+1)/(P-1), 2/(p-2) <= (2/p)(P+1)/(P-1),
sum_{p>P} p^-b <= 1.25506 b P^(1-b) / ((b-1) log P) (b > 1; from pi(x) <= 1.25506 x/log x, Rosser-Schoenfeld 1962 (3.6);
same tail lemma as runs/2026-11-23-1618/claim_v2/code/vlemma.py).
Used in: W(z) <= z/(2 C2) + z^s S'(s) for all z >= 1 (proof in ../../../notes/W_lemma.md)."""
import numpy as np, json, sys
from flint import arb, fmpq, ctx
ctx.prec = int(sys.argv[1]) if len(sys.argv) > 1 else 128
P = 10**7
sv = np.ones(P + 1, dtype=bool); sv[:2] = False; sv[4::2] = False
for i in range(3, int(P**0.5) + 1, 2):
    if sv[i]: sv[i*i::2*i] = False
primes = [int(p) for p in np.nonzero(sv)[0] if p > 2]
out = {}
for s in ("0.52", "0.54", "0.56", "0.58", "0.60", "0.63", "0.66", "0.70", "0.75"):
    sa = arb(fmpq(int(s[2:]), 100)); logS = arb(0)
    for p in primes:
        pa = arb(p); logS += (1 + 2 / (pa - 2) * pa**(-sa) + pa / (pa - 2) * pa**(-2 * sa)).log()
    fac = arb(P + 1) / arb(P - 1)
    def tail(b): return arb(fmpq(125506, 100000)) * b * arb(P)**(1 - b) / ((b - 1) * arb(P).log())
    logS += fac * (2 * tail(1 + sa) + tail(2 * sa))
    S = logS.exp(); out[s] = S.upper().str(15, radius=False)
    print("s=%s S'(s) <= %s" % (s, out[s]), flush=True)
json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else "../out/sprime.json", "w"), indent=1)
