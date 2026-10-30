"""Shared optimisation core: AEP with WEC wake-width factor xi, analytic gradient, SLSQP polish with exact constraints."""
import numpy as np, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iea37 import COS, SIN, FREQ, U, D, CI, CO, RWS, RP, CT, K, RADIUS, aep, feas
from scipy.optimize import minimize

W = 8760.*FREQ/1e6

def aep_grad_xi(x, y, xi=1.0):
    fx = x[None, :]*COS[:, None] - y[None, :]*SIN[:, None]
    fy = x[None, :]*SIN[:, None] + y[None, :]*COS[:, None]
    dx = fx[:, :, None] - fx[:, None, :]
    dy = fy[:, :, None] - fy[:, None, :]
    m = dx > 0.
    dxs = np.where(m, dx, 1.0)
    sigma = xi*(K*dxs + D/np.sqrt(8.))
    ex = np.exp(-0.5*(dy/sigma)**2)
    rad = 1. - CT/(8.*sigma**2/D**2)
    rad = np.maximum(rad, 1e-12)
    sq = np.sqrt(rad)
    la = np.where(m, (1.-sq)*ex, 0.)
    S = np.sum(la**2, axis=2)
    loss = np.sqrt(S)
    v = U*(1.-loss)
    reg = (CI <= v) & (v < RWS)
    p = np.where(reg, RP*((v-CI)/(RWS-CI))**3, np.where((RWS <= v) & (v < CO), RP, 0.))
    A = float(np.sum(W*p.sum(axis=1)))
    dp_dv = np.where(reg, 3*RP*(v-CI)**2/(RWS-CI)**3, 0.)
    safe = np.where(loss > 0, loss, 1.0)
    dv_dla = np.where(loss[:, :, None] > 0, -U*la/safe[:, :, None], 0.)
    drad_ds = CT*D**2*2/(8.*sigma**3)
    dsq_ds = drad_ds/(2*sq)
    dla_ds = (-dsq_ds)*ex + (1.-sq)*ex*(dy**2/sigma**3)
    dla_ddx = np.where(m, dla_ds*K*xi, 0.)
    dla_ddy = np.where(m, (1.-sq)*ex*(-dy/sigma**2), 0.)
    G = (W[:, None]*dp_dv)[:, :, None]*dv_dla
    gdx = G*dla_ddx; gdy = G*dla_ddy
    gfx = gdx.sum(axis=2) - gdx.sum(axis=1)
    gfy = gdy.sum(axis=2) - gdy.sum(axis=1)
    gx = np.sum(gfx*COS[:, None] + gfy*SIN[:, None], axis=0)
    gy = np.sum(-gfx*SIN[:, None] + gfy*COS[:, None], axis=0)
    return A, gx, gy

def polish(x, y, xi=1.0, margin=1e-6, maxiter=500, ftol=1e-10):
    n = len(x); R = RADIUS[n] - margin; Dmin = 2*D + margin
    iu, ju = np.triu_indices(n, 1)
    scale = 1e-3   # objective scaling
    def f(z):
        A, gx, gy = aep_grad_xi(z[:n], z[n:], xi)
        return -A*scale, -np.concatenate([gx, gy])*scale
    def cons(z):
        xx, yy = z[:n], z[n:]
        c1 = (R**2 - xx**2 - yy**2)/R**2
        c2 = ((xx[iu]-xx[ju])**2 + (yy[iu]-yy[ju])**2 - Dmin**2)/Dmin**2
        return np.concatenate([c1, c2])
    def jcons(z):
        xx, yy = z[:n], z[n:]
        J1 = np.zeros((n, 2*n)); J1[np.arange(n), np.arange(n)] = -2*xx/R**2; J1[np.arange(n), n+np.arange(n)] = -2*yy/R**2
        P = len(iu); J2 = np.zeros((P, 2*n)); ddx = 2*(xx[iu]-xx[ju])/Dmin**2; ddy = 2*(yy[iu]-yy[ju])/Dmin**2
        J2[np.arange(P), iu] = ddx; J2[np.arange(P), ju] = -ddx; J2[np.arange(P), n+iu] = ddy; J2[np.arange(P), n+ju] = -ddy
        return np.vstack([J1, J2])
    r = minimize(f, np.concatenate([x, y]), jac=True, method='SLSQP',
                 constraints=[{'type': 'ineq', 'fun': cons, 'jac': jcons}], options={'maxiter': maxiter, 'ftol': ftol})
    z = r.x
    return z[:n], z[n:]

def make_feasible(x, y, margin=1e-6):
    """Pull hubs inside the circle by scaling only offending hubs radially (does not touch spacing much)."""
    n = len(x); R = RADIUS[n] - margin
    r = np.hypot(x, y); s = np.where(r > R, R/r, 1.0)
    return x*s, y*s

def wec_run(x, y, xis=(3.0, 2.0, 1.5, 1.25, 1.0), **kw):
    for xi in xis:
        x, y = polish(x, y, xi=xi, **kw)
    return x, y

def strict_ok(x, y):
    sr, sd = feas(x, y)
    return sr >= 0 and sd >= 0

def save(path, x, y, **meta):
    json.dump(dict(x=list(map(float, x)), y=list(map(float, y)), aep=aep(x, y), **meta), open(path, 'w'))
