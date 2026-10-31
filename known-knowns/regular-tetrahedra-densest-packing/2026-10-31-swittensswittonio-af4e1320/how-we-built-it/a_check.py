"""NUMERICAL check of the closed-form wedge area a(r) (Gauss-Bonnet) against Monte-Carlo area of the wedge W*(r) = {n1.x>=h, n2.x>=h}, h=r sin(theta/2), on the unit sphere."""
import numpy as np, math
th=math.acos(1/3); s,c=math.sin(th/2),math.cos(th/2)
rng=np.random.default_rng(7)
N=4_000_000
P=rng.normal(size=(N,3)); P/=np.linalg.norm(P,axis=1)[:,None]
def a_formula(r):
    h2=r*r/3; h=r/math.sqrt(3)
    phi=math.acos((1/3+h2)/(1-h2)); psi=2*math.asin(math.sqrt(1-r*r)/math.sqrt(1-h2))
    return (2*phi-2*h*psi)/(4*math.pi)
def area_wedge(n1,d1,n2,d2): return np.mean((P@n1>=d1)&(P@n2>=d2))
print("r, closed form a(r), MC area of W*(r)")
for r in (0.1,0.3,0.6,0.8,0.9):
    h=r*s
    n1=np.array([s,0,-c]); n2=np.array([s,0,c])
    print(r,"%.5f"%a_formula(r),"%.5f"%area_wedge(n1,h,n2,h))
# (GEK Lemma 3.3 minimality of W*(r) is taken as KNOWN; a random-search check was started but not completed in the time limit and is not part of the proof)
