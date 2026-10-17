"""Bounded independent HSP4 SLP search. Reads tar members without extraction."""
from __future__ import annotations
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
import argparse, ctypes, datetime as dt, hashlib, json, math, re, sys, tarfile, threading, time, warnings
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, csr_matrix

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT.parents[1]
OUT = ROOT / 'output'
OUT.mkdir(exist_ok=True)
for folder in ['candidates', 'checkpoints']:
    (ROOT/folder).mkdir(exist_ok=True)
EVENTS = OUT/'events.jsonl'
START = time.monotonic()
STATE = {'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'pid': os.getpid(), 'status':'starting', 'rows':{}, 'tests':{}}
DEADLINE = START + 1100

def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
def emit(kind, **data):
    rec = {'utc':utc(), 'elapsed':time.monotonic()-START, 'kind':kind, **data}
    with EVENTS.open('a', encoding='utf-8') as f:
        f.write(json.dumps(rec, allow_nan=False)+'\n')
    if kind not in ['iteration']:
        print(json.dumps(rec, allow_nan=False), flush=True)
    return rec

def atomic_json(path, data):
    temp = path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(data, indent=2, allow_nan=False), encoding='utf-8')
    temp.replace(path)

def checkpoint():
    STATE['updated_utc'] = utc()
    STATE['elapsed_seconds'] = time.monotonic()-START
    atomic_json(OUT/'checkpoint.json', STATE)

def low_priority():
    if sys.platform == 'win32':
        from ctypes import wintypes
        k32=ctypes.WinDLL('kernel32', use_last_error=True)
        k32.GetCurrentProcess.argtypes=[]
        k32.GetCurrentProcess.restype=wintypes.HANDLE
        k32.SetPriorityClass.argtypes=[wintypes.HANDLE,wintypes.DWORD]
        k32.SetPriorityClass.restype=wintypes.BOOL
        k32.GetPriorityClass.argtypes=[wintypes.HANDLE]
        k32.GetPriorityClass.restype=wintypes.DWORD
        handle=k32.GetCurrentProcess()
        if not k32.SetPriorityClass(handle, 0x4000):
            raise ctypes.WinError(ctypes.get_last_error())
        STATE['priority_class']=k32.GetPriorityClass(handle)
    else:
        os.nice(10)
        STATE['priority_nice']=os.getpriority(os.PRIO_PROCESS,0)

def watchdog():
    while time.monotonic() < DEADLINE+5:
        time.sleep(min(1,max(.05,DEADLINE+5-time.monotonic())))
    (OUT/'hard_timeout.json').write_text(json.dumps({'utc':utc(),'pid':os.getpid()}))
    os._exit(124)

def measure(x):
    ii,jj=np.triu_indices(len(x),1)
    pair = np.linalg.norm(x[ii]-x[jj],axis=1)
    norms=np.linalg.norm(x,axis=1)
    return min(float(pair.min())/2, 1-float(norms.max())), float(pair.min())/2, float(norms.max())

def rebalance(x):
    r,p,q=measure(x)
    y=x/(p+q)
    return y,measure(y)[0]

def read_sources():
    table={int(a):float(b) for a,b in (line.split() for line in (RUN/'data/hsp4_radius.txt').read_text().splitlines() if line.strip())}
    exclusions=set(json.loads(re.search(r'excluded_open_pr_n: (\[[^\]]*\])',(RUN/'PREREG.v2.md').read_text()).group(1)))
    data={}
    with tarfile.open(RUN/'data/hsp4_coords.tar.gz') as tar:
        for mem in tar:
            m=re.fullmatch(r'(?:.*/)?hsp4-(\d+)\.txt',mem.name)
            if not m: continue
            n=int(m[1])
            if n not in table or n in exclusions: continue
            lines=tar.extractfile(mem).read().decode('ascii').splitlines()
            header=float(lines[0])
            records=[line.split() for line in lines[1:] if line.strip()]
            assert len(records)==n and all(len(row)==5 for row in records),(mem.name,'shape')
            assert [int(row[0]) for row in records]==list(range(1,n+1)),(mem.name,'indices')
            x=np.array([[float(v) for v in row[1:]] for row in records])
            data[n]=(x,table[n],header,mem.name)
    return data,sorted(exclusions)

def save_coords(x,n,label,r,baseline):
    path=ROOT/'candidates'/f'hsp4-{n}-{label}.txt'
    with path.open('w',encoding='ascii',newline='\n') as f:
        for row in x:
            f.write(' '.join(format(float(v),'.18e') for v in row)+'\n')
    receipt={'n':n,'dimension':4,'radius_float':r,'saved_table':baseline,'gain_float':r-baseline,
             'utc':utc(),'coordinate_file':str(path.relative_to(ROOT)),
             'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'status':'unverified numerical candidate'}
    atomic_json(path.with_suffix('.json'),receipt)
    return receipt

def lp_step(x,r,trust,rng,bias=0.):
    n,d=x.shape
    ii,jj=np.triu_indices(n,1)
    diff=x[ii]-x[jj]
    dist=np.linalg.norm(diff,axis=1)
    unit=diff/dist[:,None]
    m=len(ii)
    # Unit-vector supporting planes are global lower bounds on pair distances.
    pairrows=np.repeat(np.arange(m),9)
    paircols=np.column_stack([ii[:,None]*4+np.arange(4),jj[:,None]*4+np.arange(4),np.full((m,1),4*n)]).ravel()
    pairdata=np.column_stack([-unit,unit,np.full((m,1),2.)]).ravel()
    norms=np.linalg.norm(x,axis=1)
    boundary_unit=np.divide(x,norms[:,None],out=np.zeros_like(x),where=norms[:,None]>1e-15)
    boundrows=np.repeat(np.arange(m,m+n),5)
    boundcols=np.column_stack([np.arange(n)[:,None]*4+np.arange(4),np.full((n,1),4*n)]).ravel()
    bounddata=np.column_stack([boundary_unit,np.ones((n,1))]).ravel()
    A=coo_matrix((np.r_[pairdata,bounddata],(np.r_[pairrows,boundrows],np.r_[paircols,boundcols])),shape=(m+n,n*4+1)).tocsr()
    b=np.r_[(dist-2*r)/trust,(1-r-norms)/trust]
    # Gauge only removes infinitesimal rotations, which cannot alter the objective.
    gauge=[]
    for a in range(d):
        for z in range(a+1,d):
            row=np.zeros((n,d)); row[:,a]=-x[:,z]; row[:,z]=x[:,a]
            gauge.append(np.r_[row.ravel(),0.])
    objective=np.zeros(n*4+1); objective[-1]=-1.
    if bias: objective[:-1]=rng.normal(size=n*4)*bias/(n*4)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        opt=linprog(objective,A_ub=A,b_ub=b,A_eq=csr_matrix(np.array(gauge)),b_eq=np.zeros(6),
            bounds=[(-1.,1.)]*(n*4)+[(-1.,1.)], method='highs',
            options={'time_limit':min(2.5,max(.05,DEADLINE-time.monotonic())),
                     'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9,'threads':1})
    if not opt.success:
        return None,{'status':int(opt.status),'message':opt.message}
    step=opt.x[:-1].reshape(n,4)*trust
    best=x; best_r=r; factor_best=0.; evaluated=[]
    for factor in [1.,.5,.25,.125,.0625,.03125,.015625,.0078125]:
        y,yr=rebalance(x+factor*step)
        evaluated.append(yr)
        if yr>best_r:
            best,best_r,factor_best=y,yr,factor
    return (best,best_r), {'status':0,'predicted_dr':float(opt.x[-1]*trust),
        'max_step':float(np.max(np.abs(step))), 'factor':factor_best,
        'trial_radii':evaluated,'lp_iterations':int(opt.nit)}

def polish(x,n,baseline,iterations,trust,label,rng,bias=0.):
    x,r=rebalance(x)
    start_r=r
    naccepted=0; nfailed=0; threshold_reported=False
    for k in range(iterations):
        if time.monotonic()>DEADLINE-3: break
        old=r
        result,detail=lp_step(x,r,trust,rng,bias)
        if result is None:
            nfailed+=1; trust*=.5
        else:
            y,yr=result
            if yr>r+2e-16:
                x,r=y,yr; naccepted+=1
                if detail['factor']>=.5:
                    trust=min(.02,trust*1.35)
                else: trust*=.65
            else:
                trust*=.3
        emit('iteration',n=n,label=label,iteration=k,radius=r,gain=r-baseline,
             trust=trust,accepted=r>old,**detail)
        if r-baseline>=1e-10 and not threshold_reported:
            receipt=save_coords(x,n,label+'-threshold',r,baseline)
            emit('threshold_candidate',**receipt)
            threshold_reported=True
        STATE['active']={'n':n,'label':label,'iteration':k,'radius_float':r,
                         'gain_float':r-baseline,'trust':trust}
        checkpoint()
        if k%10==0:
            np.savez(ROOT/'checkpoints'/f'hsp4-{n}-{label}.npz',x=x,r=r,trust=trust,iteration=k)
        if trust<2e-8 and k>=4: break
    receipt=save_coords(x,n,label,r,baseline)
    emit('polish_done',n=n,label=label,start_r=start_r,radius=r,gain=r-baseline,
         accepted=naccepted,failed_lp=nfailed,iterations=k+1,trust=trust)
    return x,r,receipt

def checker_selftest():
    good=np.array([[.5,0,0,0],[-.5,0,0,0]])
    bad=np.zeros((2,4))
    good_r=measure(good)[0]; bad_r=measure(bad)[0]
    assert good_r==.5 and bad_r==0
    emit('checker_selftest',positive_radius=good_r,negative_radius=bad_r,pass_test=True)

def main():
    global DEADLINE
    ap=argparse.ArgumentParser(); ap.add_argument('--seconds',type=float,default=1100)
    ap.add_argument('--first',type=int,default=76);ap.add_argument('--last',type=int,default=120)
    ap.add_argument('--scan-iterations',type=int,default=12)
    ap.add_argument('--seed',type=int,default=20261014)
    args=ap.parse_args()
    DEADLINE=START+args.seconds
    low_priority()
    (OUT/'pid.txt').write_text(str(os.getpid())+'\n')
    threading.Thread(target=watchdog,daemon=True).start()
    STATE.update({'status':'running','args':vars(args),'numpy':np.__version__,'scipy':scipy.__version__})
    emit('start',**STATE)
    checker_selftest()
    data,excluded=read_sources()
    rows=[n for n in range(args.first,args.last+1) if n in data]
    STATE['excluded_n']=excluded; STATE['prioritized_rows']=rows
    rng=np.random.default_rng(args.seed)
    best={}
    # Decisive test H1: common-scale polish on every prioritized object.
    radial=[]
    for n in rows:
        x,table,header,member=data[n]
        raw=measure(x)[0]; y,r=rebalance(x)
        radial.append({'n':n,'raw_radius':raw,'scaled_radius':r,'gain':r-table})
        best[n]=(y,r)
    atomic_json(OUT/'radial_scan.json',radial)
    STATE['tests']['H1']={'rows':len(radial),'best_gain':max(v['gain'] for v in radial)}
    emit('radial_scan_done',**STATE['tests']['H1'])
    # Decisive test H2: cheap equal-cost scan before allocating deeper work.
    for n in rows:
        if time.monotonic()>DEADLINE-60: break
        x,r=best[n]; table=data[n][1]
        x,r,receipt=polish(x,n,table,args.scan_iterations,1e-4,'scan',rng)
        best[n]=(x,r)
        STATE['rows'][str(n)]={'table':table,'radius':r,'gain':r-table,'best_file':receipt['coordinate_file']}
        checkpoint()
    STATE['tests']['H2']={'rows':len(STATE['rows']),'best_gain':max(v['gain'] for v in STATE['rows'].values())}
    ranking=sorted(best,key=lambda n:best[n][1]-data[n][1],reverse=True)
    emit('scan_done',ranking=ranking,top=[{'n':n,'gain':best[n][1]-data[n][1]} for n in ranking[:10]])
    # Surviving leading rows get a longer continuation before perturbations.
    for n in ranking[:min(10,len(ranking))]:
        if time.monotonic()>DEADLINE-60: break
        x,r,receipt=polish(best[n][0],n,data[n][1],100,5e-4,'deep',rng)
        if r>best[n][1]:
            best[n]=(x,r)
            STATE['rows'][str(n)].update(radius=r,gain=r-data[n][1],best_file=receipt['coordinate_file'])
    # Decisive test H3: fixed-seed agitation, always retaining the best previous packing.
    perturb_tests=[]
    for cycle in range(10000):
        if time.monotonic()>DEADLINE-12: break
        n=ranking[cycle%min(8,len(ranking))]
        old,r=best[n]
        amplitude=[1e-5,1e-4,5e-4,2e-3][(cycle//min(8,len(ranking)))%4]
        norms=np.linalg.norm(old,axis=1)
        ii,jj=np.triu_indices(n,1); distances=np.linalg.norm(old[ii]-old[jj],axis=1)
        contacts=np.bincount(np.r_[ii[distances<2*r+1e-5],jj[distances<2*r+1e-5]],minlength=n)
        weights=np.where((contacts<5)&(norms<1-r-1e-5),3.,1.)
        perturb=rng.normal(size=old.shape)*amplitude*weights[:,None]
        trial=old+perturb
        label=f'perturb-{cycle:04d}'
        x,yr,receipt=polish(trial,n,data[n][1],45,max(5e-4,amplitude*2),label,rng,
                             bias=1e-7 if cycle%3==2 else 0.)
        record={'cycle':cycle,'n':n,'amplitude':amplitude,'before':r,'after':yr,'improved':yr>r}
        perturb_tests.append(record)
        emit('perturb_done',**record)
        if yr>r:
            best[n]=(x,yr)
            STATE['rows'][str(n)].update(radius=yr,gain=yr-data[n][1],best_file=receipt['coordinate_file'])
        STATE['tests']['H3']={'trials':len(perturb_tests),'improved':sum(z['improved'] for z in perturb_tests)}
        atomic_json(OUT/'perturb_tests.json',perturb_tests)
        checkpoint()
    for n,(x,r) in best.items():
        receipt=save_coords(x,n,'best',r,data[n][1])
        if str(n) in STATE['rows']:
            STATE['rows'][str(n)].update(best_file=receipt['coordinate_file'],radius=r,gain=r-data[n][1])
    STATE['status']='complete';STATE['ended_utc']=utc()
    checkpoint()
    emit('complete',best=sorted(STATE['rows'].items(),key=lambda z:z[1]['gain'],reverse=True)[:10],tests=STATE['tests'])

if __name__=='__main__':
    try: main()
    except BaseException as exc:
        STATE['status']='error';STATE['error']=repr(exc);checkpoint();raise
