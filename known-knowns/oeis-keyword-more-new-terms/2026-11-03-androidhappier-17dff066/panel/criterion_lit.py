# literal transcription of %t disjunsQ / ldrsi (criterion skeptic's own check)
import itertools,sys
from functools import lru_cache
def parts(n,m=None):
    if m is None: m=n
    if n==0: yield (); return
    for k in range(min(n,m),0,-1):
        for p in parts(n-k,k): yield (k,)+p
def disj(u):
    if len(u)==1: return True
    nl=[b for b in u if b!=()]
    if len(set(nl))!=len(nl): return False
    for a in u:
        for b in u:
            if not (a==b or not (set(a)&set(b))): return False
    return True
@lru_cache(None)
def ld(n):
    if n==1: return ((),)
    out=[]
    for c in parts(n-1):
        s=set(tuple(sorted(t)) for t in itertools.product(*[ld(k) for k in c]))
        out+= [t for t in s if disj(t)]
    return tuple(out)
N=int(sys.argv[1])
print([len(ld(n)) for n in range(1,N+1)])
