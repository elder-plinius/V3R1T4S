import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iea37 import load, aep, feas, DATA
from wflo import polish, make_feasible, strict_ok, save
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out'); os.makedirs(out, exist_ok=True)
for n in (64, 36):
    x, y = load(os.path.join(DATA, 'iea37-cs1-results', 'iea37-par12-opt%d.yaml' % n))
    a0 = aep(x, y); print(n, 'par12 as posted', a0, feas(x, y))
    xf, yf = make_feasible(x, y)
    print(n, 'radially repaired', aep(xf, yf), feas(xf, yf), strict_ok(xf, yf))
    xp, yp = polish(xf, yf, xi=1.0, maxiter=1000, ftol=1e-12)
    print(n, 'polished', aep(xp, yp), feas(xp, yp), strict_ok(xp, yp), 'gain vs par12 %.5f' % (aep(xp, yp)-a0),
          'max move %.4f m' % np.max(np.hypot(xp-x, yp-y)))
    save(os.path.join(out, 'par12_polished_%d.json' % n), xp, yp)
