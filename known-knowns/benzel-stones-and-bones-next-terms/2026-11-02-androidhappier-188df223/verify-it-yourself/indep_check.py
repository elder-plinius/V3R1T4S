"""Independent checker (no transfer matrix): region from Propp's complex-plane hexagon definition, tiles from
Euclidean adjacency, count by memoized exact-cover recursion on the full covered set. Also the stone-weight-3 sum.
Points p = u + v*w (w = e^{2 pi i/3}); |p|^2 = u^2 - u v + v^2; orientation sign of cross product is preserved."""
import sys
from functools import lru_cache
sys.setrecursionlimit(100000)
def region(a,b):
    # hexagon vertices: a w + b, -a w^2 - b, a w^2 + b w, -a - b w, a + b w^2, -a w - b w^2 ; w^2 = -1 - w
    def P(c1,cw): return (c1,cw)            # c1 + cw*w
    def W2(k): return (-k,-k)               # k w^2 = -k - k w
    def add(*ps): return (sum(p[0] for p in ps), sum(p[1] for p in ps))
    def neg(p): return (-p[0],-p[1])
    V=[add(P(0,a),P(b,0)), add(neg(W2(a)),P(-b,0)), add(W2(a),P(0,b)), add(P(-a,0),P(0,-b)), add(P(a,0),W2(b)), add(P(0,-a),neg(W2(b)))]
    def cross(o,p,q):  # in (u,v) coords; real cross = (sqrt3/2)*(du1*dv2 - du2*dv1)
        return (p[0]-o[0])*(q[1]-o[1])-(q[0]-o[0])*(p[1]-o[1])
    sgn=1 if cross(V[0],V[1],V[2])>0 else -1
    def inside(p):
        return all(sgn*cross(V[m],V[(m+1)%6],p)>=0 for m in range(6))
    corners=[(1,0),(-1,0),(0,1),(0,-1),(-1,-1),(1,1)]   # +-1, +-w, +-w^2 (w^2 = (-1,-1))
    cells=[]
    Rr=3*(a+b)+3
    for i in range(-Rr,Rr+1):
        for j in range(-Rr,Rr+1):
            k=1-i-j
            c=(i-k, j-k)   # i + j w + k w^2
            if all(inside((c[0]+d[0],c[1]+d[1])) for d in corners): cells.append(c)
    return cells
def n2(p): return p[0]*p[0]-p[0]*p[1]+p[1]*p[1]
def tiles_of(cells):
    S=set(cells); idx={c:x for x,c in enumerate(sorted(cells))}
    nbrs=[d for d in [(u,v) for u in range(-3,4) for v in range(-3,4)] if n2(d)==3]
    assert len(nbrs)==6
    T=set()
    for c in cells:
        for d in nbrs:
            t=[c,(c[0]+d[0],c[1]+d[1]),(c[0]+2*d[0],c[1]+2*d[1])]
            if all(x in S for x in t): T.add((tuple(sorted(idx[x] for x in t)),0))
        for d in nbrs:
            for e in nbrs:
                y=(c[0]+d[0],c[1]+d[1]); z=(c[0]+e[0],c[1]+e[1])
                if d<e and n2((y[0]-z[0],y[1]-z[1]))==3 and y in S and z in S:
                    T.add((tuple(sorted((idx[c],idx[y],idx[z]))),1))
    return len(cells),sorted(T)
def count(a,b,weight=1):
    nc,T=tiles_of(region(a,b))
    if nc%3: return 0
    first={}
    for t,st in T: first.setdefault(t[0],[]).append((sum(1<<x for x in t),st))
    full=(1<<nc)-1
    @lru_cache(maxsize=None)
    def f(mask):
        if mask==full: return 1
        x=(~mask & (mask+1)).bit_length()-1   # lowest uncovered cell
        tot=0
        for m,st in first.get(x,[]):
            if not mask & m: tot+=(weight if st else 1)*f(mask|m)
        return tot
    return f(0)
if __name__=="__main__":
    N=int(sys.argv[1]) if len(sys.argv)>1 else 8
    for n in range(int(sys.argv[2]) if len(sys.argv)>2 else 3,N+1):
        print("n",n,"A364416",count(n,2*n-4),"A364417",count(n,2*n-3),"A364418",count(n,2*n-4,3),"A364438",count(n,2*n-3,3),flush=True)
