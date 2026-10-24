"""Direct occupied-slot polynomial, written from model.zpl (no evaluator imports)."""
from fractions import Fraction as F
from pathlib import Path
import gzip,json,sys,time

def rows(path):
    with gzip.open(path,'rt') if str(path).endswith('.gz') else open(path) as f:
        for s in f:
            a=s.split('#')[0].split()
            if a: yield a

def near(q):
    a,b=abs(q.numerator),q.denominator
    z=(2*a+b)//(2*b)
    return z if q>=0 else -z

def run(prices,covs,sol):
    t0=time.monotonic(); raw={(int(t),s):F(p) for t,s,p in rows(prices)}
    times=sorted({t for t,s in raw}); symbols=sorted({s for t,s in raw})
    assert times==list(range(10)) and len(symbols)==400 and len(raw)==4000
    p={(t,s):v*100000/raw[0,s] for (t,s),v in raw.items()}
    h={}; x={t:[] for t in times}; seen=set()
    for a in rows(sol):
        if len(a)==2:
            assert a[0] not in h; h[a[0]]=a[1]
        else:
            assert len(a)==4
            t,s,l,z=int(a[0]),a[1],int(a[2]),int(a[3]); assert (t,s) not in seen
            seen.add((t,s)); assert t in x and s in symbols and 0<=l<=3 and 0<=z<=3
            x[t] += [(s,m,1) for m in range(l)]+[(s,m,-1) for m in range(z)]
    assert h['instance']=='po_a400_t10_s00' and int(h['budget'])==100 and F(h['lambda'])==F(1,100)
    comps=dict(risk=0,returns=0,transactions=0,liquidation=0,short_cost=0,cash_interest=0)
    active={t:{s for s,m,sign in x[t]} for t in times}; cov={}; count=0
    for t,a,b,v in rows(covs):
        t=int(t); count+=1
        if a in active[t] and b in active[t]:
            assert (t,a,b) not in cov; cov[t,a,b]=F(v)
    assert count==1600000
    constraints=[]; monomials=0; ties=0
    def rr(q):
        nonlocal ties
        ties+=int((2*abs(q.numerator))% (2*q.denominator)==q.denominator)
        return near(q)
    for t in times:
        net=sum(sign for _,_,sign in x[t]); y=10-net; s2=100-len(x[t])
        assert 0<=y<=15 and 0<=s2<=127
        assert sum((1<<k)*((y>>k)&1) for k in range(4))+net==10
        assert sum((1<<k)*((s2>>k)&1) for k in range(7))+len(x[t])==100
        constraints.append([t,len(x[t]),net,y,s2])
        for a,m,sg in x[t]:
            for b,n,tau in x[t]:
                comps['risk']+=rr(F(1,100)*sg*tau*cov[t,a,b]*p[t,a]*p[t,b]); monomials+=1
            if sg==-1: comps['short_cost']+=rr(p[t,a]/40000)
        for k in range(4): comps['cash_interest']-=rr(F(10)*(1<<k))*((y>>k)&1)
    for t in range(1,9):
        for a,m,sg in x[t]: comps['returns']-=rr(sg*(p[t+1,a]-p[t,a]))
        # Literal x_prev+x-2*x_prev*x, without an absolute-count formula.
        prev=set(x[t-1]); now=set(x[t])
        for a,m,sg in prev|now:
            u=int((a,m,sg) in prev); v=int((a,m,sg) in now)
            comps['transactions']+=rr(p[t,a]/1000)*(u+v-2*u*v)
    for a,m,sg in x[0]:
        comps['returns']-=rr(sg*(p[1,a]-p[0,a])); comps['transactions']+=rr(p[0,a]/1000)
    for a,m,sg in x[9]: comps['liquidation']+=rr(p[9,a]/1000)
    total=sum(comps.values()); assert total==int(h['objective'])
    return dict(objective=total,components=comps,constraints=constraints,covariance_rows=count,occupied_risk_monomials=monomials,rounding_tie_uses=ties,seconds=time.monotonic()-t0)

if __name__=='__main__':
    print(json.dumps(run(*sys.argv[1:]),indent=2)); print('LITERAL_SLOT_CHECK: PASS')
