"""Finite beam of disjoint balanced exchanges held over consecutive periods.

Same exact integer delta model as the earlier beam; enforce each period's budget
separately and assert the full objective after every accepted multi-asset move.
No global optimality or neighborhood exhaustion is claimed.
"""
import os,sys,time,json
from pathlib import Path
import numpy as np
from pfmodel import Model
from quoter2 import Book

def move(bk,t1,t2,rng,width=128,beamwidth=96,depthmax=3):
    m=bk.m;slack=100-np.abs(bk.W[t1:t2+1]).sum(axis=1)
    qp=bk.P[t2+1]-bk.P[t1]
    dp,vp,bp=bk.block_single(t1,t2,1);dm,vm,bm=bk.block_single(t1,t2,-1)
    ii,jj=np.nonzero(vp[:,None]&vm[None,:]&~np.eye(m.n,dtype=bool))
    if not len(ii):return 0,0
    pv=dp[ii]+dm[jj]-qp[ii,jj];pb=(bp[:,ii]+bm[:,jj]).T
    take=[];kind=pb.max(axis=1)
    for b in [-2,0,2]:
        ix=np.flatnonzero(kind==b)
        if len(ix):
            n=min(width,len(ix));take.extend(ix[np.argpartition(pv[ix],n-1)[:n]])
            take.extend(rng.choice(ix,min(width//3,len(ix)),replace=False))
    z=np.unique(take);ii,jj,pv,pb=ii[z],jj[z],pv[z],pb[z]
    pairgrad=qp[:,ii].T-qp[:,jj].T
    assets=np.stack([ii,jj],axis=1);score=pv.copy();bc=pb.copy();grad=pairgrad.copy()
    huge=np.iinfo(np.int64).max//8
    for depth in range(2,depthmax+1):
        cost=score[:,None]+pv[None,:]+grad[:,ii]-grad[:,jj]
        legal=np.ones(cost.shape,dtype=bool)
        for p in range(assets.shape[1]):legal&=(assets[:,p,None]!=ii)&(assets[:,p,None]!=jj)
        allowed=legal.copy();maxbc=np.full(cost.shape,-2*depth,dtype=np.int64)
        for k in range(len(slack)):
            v=bc[:,k,None]+pb[None,:,k];allowed&=v<=slack[k];np.maximum(maxbc,v,out=maxbc)
        masked=np.where(allowed,cost,huge);flat=int(np.argmin(masked));a,b=divmod(flat,len(ii));delta=int(masked[a,b])
        if delta<0:
            support=np.concatenate([assets[a],[ii[b],jj[b]]]);before=bk.obj
            for j in range(0,len(support),2):bk.apply(('pair',t1,t2,int(support[j]),int(support[j+1]),1,-1))
            bk.resync();assert bk.obj==before+delta and m.feasible(bk.W)
            return delta,depth
        if depth==depthmax:break
        rr=[];cc=[]
        for budgetclass in range(-2*depth,2*depth+1,2):
            ix=np.flatnonzero(legal&(maxbc==budgetclass))
            if not len(ix):continue
            count=min(beamwidth*(depth*depth+1)*2,len(ix));sel=ix[np.argpartition(cost.ravel()[ix],count-1)[:count]]
            sel=sel[np.argsort(cost.ravel()[sel])];seen=set();kept=0
            for f in sel:
                a,b=divmod(int(f),len(ii));key=(tuple(sorted(list(assets[a,::2])+[int(ii[b])])),tuple(sorted(list(assets[a,1::2])+[int(jj[b])])))
                if key in seen:continue
                seen.add(key);rr.append(a);cc.append(b);kept+=1
                if kept>=beamwidth:break
        if not rr:break
        rr=np.array(rr);cc=np.array(cc);assets=np.concatenate([assets[rr],np.stack([ii[cc],jj[cc]],axis=1)],axis=1)
        score=cost[rr,cc];bc=bc[rr]+pb[cc];grad=grad[rr]+pairgrad[cc]
    return 0,depthmax

def main():
    inst,start,out,secs,seed=sys.argv[1:];out=Path(out);out.mkdir(parents=True,exist_ok=True);(out/'pid.txt').write_text(str(os.getpid())+'\n')
    t0=time.time();end=t0+float(secs);rng=np.random.default_rng(int(seed));m=Model(inst,100,'0.01');bk=Book(m,m.read_solution(start));best=bk.obj;bestW=bk.W.copy()
    blocks=[(a,b) for a in range(9) for b in range(a,min(9,a+4))]
    def mark(**kw):print(json.dumps(dict(seconds=round(time.time()-t0,3),**kw)),flush=True)
    def save():m.write_solution(out/'best.sol',bestW,'po_a400_t10_s00','0.01','X3 block beam heuristic; independently verify')
    save();mark(stage='start',objective=best,blocks=len(blocks));rounds=0;stalls=0
    while time.time()<end and not (out/'STOP').exists():
        rounds+=1;gain=False
        for j in rng.permutation(len(blocks)):
            if time.time()>=end or (out/'STOP').exists():break
            a,b=blocks[int(j)];delta,depth=move(bk,a,b,rng)
            if delta<0:
                gain=True;bk.blocks=[(a,b)];steps,local=bk.descend(min(end,time.time()+20));bk.resync()
                mark(stage='gain',round=rounds,block=[a,b],delta=delta,depth=depth,objective=bk.obj,descent=steps)
                if bk.obj<best:best=bk.obj;bestW=bk.W.copy();save()
        mark(stage='round',round=rounds,best=best,current=bk.obj);stalls=0 if gain else stalls+1
        if stalls>=2:
            bk.W=bestW.copy();bk.resync();bk.kick(rng,2+rounds%4);bk.resync();stalls=0
            mark(stage='kick',round=rounds,objective=bk.obj)
    mark(stage='done',rounds=rounds,objective=best)

if __name__=='__main__':main()
