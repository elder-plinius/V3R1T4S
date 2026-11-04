"""Beam search over disjoint balanced exchanges (up to eight assets).
Integer search scores; explicit output still needs an exact independent checker.
"""
import os,sys,time,json
from pathlib import Path
import numpy as np
from pfmodel import Model
from quoter2 import Book

def beam_move(bk,k,rng,width=192,beamwidth=128,depthmax=4):
    m=bk.m;w=bk.W[k];slack=100-int(abs(w).sum());qp=m.Qs[k]
    dp,vp,bp=bk.block_single(k,k,1);dm,vm,bm=bk.block_single(k,k,-1)
    ii,jj=np.nonzero(vp[:,None]&vm[None,:]&~np.eye(m.n,dtype=bool))
    pv=dp[ii]+dm[jj]-qp[ii,jj];pb=bp[0,ii]+bm[0,jj];take=[]
    for b in [-2,0,2]:
        ix=np.flatnonzero(pb==b)
        if len(ix):
            n=min(width,len(ix));take.extend(ix[np.argpartition(pv[ix],n-1)[:n]])
            take.extend(rng.choice(ix,min(width//3,len(ix)),replace=False))
    z=np.unique(take);ii,jj,pv,pb=ii[z],jj[z],pv[z],pb[z]
    pairgrad=qp[:,ii].T-qp[:,jj].T
    assets=np.stack([ii,jj],axis=1);score=pv.copy();bc=pb.copy();grad=pairgrad.copy()
    for depth in range(2,depthmax+1):
        cost=score[:,None]+pv[None,:]+grad[:,ii]-grad[:,jj]
        legal=np.ones(cost.shape,dtype=bool)
        for p in range(assets.shape[1]):legal&=(assets[:,p,None]!=ii)&(assets[:,p,None]!=jj)
        budget=bc[:,None]+pb
        cost[~legal]=np.iinfo(np.int64).max//8
        allowed=legal&(budget<=slack)
        masked=np.where(allowed,cost,np.iinfo(np.int64).max//8)
        flat=int(np.argmin(masked));a,b=divmod(flat,len(ii));delta=int(masked[a,b])
        if delta<0:
            support=np.concatenate([assets[a],[ii[b],jj[b]]]);before=bk.obj
            for j in range(0,len(support),2):bk.apply(('pair',k,k,int(support[j]),int(support[j+1]),1,-1))
            bk.resync();assert bk.obj==before+delta and m.feasible(bk.W)
            return delta,depth,len(ii),len(score)
        if depth==depthmax:break
        rr=[];cc=[]
        for netbc in range(-2*depth,2*depth+1,2):
            flatix=np.flatnonzero(legal&(budget==netbc))
            if len(flatix):
                # A final signed support can arise through multiple pairings/orderings.
                # Keep distinct positive/negative support sets, not duplicate paths.
                count=min(beamwidth*(depth*depth+1)*2,len(flatix))
                sel=flatix[np.argpartition(cost.ravel()[flatix],count-1)[:count]]
                sel=sel[np.argsort(cost.ravel()[sel])]
                seen=set();kept=0
                for f in sel:
                    a,b=divmod(int(f),len(ii))
                    key=(tuple(sorted(list(assets[a,::2])+[int(ii[b])])),tuple(sorted(list(assets[a,1::2])+[int(jj[b])])))
                    if key in seen:continue
                    seen.add(key);rr.append(a);cc.append(b);kept+=1
                    if kept>=beamwidth:break
        if not rr:break
        rr=np.array(rr);cc=np.array(cc)
        assets=np.concatenate([assets[rr],np.stack([ii[cc],jj[cc]],axis=1)],axis=1)
        score=cost[rr,cc];bc=budget[rr,cc];grad=grad[rr]+pairgrad[cc]
    return 0,depthmax,len(ii),len(score)

def main():
    inst,start,out,secs,seed=sys.argv[1:];out=Path(out);out.mkdir(parents=True,exist_ok=True);(out/'pid.txt').write_text(str(os.getpid())+'\n')
    t0=time.time();end=t0+float(secs);rng=np.random.default_rng(int(seed));m=Model(inst,100,'0.01');bk=Book(m,m.read_solution(start));best=bk.obj;bestW=bk.W.copy()
    def mark(**kw):print(json.dumps(dict(seconds=round(time.time()-t0,3),**kw)),flush=True)
    def save():m.write_solution(out/'best.sol',bestW,'po_a400_t10_s00','0.01','X3 distinct-support beam heuristic; independently verify')
    save();mark(stage='start',objective=best);rounds=0;stalls=0
    while time.time()<end and not (out/'STOP').exists():
        rounds+=1;gain=False
        depth=2 if rounds==1 else 3 if rounds==2 else 4
        for k in rng.permutation(9):
            if time.time()>=end or (out/'STOP').exists():break
            k=int(k);delta,d,p,b=beam_move(bk,k,rng,160 if rounds<3 else 320,96 if rounds<3 else 192,depth)
            if delta<0:
                gain=True;bk.blocks=[(k,k)];steps,local=bk.descend(min(end,time.time()+45))
                mark(stage='gain',round=rounds,period=k,delta=delta,depth=d,pairs=p,beam=b,objective=bk.obj,descent=steps)
                if bk.obj<best:best=bk.obj;bestW=bk.W.copy();save()
        mark(stage='round',round=rounds,depth=depth,best=best,current=bk.obj)
        stalls=0 if gain else stalls+1
        if stalls>=3:
            bk.W=bestW.copy();bk.resync();k=int(rng.integers(9));bk.blocks=[(k,k)];done=0
            for _ in range(800):
                i,j=rng.choice(m.n,2,replace=False);a=int(rng.choice([-1,1]));w=bk.W[k].copy();w[i]+=a;w[j]-=a
                if abs(w).max()<=3 and abs(w).sum()<=100:
                    bk.apply(('pair',k,k,int(i),int(j),a,-a));done+=1
                    if done>=2+rounds%6:break
            bk.resync();steps,local=bk.descend(min(end,time.time()+45));stalls=0
            if bk.obj<best:best=bk.obj;bestW=bk.W.copy();save()
            mark(stage='kick',round=rounds,period=k,objective=bk.obj,steps=steps)
    mark(stage='done',rounds=rounds,objective=best)

if __name__=='__main__':main()
