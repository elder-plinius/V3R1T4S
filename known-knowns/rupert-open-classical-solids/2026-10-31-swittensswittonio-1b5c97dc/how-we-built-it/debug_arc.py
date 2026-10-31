import itertools, numpy as np
from fractions import Fraction as F
h=F(1,2)
one=(F(1),F(0)); phi=(h,h); phi2=(3*h,h); phi3=(F(2),F(1)); two_phi=(F(1),F(1)); twoplus=(5*h,h); zero=(F(0),F(0))
neg=lambda x:(-x[0],-x[1])
fams=[(one,one,phi3),(phi2,phi,two_phi),(twoplus,zero,phi2)]
allv=set()
for f in fams:
    for p in [f,(f[1],f[2],f[0]),(f[2],f[0],f[1])]:
        for s in itertools.product((1,-1),repeat=3):
            allv.add(tuple(c if si>0 else neg(c) for c,si in zip(p,s)))
V=sorted(allv)
S5=5**.5
Vf=np.array([[float(c[0])+float(c[1])*S5 for c in v] for v in V])
def Rot(r):
    r=np.array(r); rr=r.dot(r)
    K=np.array([[0,-r[2],r[1]],[r[2],0,-r[0]],[-r[1],r[0],0]])
    return ((1-rr)*np.eye(3)+2*np.outer(r,r)+2*K)/(1+rr)
a1=(-5+3*S5)/10; a3=(-5+S5)/10
for sigma in (1,-1):
    rA=sigma*np.array([a1,0,a3])
    R=Rot(rA)
    n1=-655/128-131/128*S5; n2=87/64+5/2*S5
    e=0.1; u=(1-2*e,0,2+e)
    n=np.array([u[2]*n1,u[2]*n2,-u[0]*n1-u[1]*n2])
    print('sigma',sigma)
    for a in range(60):
        for b in range(60):
            if abs(n@(R@Vf[a]-Vf[b]))<1e-9: print(' plug',a,'hole',b)
