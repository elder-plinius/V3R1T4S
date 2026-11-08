# Program C (Python): literal transcription of the Mathematica patterns of A326245/6/9, A326335/6.
# croXQ: blocks {..x..y..},{..z..t..} with x<z<y<t or z<x<t<y; capXQ: x<z<t<y or z<x<y<t;
# nesXQ: same as capXQ but x,y consecutive in their block and z,t consecutive in theirs.
# Connectivity of the block graph by repeated merging of components (like csm).
import sys, itertools
def parts(s):
    if not s: yield []; return
    f=s[0]
    for p in parts(s[1:]):
        for i in range(len(p)): yield p[:i]+[[f]+p[i]]+p[i+1:]
        yield [[f]]+p
def pairs(B, consecutive):
    B=sorted(B)
    return list(zip(B,B[1:])) if consecutive else list(itertools.combinations(B,2))
def rel(A,B,kind):
    if kind=='cro':
        return any(x<z<y<t or z<x<t<y for x,y in pairs(A,False) for z,t in pairs(B,False))
    cons = (kind=='nes')
    return any(x<z<t<y or z<x<y<t for x,y in pairs(A,cons) for z,t in pairs(B,cons))
def ncomp(p, kind):
    comps=[{i} for i in range(len(p))]
    changed=True
    while changed:
        changed=False
        for a,b in itertools.combinations(range(len(comps)),2):
            if any(rel(p[i],p[j],kind) for i in comps[a] for j in comps[b]):
                comps[a]|=comps[b]; del comps[b]; changed=True; break
    return len(comps)
lo,hi=int(sys.argv[1]),int(sys.argv[2])
print("n A326245 A326246 A326249 A326335 A326336",flush=True)
for n in range(lo,hi+1):
    c=[0]*5
    for p in parts(list(range(1,n+1))):
        pr=list(itertools.combinations(p,2))
        cro=any(rel(A,B,'cro') for A,B in pr); cap=any(rel(A,B,'cap') for A,B in pr); nes=any(rel(A,B,'nes') for A,B in pr)
        c[0]+= cro and not cap; c[1]+= cro and cap; c[2]+= cap and not nes
        c[3]+= ncomp(p,'nes')<=1; c[4]+= ncomp(p,'cap')<=1
    print(n,*c,flush=True)
