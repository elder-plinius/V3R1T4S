"""Host side of the GPU skew-symmetric LABS search (CuPy RawModule)."""
import os, glob, site, math
import numpy as np

def _nvrtc_path():
    for sp in site.getsitepackages():
        for sub in ('nvidia/cuda_nvrtc/lib', 'nvidia/cuda_runtime/lib'):
            p = os.path.join(sp, sub)
            if os.path.isdir(p) and p not in os.environ.get('LD_LIBRARY_PATH', ''):
                os.environ['LD_LIBRARY_PATH'] = p + ':' + os.environ.get('LD_LIBRARY_PATH', '')
_nvrtc_path()
import cupy as cp

HERE = os.path.dirname(os.path.abspath(__file__))
_mod = None
def module():
    global _mod
    if _mod is None:
        src = open(os.path.join(HERE, 'skew_kernels.cu')).read()
        _mod = cp.RawModule(code=src, options=('-std=c++17',))
    return _mod

def energy_ref(s):
    """Exact integer energy, numpy int64 correlation."""
    s = np.asarray(s, dtype=np.int64)
    c = np.correlate(s, s, mode='full')[len(s):]
    return int(np.dot(c, c))

def energy_pure(s):
    """Exact integer energy in pure Python, independent of numpy."""
    s = [int(x) for x in s]; L = len(s); E = 0
    for k in range(1, L):
        c = 0
        for i in range(L - k): c += s[i] * s[i + k]
        E += c * c
    return E

def skew_expand(half):
    """half = s[0..n] (+-1). Standard skew symmetry s[n+j] = (-1)^j s[n-j]."""
    half = np.asarray(half, dtype=np.int8); n = len(half) - 1
    j = np.arange(1, n + 1)
    right = half[n - j] * np.where(j % 2 == 0, 1, -1).astype(np.int8)
    return np.concatenate([half, right]).astype(np.int8)

def is_skew(s):
    s = np.asarray(s); L = len(s)
    if L % 2 == 0: return False
    n = (L - 1) // 2
    return all(s[n + j] == (s[n - j] if j % 2 == 0 else -s[n - j]) for j in range(1, n + 1))

def bits(s): return ''.join('1' if x > 0 else '0' for x in s)
def from_bits(b): return np.array([1 if c == '1' else -1 for c in b], dtype=np.int8)

class SkewGPU:
    def __init__(self, L, W, threads=None):
        assert L % 2 == 1 and L >= 5
        self.L, self.W, self.n = L, W, (L - 1) // 2
        self.NV = self.n + 1
        self.T = threads or min(1024, 32 * math.ceil(self.NV / 32))
        assert self.T >= self.NV and self.T % 32 == 0
        n, NV = self.n, self.NV
        self.S = cp.zeros(W * L, dtype=cp.int8); self.bestS = cp.zeros(W * L, dtype=cp.int8)
        self.C = cp.zeros(W * (n + 1), dtype=cp.int32); self.tabu = cp.zeros(W * NV, dtype=cp.int32)
        self.E = cp.zeros(W, dtype=cp.int32); self.bestE = cp.zeros(W, dtype=cp.int32)
        self.step = cp.zeros(W, dtype=cp.int32); self.mask = cp.zeros(W, dtype=cp.int32)
        self.odd = cp.zeros(W, dtype=cp.int32)
        self.frozen = cp.zeros(W, dtype=cp.int32)
        m = module()
        self.k_tabu, self.k_init, self.k_dE = m.get_function('skew_tabu'), m.get_function('skew_init'), m.get_function('skew_dE_all')
        self.k_saw = m.get_function('skew_saw')
        self.Z = cp.asarray(np.random.default_rng(987654321).integers(1, 2**63, size=NV, dtype=np.int64).astype(np.uint64)
                            ^ (np.random.default_rng(123456789).integers(1, 2**63, size=NV, dtype=np.int64).astype(np.uint64) << np.uint64(1)))
        self.stuck = cp.zeros(W, dtype=cp.int32)
        self.sh_tabu = 32 * 8 + (5 * n + 1 + n + 1 + 8) * 4
        self.sh_init = (L + 4) * 4
        self.sh_dE = (5 * n + 1 + n + 1) * 4

    def set_start(self, idx, seqs):
        idx = np.asarray(idx, dtype=np.int64); seqs = np.asarray(seqs, dtype=np.int8)
        S2 = self.S.reshape(self.W, self.L); S2[cp.asarray(idx)] = cp.asarray(seqs)
        self.mask.fill(0); self.mask[cp.asarray(idx)] = 1
        self.k_init((self.W,), (256,), (np.int32(self.L), self.mask, self.S, self.C, self.E, self.bestE,
                                         self.bestS, self.tabu, self.step, self.odd), shared_mem=self.sh_init)
        if int(self.odd[cp.asarray(idx)].max()) != 0: raise ValueError('start sequence not skew-symmetric')

    def run(self, nsteps, tenure_min, tenure_span, seed):
        self.k_tabu((self.W,), (self.T,), (np.int32(self.L), np.int32(nsteps), np.uint32(seed & 0xFFFFFFFF),
                                           np.int32(tenure_min), np.int32(tenure_span), self.S, self.C, self.E,
                                           self.bestE, self.bestS, self.tabu, self.step, self.frozen), shared_mem=self.sh_tabu)

    def run_saw(self, nsteps, tbl, seed):
        assert tbl & (tbl - 1) == 0
        sh = 34 * 8 + tbl * 4 + (5 * self.n + 1 + self.n + 1 + 8) * 4
        if sh > 48 * 1024:
            self.k_saw.max_dynamic_shared_size_bytes = sh
        self.k_saw((self.W,), (self.T,), (np.int32(self.L), np.int32(nsteps), np.uint32(seed & 0xFFFFFFFF), np.int32(tbl),
                                          self.Z, self.S, self.C, self.E, self.bestE, self.bestS, self.step, self.frozen,
                                          self.stuck), shared_mem=sh)

    def set_frozen(self, P):
        self.frozen[:] = cp.asarray(np.asarray(P, dtype=np.int32))

    def dE_all(self):
        out = cp.zeros(self.W * self.NV, dtype=cp.int32)
        self.k_dE((self.W,), (self.T,), (np.int32(self.L), self.S, self.C, out), shared_mem=self.sh_dE)
        return cp.asnumpy(out).reshape(self.W, self.NV)

    def get(self):
        return (cp.asnumpy(self.bestE), cp.asnumpy(self.bestS).reshape(self.W, self.L),
                cp.asnumpy(self.E), cp.asnumpy(self.S).reshape(self.W, self.L))
