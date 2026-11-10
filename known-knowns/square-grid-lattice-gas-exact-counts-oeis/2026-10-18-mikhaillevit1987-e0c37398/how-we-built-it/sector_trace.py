"""Independent lens: whole-row transfer matrix split into flux sectors, trace(T^n) mod small primes via dense
float64 BLAS products (exact because m * p^2 < 2^53). Shares no code with ice.rs.
Row rule: a = vertical bits below the row, b = bits above; h_c = a_c + h_{c-1} - b_c must stay in {0,1}
around the cycle and return to h_{-1} = x0. popcount(a) == popcount(b) is forced, so T is block diagonal.
Usage: python sector_trace.py n p1 [p2 ...]"""
import sys, itertools, json, time
import numpy as np

def sector_states(n, k):
    return np.array([sum(1 << i for i in c) for c in itertools.combinations(range(n), k)], dtype=np.int64)

def sector_T(n, st):
    a = st[:, None]; b = st[None, :]
    T = np.zeros((len(st), len(st)), dtype=np.int8)
    for x0 in (0, 1):
        h = np.full((len(st), len(st)), x0, dtype=np.int8)
        ok = np.ones_like(h, dtype=bool)
        for c in range(n):
            h = ((a >> c) & 1).astype(np.int8) + h - ((b >> c) & 1).astype(np.int8)
            ok &= (h == 0) | (h == 1)
        ok &= h == x0
        T += ok.astype(np.int8)
    return T

def matmul_mod(A, B, p):
    return np.fmod(A @ B, p)

def trace_pow(T, n, p):
    M = T.astype(np.float64)
    R = None
    e = n
    while e:
        if e & 1:
            R = M if R is None else matmul_mod(R, M, p)
        e >>= 1
        if e:
            M = matmul_mod(M, M, p)
    return int(round(np.trace(R))) % p

if __name__ == '__main__':
    n = int(sys.argv[1]); ps = [int(x) for x in sys.argv[2:]]
    for p in ps:
        assert (1 << n) // 1 * p * p < 2 ** 53 or True
    t0 = time.time()
    tot = {p: 0 for p in ps}
    for k in range(n + 1):
        st = sector_states(n, k)
        assert len(st) * max(ps) ** 2 < 2 ** 53, 'float64 exactness bound violated'
        T = sector_T(n, st)
        for p in ps:
            tot[p] = (tot[p] + trace_pow(T, n, p)) % p
    print(json.dumps({'n': n, 'residues': {str(p): tot[p] for p in ps}, 'seconds': round(time.time() - t0, 1)}))
