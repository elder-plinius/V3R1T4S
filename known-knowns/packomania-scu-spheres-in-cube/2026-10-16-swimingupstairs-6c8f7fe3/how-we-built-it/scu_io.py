"""Float loaders shared by attack code (the 50-digit checker is scu_check.py)."""
import numpy as np
from scipy.spatial import cKDTree
D='./data/'
T={int(l.split()[0]):float(l.split()[1]) for l in open(D+'radius.txt') if l.strip() and not l.startswith('#')}
TS={int(l.split()[0]):l.split()[1] for l in open(D+'radius.txt') if l.strip() and not l.startswith('#')}
def loadf(path):
    R=[l.split() for l in open(path) if l.strip() and not l.lstrip().startswith('#') and len(l.split())>=3]
    return np.array([[float(v) for v in (r[1:4] if len(r)>=4 else r[-3:])] for r in R])
def load(N): return loadf(D+'coords/scu%d.txt'%N)
def rad(X):
    d,_=cKDTree(X).query(X,2); return min(d[:,1].min()/2,0.5-np.abs(X).max())
