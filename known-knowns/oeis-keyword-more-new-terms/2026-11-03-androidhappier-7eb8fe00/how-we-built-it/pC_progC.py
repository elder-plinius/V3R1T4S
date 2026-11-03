# Program C: Matula-Goebel route. Enumerate all rooted trees with n nodes as MG numbers (A000081 counts), then test
# membership in A316494 by its comment rule: m in A316494 iff m=1, or m prime with primepi(m) in A316494, or the prime
# indices of m are distinct, pairwise coprime and all in A316494. Count by n. Usage: progC.py NMAX
import sys
from functools import lru_cache
from math import gcd
from sympy import prime, primepi, factorint
N=int(sys.argv[1])
trees={1:{1}}
def multisets(n, maxsize):  # multisets of trees (as MG numbers) with total size n, sizes <= maxsize, nonincreasing
    if n==0: yield 1; return
    for s in range(min(n,maxsize),0,-1):
        for t in trees[s]:
            for rest in multisets(n-s, s):
                yield prime(t)*rest
for n in range(2,N+1):
    # avoid duplicate multisets from same-size choices: use a set
    trees[n]=set(multisets(n-1,n-1))
@lru_cache(None)
def inA(m):
    if m==1: return True
    f=factorint(m)
    if any(e>1 for e in f.values()): return False
    idx=[int(primepi(p)) for p in f]
    if not all(inA(i) for i in idx): return False
    return all(gcd(a,b)==1 for i,a in enumerate(idx) for b in idx[i+1:])
for n in range(1,N+1):
    print(n, len(trees[n]), sum(1 for m in trees[n] if inA(m)), flush=True)
mg=sorted(m for n in trees for m in trees[n] if inA(m) and m<=330)
print("A316494 prefix:", ",".join(map(str,mg)))
