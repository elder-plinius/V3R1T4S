import os, sys, re, json, numpy as np
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RUN, 'checker'))
import glue, lead
from scipy.optimize import minimize
D = os.path.join(RUN, 'data')
def table(metal):
    f = 'Al_table.html' if metal == 'Al' else 'lead_table.html'
    html = open(os.path.join(D, f)).read()
    rows = re.findall(r'points/(\d+)">\d+</A></TD>\s*<TD[^>]*>.*?</TD>\s*<TD[^>]*>\s*([-\d.]+)\s*</TD>', html, re.S)
    return {int(n): float(e) for n, e in rows}
def posted(metal, n):
    return glue.load(os.path.join(D, 'Al_points' if metal == 'Al' else 'lead_points', str(n)))
EG = {'Al': glue.eg, 'Pb': lead.eg}
def relax(metal, X, gtol=1e-6, maxiter=3000):
    r = minimize(EG[metal], np.asarray(X, float).ravel(), jac=True, method='L-BFGS-B',
                 options={'gtol': gtol, 'ftol': 1e-15, 'maxiter': maxiter})
    return r.fun, r.x.reshape(-1, 3)
def surface_sites(X, k=60, rng=None, d0=2.8):
    """Candidate adatom positions: outward along directions from centroid, placed at d0 beyond the outermost atom near that direction."""
    rng = rng or np.random.default_rng()
    c = X.mean(0); out = []
    for _ in range(k):
        u = rng.normal(size=3); u /= np.linalg.norm(u)
        proj = (X - c) @ u
        out.append(c + u * (proj.max() + 0.8 * d0))
    return out
