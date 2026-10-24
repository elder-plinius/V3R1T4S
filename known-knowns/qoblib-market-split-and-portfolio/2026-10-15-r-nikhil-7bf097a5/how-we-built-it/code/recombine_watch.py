"""Continuing chain-DP recombination of independent live search checkpoints."""
from pathlib import Path
import os,sys,time,json
import numpy as np
from pfmodel import Model
from quoter2 import Book
from long_periods import mix

def main():
    inst,run,out,secs=sys.argv[1:];run=Path(run);out=Path(out);out.mkdir(parents=True,exist_ok=True);(out/'pid.txt').write_text(str(os.getpid())+'\n')
    t0=time.time();end=t0+float(secs);m=Model(inst,100,'0.01');best=10**30;old_state=None;checks=0
    def mark(**kw):print(json.dumps(dict(seconds=round(time.time()-t0,3),**kw)),flush=True)
    paths=[run/'candidate.sol']
    while time.time()<end and not (out/'STOP').exists():
        sols=paths+sorted((run/'attempts/quoter').glob('*/best.sol'))+sorted((run/'attempts/solver').glob('*/best.sol'))
        sols=[p for p in sols if p.parent!=out]
        pools=[{} for _ in range(9)];used=[];state=[]
        for p in sols:
            try:
                a=p.read_bytes();b=p.read_bytes()
                if a!=b:continue
                temp=out/'snapshot.sol';temp.write_bytes(a);W=m.read_solution(temp)
                declared=next(int(s.split()[1]) for s in a.decode().splitlines() if s.startswith('objective '))
                if not m.feasible(W) or W[9].any() or m.objective(W)!=declared:continue
                for k in range(9):pools[k][W[k].tobytes()]=W[k].copy()
                used.append([str(p.relative_to(run)),declared]);state.append((str(p),declared))
            except (ValueError,OSError,StopIteration,IndexError):continue
        for p in sorted((run/'attempts/quoter').glob('*/pool-*.npz')):
            try:
                stamp=p.stat().st_mtime_ns
                with np.load(p) as z:rows=z['rows'].copy();k=int(z['period'])
                if p.stat().st_mtime_ns!=stamp:continue
                for w in rows:
                    if abs(w).max()<=3 and abs(w).sum()<=100 and -5<=w.sum()<=10:pools[k][w.tobytes()]=w.copy()
                state.append((str(p),stamp))
            except (ValueError,OSError,EOFError,KeyError):continue
        if old_state!=state and all(pools):
            old_state=state;checks+=1;W=mix(m,pools);raw=m.objective(W)
            bk=Book(m,W);steps,local=bk.descend(min(end,time.time()+45));val=bk.obj
            assert m.objective(bk.W)==val and m.feasible(bk.W)
            if val<best:
                best=val;m.write_solution(out/'best.sol',bk.W,'po_a400_t10_s00','0.01','X3 continuing pool-DP recombination; independently verify')
                (out/f'best-{checks:04d}.sol').write_bytes((out/'best.sol').read_bytes())
            mark(stage='mix',check=checks,inputs=used,pools=[len(p) for p in pools],raw=raw,descent_steps=steps,local=local,objective=val,best=best)
        # Cooperative, short sleep; the operator can touch STOP. The parent keeps communicating.
        for _ in range(45):
            if time.time()>=end or (out/'STOP').exists():break
            time.sleep(1)
    mark(stage='done',checks=checks,objective=best)

if __name__=='__main__':main()
