"""Check accepted beam deltas on real and synthetic net-changing fixtures."""
import sys,json
from pathlib import Path
import numpy as np
from pfmodel import Model
from quoter2 import Book
from net_beam import move

r=Path(sys.argv[1]);m=Model(r/'instance',100,'0.01');rng=np.random.default_rng(276)
for k in [0,4,8]:
    bk=Book(m,np.zeros((10,400),dtype=np.int64));before=bk.obj;delta,depth=move(bk,k,rng,32,24,3)
    record={'fixture':'actual_empty_book','period':k,'before':before,'delta':delta,'depth':depth,'after':bk.obj,'full_objective':m.objective(bk.W),'net':int(bk.W[k].sum()),'valid':bool(m.feasible(bk.W))}
    print(json.dumps(record),flush=True)
    assert bk.obj==before+delta==m.objective(bk.W) and m.feasible(bk.W)
original=m.lin.copy()
for k in [0,4,8]:
    for direction in [-1,1]:
        m.lin=original.copy();m.lin[k,:8]=-direction*1000000;m.r=10-m.lin
        bk=Book(m,np.zeros((10,400),dtype=np.int64));before=bk.obj;delta,depth=move(bk,k,rng,32,24,3)
        record={'fixture':'synthetic_linear_coefficients','period':k,'direction':direction,'before':before,'delta':delta,'depth':depth,'after':bk.obj,'full_objective':m.objective(bk.W),'net':int(bk.W[k].sum()),'valid':bool(m.feasible(bk.W))}
        print(json.dumps(record),flush=True)
        assert delta<0 and direction*int(bk.W[k].sum())>0 and bk.obj==before+delta==m.objective(bk.W) and m.feasible(bk.W)
print('NET_BEAM_FIXTURE_CHECK: PASS')
