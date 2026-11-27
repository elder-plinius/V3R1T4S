#!/usr/bin/env python3
# famgen.py: independent regeneration of the family from a parameter file (no fam5).
# Usage: famgen.py IN.par OUT.json [BITS] [OUT.cfg]
# Formula: frame (0,0,1), (Px/2,0,m1). Segment (anch,c,off,hl,M,n,L; dy_l,w_l,phi_l):
#  sp=2hl/n, tau_i=hl(2i+1-n)/n, y_l=off+dy_l, mass=M w_l/(n sum w).
#  anch=0: t=c+tau_i+phi_l sp; atoms (+-t,+-y_l).
#  anch=1: t=tau_i+sgn(tau_i)phi_l sp, sgn(0)=+1; atoms (t,+-y_l).
import sys,json
def parse(path):
    T=[l.split() for l in open(path) if l.strip() and l[0]!='#']
    Px,Py,m1,K=float(T[0][0]),float(T[0][1]),float(T[0][2]),int(T[0][3]);i=1;S=[]
    for j in range(K):
        a,c,off,hl,M,n,L=T[i];i+=1;lv=[tuple(map(float,T[i+q])) for q in range(int(L))];i+=int(L)
        S.append(dict(anch=int(a),c=float(c),off=float(off),hl=float(hl),M=float(M),n=int(n),L=int(L),lv=lv))
    return Px,Py,m1,S
def atoms(Px,Py,m1,S):
    A=[(0.0,0.0,1.0),(Px/2,0.0,m1)]
    for f in S:
        n=f['n'];ws=sum(l[1] for l in f['lv']);sp=2*f['hl']/n;c=f['c'] if f['anch']==0 else 0.0
        for i in range(n):
            tau=f['hl']*(2*i+1-n)/n
            for dy,w,phi in f['lv']:
                y=f['off']+dy;m=f['M']*w/ws/n
                if f['anch']==0:
                    t=c+tau+phi*sp;A+=[(t,y,m),(t,-y,m),(-t,y,m),(-t,-y,m)]
                else:
                    t=tau+phi*sp if tau>=0 else tau-phi*sp;A+=[(t,y,m),(t,-y,m)]
    return A
def cert(Px,Py,A,bits):
    Sc=1<<bits;Lx,Ly=round(float('%.15g'%Px)*Sc),round(float('%.15g'%Py)*Sc);at={}
    for x,y,m in A:
        x,y,m=(float('%.15g'%v) for v in (x,y,m))
        k=(round(x*Sc)%Lx,round(y*Sc)%Ly);at[k]=at.get(k,0)+round(m*Sc)
    return dict(bits=bits,Lx=Lx,Ly=Ly,atoms=[[a,b,m] for (a,b),m in sorted(at.items())])
if __name__=='__main__':
    bits=int(sys.argv[3]) if len(sys.argv)>3 else 30
    Px,Py,m1,S=parse(sys.argv[1]);A=atoms(Px,Py,m1,S);c=cert(Px,Py,A,bits)
    json.dump(c,open(sys.argv[2],'w'))
    print(f"formula_atoms={len(A)} cert_atoms={len(c['atoms'])} merged={len(A)-len(c['atoms'])} mass={sum(a[2] for a in A):.10f} ceiling={Px*Py/sum(a[2] for a in A):.10f}")
