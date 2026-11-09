"""Vectorized re-implementation of the official iea37-aepcalc.py (case study 1), plus analytic gradient.
Same equations: simplified Bastankhah Gaussian wake, sqrt-sum-of-squares superposition, cubic power curve."""
import numpy as np, yaml, os
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', '..', 'data', 'cs1-2')
DIRS = np.arange(16) * 22.5
FREQ = np.array([.025, .024, .029, .036, .063, .065, .100, .122, .063, .038, .039, .083, .213, .046, .032, .022])
U = 9.8; D = 130.0; CI = 4.0; CO = 25.0; RWS = 9.8; RP = 3350000.0
CT = 4.0*1./3.*(1.0-1./3.); K = 0.0324555
RADIUS = {16: 1300.0, 36: 2000.0, 64: 3000.0}
th = np.radians(270. - DIRS)
COS = np.cos(-th); SIN = np.sin(-th)

def frames(x, y):
    fx = x[None, :]*COS[:, None] - y[None, :]*SIN[:, None]
    fy = x[None, :]*SIN[:, None] + y[None, :]*COS[:, None]
    return fx, fy

def dir_power(x, y):
    fx, fy = frames(x, y)
    dx = fx[:, :, None] - fx[:, None, :]   # [d, i, j] = x_i - x_j
    dy = fy[:, :, None] - fy[:, None, :]
    m = dx > 0.
    dxs = np.where(m, dx, 1.0)
    sigma = K*dxs + D/np.sqrt(8.)
    ex = np.exp(-0.5*(dy/sigma)**2)
    rad = 1. - CT/(8.*sigma**2/D**2)
    la = np.where(m, (1.-np.sqrt(rad))*ex, 0.)
    loss = np.sqrt(np.sum(la**2, axis=2))
    v = U*(1.-loss)
    p = np.where((CI <= v) & (v < RWS), RP*((v-CI)/(RWS-CI))**3, np.where((RWS <= v) & (v < CO), RP, 0.))
    return p.sum(axis=1)

def aep(x, y):
    return float(np.sum(8760.*FREQ*dir_power(x, y))/1e6)

def aep_grad(x, y):
    """AEP and analytic gradient d AEP / d(x,y) (valid where no turbine sits exactly at a power-curve kink or x-tie)."""
    fx, fy = frames(x, y)
    dx = fx[:, :, None] - fx[:, None, :]
    dy = fy[:, :, None] - fy[:, None, :]
    m = dx > 0.
    dxs = np.where(m, dx, 1.0)
    sigma = K*dxs + D/np.sqrt(8.)
    ex = np.exp(-0.5*(dy/sigma)**2)
    rad = 1. - CT/(8.*sigma**2/D**2)
    sq = np.sqrt(rad)
    la = np.where(m, (1.-sq)*ex, 0.)
    S = np.sum(la**2, axis=2)
    loss = np.sqrt(S)
    v = U*(1.-loss)
    reg = (CI <= v) & (v < RWS)
    p = np.where(reg, RP*((v-CI)/(RWS-CI))**3, np.where((RWS <= v) & (v < CO), RP, 0.))
    w = 8760.*FREQ/1e6
    A = float(np.sum(w*p.sum(axis=1)))
    dp_dv = np.where(reg, 3*RP*(v-CI)**2/(RWS-CI)**3, 0.)
    safe = np.where(loss > 0, loss, 1.0)
    dv_dla = np.where(loss[:, :, None] > 0, -U*la/safe[:, :, None], 0.)   # d v_i / d la_ij
    # d la / d sigma, d la / d dy
    drad_ds = CT*D**2*2/(8.*sigma**3)
    dsq_ds = drad_ds/(2*sq)
    dla_ds = (-dsq_ds)*ex + (1.-sq)*ex*(dy**2/sigma**3)
    dla_ddx = np.where(m, dla_ds*K, 0.)
    dla_ddy = np.where(m, (1.-sq)*ex*(-dy/sigma**2), 0.)
    G = (w[:, None]*dp_dv)[:, :, None]*dv_dla    # dA / d la_ij  [d,i,j]
    gdx = G*dla_ddx; gdy = G*dla_ddy
    gfx = gdx.sum(axis=2) - gdx.sum(axis=1)
    gfy = gdy.sum(axis=2) - gdy.sum(axis=1)
    gx = np.sum(gfx*COS[:, None] + gfy*SIN[:, None], axis=0)
    gy = np.sum(-gfx*SIN[:, None] + gfy*COS[:, None], axis=0)
    return A, gx, gy

def load(f):
    d = yaml.safe_load(open(f))['definitions']['position']['items']
    return np.asarray(d['xc'], float), np.asarray(d['yc'], float)

def feas(x, y):
    n = len(x); r = np.hypot(x, y)
    dist = np.hypot(x[:, None]-x[None, :], y[:, None]-y[None, :]); dist[np.diag_indices(n)] = np.inf
    return RADIUS[n]-r.max(), dist.min()-2*D
