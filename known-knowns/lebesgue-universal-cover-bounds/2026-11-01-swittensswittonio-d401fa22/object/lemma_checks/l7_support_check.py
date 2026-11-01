# L7 numerical break attempt: derived support function hB vs brute force over arc+corner points; diameter; width; containment.
import numpy as np
from common import *
rng=np.random.default_rng(1)
for n in (3,5,7,9,11):
    P=boundary_points(n,0,(0,0),2000)
    th=rng.uniform(-10,10,200000)
    u=np.stack([np.cos(th),np.sin(th)],1)
    brute=(u@P.T).max(1)
    h=hB(n,th)
    w=h+hB(n,th+np.pi)
    # diameter of sampled boundary (extreme points live on boundary)
    from scipy.spatial.distance import pdist
    diam=pdist(P[::7]).max()
    # every boundary sample inside all unit discs about corners
    V=corners(n)
    inside=(np.sqrt(((P[:,None,:]-V[None])**2).sum(-1)).max(1)-1).max()
    print(f"n={n} max|h-brute|={np.abs(h-brute).max():.3e} width range [{w.min():.15f},{w.max():.15f}] diam(sample)={diam:.15f} max(dist to corner)-1={inside:.2e} R_n={Rn(n):.12f} max|h(th)-R_n|-excess={max(0,h.max()-Rn(n)):.2e}")
t3=(-0.012158832,-0.000000037);rho=1.256661190;t5=(0.022996607,-0.000003897)
print("A_inner",A_inner(t3,rho,t5),"A_outer",A_outer(t3,rho,t5,20000),A_outer(t3,rho,t5,200000))
