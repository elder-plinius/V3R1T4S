"""GEK Lemma 3.1 proof step: 'translate a face through the centre; the edge distance does not grow'.  Test numerically.
Wedge {n1.x<=s1}∩{n2.x<=s2}, n1.n2=-cos(theta), c=0 not interior (s1<=0).  Edge = line P1∩P2.  Translating P1 to P1'={n1.x=0}
gives edge' = P1'∩P2.  Compare distance from 0 to the two lines (exact formula)."""
import numpy as np, math
th=math.acos(1/3)
def edge_dist(n1,s1,n2,s2):
    d=np.cross(n1,n2); d/=np.linalg.norm(d)
    # closest point on line to origin: solve n1.x=s1, n2.x=s2, d.x=0
    M=np.array([n1,n2,d]); x=np.linalg.solve(M,[s1,s2,0]); return np.linalg.norm(x)
n1=np.array([1.0,0,0]); n2=np.array([-math.cos(th),math.sin(th),0])
worst=(0,None)
for s1 in np.linspace(-0.9,0,91):
    for s2 in np.linspace(-0.9,0.9,181):
        e=edge_dist(n1,s1,n2,s2); e2=edge_dist(n1,0.0,n2,s2)     # translate plane 1 through the centre
        if e2-e>worst[0]: worst=(e2-e,(s1,s2,e,e2))
print("max over grid of  e' - e :",worst[0],"at (s1,s2,e,e')=",worst[1])
s1,s2,e,e2=worst[1]; print("ratio e'/e =",e2/e,"  1/sin(theta)=",1/math.sin(th))
# the slab thickness |s2| <= e always (plane 2 contains the edge)
bad=0
for s1 in np.linspace(-0.9,0,31):
    for s2 in np.linspace(-0.9,0.9,61):
        if abs(s2)>edge_dist(n1,s1,n2,s2)+1e-12: bad+=1
print("violations of |s2|<=e:",bad)
