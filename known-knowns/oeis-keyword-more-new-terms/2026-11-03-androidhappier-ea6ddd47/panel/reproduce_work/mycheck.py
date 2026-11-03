# Independent checker for A214570. Two parts:
# (1) brute force from definition for n<=11: enumerate all ordered (plane) trees, canonicalize as rooted trees, count class sizes.
# (2) exhaustive enumeration of all rooted trees n<=17 (children multisets of earlier trees), c(t) computed
#     recursively as number of distinct orderings: multinomial(deg; mults) * prod c(child).
import sys
from math import factorial
from collections import Counter
N=int(sys.argv[1]) if len(sys.argv)>1 else 17
# part 1
def plane(n):
    # ordered trees with n nodes as tuple of children (ordered)
    if n==1: return [()]
    res=[]
    def forests(m):
        if m==0: return [()]
        out=[]
        for k in range(1,m+1):
            for t in P[k]:
                for f in forests(m-k): out.append((t,)+f)
        return out
    return [f for f in forests(n-1)]
P={}
def canon(t): return tuple(sorted(canon(c) for c in t))
brute=[]
for n in range(1,12):
    P[n]=plane(n)
    cnt=Counter(canon(t) for t in P[n])
    brute.append(max(cnt.values()))
    print("brute",n,len(P[n]),len(cnt),max(cnt.values()),flush=True)
# part 2
trees={}  # size -> list of (c)
ids=[] # global list: (size, c)
bysize={}
for n in range(1,N+1):
    out=[]
    # enumerate multisets of child ids (global index nonincreasing) with sizes summing n-1
    def rec(rem, maxid, cnts, prodc):
        if rem==0:
            deg=sum(cnts.values()); m=factorial(deg)
            for v in cnts.values(): m//=factorial(v)
            out.append(m*prodc); return
        for i in range(maxid,-1,-1):
            s,c=ids[i]
            if s<=rem:
                cnts[i]=cnts.get(i,0)+1
                rec(rem-s,i,cnts,prodc*c)
                cnts[i]-=1
                if cnts[i]==0: del cnts[i]
    rec(n-1,len(ids)-1,{},1)
    for c in out: ids.append((n,c))
    from math import comb
    cat=comb(2*(n-1),n-1)//n
    mx=max(out)
    print("enum",n,len(out),sum(out)==cat,mx,out.count(mx),flush=True)
