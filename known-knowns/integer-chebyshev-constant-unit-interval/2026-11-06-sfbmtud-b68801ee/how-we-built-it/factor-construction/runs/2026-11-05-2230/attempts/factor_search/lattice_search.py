"""Independent weighted-sample LLL search; all generated coefficients are exact."""
import json,math,time,resource,argparse,random,os,hashlib
from pathlib import Path
from flint import fmpz_poly,fmpz_mat
BASE=Path(__file__).resolve().parent
DATA=json.loads((BASE.parent.parent/'data/upper_certificate.json').read_text())
LIB=DATA['factors']; KNOWN={tuple(q['coeffs_desc_w']) for q in LIB}; DEN=DATA['N_w_degree']; ORIGINAL_KNOWN=set(KNOWN)
def eval_num(c,n,q):
    z=c[0]; dq=q
    for a in c[1:]:z=z*n+a*dq;dq*=q
    return z

def keypoly(p):
    c=list(map(int,p.coeffs()))
    if c[-1]<0:c=[-a for a in c]
    return tuple(c[::-1])

def create(N,mode,seed,drop=0,extra_nodes=None,max_residual=65,lll_delta=0.99,return_matrix=False,node_bits=18,node_jitter=2):
    rng=random.Random(seed); es=[int(N*f['e']//DEN) for f in LIB]
    # Removing some prescribed factors explores nonintegral rounding choices.
    for _ in range(drop):
        opts=[i for i,e in enumerate(es) if e and LIB[i]['degw']<=7]
        if opts:es[rng.choice(opts)]-=1
    k=sum(e*f['degw'] for e,f in zip(es,LIB));d=N-k
    if not 2<=d<=max_residual:return None
    q=2**node_bits; m=max(3*d+9,70)
    if mode=='cheb':ns=sorted(set(round(q*(1-math.cos(math.pi*(j+.5)/m))/8) for j in range(m)))
    elif mode=='random':ns=sorted(set(rng.randrange(1,q//4) for _ in range(m)))
    elif mode=='uniform':ns=[round(q*(j+.5)/(4*m)) for j in range(m)]
    else:raise ValueError(mode)
    if extra_nodes is not None:ns=sorted(set(ns+[min(q//4-1,max(1,round(q*x)+rng.randrange(-node_jitter,node_jitter+1))) for x in extra_nodes]))
    fixed=[f for e,f in zip(es,LIB) if e]
    fe=[e for e in es if e]
    nums=[math.prod(abs(eval_num(f['coeffs_desc_w'],n,q))**e for f,e in zip(fixed,fe)) for n in ns]
    mx=max(nums);scale=10**(2*d+20)
    rows=[]
    for j in range(d+1):
        ident=[0]*(d+1);ident[j]=1
        rows.append(ident+[(scale*z*n**j)//(mx*q**j) for z,n in zip(nums,ns)])
    st=time.perf_counter();L=fmpz_mat(rows).lll(delta=lll_delta);elapsed=time.perf_counter()-st
    polys=[]
    for i in range(L.nrows()):
        polys.append(fmpz_poly([L[i,j] for j in range(d+1)]))
    # Nearby lattice vectors: exact sums/differences of the shortest basis rows.
    for i in range(min(6,len(polys))):
        for j in range(i):
            polys.extend([polys[i]+polys[j],polys[i]-polys[j]])
    return (d,es,polys,elapsed,L) if return_matrix else (d,es,polys,elapsed)

def main():
    a=argparse.ArgumentParser();a.add_argument('--seconds',type=float,default=45);a.add_argument('--seed',type=int,default=1);a.add_argument('--out',default='pilot');a.add_argument('--max-degree',type=int,default=50);a.add_argument('--random-N',action='store_true');a.add_argument('--dual');a.add_argument('--certificate');a.add_argument('--max-total-degree',type=int,default=350);a.add_argument('--max-residual',type=int,default=65);a.add_argument('--lll-delta',type=float,default=0.99);a.add_argument('--node-bits',type=int,default=18);a.add_argument('--node-jitter',type=int,default=2);o=a.parse_args()
    global DATA,LIB,DEN,KNOWN
    if o.certificate:
        DATA=json.loads(Path(o.certificate).read_text());LIB=DATA['factors'];DEN=DATA['N_w_degree'];KNOWN=ORIGINAL_KNOWN|{tuple(q['coeffs_desc_w']) for q in LIB}
    source_hash=hashlib.sha256(json.dumps(DATA,sort_keys=True).encode()).hexdigest()
    (BASE/(o.out+'.pid')).write_text(str(os.getpid())+'\n')
    start=time.perf_counter();rng=random.Random(o.seed);candidates={};jobs=[];inputs=0
    Ns=[40,60,80,100,120,150,180,200,240,280,320]
    extra_nodes=[float(x) for x in json.loads(Path(o.dual).read_text())['support_w']] if o.dual else None
    checkpoint=BASE/(o.out+'.json')
    while time.perf_counter()-start<o.seconds:
        N=Ns[len(jobs)%len(Ns)] if len(jobs)<len(Ns) else rng.choice(Ns)
        if o.random_N:N=rng.randrange(35,o.max_total_degree+1)
        mode=['cheb','uniform','random'][len(jobs)%3]; seed=rng.randrange(2**31);drop=0 if len(jobs)<len(Ns) else rng.randrange(3)
        trial=create(N,mode,seed,drop,extra_nodes,o.max_residual,o.lll_delta,node_bits=o.node_bits,node_jitter=o.node_jitter)
        if trial is None:continue
        d,es,polys,lll_time=trial
        count0=len(candidates)
        for p in polys:
            inputs+=1
            _,fac=p.factor()
            for f,e in fac:
                if f.degree()<1 or f.degree()>o.max_degree:continue
                c=keypoly(f)
                if c not in KNOWN and c not in candidates:
                    candidates[c]={'id':'lll_'+str(len(candidates)),'coeffs_desc_w':list(c),'degree':len(c)-1,'primitive':True,'irreducible_over_Q':True,'origin':{'method':'weighted_exact_sample_lll','N':N,'residual_degree':d,'mode':mode,'seed':seed,'drop':drop,'prescribed_exponents':es,'weight_certificate':o.certificate or '../../data/upper_certificate.json','weight_data_sha256_canonical_json':source_hash,'support_source':o.dual,'lll_delta':o.lll_delta,'node_bits':o.node_bits,'node_jitter':o.node_jitter}}
        job={'N':N,'degree':d,'mode':mode,'seed':seed,'drop':drop,'lll_seconds':lll_time,'new_factors':len(candidates)-count0,'elapsed_seconds':time.perf_counter()-start}
        jobs.append(job)
        state={'claim_level':'HEURISTIC','variable':'w','coefficient_order':'descending','candidates':list(candidates.values()),'jobs':jobs,'polynomials_factored':inputs,'elapsed_seconds':time.perf_counter()-start,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
        checkpoint.write_text(json.dumps(state,indent=2));print(json.dumps(job),flush=True)
    print(json.dumps({k:v for k,v in state.items() if k not in ['candidates','jobs']}),flush=True)
if __name__=='__main__':main()
