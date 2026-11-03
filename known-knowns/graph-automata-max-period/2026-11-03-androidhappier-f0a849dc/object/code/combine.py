"""Program B, step 2: a(n) = max over integer partitions n = k1+...+kr and choices p_i in P(k_i) of lcm(p_i),
where P(k) is the set of Life cycle lengths achieved on CONNECTED graphs of order k (from lifeB output files).
A disjoint union evolves componentwise, so its cycle lengths are exactly the lcms of component cycle lengths."""
import sys, math, re, functools
d = sys.argv[1]; nmax = int(sys.argv[2])
P = {}
for k in range(1, nmax+1):
    txt = open(f"{d}/B_order{k}.txt").read()
    P[k] = set(map(int, re.search(r"periods:(.*)", txt).group(1).split()))
@functools.lru_cache(None)
def reach(n, maxpart):
    """set of cycle lengths achievable on graphs of order n whose components have order <= maxpart"""
    if n == 0: return frozenset([1])
    out = set()
    for k in range(1, min(n, maxpart)+1):
        for q in reach(n-k, k):
            for p in P[k]: out.add(math.lcm(p, q))
    return frozenset(out)
for n in range(1, nmax+1):
    R = reach(n, n)
    print(f"n={n} a(n)={max(R)} connected_max={max(P[n])} all_periods={sorted(R)}")
