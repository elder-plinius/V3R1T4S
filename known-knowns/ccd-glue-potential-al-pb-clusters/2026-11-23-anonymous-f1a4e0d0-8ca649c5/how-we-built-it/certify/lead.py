"""Lim-Ong-Ercolessi Pb glue potential, transcribed piecewise from the archived lead.f (data/). numpy energy+gradient."""
import numpy as np
RRD,RRB,RRC,RHOD,RHOA=0.3471540742235355E+01,0.4909500000000000E+01,0.5503000000000000E+01,0.85,0.3
R1I,R2I,R3I,R1II,R2II,R3II,R2III,R3III=-0.38,0.245,-0.5166666666666667,-0.38,0.245,-0.1715828759323021,0.1308624193974091E+01,0.7699032959082642
DB,UB,DSW=12.0,-1.85,0.9081433382788202E+01
B0I,B1I,B2I,B3I,B4I=-0.1536837858573856E+01,-0.185,-0.1515954156009047E-01,-0.1478056600250295E-02,0.0
B2II,B3II,B4II,B2III,B3III=0.1526631307568407E-01,-0.1820707358322264E-01,-0.3714503267605675E-02,0.1526631307568407E-01,0.3239697893498678E-01
D,A,RC=0.3471540742235355E+01,0.4909500000000000E+01,0.423E+01
A0I,A1I,A2I,A3I,A4I=-0.03,0.0,0.1102661976296813,-0.8166666666666667,0.4072201316247714E-01
A0II,A1II,A2II,A3II,A4II,A5II,A6II=-0.03,0.0,0.1102661976296813,-0.8166666666666667,0.3439976422630956E+01,-0.5105760527431719E+01,0.2448028237231130E+01
def rh(r):
    f=np.zeros_like(r); d=np.zeros_like(r)
    m3=(r>=RRB)&(r<RRC); x=r[m3]-RRC; f[m3]=x*x*(R2III+x*R3III); d[m3]=x*(2*R2III+3*x*R3III)
    m2=(r>=RRD)&(r<RRB); x=r[m2]-RRD; f[m2]=RHOD+x*(R1II+x*(R2II+x*R3II)); d[m2]=R1II+x*(2*R2II+3*x*R3II)
    m1=r<RRD; x=r[m1]-RRD; f[m1]=RHOD+x*(R1I+x*(R2I+x*R3I)); d[m1]=R1I+x*(2*R2I+3*x*R3I)
    return f,d
def uu(n):
    f=np.empty_like(n); d=np.empty_like(n)
    m3=n>DB; x=n[m3]-DB; f[m3]=UB+x*x*(B2III+x*B3III); d[m3]=x*(2*B2III+3*x*B3III)
    m2=(n>DSW)&~m3; x=n[m2]-DB; f[m2]=UB+x*x*(B2II+x*(B3II+x*B4II)); d[m2]=x*(2*B2II+x*(3*B3II+4*x*B4II))
    m1=n<=DSW; x=n[m1]-DSW; f[m1]=B0I+x*(B1I+x*(B2I+x*(B3I+x*B4I))); d[m1]=B1I+x*(2*B2I+x*(3*B3I+4*x*B4I))
    return f,d
def v2(r):
    f=np.zeros_like(r); d=np.zeros_like(r)
    # region III (r >= A) is unreachable because RC < A
    m2=(r>=D)&(r<RC); x=r[m2]-D
    f[m2]=A0II+x*(A1II+x*(A2II+x*(A3II+x*(A4II+x*(A5II+x*A6II)))))
    d[m2]=A1II+x*(2*A2II+x*(3*A3II+x*(4*A4II+x*(5*A5II+6*x*A6II))))
    m1=r<D; x=r[m1]-D; f[m1]=A0I+x*(A1I+x*(A2I+x*(A3I+x*A4I))); d[m1]=A1I+x*(2*A2I+x*(3*A3I+4*x*A4I))
    return f,d
def eg(x):
    X=np.asarray(x,float).reshape(-1,3); n=len(X); i,j=np.triu_indices(n,1)
    dv=X[i]-X[j]; r=np.sqrt((dv*dv).sum(1))
    p,dp=v2(r); q,dq=rh(r); rho=np.bincount(i,q,n)+np.bincount(j,q,n)
    u,du=uu(rho); E=p.sum()+u.sum()
    W=(dp+(du[i]+du[j])*dq)/r; F=dv*W[:,None]; g=np.zeros_like(X)
    np.add.at(g,i,F); np.add.at(g,j,-F); return E,g.ravel()
