import sys,os,numpy as np; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from lj_lib import *
X=load(sys.argv[1]); n=len(X)
def H_full(X):
    d=X[:,None,:]-X[None,:,:]; r2=(d**2).sum(-1); np.fill_diagonal(r2,1.0)
    a=(-48*r2**-7+24*r2**-4); b=(672*r2**-8-192*r2**-5); I=np.eye(3)
    blk=-(a[:,:,None,None]*I+b[:,:,None,None]*d[:,:,:,None]*d[:,:,None,:])
    for i in range(n): blk[i,i]=0
    H=blk.transpose(0,2,1,3).reshape(3*n,3*n).copy()
    for i in range(n): H[3*i:3*i+3,3*i:3*i+3]=-blk[i].sum(0)
    return H
for k in range(4):
    E,g=eg(X); w,V=np.linalg.eigh(H_full(X)); m=w>1e-6
    Vm=V[:,m]; dx=np.dot(Vm, np.dot(Vm.T, g.ravel())/w[m])*-1; X=X+dx.reshape(n,3)
    E2,g2=eg(X); print("newton %d E=%.12f grad=%.3e"%(k,E2,np.linalg.norm(g2)))
w=np.linalg.eigvalsh(H_full(X)); print("n_neg=%d n_zero=%d min_pos=%.6f"%((w<-1e-6).sum(),(abs(w)<1e-6).sum(),w[w>1e-6].min()))
np.savetxt(sys.argv[2],X,fmt='%.20e'); print("E_mp30=",energy_mp(X))
