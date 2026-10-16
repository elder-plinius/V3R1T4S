"""check.py coords record [--mp] [--hess]: polish, report E, grad, Hessian (6 zero modes expected), beats record by 1e-5?"""
import sys,os,numpy as np; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from lj_lib import *
X=load(sys.argv[1]); rec=float(sys.argv[2]); E0=energy(X); Y=relax(X); E1,g=eg(Y)
print("N=%d E_input=%.9f E_polished=%.9f grad=%.2e"%(len(X),E0,E1,np.linalg.norm(g)))
if '--hess' in sys.argv:
    ev=hessian_eigs(Y); print("hess n_neg(<-1e-6)=%d n_zero(|ev|<1e-6)=%d lowest7=%s"%((ev<-1e-6).sum(),(abs(ev)<1e-6).sum(),np.round(ev[:7],8)))
if '--mp' in sys.argv: print("E_mp30=",energy_mp(Y))
print("record=%.6f diff=%.3e BEATS_RECORD_BY_1e-5=%s"%(rec,E1-rec,E1<rec-1e-5))
