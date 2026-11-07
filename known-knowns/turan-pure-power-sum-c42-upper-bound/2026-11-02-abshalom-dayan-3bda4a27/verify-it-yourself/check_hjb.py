#!/usr/bin/env python3
"""Checks (HJB),(INIT),(TERM) of the verification theorem on a bilinear table V.
Lower bounds use corners of each cell, a chord bound in psi and rho, and explicit curvature bounds; pad covers float rounding.
Output: smallest certified G (over all cells), m (TERM margin). Exit 0 only if G>=kappa_req."""
import numpy as np, sys, json, time, signal
PAD=1e-10
def main():
    base=sys.argv[1];kappa_req=float(sys.argv[2]);lo=int(sys.argv[3]) if len(sys.argv)>3 else 0;hi=int(sys.argv[4]) if len(sys.argv)>4 else None
    P=json.load(open(base+'.json'));V=np.load(base+'.npy')
    T,b=P['T'],P['b'];beta=P['beta_im']*1j;gam=P['gamma_re']+1j*P['gamma_im'];L0,L1,al,L=P['L0'],P['L1'],P['al'],P['L'];nt,nth=P['nt'],P['nth']
    assert abs(gam)<=1 and V.shape==(nt+1,nth)
    d=L/nt;dth=2*np.pi/nth;tau=-L+d*np.arange(nt+1);th=np.arange(nth)*dth
    rlo=2**-.5-b;rhi=2**-.5+b;assert rlo>T
    # curvature constants on the band, valid for all psi (see REPRODUCE notes)
    Wpp=T*rhi/(rlo-T)                       # |W''| in psi
    u_max=rhi+T+rhi**2                      # |W-rho^2|
    epp=(T**2+u_max*Wpp)/rlo               # e'' in psi
    W_rr=1/(rlo-T)                          # |W_rho rho|
    up=1+2*rhi;upp=W_rr+2
    e_rr=(up**2+u_max*upp)/rlo+2*u_max*up/rlo**2+u_max**2/rlo**3
    e_max=u_max**2/(2*rlo)
    nr=int(P.get('nrho',9));rhos=np.linspace(rlo,rhi,nr);dr=(rhi-rlo)/(nr-1)
    C=(gam*beta*np.exp(1j*th)).real
    M0=64;DEPTH=6
    worst=np.inf;worst_at=None;t0=time.time();nref=0
    hi=nt if hi is None else hi
    for i in range(lo,hi):
        V0=V[i];V1=V[i+1];Vt=(V1-V0)/d
        Vp=[(np.roll(V[i+c],-1)-V[i+c])/dth for c in (0,1)]
        xhi=np.exp(tau[i+1])
        Eab=d**2/8*(rhi*xhi*abs(beta)*(T+2)+L1*al**2*xhi**al*e_max)+dth**2/8*(2*rhi*xhi*abs(beta))
        for c in (0,1):
            x=np.exp(tau[i+c]);p=L1*x**al;Vh=V[i+c]
            Er=dr**2/8*(p*e_r_r(e_rr)+2*T/rlo**3*np.abs(Vp[c]).max()+W_rr*np.abs(Vh).max())
            for sh in (0,1):
                Vtc=np.roll(Vt,-sh);Vhc=np.roll(Vh,-sh);Cc=np.roll(C,-sh)
                for rho in rhos:
                    a=rho*(1+beta*x)
                    fmin=abs(a)-T;assert fmin>0
                    Kc=np.abs(Vp[c])*T/rho+np.abs(Vhc)*Wpp+p*epp+T*(T*abs(a)/fmin)
                    A=Vtc+2*rho*x*Cc;B=-T*Vp[c]/rho;CC=Vhc
                    def Gfun(j,psi):
                        s=np.sin(psi);Wv=np.abs(rho-T*np.exp(1j*psi))
                        return A[j]+B[j]*s+CC[j]*Wv-T*np.abs(a-T*np.exp(1j*psi))+p*(Wv-rho*rho)**2/(2*rho)
                    M=M0;dl=2*np.pi/M;psi=np.arange(M+1)*dl
                    s=np.sin(psi);Wv=np.abs(rho-T*np.exp(1j*psi));b0=-T*np.abs(a-T*np.exp(1j*psi))+p*(Wv-rho*rho)**2/(2*rho)
                    G=A[:,None]+B[:,None]*s[None,:]+CC[:,None]*Wv[None,:]+b0[None,:]
                    cm=np.minimum(G[:,:-1],G[:,1:])
                    need=kappa_req+Eab+Er+PAD
                    lb=cm-Kc[:,None]*dl**2/8
                    jj,mm=np.nonzero(lb<need)
                    glob=(cm-Kc[:,None]*dl**2/8).min(1) if jj.size==0 else None
                    pl=psi[mm];depth=0;curw=dl;cellmin=lb.min(1)
                    # refine failing intervals by 4 repeatedly
                    fin=np.full(nth,np.inf);ok=np.ones(nth,bool);ok[np.unique(jj)]=False
                    if ok.any():
                        fin[ok]=lb[ok].min(1)
                    while jj.size and depth<DEPTH:
                        depth+=1;curw/=4;nref+=jj.size
                        j4=np.repeat(jj,4);pl4=(pl[:,None]+curw*np.arange(4)[None,:]).ravel()
                        g0=Gfun(j4,pl4);g1=Gfun(j4,pl4+curw)
                        l=np.minimum(g0,g1)-Kc[j4]*curw**2/8
                        keep=l<need
                        np.minimum.at(fin,j4[~keep],l[~keep])
                        jj,pl=j4[keep],pl4[keep]
                    if jj.size:
                        g=Gfun(jj,pl);l=np.minimum(g,Gfun(jj,pl+curw))-Kc[jj]*curw**2/8
                        np.minimum.at(fin,jj,l)
                    g=fin-Eab-Er-PAD
                    jw=int(g.argmin())
                    if g[jw]<worst: worst=float(g[jw]);worst_at=(i,c,sh,jw,float(rho))
        if (i-lo)%100==0: print(f"row {i} worst {worst:.6f} at {worst_at} refined {nref} t={time.time()-t0:.0f}",flush=True)
    print(f"HJB rows {lo}..{hi}: worst certified G = {worst:.8f} at {worst_at}, refined {nref}, t={time.time()-t0:.0f}",flush=True)
    # INIT
    init=T+(T+2)*abs(beta)*np.exp(-L)
    print("INIT slack",V[0].min()-init)
    # TERM on psi in [pi,2pi], rho grid
    best=np.inf;M=1<<16;dl=np.pi/M;psi=np.pi+np.arange(M+1)*dl
    Kt=T*abs(gam)+L0*epp;Er=dr**2/8*(L0*e_rr)
    for rho in rhos:
        Wv=np.abs(rho-T*np.exp(1j*psi))
        t=(gam*(T*np.exp(1j*psi)-beta*rho)).real+L0*(Wv-rho*rho)**2/(2*rho)
        best=min(best,np.minimum(t[:-1],t[1:]).min()-Kt*dl**2/8-Er-PAD)
    m=best-V[nt,0]
    C1=L0+L1/al;mu=max((T*T-r*r*(1-r*r))/(2*r) for r in rhos);mu=max(mu,(T*T-.25)/(2*rlo)+0)
    print(f"TERM min {best:.8f}, V(0,0) {V[nt,0]:.8f}, m={m:.8f}, C'={C1:.5f}, eta=m/C'={m/C1:.8f}, mu_max={mu:.8f}, mu*L={mu*L:.6f}, 2b={2*b}")
    print("Lip V_tau,V_phi",np.abs((V[1:]-V[:-1])/d).max(),np.abs((np.roll(V,-1,1)-V)/dth).max())
    print("PASS" if (worst>=kappa_req and V[0].min()>=init and m/C1>mu and mu*L<2*b) else "FAIL")
def e_r_r(x): return x
main()
