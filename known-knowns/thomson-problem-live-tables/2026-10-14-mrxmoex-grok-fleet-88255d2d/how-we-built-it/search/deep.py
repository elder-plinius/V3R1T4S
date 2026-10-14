import sys,os; [os.environ.setdefault(v,"1") for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS")]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import numpy as np, fastpol as F
x=F.norm(np.loadtxt(sys.argv[1])).ravel(); g=F.eg(x)[1]; a=1e-6
for it in range(50000):
    xn=F.norm((x-a*g).reshape(-1,3)).ravel(); gn=F.eg(xn)[1]; s=xn-x; y=gn-g
    a=min(abs(s@s/(s@y)) if s@y!=0 else 1e-6,1e-3); x,g=xn,gn
    if abs(g).max()<1e-10: break
np.savetxt(sys.argv[2],x.reshape(-1,3),fmt='%.20f'); print('it',it,'gmax %.2e'%abs(g).max(),'E64 %.9f'%F.energy(x.reshape(-1,3)))
