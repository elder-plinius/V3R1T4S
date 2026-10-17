"""polish lens: pair-list versions of the C LSE ladder and of the penalty threshold descent (liblse4.so), for large N.
The list holds the pairs within W of the current max (rebuilt before every C call). The value returned by every C call
is the TRUE all-pairs float64 max (cmax), and the caller keeps a stage only if that true max drops, so the list is a
speed device only and can never make a worse code look better."""
import ctypes, os, time
import numpy as np
import bsopt as B

_l = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), "liblse4.so"))
_dp = ctypes.POINTER(ctypes.c_double)
_ip = ctypes.POINTER(ctypes.c_int)
_l.set_list.restype = None
_l.set_list.argtypes = [ctypes.c_int, _ip, _ip]
_l.lbfgs_polish_list.restype = ctypes.c_double
_l.lbfgs_polish_list.argtypes = [ctypes.c_int, ctypes.c_int, _dp, ctypes.c_int, _dp, ctypes.c_int, ctypes.c_int, _dp, _dp]
_l.lbfgs_pen_list.restype = ctypes.c_double
_l.lbfgs_pen_list.argtypes = [ctypes.c_int, ctypes.c_int, _dp, ctypes.c_double, ctypes.c_int, ctypes.c_int, _dp, _dp]
_MEM = 10


def set_window(O, Y, W):
    G = Y @ Y.T
    np.fill_diagonal(G, -3.0)
    c = G.max()
    I, J = np.nonzero(np.triu(G >= c - W, 1))
    O.LI = np.ascontiguousarray(I, dtype=np.int32)
    O.LJ = np.ascontiguousarray(J, dtype=np.int32)
    _l.set_list(int(O.LI.size), O.LI.ctypes.data_as(_ip), O.LJ.ctypes.data_as(_ip))
    return int(O.LI.size)


def _lw(O):
    if not hasattr(O, "lw"):
        O.lw = np.zeros((2 * _MEM + 4) * O.N * O.d + 2 * _MEM + 8)
    return O.lw


def lpolish(O, X, betas, maxiter=300, W=2e-3):
    N, d = O.N, O.d
    Y = B.normalize(X)
    set_window(O, Y, W)
    x = np.ascontiguousarray(Y.ravel(), dtype=np.float64).copy()
    bt = np.ascontiguousarray(np.array(betas, dtype=np.float64))
    c = _l.lbfgs_polish_list(N, d, x.ctypes.data_as(_dp), len(betas), bt.ctypes.data_as(_dp), int(maxiter), _MEM,
                             O.wp, _lw(O).ctypes.data_as(_dp))
    return x.reshape(N, d), c


def lpen(O, Y, t, maxiter=3000, W=1e-3):
    N, d = O.N, O.d
    Y = B.normalize(Y)
    set_window(O, Y, W)
    x = np.ascontiguousarray(Y.ravel(), dtype=np.float64).copy()
    c = _l.lbfgs_pen_list(N, d, x.ctypes.data_as(_dp), float(t), int(maxiter), _MEM, O.wp, _lw(O).ctypes.data_as(_dp))
    return x.reshape(N, d), c


def lprecise(O, Y, time_cap=30.0, delta0=1e-7, maxiter=3000, W=1e-3, c_stop=None):
    """bsprec.precise with the pair-list penalty; CPU-time cap."""
    t0 = time.process_time()
    Y = B.normalize(Y)
    c = O.cmax(Y)
    delta = delta0
    steps = 0
    while time.process_time() - t0 < time_cap and delta > 1e-16 and not (c_stop is not None and c <= c_stop):
        Z, cz = lpen(O, Y, c - delta, maxiter, W)
        steps += 1
        if cz < c:
            Y, c = Z, cz
            delta *= 2.0
        else:
            delta *= 0.3
    return Y, c, steps
