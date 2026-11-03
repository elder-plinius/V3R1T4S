# A325786 Program C: literal transcription of the OEIS Mathematica %t code.
import sys
def permutations(p):  # Mathematica Permutations: distinct permutations of a multiset
    p = sorted(p)
    def rec(rem):
        if not rem: yield (); return
        for i, x in enumerate(rem):
            if i and rem[i - 1] == x: continue
            for r in rec(rem[:i] + rem[i + 1:]): yield (x,) + r
    yield from rec(p)
def partitions(n, m=None):
    if m is None: m = n
    if n == 0: yield (); return
    for p in range(min(n, m), 0, -1):
        for r in partitions(n - p, p): yield (p,) + r
def rotate_right(q, r): r %= len(q); return q[-r:] + q[:-r] if r else q
def neckQ(q): return all(q <= rotate_right(q, r) for r in range(1, len(q)))   # OrderedQ[{q, rot}]
def subalt(q):
    k = len(q); out = set()
    for i in range(k):
        for j in range(i + 1, k + 1): out.add(q[i:j])                 # {___, s__, ___}
    for i in range(k):
        for j in range(i + 1, k + 1):                                 # {t___, __, u___} -> {u, t}
            v = q[j:] + q[:i]
            if v: out.add(v)
    return out
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for n in range(lo, hi + 1):
    comps = set()
    for p in partitions(n): comps |= set(permutations(p))
    c = sum(1 for q in comps if neckQ(q) and sorted(set(sum(s) for s in subalt(q))) == list(range(1, n + 1)))
    print(n, c, flush=True)
