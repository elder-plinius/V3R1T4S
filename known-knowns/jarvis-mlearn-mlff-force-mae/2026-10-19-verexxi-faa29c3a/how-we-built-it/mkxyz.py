import sys; sys.path.insert(0,'src')
import numpy as np, mldata as m, os
from ase import Atoms
from ase.io import write
def mk(s, with_f=True):
    a=Atoms(s['z'],positions=s['pos'],cell=s['cell'],pbc=True)
    a.info['REF_energy']=s['e']; a.arrays['REF_forces']=s['f']; a.info['jid']=s['jid']
    return a
def build(el, out='work'):
    os.makedirs(f'{out}/{el}',exist_ok=True)
    tr=m.structs(el,'train')
    val=[s for i,s in enumerate(tr) if i%10==5]; fit=[s for i,s in enumerate(tr) if i%10!=5]
    write(f'{out}/{el}/fit.xyz',[mk(s) for s in fit]); write(f'{out}/{el}/val.xyz',[mk(s) for s in val])
    write(f'{out}/{el}/train_all.xyz',[mk(s) for s in tr])
    print(el,len(fit),len(val),len(tr))
if __name__=='__main__':
    for el in sys.argv[1:]: build(el)
