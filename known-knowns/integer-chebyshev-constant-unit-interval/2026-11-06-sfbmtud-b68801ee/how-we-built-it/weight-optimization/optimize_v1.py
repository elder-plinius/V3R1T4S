#!/usr/bin/env python3
"""Heuristic semi-infinite LP search; never a rigorous certificate checker."""
import argparse, hashlib, json, math, resource, time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog, brentq
from flint import ctx, fmpz_poly, arb, arb_poly

def write(path, value):
    p = Path(path); tmp = p.with_suffix(p.suffix+'.tmp')
    tmp.write_text(json.dumps(value, indent=2)+'\n'); tmp.replace(p)

class Library:
    def __init__(self, factors):
        self.factors=factors; self.deg=np.array([f['degw'] for f in factors],float)
        self.roots=[]; self.groups=[]; self.loglead=[]; self.nonreal=0
        for j,f in enumerate(factors):
            q=fmpz_poly(list(reversed(f['coeffs_desc_w'])))
            roots=q.complex_roots()
            assert sum(m for _,m in roots)==f['degw']
            self.loglead.append(math.log(abs(f['coeffs_desc_w'][0])))
            for z,m in roots:
                im=float(z.imag); re=float(z.real)
                self.nonreal += int(not z.imag.contains(0))*m
                for _ in range(m): self.roots.append(complex(re,im)); self.groups.append(j)
        self.roots=np.array(self.roots); self.groups=np.array(self.groups,dtype=int)
        self.loglead=np.array(self.loglead)

    def features(self, points):
        out=np.empty((len(points),len(self.factors)))
        for start in range(0,len(points),512):
            p=np.asarray(points[start:start+512])
            logs=np.log(np.maximum(np.abs(p[:,None]-self.roots[None,:]),1e-300))
            for j in range(len(self.factors)):
                out[start:start+len(p),j]=(self.loglead[j]+logs[:,self.groups==j].sum(axis=1))/self.deg[j]
        return out

    def extrema(self, weights):
        c=weights/self.deg; rw=c[self.groups]; active=rw>0
        rr=self.roots[active]; ww=rw[active]; constant=float(c @ self.loglead)
        def value(x):return constant+float(ww @ np.log(np.maximum(np.abs(x-rr),1e-300)))
        def derivative(x):return float(np.sum((ww/(x-rr)).real))
        points=[0.,.25]
        cuts=sorted(set([0.,.25]+[float(z.real) for z in rr if abs(z.imag)<1e-35 and 0<z.real<.25]))
        for a,b in zip(cuts,cuts[1:]):
            lo=max(np.nextafter(a,b),a+(b-a)*1e-10)
            hi=min(np.nextafter(b,a),b-(b-a)*1e-10)
            if not lo<hi:continue
            dl,dh=derivative(lo),derivative(hi)
            if dl>0 and dh<0:
                try:points.append(brentq(derivative,lo,hi,xtol=5e-324,rtol=1e-14,maxiter=200))
                except (ValueError,RuntimeError):points.append((a+b)/2)
            else:points.append(lo if dl<=0 else hi)
        vals=np.array([value(x) for x in points])
        order=np.argsort(vals)[::-1]
        return np.array(points), vals, [(float(points[i]),float(vals[i])) for i in order[:10]]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('certificate');ap.add_argument('output')
    ap.add_argument('--iterations',type=int,default=10);ap.add_argument('--seconds',type=float,default=540)
    ap.add_argument('--extra-factors');ap.add_argument('--degree-scale',type=int,default=10**15)
    args=ap.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    begin=time.monotonic();ctx.prec=256
    source=Path(args.certificate);cert=json.loads(source.read_text());factors=cert['factors'].copy()
    if args.extra_factors:
        extra=json.loads(Path(args.extra_factors).read_text())['candidates']
        existing={tuple(f['coeffs_desc_w']) for f in factors}
        for x in extra:
            coeff=x['coeffs_desc_w']
            if tuple(coeff) not in existing:
                factors.append({'e':0,'degw':len(coeff)-1,'coeffs_desc_w':coeff});existing.add(tuple(coeff))
    lib=Library(factors)
    w=np.array([f['e']*f['degw']/cert['N_w_degree'] for f in factors]);assert abs(w.sum()-1)<1e-12
    checks=[]
    for num,den in [(1,11),(1,17),(5,23),(1,7),(0,1),(1,4)]:
        x=arb(num)/den
        for j,f in enumerate(factors):
            q=arb_poly(list(reversed(f['coeffs_desc_w'])));v=abs(q(x))
            if v>0:
                exact=float(v.log()/f['degw']);approx=lib.features([num/den])[0,j]
                checks.append(abs(exact-approx))
    points,vals,top=lib.extrema(w)
    baseline={'maximum_log_w_estimate':float(vals.max()),'normalized_norm_estimate':math.exp(float(vals.max())/2),'top_points':top}
    mesh=np.unique(np.concatenate([points,np.linspace(0,.25,2001)]));history=[]
    for iteration in range(args.iterations):
        if time.monotonic()-begin>args.seconds:break
        phi=lib.features(mesh);m=len(factors)
        A=np.column_stack([phi,-np.ones(len(mesh))])
        eq=np.zeros((1,m+1));eq[0,:m]=1
        obj=np.zeros(m+1);obj[-1]=1
        sol=linprog(obj,A_ub=A,b_ub=np.zeros(len(mesh)),A_eq=eq,b_eq=[1.],bounds=[(0,None)]*m+[(None,None)],method='highs',options={'time_limit':30,'dual_feasibility_tolerance':1e-10,'primal_feasibility_tolerance':1e-10})
        if not sol.success:
            write(out/'failure.json',{'message':sol.message,'iteration':iteration});break
        w=sol.x[:m];points,vals,top=lib.extrema(w);duals=-sol.ineqlin.marginals;active=duals>1e-12
        dual={'kind':'HEURISTIC sampled-LP dual, not exact proof','support_w':[format(x,'.17g') for x in mesh[active]],'masses':[format(x,'.17g') for x in duals[active]],'objective_log_w':format(sol.fun,'.17g'),'source':'independent HiGHS exchange LP','factor_sha256':hashlib.sha256(json.dumps(factors,sort_keys=True).encode()).hexdigest()}
        write(out/'dual_measure.json',dual)
        exponents=[max(0,int(round(args.degree_scale*w[j]/f['degw']))) for j,f in enumerate(factors)]
        degree=sum(e*f['degw'] for e,f in zip(exponents,factors))
        proposed=[dict(f,e=e) for f,e in zip(factors,exponents) if e]
        candidate={'problem':'candidate upper bound, NOT YET RIGOROUSLY CERTIFIED','variable':'w=x(1-x)','N_w_degree':degree,'x_degree':2*degree,'n_factors':len(proposed),'factors':proposed,'source_certificate_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'iteration':iteration}
        write(out/'candidate.json',candidate)
        rounded=np.array([e*f['degw']/degree for e,f in zip(exponents,factors)])
        _,rv,rtop=lib.extrema(rounded)
        row={'iteration':iteration,'sample_count':len(mesh),'lp_log_w':float(sol.fun),'continuous_log_w_estimate':float(vals.max()),'exchange_gap_estimate':float(vals.max()-sol.fun),'rounded_norm_estimate':math.exp(float(rv.max())/2),'active_factors':sum(e>0 for e in exponents),'top_points':rtop,'elapsed_seconds':time.monotonic()-begin,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
        history.append(row);print(json.dumps(row),flush=True)
        write(out/'checkpoint.json',{'baseline':baseline,'feature_max_error':max(checks),'nonreal_roots':lib.nonreal,'history':history})
        mesh=np.unique(np.concatenate([mesh,points]))
    write(out/'summary.json',{'classification':'HEURISTIC','baseline':baseline,'feature_max_error':max(checks),'nonreal_roots':lib.nonreal,'history':history,'elapsed_seconds':time.monotonic()-begin,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})

if __name__=='__main__':main()
