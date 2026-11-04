"""Longer per-period ILS, retaining pools and recombining by exact chain DP.
Independent final rational verification is mandatory. Cooperative STOP supported.
"""
import sys,time,json,os
from pathlib import Path
import numpy as np
from pfmodel import Model
from quoter2 import Book

def kick(bk,rng,k,n):
    done=0
    for _ in range(800):
        i,j=rng.choice(bk.m.n,2,replace=False);a=int(rng.choice([-1,1]));w=bk.W[k].copy();w[i]+=a;w[j]-=a
        if np.max(abs(w))<=3 and np.sum(abs(w))<=bk.m.B:
            bk.apply(('pair',k,k,int(i),int(j),a,-a));done+=1
            if done>=n:break
    bk.resync()

def mix(m,pools):
    cands=[list(p.values()) for p in pools];L=9
    node=[np.array([int(w@m.Q[k]@w+m.lin[k]@w+m.s[k]@np.maximum(-w,0)) for w in cands[k]]) for k in range(L)]
    cost=node[0]+np.array([int(m.d[0]@abs(w)) for w in cands[0]]);back=[None]
    for k in range(1,L):
        A=np.array(cands[k-1]);nc=np.zeros(len(cands[k]),dtype=np.int64);ix=np.zeros(len(nc),dtype=np.int64)
        for j,w in enumerate(cands[k]):
            z=abs(A-w)@m.d[k]+cost;ix[j]=np.argmin(z);nc[j]=z[ix[j]]+node[k][j]
        cost=nc;back.append(ix)
    j=int(np.argmin(cost));W=np.zeros((10,m.n),dtype=np.int64)
    for k in range(L-1,-1,-1):
        W[k]=cands[k][j]
        if k:j=int(back[k][j])
    assert m.feasible(W) and m.objective(W)==int(min(cost))-1000
    return W

def main():
    inst,start,out,secs,seed=sys.argv[1:];out=Path(out);out.mkdir(parents=True,exist_ok=True);(out/'pid.txt').write_text(str(os.getpid())+'\n')
    t0=time.time();deadline=t0+float(secs);rng=np.random.default_rng(int(seed));m=Model(inst,100,'0.01');W=m.read_solution(start);best=m.objective(W)
    pools=[{W[k].tobytes():W[k].copy()} for k in range(9)]
    def mark(**kw):print(json.dumps(dict(seconds=round(time.time()-t0,3),**kw)),flush=True)
    def save():m.write_solution(out/'best.sol',W,'po_a400_t10_s00','0.01','X3 longer period ILS and pool DP; independent verification required')
    save();mark(stage='start',objective=best)
    epoch=0
    while time.time()<deadline and not (out/'STOP').exists():
        epoch+=1
        for k in rng.permutation(9):
            k=int(k)
            if time.time()>=deadline or (out/'STOP').exists():break
            until=min(deadline,time.time()+(30 if epoch==1 else 120));bk=Book(m,W);bk.blocks=[(k,k)]
            cur=bk.obj;row=bk.W[k].copy();bestlocal=cur;localrow=row.copy();threshold=1500.;it=0;last=time.time()
            while time.time()<until and not (out/'STOP').exists():
                bk.W[k]=row;bk.resync();kick(bk,rng,k,[2,4,8][(epoch+k)%3]+int(rng.integers(4)))
                steps,local=bk.descend(until)
                if not local:break
                assert bk.obj==m.objective(bk.W) and m.feasible(bk.W)
                pools[k][bk.W[k].tobytes()]=bk.W[k].copy();it+=1
                if bk.obj<bestlocal:bestlocal=bk.obj;localrow=bk.W[k].copy()
                if bk.obj<cur+threshold:cur=bk.obj;row=bk.W[k].copy()
                threshold*=0.994
                if it%30==0:row=localrow.copy();cur=bestlocal;threshold=1500.
                if time.time()-last>=30:mark(stage='period_mark',epoch=epoch,period=k,iterations=it,bestlocal=bestlocal,pool=len(pools[k]));last=time.time()
            if bestlocal<best:W[k]=localrow;best=m.objective(W);save();mark(stage='period_gain',epoch=epoch,period=k,objective=best)
            # Keep useful states by their cost with current neighbours.
            if len(pools[k])>240:
                bk=Book(m,W);vals=[]
                for key,row0 in pools[k].items():
                    bk.W[k]=row0;vals.append((m.objective(bk.W),key))
                keep=[key for val,key in sorted(vals)[:240]];pools[k]={key:pools[k][key] for key in keep}
            pools[k][W[k].tobytes()]=W[k].copy()
            np.savez(out/f'pool-{k}.npz',rows=np.array(list(pools[k].values())),period=k)
            mark(stage='period_done',epoch=epoch,period=k,iterations=it,bestlocal=bestlocal,objective=best,pool=len(pools[k]))
        cand=mix(m,pools);val=m.objective(cand)
        if val<best:W=cand;best=val;save()
        mark(stage='epoch_done',epoch=epoch,objective=best,pools=[len(p) for p in pools])
    mark(stage='done',epochs=epoch,objective=best)

if __name__=='__main__':main()
