"""Finite multi-asset beam allowing net exposure to change, not just swaps.

Keep separate gross-budget and net-change strata. Every accepted full move is
checked against the integer objective and all period constraints. This search
does not establish any global lower bound or exhausted neighborhood.
"""
import os,sys,time,json
from pathlib import Path
import numpy as np
from pfmodel import Model
from quoter2 import Book

def move(bk,k,rng,width=96,beamwidth=64,depthmax=4):
    m=bk.m;w=bk.W[k];slack=100-int(abs(w).sum());net=int(w.sum());qp=m.Qs[k]
    singles={a:bk.block_single(k,k,a) for a in [-1,1]};parts=[]
    for si,sj in [(1,-1),(1,1),(-1,-1)]:
        di,vi,bi=singles[si];dj,vj,bj=singles[sj]
        ii,jj=np.nonzero(vi[:,None]&vj[None,:]&~np.eye(m.n,dtype=bool))
        if si==sj:
            z=ii<jj;ii,jj=ii[z],jj[z]
        pv=di[ii]+dj[jj]+si*sj*qp[ii,jj];pb=bi[0,ii]+bj[0,jj]
        take=[]
        for budgetclass in [-2,0,2]:
            ix=np.flatnonzero(pb==budgetclass)
            if len(ix):
                n=min(width,len(ix));take.extend(ix[np.argpartition(pv[ix],n-1)[:n]])
                take.extend(rng.choice(ix,min(width//3,len(ix)),replace=False))
        if take:
            z=np.unique(take);parts.append((ii[z],jj[z],np.full(len(z),si),np.full(len(z),sj),pv[z],pb[z]))
    if not parts:return 0,0
    ii,jj,si,sj,pv,pb=[np.concatenate([p[j] for p in parts]) for j in range(6)];pn=si+sj
    pairgrad=si[:,None]*qp[:,ii].T+sj[:,None]*qp[:,jj].T
    assets=np.stack([ii,jj],axis=1);signs=np.stack([si,sj],axis=1)
    score=pv.copy();bc=pb.copy();nc=pn.copy();grad=pairgrad.copy();huge=np.iinfo(np.int64).max//8
    for depth in range(2,depthmax+1):
        cost=score[:,None]+pv[None,:]+grad[:,ii]*si+grad[:,jj]*sj
        legal=np.ones(cost.shape,dtype=bool)
        for p in range(assets.shape[1]):legal&=(assets[:,p,None]!=ii)&(assets[:,p,None]!=jj)
        budget=bc[:,None]+pb;netdelta=nc[:,None]+pn
        allowed=legal&(budget<=slack)&(net+netdelta>=-5)&(net+netdelta<=10)
        masked=np.where(allowed,cost,huge);flat=int(np.argmin(masked));a,b=divmod(flat,len(ii));delta=int(masked[a,b])
        if delta<0:
            support=np.concatenate([assets[a],[ii[b],jj[b]]]);sgn=np.concatenate([signs[a],[si[b],sj[b]]]);before=bk.obj
            for j in range(0,len(support),2):bk.apply(('pair',k,k,int(support[j]),int(support[j+1]),int(sgn[j]),int(sgn[j+1])))
            bk.resync();assert bk.obj==before+delta and m.feasible(bk.W)
            return delta,depth
        if depth==depthmax:break
        rr=[];cc=[]
        for budgetclass in range(-2*depth,2*depth+1,2):
            for netclass in range(-2*depth,2*depth+1,2):
                ix=np.flatnonzero(legal&(budget==budgetclass)&(netdelta==netclass))
                if not len(ix):continue
                count=min(beamwidth*(depth*depth+1)*2,len(ix));sel=ix[np.argpartition(cost.ravel()[ix],count-1)[:count]]
                sel=sel[np.argsort(cost.ravel()[sel])];seen=set();kept=0
                for f in sel:
                    a,b=divmod(int(f),len(ii));ids=np.concatenate([assets[a],[ii[b],jj[b]]]);ss=np.concatenate([signs[a],[si[b],sj[b]]])
                    key=(tuple(sorted(ids[ss==1])),tuple(sorted(ids[ss==-1])))
                    if key in seen:continue
                    seen.add(key);rr.append(a);cc.append(b);kept+=1
                    if kept>=beamwidth:break
        if not rr:break
        rr=np.array(rr);cc=np.array(cc)
        assets=np.concatenate([assets[rr],np.stack([ii[cc],jj[cc]],axis=1)],axis=1);signs=np.concatenate([signs[rr],np.stack([si[cc],sj[cc]],axis=1)],axis=1)
        score=cost[rr,cc];bc=budget[rr,cc];nc=netdelta[rr,cc];grad=grad[rr]+pairgrad[cc]
    return 0,depthmax

def main():
    inst,start,out,secs,seed=sys.argv[1:];out=Path(out);out.mkdir(parents=True,exist_ok=True);(out/'pid.txt').write_text(str(os.getpid())+'\n')
    t0=time.time();end=t0+float(secs);rng=np.random.default_rng(int(seed));m=Model(inst,100,'0.01');bk=Book(m,m.read_solution(start));best=bk.obj;bestW=bk.W.copy()
    def mark(**kw):print(json.dumps(dict(seconds=round(time.time()-t0,3),**kw)),flush=True)
    def save():m.write_solution(out/'best.sol',bestW,'po_a400_t10_s00','0.01','X3 variable-net beam heuristic; independently verify')
    save();mark(stage='start',objective=best);rounds=0;stalls=0
    while time.time()<end and not (out/'STOP').exists():
        rounds+=1;gain=False
        for k in rng.permutation(9):
            if time.time()>=end or (out/'STOP').exists():break
            k=int(k);delta,depth=move(bk,k,rng,depthmax=3 if rounds<3 else 4)
            if delta<0:
                gain=True;bk.blocks=[(k,k)];steps,local=bk.descend(min(end,time.time()+20));bk.resync()
                mark(stage='gain',round=rounds,period=k,delta=delta,depth=depth,objective=bk.obj,descent=steps,net=int(bk.W[k].sum()))
                if bk.obj<best:best=bk.obj;bestW=bk.W.copy();save()
        mark(stage='round',round=rounds,best=best,current=bk.obj);stalls=0 if gain else stalls+1
        if stalls>=2 or rounds%10==0:
            bk.W=bestW.copy();bk.resync();bk.kick(rng,2+rounds%3);bk.resync();stalls=0
            bk.blocks=[(k,k) for k in range(9)];steps,local=bk.descend(min(end,time.time()+20));bk.resync()
            assert m.feasible(bk.W)
            if bk.obj<best:best=bk.obj;bestW=bk.W.copy();save()
            mark(stage='kick',round=rounds,objective=bk.obj,descent=steps,local=local)
    mark(stage='done',rounds=rounds,objective=best)

if __name__=='__main__':main()
