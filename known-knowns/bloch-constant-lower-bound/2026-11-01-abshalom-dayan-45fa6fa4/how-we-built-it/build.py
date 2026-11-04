"""build.py base eta r1 m : point certificates (adaptive nodes, target margin m) and integral cert at r1. Search only."""
import sys,numpy as np,time,math,json
base=sys.argv[1];sys.path.insert(0,base+'/code')
from cp import *
K=int(sys.argv[5]) if len(sys.argv)>5 else 320; rmax=.97
eta=float(sys.argv[2]);r1=float(sys.argv[3]);m=float(sys.argv[4])
r0=1/3**.5
# data/wikstrom_src (not shipped): from doi:10.5281/zenodo.21975862
z=np.load(base+'/../../data/wikstrom_src/variable_radius_certificate.npz',allow_pickle=False)
state=[z['rho'],z['psi'],z['point_gams'][16]]
B=Bk(K)
def e_fn(x,lamrow):
    rho,psi,gam,lam,q,tl=lamrow
    k=np.arange(K+1); w=x**k; d=w+q
    tail0=math.e/2*x**(K+1)*((K+3)/(1-x)+x/(1-x)**2)
    return d[0]-lam.sum()-(B[4:]*abs(d[4:])).sum()-tl-tail0-abs(d[2])-eta*abs(d[3])
def cert_at(x,rounds=9):
    global state
    w,P=point_problem(x,K,eta)
    best,h=loop(P,*state,K,rmax,rounds=rounds,evalf=evalf_pt(w,K,eta),verbose=False)
    val,rh,pp,gg,lam,a=best
    k=lam>1e-12; rh,pp,gg,lam=rh[k],pp[k],gg[k],lam[k]
    state=[rh,pp,gg]
    q=lam@rowmat(rh,pp,gg,K)
    tl=math.e/2*np.sum(lam*(1-rh**2)*rh**(K+1)*((K+3)/(1-rh)+rh/(1-rh)**2))
    return (rh,pp,gg,lam,q,tl),val
t0=time.time()
c,v=cert_at(r1,rounds=16); print('r1 val',v,flush=True)
nodes=[r1];certs=[c]
x=r1
while x>r0:
    # find y<x with e(y)>=m via scan
    lo=x;step=1e-6
    while lo-step>r0-1e-5 and e_fn(lo-step,c)>=1.5*m:
        lo-=step; step*=1.15
    y=lo
    xn=max(math.nextafter(r0,1) if False else r0, y-(x-y)*.9)
    while True:
        cn,vn=cert_at(xn,rounds=6)
        ok=e_fn(y,cn)>=1.5*m
        if ok: break
        xn=y-(y-xn)*.6
    nodes.append(xn);certs.append(cn);c=cn;
    print('node',xn,'val',vn,'n rows',len(cn[0]),'t',round(time.time()-t0),flush=True)
    x=xn
    if x<=r0: break
# ensure first node is exactly double nearest r0 from below/at; verifier starts just under nodes[0]
nodes=nodes[::-1];certs=certs[::-1]
def rows(c): 
    return [[float(a).hex(),float(b).hex(),float(g).hex(),float(l).hex()] for a,b,g,l in zip(c[0],c[1],c[2],c[3])]
tag='eta%g_r%.5f'%(eta,r1)
json.dump({'kind':'points','K':K,'eta':eta.hex(),'r1':r1.hex(),'nodes':[float(n).hex() for n in nodes],'subdiv':1,'bisect_target':m,
  'certs':[rows(c) for c in certs]},open(base+'/certs/pts_%s.json'%tag,'w'))
# integral
w,P=integral_problem(r1,K)
s=np.load(base+'/certs/t2.npz',allow_pickle=False)
best,h=loop(P,s['rho'],s['psi'],s['gam'],K,rmax,rounds=22,evalf=evalf_int(w,K),verbose=False)
val,rh,pp,gg,lam,a=best
lam=np.where(lam>1e-13,lam,0.0)
save_cert(base+'/certs/int_%s.json'%tag,'integral',K,r1,eta,rh,pp,gg,lam)
print('integral float',val,'obj',h[-1][1]-sq,'nodes',len(nodes),'nnz',(lam>0).sum(),'t',round(time.time()-t0),flush=True)
