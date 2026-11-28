# Third method for A214570 (small n): ordered trees as nested tuples generated recursively (no Dyck words),
# rooted-tree class = recursively sorted tuple; Counter of class sizes; max.  Negative fixture: drop the
# multiplicity division, i.e. max over rooted trees of prod deg! (overcounts identical siblings).
from collections import Counter
from functools import lru_cache
from math import factorial, prod
DATA=[1,1,1,2,3,4,6,12,24,40,60,120,240,420,840,1680]
@lru_cache(None)
def ordered(n):            # ordered trees with n vertices
    if n==1: return [()]
    return [ (t,)+f for s in range(1,n) for t in ordered(s) for f in forests(n-1-s) ]
@lru_cache(None)
def forests(m):
    if m==0: return [()]
    return [ (t,)+f for s in range(1,m+1) for t in ordered(s) for f in forests(m-s) ]
def canon(t): return tuple(sorted(canon(c) for c in t))
def degprod(t): return factorial(len(t))*prod(degprod(c) for c in t)
for n in range(1,13):
    C=Counter(canon(t) for t in ordered(n)); a=max(C.values())
    neg=max(degprod(t) for t in C)
    print(n,a,"DATA" if a==DATA[n-1] else "MISMATCH","| ordered",sum(C.values()),"| negative(no mult division)",neg,"differs" if neg!=DATA[n-1] else "same")
