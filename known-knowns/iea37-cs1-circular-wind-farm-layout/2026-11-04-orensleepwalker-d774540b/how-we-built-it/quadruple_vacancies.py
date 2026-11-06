"""Sequential exact marginal beam screening of four vacated hubs, then full64 polish.

Own unpublished seeds only. The intermediate63-hub score is a proposal heuristic;
only unchanged-model64-hub scores can enter the elite pool or count as results.
"""
import argparse, hashlib, json, os, signal, sys, time
from pathlib import Path
from datetime import datetime
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'coordinate64/code'))
import insertion as m

stopping=False
class StopRequested(Exception): pass
def on_signal(sig,frame):
    global stopping
    stopping=True
signal.signal(signal.SIGTERM,on_signal);signal.signal(signal.SIGINT,on_signal)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def propose(p,rng,pair,grid_size):
    rest=np.delete(p,pair,axis=0);positions=m.grid(rng,grid_size)
    positions=positions[np.min(np.sum((positions[:,None]-rest[None])**2,axis=2),axis=1)>260.001**2]
    beam=[(0.,[])]
    for stage in range(len(pair)):
        children=[]
        for _,placed in beam:
            base=np.vstack([rest,np.array(placed).reshape(-1,2)])
            pos=positions[np.min(np.sum((positions[:,None]-base[None])**2,axis=2),axis=1)>260.001**2]
            values=m.insertion_scores(np.vstack([base,[[0.,0.]]]),len(base),pos)
            chosen=[]
            for j in np.argsort(-values):
                if any(np.linalg.norm(pos[j]-x)<350 for x in chosen):continue
                chosen.append(pos[j]);children.append((float(values[j]),placed+[pos[j].tolist()]))
                if len(chosen)==4:break
        beam=[];seen=set()
        for value,placed in sorted(children,key=lambda x:-x[0]):
            key=tuple(sorted(tuple(x) for x in placed))
            if key in seen:continue
            seen.add(key)
            if beam and min(m.distance(np.array(placed),np.array(v[1])) for v in beam)<100:continue
            beam.append((value,placed))
            if len(beam)==6:break
    records=[]
    for value,placed in beam:
        q=p.copy();q[pair]=placed;full=m.energy(q);error=abs(full-value)
        if error>1e-7:raise ValueError('quadruple marginal/full64 mismatch')
        records.append((full,q,{'vacated':pair.tolist(),'inserted':placed,'screen_error_MWh':error}))
    return sorted(records,key=lambda x:-x[0])

def main(a):
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True);frozen=out/'frozen';frozen.mkdir(exist_ok=True)
    deadline=datetime.fromisoformat(a.deadline).timestamp();rng=np.random.default_rng(a.seed)
    start=json.loads(Path(a.own_seed).read_text());start['artifact_sha256']=sha(a.own_seed);start['artifact_path']=str(Path(a.own_seed).resolve())
    best=start;pool=[start];trial=0;polishes=0;history=[];checkpoint=out/'checkpoint.json'
    if checkpoint.exists():
        ck=json.loads(checkpoint.read_text());best=ck['best'];pool=ck['pool'];trial=ck['trial'];polishes=ck['polishes'];rng.bit_generator.state=ck['rng_state']
    codehash=sha(__file__)
    m.dump(out/'process.json',{'pid':os.getpid(),'utc':m.utc(),'args':vars(a),'code_sha256':codehash,'insertion_sha256':sha(m.__file__),'source_sha256':sha(a.own_seed)})
    def stop():return stopping or (out/'STOP').exists() or time.time()>=deadline
    def save():m.dump(checkpoint,{'utc':m.utc(),'best':best,'pool':pool,'trial':trial,'polishes':polishes,'history':history[-100:],'rng_state':rng.bit_generator.state})
    def cb(z):
        if stop():raise StopRequested()
    save();m.dump(out/'best.json',best)
    while not stop() and trial<a.max_trials:
        for name in a.inbox:
            incoming=Path(name)
            if not incoming.exists():continue
            raw=incoming.read_bytes();candidate=json.loads(raw);pp=np.array(candidate['coordinates_m'])
            if pp.shape!=(64,2) or not np.isfinite(pp).all():raise ValueError('bad own inbox')
            if not m.e.geometry(pp.ravel()/3000)['strictly_feasible']:continue
            value=m.energy(pp)
            if value<=best['aep_MWh']+1e-7:continue
            digest=hashlib.sha256(raw).hexdigest();dest=frozen/(digest+'.json')
            if not dest.exists():dest.write_bytes(raw);dest.chmod(0o444)
            candidate.update(aep_MWh=value,artifact_sha256=digest,artifact_path=str(dest.resolve()))
            best=candidate;pool.append(candidate);pool=sorted(pool,key=lambda x:-x['aep_MWh'])[:6];m.dump(out/'best.json',best);save()
            print(json.dumps({'event':'own_import','sha256':digest,'aep_MWh':value}),flush=True)
        source=best if trial%3 else pool[int(rng.integers(len(pool)))];p=np.array(source['coordinates_m'])
        pair=rng.choice(64,4,replace=False)
        if trial%2==0:
            d=np.sum((p-p[pair[0]])**2,axis=1);pair[1:]=rng.choice(np.argsort(d)[1:11],3,replace=False)
        trial+=1;t=time.time();props=propose(p,rng,pair,a.grid)
        m.dump(out/f'proposals-{trial:05d}.json',{'utc':m.utc(),'source_sha256':source['artifact_sha256'],'trial':trial,'seconds':time.time()-t,'proposals':[{'score_MWh':v[0],**v[2]} for v in props]})
        for value,q,info in props[:a.polishes]:
            if stop():break
            t=time.time()
            try:r=minimize(m.e.objective,q.ravel()/3000,jac=True,method='SLSQP',constraints={'type':'ineq','fun':m.e.constraints,'jac':m.e.constraint_jac},callback=cb,options={'maxiter':450,'ftol':1e-12})
            except StopRequested:break
            polishes+=1;obj=m.object_for(r.x.reshape(64,2)*3000,{'trial':trial,'polish':polishes,'pair_proposal':info,'source_sha256':source['artifact_sha256'],'source_path':source['artifact_path'],'seed':a.seed,'code_sha256':codehash,'nit':int(r.nit),'solver_success':bool(r.success),'seconds':time.time()-t})
            valid=obj['geometry']['strictly_feasible'];dist=min(m.distance(np.array(x['coordinates_m']),np.array(obj['coordinates_m'])) for x in pool) if valid else 0
            improved=valid and obj['aep_MWh']>best['aep_MWh']+1e-7
            admitted=valid and dist>30 and (len(pool)<6 or obj['aep_MWh']>min(x['aep_MWh'] for x in pool))
            if improved or admitted:
                raw=(json.dumps(obj,indent=2,allow_nan=False)+'\n').encode();digest=hashlib.sha256(raw).hexdigest();path=frozen/(digest+'.json');path.write_bytes(raw);path.chmod(0o444)
                obj['artifact_sha256']=digest;obj['artifact_path']=str(path.resolve())
            if improved:best=obj;m.dump(out/'best.json',best)
            if admitted:pool.append(obj);pool=sorted(pool,key=lambda x:-x['aep_MWh'])[:6]
            record={k:v for k,v in obj.items() if k!='coordinates_m'};record.update({'event':'IMPROVEMENT' if improved else 'polish','best_MWh':best['aep_MWh'],'pool':len(pool)})
            print(json.dumps(record),flush=True);history.append(record);save()
        save()
    m.dump(out/'complete.json',{'utc':m.utc(),'trial':trial,'polishes':polishes,'best_MWh':best['aep_MWh'],'best_sha256':best['artifact_sha256'],'stop_file':(out/'STOP').exists(),'signal':stopping,'deadline':time.time()>=deadline});save()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--inbox',nargs='*',default=[]);p.add_argument('--own-seed',required=True);p.add_argument('--output',required=True);p.add_argument('--deadline',required=True);p.add_argument('--seed',type=int,default=2026110407);p.add_argument('--max-trials',type=int,default=100000);p.add_argument('--grid',type=int,default=1800);p.add_argument('--polishes',type=int,default=6);main(p.parse_args())
