"""Combine shortlisted disjoint balanced exchanges, then exact pair descent.
Search heuristic only; final objects require independent rational verification.
"""
import os,sys,time,json
from pathlib import Path
import numpy as np
from pfmodel import Model
from quoter2 import Book

def four_move(bk,k,rng,width=192,random_n=64):
    m=bk.m; w=bk.W[k]; slack=m.B-int(np.abs(w).sum())
    plus, vp, bp=bk.block_single(k,k,1)
    minus,vm,bm=bk.block_single(k,k,-1)
    i,j=np.nonzero(vp[:,None]&vm[None,:]&~np.eye(m.n,dtype=bool))
    v=plus[i]+minus[j]-m.Qs[k,i,j]
    bc=bp[0,i]+bm[0,j]
    chosen=[]
    for b in [-2,0,2]:
        ix=np.flatnonzero(bc==b)
        if len(ix):
            take=min(width,len(ix)); z=ix[np.argpartition(v[ix],take-1)[:take]]
            chosen.extend(z.tolist())
            if len(ix)>take: chosen.extend(rng.choice(ix,min(random_n,len(ix)),replace=False).tolist())
    z=np.unique(chosen); i,j,v,bc=i[z],j[z],v[z],bc[z]
    q=m.Qs[k]
    M=v[:,None]+v[None,:]+q[i[:,None],i]-q[i[:,None],j]-q[j[:,None],i]+q[j[:,None],j]
    ok=(i[:,None]!=i)&(i[:,None]!=j)&(j[:,None]!=i)&(j[:,None]!=j)&(bc[:,None]+bc<=slack)
    M[~ok]=np.iinfo(np.int64).max//4
    z=int(np.argmin(M)); a,b=divmod(z,len(i)); delta=int(M[a,b])
    if delta<0:
        before=bk.obj
        bk.apply(('pair',k,k,int(i[a]),int(j[a]),1,-1))
        bk.apply(('pair',k,k,int(i[b]),int(j[b]),1,-1))
        bk.resync()
        assert bk.obj==before+delta and m.feasible(bk.W),(before,delta,bk.obj)
        return delta,[int(i[a]),int(j[a]),int(i[b]),int(j[b])],len(i)
    return 0,None,len(i)

def main():
    inst,start,out,secs,seed=sys.argv[1:]; out=Path(out); out.mkdir(parents=True,exist_ok=True)
    Path(out/'pid.txt').write_text(str(os.getpid())+'\n')
    t0=time.time(); deadline=t0+float(secs); rng=np.random.default_rng(int(seed))
    m=Model(inst,100,'0.01'); W=m.read_solution(start); bk=Book(m,W)
    def mark(**kw):
        print(json.dumps(dict(seconds=round(time.time()-t0,3),**kw)),flush=True)
    mark(stage='loaded',objective=bk.obj,feasible=m.feasible(W),fallbacks=m.n_exact_fallback)
    np.savez(out/'model-cache.npz',Q=m.Q,Qs=m.Qs,r=m.r,d=m.d,s=m.s,order=np.array(m.order),W=W)
    steps,local=bk.descend(min(deadline,time.time()+120))
    mark(stage='initial_pair_descent',steps=steps,local=local,objective=bk.obj)
    best=bk.obj; bestW=bk.W.copy(); m.write_solution(out/'best.sol',bestW,'po_a400_t10_s00','0.01','X3 four-exchange heuristic; independently verify')
    # Test three distinct shortlist widths before scaling. All time-limited searches.
    for width in [64,192,512]:
        for k in range(9):
            if time.time()>=deadline: break
            delta,mv,n=four_move(bk,k,rng,width,width//4)
            mark(stage='four_move',width=width,period=k,delta=delta,pairs=n,objective=bk.obj)
            if delta<0:
                bk.blocks=[(k,k)]; steps,local=bk.descend(min(deadline,time.time()+60))
                mark(stage='after_four_descent',period=k,steps=steps,local=local,objective=bk.obj)
                if bk.obj<best:
                    best=bk.obj;bestW=bk.W.copy();m.write_solution(out/'best.sol',bestW,'po_a400_t10_s00','0.01','X3 four-exchange heuristic; independently verify')
    rounds=0; stalls=0
    while time.time()<deadline:
        rounds+=1; improved=False
        for k in rng.permutation(9):
            if time.time()>=deadline: break
            k=int(k); delta,mv,n=four_move(bk,k,rng,384,192)
            if delta<0:
                improved=True; bk.blocks=[(k,k)];steps,local=bk.descend(min(deadline,time.time()+75))
                mark(stage='round_improvement',round=rounds,period=k,delta=delta,steps=steps,objective=bk.obj)
                if bk.obj<best:
                    best=bk.obj;bestW=bk.W.copy();m.write_solution(out/'best.sol',bestW,'po_a400_t10_s00','0.01','X3 four-exchange heuristic; independently verify')
        stalls=0 if improved else stalls+1
        mark(stage='round_end',round=rounds,best=best,current=bk.obj,stalls=stalls)
        if stalls>=3:
            # A small feasible net-preserving kick and local descent is a new book;
            # retain the best checkpoint and vary the period/basin.
            bk.W=bestW.copy();bk.resync();k=int(rng.integers(9));bk.blocks=[(k,k)]
            done=0
            for _ in range(400):
                i,j=rng.choice(m.n,2,replace=False);a=int(rng.choice([-1,1])); ww=bk.W[k].copy();ww[i]+=a;ww[j]-=a
                if abs(ww).max()<=3 and abs(ww).sum()<=100:
                    bk.apply(('pair',k,k,int(i),int(j),a,-a));done+=1
                    if done>=4+rounds%5:break
            bk.resync();steps,local=bk.descend(min(deadline,time.time()+120));stalls=0
            mark(stage='kick_descent',period=k,kicks=done,steps=steps,objective=bk.obj)
            if bk.obj<best:
                best=bk.obj;bestW=bk.W.copy();m.write_solution(out/'best.sol',bestW,'po_a400_t10_s00','0.01','X3 four-exchange heuristic; independently verify')
    mark(stage='done',objective=best,rounds=rounds)

if __name__=='__main__': main()
