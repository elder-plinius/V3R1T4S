"""Precise final polish (penalty-threshold descent, H4 machinery) with the C L-BFGS of liblse3.so."""
import ctypes, os, time
import numpy as np
import bsopt as B

_lib3 = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), "liblse3.so"))
_dp = ctypes.POINTER(ctypes.c_double)
_lib3.lbfgs_pen.restype = ctypes.c_double
_lib3.lbfgs_pen.argtypes = [ctypes.c_int, ctypes.c_int, _dp, ctypes.c_double, ctypes.c_int, ctypes.c_int, _dp, _dp]
_lib3.lbfgs_polish.restype = ctypes.c_double
_lib3.lbfgs_polish.argtypes = [ctypes.c_int, ctypes.c_int, _dp, ctypes.c_int, _dp, ctypes.c_int, ctypes.c_int, _dp, _dp]
_MEM = 10


def pen_polish(obj, Y, t, maxiter=3000):
    N, d = obj.N, obj.d
    n = N * d
    if not hasattr(obj, "lw"):
        obj.lw = np.zeros((2 * _MEM + 4) * n + 2 * _MEM + 8)
    x = np.ascontiguousarray(B.normalize(Y).ravel(), dtype=np.float64).copy()
    c = _lib3.lbfgs_pen(N, d, x.ctypes.data_as(_dp), float(t), int(maxiter), _MEM, obj.wp, obj.lw.ctypes.data_as(_dp))
    return x.reshape(N, d), c


def precise(obj, Y, time_cap=30.0, delta0=1e-7, maxiter=3000):
    """Threshold descent: t = c - delta; accept the penalty minimiser if its cmax < c; adapt delta."""
    t0 = time.time()
    Y = B.normalize(Y)
    c = obj.cmax(Y)
    delta = delta0
    steps = 0
    while time.time() - t0 < time_cap and delta > 1e-16:
        Z, cz = pen_polish(obj, Y, c - delta, maxiter)
        steps += 1
        if cz < c:
            Y, c = Z, cz
            delta *= 2.0
        else:
            delta *= 0.3
    return Y, c, steps
