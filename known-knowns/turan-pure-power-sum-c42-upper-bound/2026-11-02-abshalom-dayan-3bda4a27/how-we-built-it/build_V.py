#!/usr/bin/env python3
"""Builds the table V for the verification theorem (float; nothing here is trusted, check_hjb.py checks the table)."""
import numpy as np, sys, json, time, signal
signal.alarm(580)
out,T,b,nt,kap,gam,sig=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),int(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6]),float(sys.argv[7])
P=dict(T=T,b=b,beta_im=-0.85,gamma_re=0.5,gamma_im=0.866,L0=5.0,L1=10.0,al=1.2,L=8.0,nt=nt)
beta=P['beta_im']*1j;gam_c=P['gamma_re']+1j*P['gamma_im'];L=P['L']
d=L/nt;tau=-L+d*np.arange(nt+1);nth=int(round(2*np.pi/(d*.5)));nth+=nth%2;dth=2*np.pi/nth;th=np.arange(nth)*dth
P['nth']=nth
rhos=np.linspace(2**-.5-b,2**-.5+b,3);npsi=192;psi=(np.arange(npsi)+.5)*2*np.pi/npsi
R=np.repeat(rhos,npsi);w=R-T*np.exp(1j*np.tile(psi,3));W=np.abs(w);e=(W-R**2)**2/(2*R)
C=(gam_c*beta*np.exp(1j*th)).real
init=T+(T+2)*abs(beta)*np.exp(-L)+1e-6
U=np.zeros((nt+1,nth));U[0]=init
idx0=(w.imag/R)*d/dth;J=np.arange(nth);t0=time.time()
for i in range(nt):
    x=np.exp(.5*(tau[i]+tau[i+1]))
    g=T*np.abs(w+beta*x*R)-P['L1']*x**P['al']*e+kap*x**gam;ga=2*R*x
    best=np.full(nth,-1e9)
    for s in range(0,len(w),144):
        sl=slice(s,s+144)
        idx=J[None,:]-idx0[sl][:,None];f=np.floor(idx).astype(int);fr=idx-f
        Uo=U[i][f%nth]*(1-fr)+U[i][(f+1)%nth]*fr
        best=np.maximum(best,((g[sl][:,None]-ga[sl][:,None]*C[None,:])*d+(1-W[sl][:,None]*d)*Uo).max(0))
    U[i+1]=best
if sig>0:
    k=np.fft.rfftfreq(nth,1/nth)
    U=np.fft.irfft(np.fft.rfft(U,axis=1)*np.exp(-.5*(sig*k)**2),n=nth,axis=1)
U[0]=np.maximum(U[0],init)
np.save(out+'.npy',U);json.dump(P,open(out+'.json','w'))
print("built",out,"nth",nth,"V00",U[-1,0],"t",time.time()-t0)
