import ctypes, os, numpy as np
_lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'librelax.so'))
_P = ctypes.POINTER(ctypes.c_double)
_lib.relax.argtypes = [_P, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int]
_lib.relax.restype = ctypes.c_int
_lib.feasible.argtypes = [_P, ctypes.c_int]
_lib.feasible.restype = ctypes.c_double
D = 4

def table(path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/packomania.com_hsp4_txt_radius.txt')):
    t = {}
    for line in open(path):
        p = line.split()
        if len(p) >= 2 and p[0].isdigit(): t[int(p[0])] = float(p[1])
    return t

def relax(x, r0, k0=1e2, k1=1e11, kfac=10.0, maxit=4000):
    n = x.shape[0]
    v = np.ascontiguousarray(np.concatenate([x.ravel(), [r0]]), dtype=np.float64)
    _lib.relax(v.ctypes.data_as(_P), n, k0, k1, kfac, maxit)
    y = np.ascontiguousarray(v[:-1].reshape(n, D).copy())
    r = _lib.feasible(y.ctypes.data_as(_P), n)
    return y, r

def feasible_np(x):
    from scipy.spatial.distance import pdist
    return min(pdist(x).min() / 2, 1 - np.linalg.norm(x, axis=1).max())

_mc = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libmc.so'))
_mc.mc.argtypes = [_P, ctypes.c_int, _P, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_uint64]
_mc.mc.restype = ctypes.c_double
def mc(x, r, nsweeps, growth=0.3, step0=0.5, seed=1):
    x = np.ascontiguousarray(x, dtype=np.float64).copy()
    rr = ctypes.c_double(r)
    rate = _mc.mc(x.ctypes.data_as(_P), x.shape[0], ctypes.byref(rr), nsweeps, growth, step0, seed)
    return x, rr.value, rate

def random_feasible(N, rng):
    x = rng.normal(size=(N, 4)); x /= np.linalg.norm(x, axis=1)[:, None]
    x *= rng.random(N)[:, None] ** 0.25 * 0.9
    return x, max(1e-6, feasible_np(x) * 0.999)

_lib.riesz_anneal.argtypes = [_P, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int]
def riesz(x, p0=6, p1=96, pfac=2, maxit=3000):
    n = x.shape[0]
    v = np.ascontiguousarray(np.concatenate([x.ravel(), [0.0]]), dtype=np.float64)
    _lib.riesz_anneal(v.ctypes.data_as(_P), n, p0, p1, pfac, maxit)
    return v[:-1].reshape(n, D).copy()
