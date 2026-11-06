# Program A (A155520): backward DP on Dyck words.  A leaf of an ordered tree = a "UD" factor of its
# Dyck word; deleting it removes that factor.  D(*) = 1;  D(T) = sum over the DISTINCT words T'
# obtained by deleting one UD factor of D(T').  Row n = histogram of D over all Dyck words of
# semilength n, listed k = 1..max (zeros kept).  usage: python3 progA.py NMAX
import sys
from functools import lru_cache
from collections import Counter
@lru_cache(None)
def D(w):
    if w == "": return 1
    return sum(D(t) for t in {w[:i] + w[i+2:] for i in range(len(w) - 1) if w[i:i+2] == "UD"})
def dyck(n):
    out = []
    def g(s, o, c):
        if o == n and c == n: out.append(s); return
        if o < n: g(s + "U", o + 1, c)
        if c < o: g(s + "D", o, c + 1)
    g("", 0, 0); return out
for n in range(1, int(sys.argv[1]) + 1):
    C = Counter(D(w) for w in dyck(n)); m = max(C)
    row = [C.get(k, 0) for k in range(1, m + 1)]
    print(n, "sum=%d" % sum(row), "wsum=%d" % sum(k * c for k, c in C.items()), "row:", ",".join(map(str, row)), flush=True)
