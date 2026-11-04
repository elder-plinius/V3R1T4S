#!/usr/bin/env python
"""Own Arb verifier for near-branch certificates (Theorem 3.2 and (19) of Wikstrom 2608.17660, re-derived).
usage:
  arbverify.py integral CERT.json [--prec 128,256] [--min-gain G]
  arbverify.py points   CERT.json [--prec 128,256] [--min-margin M] [--table FILE]
Certificate rows are hex floats (rho,psi,gamma,lambda); doubles are read exactly."""
import sys,json,time
from flint import arb,ctx
def BK(K):
    out=[None]*(K+1)
    for k in range(1,K+1):
        out[k]=((arb(k+2)/k)**(arb(k)/2))*(arb(k+2)/2)
    return out
def parse(rows):
    R=[]
    for ro,ps,ga,la in rows:
        ro,ps,ga,la=[float.fromhex(v) for v in (ro,ps,ga,la)]
        if not (la>=0): raise ValueError('REJECT negative multiplier %r'%la)
        if not (0<=ro<1): raise ValueError('REJECT rho out of range %r'%ro)
        R.append((ro,ps,ga,la))
    return R
def multipliers(R,K):
    """q_k=sum lam_j (1-rho^2) rho^k cos(k psi-gamma), sumlam, T (lambda tail)."""
    q=[arb(0)]*(K+1); sl=arb(0); T=arb(0); e=arb(1).exp()
    for ro,ps,ga,la in R:
        A,PS,GA,L=arb(ro),arb(ps),arb(ga),arb(la)
        sl+=L; c=L*(1-A*A)
        pw=arb(1)
        for k in range(K+1):
            q[k]=q[k]+c*pw*((k*PS-GA).cos()); pw=pw*A
        # sum_{k>K}(k+2)rho^k = rho^(K+1) [ (K+3)/(1-rho) + rho/(1-rho)^2 ]; pw=rho^(K+1) now
        T+=c*pw*((K+3)/(1-A)+A/((1-A)*(1-A)))
    return q,sl,e/2*T
def lower(x):  # exact-enough lower end as arb -> float string
    return x.lower()
def integral(cert,prec):
    ctx.prec=prec
    K=cert['K']; r=arb(float.fromhex(cert['r'])); eta=arb(float.fromhex(cert['eta']))
    R=parse(cert['rows']); B=BK(K); q,sl,T=multipliers(R,K)
    d=[r**(k+1)/(k+1)+q[k] for k in range(K+1)]
    e=arb(1).exp()
    T0=e/2*arb(K+3)/(K+2)*r**(K+2)/(1-r)
    s=arb(0)
    for k in range(4,K+1): s+=B[k]*abs(d[k])
    a0=d[0]-sl-s-T-T0; a2=d[2]; a3=d[3]
    gain=a0-a2-arb(3).sqrt()/4
    slope=a2-2*eta*abs(a3)
    A=a2+eta*abs(a3)
    return dict(a0=a0,a2=a2,a3=a3,gain=gain,slope=slope,side_lhs=2*A,side_rhs=a0-A,T=T,T0=T0,sumB=s,sl=sl,
                nrows=len(R),maxrho=max(x[0] for x in R),d=d)
def points(cert,prec,table=None):
    ctx.prec=prec
    K=cert['K']; eta=arb(float.fromhex(cert['eta'])); B=BK(K); e=arb(1).exp()
    nodes=[float.fromhex(v) for v in cert['nodes']]; sub=cert['subdiv']
    certs=[multipliers(parse(rw),K) for rw in cert['certs']]
    r0=1/arb(3).sqrt()
    import math
    lo0=math.nextafter(nodes[0],0)
    if not (arb(lo0)<r0): raise ValueError('REJECT first node does not start below r0')
    if not (nodes[-1]==float.fromhex(cert['r1'])): raise ValueError('REJECT last node is not r1')
    for a,b in zip(nodes,nodes[1:]):
        if not a<b: raise ValueError('REJECT nodes not increasing')
    minv=None; rowsout=[]
    def powers(x):
        P=[arb(1)]*(K+1); A=arb(x)
        for k in range(1,K+1): P[k]=P[k-1]*A
        return P
    def ev(q,sl,T,hi,pl,ph):
        AHI=arb(hi)
        tail0=e/2*AHI**(K+1)*((K+3)/(1-AHI)+AHI/((1-AHI)*(1-AHI)))
        s=arb(0)
        for k in range(4,K+1): s+=B[k]*abs(pl[k].union(ph[k])+q[k])
        return (1+q[0])-sl-s-T-tail0-a2box*abs(pl[2].union(ph[2])+q[2])-eta*abs(pl[3].union(ph[3])+q[3])
    a2box=arb(float.fromhex(cert['a2box'])) if 'a2box' in cert else arb(1)
    target=cert.get('bisect_target')
    if target is not None: target=arb(target)
    def leaf(j,lo,hi,Pl,Ph,depth):
        nonlocal minv
        v1=ev(*certs[j],hi,Pl,Ph); v2=ev(*certs[j+1],hi,Pl,Ph)
        lb=v1 if v1.lower()>v2.lower() else v2
        if target is not None and not (lb.lower()>target) and depth<24:
            mid=lo+(hi-lo)/2
            if not lo<mid<hi: raise ValueError('REJECT cannot bisect')
            Pm=powers(mid); leaf(j,lo,mid,Pl,Pm,depth+1); leaf(j,mid,hi,Pm,Ph,depth+1); return
        if minv is None or lb.lower()<minv.lower(): minv=lb
        rowsout.append((lo.hex(),hi.hex(),lb.lower().str(16,radius=False)))
    for j in range(len(nodes)-1):
        a,b=nodes[j],nodes[j+1]
        A=lo0 if j==0 else a
        ends=[A+(b-A)*i/sub for i in range(sub)]+[b]
        for i in range(1,len(ends)):
            if not ends[i-1]<ends[i]: raise ValueError('REJECT subinterval order')
        P=[powers(x) for x in ends]
        for i in range(sub): leaf(j,ends[i],ends[i+1],P[i],P[i+1],0)
    if table:
        with open(table,'w') as f:
            f.write('# lo hi certified_lower_bound_of_f(prec=%d) (adjacent rows share endpoints: cover check in main)\n'%prec)
            for t in rowsout: f.write(' '.join(t)+'\n')
    # cover check: leaves consecutive from below r0 to r1
    for u,w in zip(rowsout,rowsout[1:]):
        if u[1]!=w[0]: raise ValueError('REJECT gap in subintervals')
    if float.fromhex(rowsout[0][0])!=lo0 or float.fromhex(rowsout[-1][1])!=nodes[-1]: raise ValueError('REJECT cover ends')
    return dict(margin=minv,nsub=len(rowsout),nodes=len(nodes))
def main():
    a=sys.argv[1:]; mode=a[0]; cert=json.load(open(a[1]))
    precs=[128,256]; ming=None; table=None
    if '--prec' in a: precs=[int(x) for x in a[a.index('--prec')+1].split(',')]
    if '--min' in a: ming=a[a.index('--min')+1]
    if '--table' in a: table=a[a.index('--table')+1]
    ok=True; res=[]
    try:
        for p in precs:
            t=time.time()
            if mode=='integral':
                v=integral(cert,p); res.append(v)
                print('prec',p,'rows',v['nrows'],'maxrho',v['maxrho'],'K',cert['K'])
                for n in 'a0 a2 a3 sumB T T0 sl'.split(): print('  ',n,v[n].str(25))
                print('   gain   ',v['gain'].str(25)); print('   slope a2-2eta|a3|',v['slope'].str(20))
                print('   side 2A',v['side_lhs'].str(12),' a0-A',v['side_rhs'].str(12))
                good=v['slope']>0 and v['side_lhs']<v['side_rhs']
                if ming is not None: good=good and v['gain']>arb(ming)
                ok=ok and bool(good)
            else:
                v=points(cert,p,table if p==precs[-1] else None); res.append(v)
                print('prec',p,'nsub',v['nsub'],'nodes',v['nodes'],'margin_lower',v['margin'].lower().str(18,radius=False))
                good=v['margin'].lower()>(arb(ming) if ming is not None else arb(0))
                ok=ok and bool(good)
            print('   elapsed',round(time.time()-t,2))
        if len(res)==2:
            key='gain' if mode=='integral' else 'margin'
            if mode=='integral' and not res[0][key].overlaps(res[1][key]): ok=False; print('precisions disagree')
    except ValueError as e:
        print(e); ok=False
    print('VERDICT','PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
if __name__=='__main__': main()
