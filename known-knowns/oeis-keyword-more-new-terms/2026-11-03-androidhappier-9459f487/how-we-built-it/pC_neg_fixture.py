# negative fixture: nesting tested on ANY pairs (not consecutive) collapses into capturing; must NOT reproduce
# A326249 / A326335 DATA. Prints variant vs DATA for n=0..9.
import itertools
D249=[0,0,0,0,0,1,9,55,283,1324]; D335=[1,1,1,1,2,6,21,86,394,1974]; D336=[1,1,1,1,2,7,24,100,458,2279]
def parts(s):
    if not s: yield []; return
    f=s[0]
    for p in parts(s[1:]):
        for i in range(len(p)): yield p[:i]+[[f]+p[i]]+p[i+1:]
        yield [[f]]+p
def cap(A,B): return any(x<z<t<y or z<x<y<t for x,y in itertools.combinations(sorted(A),2) for z,t in itertools.combinations(sorted(B),2))
def conn(p,rel):
    if len(p)<=1: return True
    seen={0}; st=[0]
    while st:
        v=st.pop()
        for w in range(len(p)):
            if w not in seen and rel(p[v],p[w]): seen.add(w); st.append(w)
    return len(seen)==len(p)
v249=[];v335=[];v336=[]
for n in range(10):
    P=list(parts(list(range(1,n+1))))
    wrongnes=cap  # wrong: any pairs
    v249.append(sum(1 for p in P if any(cap(A,B) for A,B in itertools.combinations(p,2)) and not any(wrongnes(A,B) for A,B in itertools.combinations(p,2))))
    v335.append(sum(1 for p in P if conn(p,wrongnes)))
    # wrong for A326336: crossing edges instead of capturing
    cro=lambda A,B: any(x<z<y<t or z<x<t<y for x,y in itertools.combinations(sorted(A),2) for z,t in itertools.combinations(sorted(B),2))
    v336.append(sum(1 for p in P if conn(p,cro)))
print("A326249 variant (nesting=any pairs):",v249,"DATA",D249,"reproduces:",v249==D249)
print("A326335 variant (nesting=any pairs):",v335,"DATA",D335,"reproduces:",v335==D335)
print("A326336 variant (crossing edges)   :",v336,"DATA",D336,"reproduces:",v336==D336)
