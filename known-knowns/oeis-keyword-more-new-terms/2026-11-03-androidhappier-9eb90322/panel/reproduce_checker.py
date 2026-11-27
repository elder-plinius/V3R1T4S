# Independent checker: plane trees as nested tuples (tuple of child subtrees).
# D(T) = number of distinct sequences T_0..T_n (as trees), T_{i-1} = T_i minus a leaf.
# => D(T) = sum over DISTINCT trees T' obtainable by deleting one leaf of D(T').
import sys
from functools import lru_cache
from collections import Counter
def trees(n):
    # all plane trees with n edges: root's children forest
    @lru_cache(None)
    def forests(m):
        if m==0: return [()]
        out=[]
        for a in range(m):  # first child subtree has a edges (plus 1 edge to it)
            for t in forests(a):
                for rest in forests(m-1-a):
                    out.append((t,)+rest)
        return out
    return forests(n)
def deletions(t):
    res=set()
    for i,c in enumerate(t):
        if c==(): res.add(t[:i]+t[i+1:])
        else:
            for c2 in deletions(c): res.add(t[:i]+(c2,)+t[i+1:])
    return res
@lru_cache(None)
def D(t):
    if t==(): return 1
    return sum(D(s) for s in deletions(t))
cat=[1,1,2,5,14,42,132,429,1430]
for n in range(1,int(sys.argv[1])+1):
    ts=trees(n); assert len(ts)==cat[n]
    c=Counter(D(t) for t in ts); K=max(c)
    row=[c.get(k,0) for k in range(1,K+1)]
    print(n,sum(row),sum(k*v for k,v in c.items()),",".join(map(str,row)))
# %e checks (UDUUDD = (( ),(( ),)) ... glove: UD UUDD -> root child leaf, child with child)
def dyck(t): return "".join("U"+dyck(c)+"D" for c in t)
if len(sys.argv)>2:
    m={dyck(t):D(t) for t in trees(3)}; print("e:",m)
    # negative: leaf-labelled count (multiset of deletions) would break row 2
    def L(t):
        if t==(): return 1
        tot=0
        for i,c in enumerate(t):
            if c==(): tot+=L(t[:i]+t[i+1:])
            else:
                for c2 in deletions(c): pass
        return tot
    print("neg labelled UDUD:", L(((),())))
