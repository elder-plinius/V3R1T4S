"""Ercolessi-Adams Al glue potential: coefficients parsed from the archived aluminum.f (data/), C core + mpmath reference."""
import ctypes, os, re, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'data', 'aluminum.f')
def parse(src=SRC):
    txt = open(src).read().replace('D', 'E').replace('d+', 'E+').replace('d-', 'E-')
    out = {}
    for tag in ('v2', 'rh', 'uu'):
        arrs = {}
        for c in 'xybcd':
            vals = re.findall(r'data\s+%s%s\(\s*(\d+)\)\s*/\s*([-+.\dE]+)\s*/' % (c, tag), txt)
            arrs[c] = [float(v) for _, v in sorted(vals, key=lambda t: int(t[0]))]
        out[tag] = arrs
    am = re.findall(r'parameter \((arg(?:max|min))=\s*([-+.\dE]+)\)', txt)
    out['argmax_v2'], out['argmax_rh'], out['argmin_uu'] = float(am[0][1]), float(am[1][1]), float(am[2][1])
    return out
C = parse()
_tab = []
for tag in ('v2', 'rh', 'uu'):
    _tab.append(len(C[tag]['x']))
    for c in 'xybcd': _tab += C[tag][c]
_tab += [C['argmax_v2'], C['argmax_rh'], C['argmin_uu']]
_tab = np.array(_tab, float)
_lib = ctypes.CDLL(os.path.join(HERE, 'libglue.dylib'))
_lib.glue_eg.restype = ctypes.c_double
_lib.glue_eg.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
_lib.glue_init.argtypes = [ctypes.c_void_p]
_lib.glue_init(_tab.ctypes.data)
def eg(x):
    x = np.ascontiguousarray(x, float).ravel(); g = np.empty_like(x)
    return _lib.glue_eg(len(x) // 3, x.ctypes.data, g.ctypes.data), g
def energy(x): return eg(x)[0]
def load(path):
    return np.array([[float(v) for v in l.split()] for l in open(path) if l.strip()])
# mpmath reference (same spline semantics), for certification
def _sev_mp(a, u):
    import mpmath as mp
    xs = a['x']; n = len(xs)
    if u < xs[0]: i = 0
    else:
        i, j = 0, n
        while j > i + 1:
            k = (i + j) // 2
            if u < xs[k]: j = k
            else: i = k
    dx = u - mp.mpf(xs[i])
    return mp.mpf(a['y'][i]) + dx*(mp.mpf(a['b'][i]) + dx*(mp.mpf(a['c'][i]) + dx*mp.mpf(a['d'][i])))
def energy_mp(X, dps=30):
    import mpmath as mp
    mp.mp.dps = dps
    X = [[mp.mpf(repr(float(v))) if not isinstance(v, mp.mpf) else v for v in row] for row in X]
    n = len(X); rho = [mp.mpf(0)]*n; E = mp.mpf(0)
    for i in range(n):
        for j in range(i+1, n):
            r = mp.sqrt(sum((X[i][k]-X[j][k])**2 for k in range(3)))
            if r >= C['argmax_v2']: continue
            E += _sev_mp(C['v2'], r); f = _sev_mp(C['rh'], r) if r < C['argmax_rh'] else 0
            rho[i] += f; rho[j] += f
    for i in range(n):
        if rho[i] > C['argmin_uu']: E += _sev_mp(C['uu'], rho[i])
    return E
