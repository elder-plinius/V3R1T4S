"""Fresh-start 36-turbine wrapper of the validated original-model engine."""
import argparse
import importlib.util
from pathlib import Path
import numpy as np

RUN=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('engine',RUN/'claim/author-code/search.py')
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
engine.N=36
engine.R=2000.
engine.PAIRS=np.triu_indices(36,1)
engine.SCALE=36*3.35*8760

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True)
    p.add_argument('--deadline',required=True);p.add_argument('--seed',type=int,default=20261136)
    p.add_argument('--max-restarts',type=int,default=1000000)
    p.add_argument('--maxiter',type=int,default=350)
    engine.run(p.parse_args())
