# Independent checker: enumerate rooted ordered (plane) trees with n non-root vertices
# as parent arrays; count increasing labelings by brute force over all n! labelings.
import itertools, sys
def plane_trees(n):
    # ordered forest of n nodes -> list of trees as nested tuples
    if n==0: yield (); return
    for k in range(n):  # first tree has k+1 nodes (root + k descendants)
        for sub in plane_trees(k):
            for rest in plane_trees(n-1-k):
                yield ((sub,),)+rest if False else ((sub),)+rest
def parents(forest):
    par=[]
    def walk(f,p):
        for ch in f:
            i=len(par); par.append(p); walk(ch,i)
    walk(forest,-1); return par   # -1 = root
def count(par):
    n=len(par); c=0
    for perm in itertools.permutations(range(1,n+1)):
        if all(par[i]<0 or perm[par[i]]<perm[i] for i in range(n)): c+=1
    return c
N=int(sys.argv[1]) if len(sys.argv)>1 else 6
seq=[]
for n in range(N+1):
    row=sorted((count(parents(f)) for f in plane_trees(n)),reverse=True)
    print(n,len(row),sum(row),file=sys.stderr); seq+=row
print(",".join(map(str,seq)))
