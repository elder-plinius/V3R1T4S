"""Exact one-hub replacement screening; unchanged-engine SLSQP polish."""
import argparse, importlib.util, json, hashlib, os, time
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
from scipy.optimize import minimize, linear_sum_assignment
from scipy.spatial.distance import cdist
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('original_engine', ROOT/'attempts/optimizer64/code/engine_search.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
e.N=64;e.R=3000.;e.PAIRS=np.triu_indices(64,1);e.SCALE=64*3.35*8760
THRESHOLD=1513312.1936;C=e.C[:,0,0];S=e.S[:,0,0]
def utc():return datetime.now(timezone.utc).isoformat()
def dump(path,obj):
    path=Path(path);tmp=path.with_suffix(path.suffix+'.new');tmp.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n');tmp.replace(path)
def energy(p):return -e.objective(np.asarray(p).ravel()/e.R)[0]*e.SCALE
def deficits(delta):
    dx=C[:,None,None]*delta[None,:,:,0]-S[:,None,None]*delta[None,:,:,1]
    dy=S[:,None,None]*delta[None,:,:,0]+C[:,None,None]*delta[None,:,:,1]
    w=.0324555*np.maximum(dx,0)+130/np.sqrt(8)
    return np.where(dx>0,(1-np.sqrt(1-(8/9)*130**2/(8*w*w)))*np.exp(-.5*(dy/w)**2),0)
def power(q):
    speed=9.8*(1-np.sqrt(np.maximum(q,0)))
    return np.where((speed>=4)&(speed<9.8),3.35*((speed-4)/5.8)**3,np.where((speed>=9.8)&(speed<25),3.35,0))
def insertion_scores(p,i,candidates,batch=256):
    others=np.delete(p,i,axis=0);d=deficits(others[:,None,:]-others[None,:,:]);base=np.sum(d*d,axis=2);scores=np.empty(len(candidates))
    for start in range(0,len(candidates),batch):
        q=candidates[start:start+batch]
        outgoing=deficits(others[:,None,:]-q[None,:,:]).transpose(0,2,1)
        incoming=deficits(q[:,None,:]-others[None,:,:])
        pw=power(base[:,None,:]+outgoing*outgoing).sum(axis=2)+power(np.sum(incoming*incoming,axis=2))
        scores[start:start+len(q)]=8760*np.sum(e.FREQ[:,None]*pw,axis=0)
    return scores
def grid(rng,size):
    pts=[]
    for radius,count in [(2999.9998,480),(2850.,240),(2600.,180),(2200.,144),(1800.,120),(1300.,96),(700.,48)]:
        a=np.arange(count)*2*np.pi/count+rng.uniform(0,2*np.pi/count);pts.extend(np.c_[radius*np.cos(a),radius*np.sin(a)])
    n=size-len(pts)
    if n>0:
        r=2999.9998*np.sqrt(rng.random(n));a=rng.uniform(0,2*np.pi,n);pts.extend(np.c_[r*np.cos(a),r*np.sin(a)])
    return np.asarray(pts)
def screen(p,rng,size,per_hub):
    positions=grid(rng,size);proposals=[];all_d2=np.sum((positions[:,None,:]-p[None,:,:])**2,axis=2)
    for i in range(64):
        keep=np.ones(64,dtype=bool);keep[i]=False
        idx=np.flatnonzero((all_d2[:,keep].min(axis=1)>260.001**2)&(all_d2[:,i]>350.**2))
        vals=insertion_scores(p,i,positions[idx]);chosen=[]
        for k in np.argsort(-vals):
            pos=positions[idx[k]]
            if all(np.linalg.norm(pos-x)>350 for x in chosen):
                proposals.append({'score':float(vals[k]),'hub':i,'position':pos.tolist()});chosen.append(pos)
                if len(chosen)>=per_hub:break
    return sorted(proposals,key=lambda x:-x['score'])
def object_for(p,meta):return {'coordinates_m':p.tolist(),'aep_MWh':energy(p),'geometry':e.geometry(p.ravel()/e.R),'utc':utc(),**meta}
def distance(a,b):
    cost=cdist(a,b);i,j=linear_sum_assignment(cost);return float(np.sqrt(np.mean(cost[i,j]**2)))
def validate(rng,out):
    p=np.array(json.loads((ROOT/'data/starting-own-64.json').read_text())['coordinates_m']);residuals=[]
    for i in [0,16,37,63]:
        q=grid(rng,1600)[rng.choice(1600,8,replace=False)];vals=insertion_scores(p,i,q)
        for x,v in zip(q,vals):
            pp=p.copy();pp[i]=x;residuals.append(abs(float(v)-energy(pp)))
    z=p.ravel()/e.R+rng.normal(0,.0001,128);v,g=e.objective(z);checks=[]
    for j in rng.choice(128,16,replace=False):
        zz=z.copy();zz[j]+=1e-6;vp=e.objective(zz)[0];zz[j]-=2e-6;vm=e.objective(zz)[0];checks.append(abs((vp-vm)/2e-6-g[j]))
    record={'utc':utc(),'pid':os.getpid(),'start_aep_MWh':energy(p),'max_marginal_full_abs_MWh':max(residuals),'max_gradient_absolute_error':max(checks),'samples':len(residuals),'gradient_samples':len(checks)}
    dump(out/'validation.json',record);print(json.dumps({'event':'validation',**record}),flush=True);assert max(residuals)<1e-7 and max(checks)<1e-6
    return p
def run(args):
    out=HERE/args.output;out.mkdir(parents=True,exist_ok=True);rng=np.random.default_rng(args.seed);deadline=datetime.fromisoformat(args.deadline).timestamp()
    dump(out/'process.json',{'pid':os.getpid(),'utc':utc(),'deadline':args.deadline,'argv':vars(args),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'input_sha256':hashlib.sha256((ROOT/'data/starting-own-64.json').read_bytes()).hexdigest()})
    p=validate(rng,out);best=object_for(p,{'source':'starting-own-64.json'});beam=[best];generation=0;total=0;history=[];ck=out/'checkpoint.json'
    if ck.exists() and not args.pilot:
        state=json.loads(ck.read_text());beam=state['beam'];best=state['best'];generation=state['generation'];total=state['total'];rng.bit_generator.state=state['rng_state'];history=state.get('history',[])
    while time.time()<deadline:
        source=beam[generation%len(beam)];p=np.array(source['coordinates_m']);t=time.time();proposals=screen(p,rng,args.grid,1 if args.pilot else args.per_hub)
        dump(out/f'screen-{generation:04d}.json',{'utc':utc(),'source':source,'elapsed':time.time()-t,'proposals':proposals})
        print(json.dumps({'event':'screen','generation':generation,'elapsed':time.time()-t,'source_MWh':source['aep_MWh'],'best':proposals[:3]}),flush=True)
        candidates=[]
        for passno in range(args.per_hub):
            hub_counts={}
            for proposal in proposals:
                h=proposal['hub'];count=hub_counts.get(h,0);hub_counts[h]=count+1
                if count==passno:candidates.append(proposal)
        for proposal in candidates[:1 if args.pilot else args.polishes]:
            if time.time()>=deadline:break
            q=p.copy();q[proposal['hub']]=proposal['position'];total+=1;t=time.time()
            result=minimize(e.objective,q.ravel()/e.R,jac=True,method='SLSQP',constraints={'type':'ineq','fun':e.constraints,'jac':e.constraint_jac},options={'maxiter':args.maxiter,'ftol':1e-12})
            obj=object_for(result.x.reshape(64,2)*e.R,{'generation':generation,'polish':total,'proposal':proposal,'source_aep_MWh':source['aep_MWh'],'solver_success':bool(result.success),'nit':int(result.nit),'seconds':time.time()-t,'seed':args.seed});feasible=obj['geometry']['strictly_feasible']
            if feasible and obj['aep_MWh']>best['aep_MWh']:
                best=obj;dump(out/'best.json',best)
            if feasible and obj['aep_MWh']>THRESHOLD:
                hitpath=out/f'HIT-{total:06d}.json';dump(hitpath,obj);print(json.dumps({'event':'HIT','path':str(hitpath),'aep_MWh':obj['aep_MWh'],'geometry':obj['geometry']}),flush=True)
            min_dist=min(distance(np.array(x['coordinates_m']),np.array(obj['coordinates_m'])) for x in beam) if feasible else None
            if feasible and min_dist>30:
                beam.append(obj);beam=sorted(beam,key=lambda x:-x['aep_MWh'])[:args.beam]
            rec={k:v for k,v in obj.items() if k!='coordinates_m'};rec.update({'event':'polish','beam_size':len(beam),'beam_nearest_RMS_m':min_dist,'best_MWh':best['aep_MWh']});print(json.dumps(rec),flush=True);history.append(rec)
            dump(ck,{'utc':utc(),'generation':generation,'total':total,'beam':beam,'best':best,'rng_state':rng.bit_generator.state,'history':history[-200:]})
        generation+=1;dump(ck,{'utc':utc(),'generation':generation,'total':total,'beam':beam,'best':best,'rng_state':rng.bit_generator.state,'history':history[-200:]})
        if args.pilot:break
    print(json.dumps({'event':'complete','utc':utc(),'pid':os.getpid(),'total':total,'generation':generation,'best_MWh':best['aep_MWh']}),flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='output');ap.add_argument('--deadline',required=True);ap.add_argument('--seed',type=int,default=2026110403);ap.add_argument('--grid',type=int,default=3200);ap.add_argument('--per-hub',type=int,default=4);ap.add_argument('--polishes',type=int,default=160);ap.add_argument('--beam',type=int,default=6);ap.add_argument('--maxiter',type=int,default=450);ap.add_argument('--pilot',action='store_true');run(ap.parse_args())
