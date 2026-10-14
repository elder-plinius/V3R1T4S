"""Fast Thomson polisher: numba-jitted Coulomb energy+gradient, scipy L-BFGS, seed generators, defect-aware kicks."""
import numpy as np, re, math
from numba import njit
from scipy.optimize import minimize
from scipy.spatial import ConvexHull

@njit(cache=True, fastmath=False)
def _eg(x):
    n = x.size // 3
    U = np.empty((n, 3)); nr = np.empty(n)
    for i in range(n):
        a = math.sqrt(x[3*i]**2 + x[3*i+1]**2 + x[3*i+2]**2); nr[i] = a
        U[i, 0] = x[3*i]/a; U[i, 1] = x[3*i+1]/a; U[i, 2] = x[3*i+2]/a
    G = np.zeros((n, 3)); E = 0.0
    for i in range(n):
        ei = 0.0
        for j in range(i+1, n):
            dx = U[i, 0]-U[j, 0]; dy = U[i, 1]-U[j, 1]; dz = U[i, 2]-U[j, 2]
            r2 = dx*dx+dy*dy+dz*dz; ir = 1.0/math.sqrt(r2); ir3 = ir*ir*ir
            ei += ir
            G[i, 0] -= dx*ir3; G[i, 1] -= dy*ir3; G[i, 2] -= dz*ir3
            G[j, 0] += dx*ir3; G[j, 1] += dy*ir3; G[j, 2] += dz*ir3
        E += ei
    g = np.empty(3*n)
    for i in range(n):
        d = G[i, 0]*U[i, 0]+G[i, 1]*U[i, 1]+G[i, 2]*U[i, 2]
        for k in range(3):
            g[3*i+k] = (G[i, k]-d*U[i, k])/nr[i]
    return E, g

def eg(x): return _eg(np.ascontiguousarray(x, dtype=np.float64))

def norm(P): return P/np.linalg.norm(P, axis=1)[:, None]

def energy(P):
    """float64 pairwise sum, sorted (accurate reference, numpy)."""
    U = norm(P); i, j = np.triu_indices(len(U), 1)
    return float(np.sum(np.sort(1.0/np.linalg.norm(U[i]-U[j], axis=1))))

def polish(P, gtol=1e-6, maxiter=20000, maxcor=20):
    r = minimize(eg, norm(P).ravel(), jac=True, method='L-BFGS-B',
                 options=dict(gtol=gtol, ftol=1e-16 if gtol < 1e-8 else 2.2e-12, maxiter=maxiter, maxcor=maxcor))
    Q = norm(r.x.reshape(-1, 3)); return Q, float(r.fun), int(r.nit)

def fine(P): Q, _, _ = polish(P, gtol=1e-12, maxcor=30); return Q, energy(Q)

def load_pts(f):
    v = [float(x) for x in open(f).read().split() if re.match(r'^[-+0-9.eE]+$', x)]
    return norm(np.array(v[:len(v)//3*3]).reshape(-1, 3))

# ---------- seeds ----------
def spiral(N, offset=0.5, rng=None, jitter=0.0):
    """generalized spiral (Rakhmanov-Saff-Zhou / Fibonacci) layout."""
    k = np.arange(N); z = 1-2*(k+offset)/N; th = np.pi*(3-np.sqrt(5))*k
    if rng is not None: th = th + rng.uniform(0, 2*np.pi)
    r = np.sqrt(1-z*z); P = np.c_[r*np.cos(th), r*np.sin(th), z]
    if jitter and rng is not None: P = P+rng.normal(scale=jitter, size=P.shape)
    return norm(P)

def rsz_spiral(N):
    z = -1+2*np.arange(N)/(N-1); ph = np.zeros(N)
    for k in range(1, N-1): ph[k] = (ph[k-1]+3.6/np.sqrt(N*(1-z[k]**2))) % (2*np.pi)
    r = np.sqrt(np.clip(1-z*z, 0, 1)); return norm(np.c_[r*np.cos(ph), r*np.sin(ph), z])

def random_pts(N, rng): return norm(rng.normal(size=(N, 3)))

def remove_point(P, rng):
    """N+1 -> N: remove a point (prefer defects / high local energy)."""
    c = coordination(P); cand = np.where(c != 6)[0]
    i = rng.choice(cand) if len(cand) and rng.random() < 0.7 else rng.integers(len(P))
    return np.delete(P, i, axis=0)

def add_point(P, rng):
    """N-1 -> N: insert at a large hole (circumcentre of a big hull facet)."""
    h = ConvexHull(P); T = P[h.simplices]
    c = norm(np.cross(T[:, 1]-T[:, 0], T[:, 2]-T[:, 0]))
    c *= np.sign((c*T[:, 0]).sum(1))[:, None]
    rad = np.linalg.norm(T[:, 0]-c, axis=1); top = np.argsort(rad)[-8:]
    return np.vstack([P, c[rng.choice(top)]])

# ---------- defects ----------
def coordination(P):
    h = ConvexHull(P); n = len(P); nb = [set() for _ in range(n)]
    for a, b, c in h.simplices:
        nb[a] |= {b, c}; nb[b] |= {a, c}; nb[c] |= {a, b}
    return np.array([len(s) for s in nb])

def defect_kick(P, rng, mode=None):
    """perturb a defect cluster (5/7-coordinated points and their neighbourhood)."""
    c = coordination(P); D = np.where(c != 6)[0]
    if len(D) == 0: D = np.arange(len(P))
    mode = mode or rng.choice(['rotate', 'jiggle', 'swap', 'move'])
    k = rng.choice(D); ctr = P[k]
    ang = rng.uniform(0.12, 0.35); m = P@ctr > np.cos(ang)
    Q = P.copy()
    if mode == 'rotate':
        a = rng.uniform(0.2, 1.2)*rng.choice([-1, 1])
        K = np.array([[0, -ctr[2], ctr[1]], [ctr[2], 0, -ctr[0]], [-ctr[1], ctr[0], 0]])
        R = np.eye(3)+np.sin(a)*K+(1-np.cos(a))*K@K; Q[m] = Q[m]@R.T
    elif mode == 'jiggle':
        Q[m] += rng.normal(scale=rng.uniform(0.02, 0.06), size=(m.sum(), 3))
    elif mode == 'swap':
        # move a defect point to another defect region (glides a disclination)
        j = rng.choice(D); Q[k] = P[j]+rng.normal(scale=0.03, size=3)
        Q[m] += rng.normal(scale=0.01, size=(m.sum(), 3))
    else:  # remove the defect point and re-insert at largest hole
        Q = add_point(np.delete(P, k, axis=0), rng)
    return norm(Q)
