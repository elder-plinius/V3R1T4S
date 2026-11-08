"""Standalone check of the claimed VarBench state (run from the package folder: sh verify-it-yourself/run_checks.sh).

The state is object/r10_J0.9_B1.onnx: input spins [batch, 100] float32 (+1 = up, -1 = down, site k = 10 r + c),
outputs log_abs_psi [batch] and phase [batch].  Needs Python 3 with numpy and onnxruntime; runs on the CPU.

1. sha256 of every file in object/ equals verify-it-yourself/expected_sha256.txt.
2. The ONNX file has the stated input and outputs and evaluates any batch size.
3. object/r10_J0.9_B1.reference_values.csv: 100 Sz = 0 configurations whose log|psi| and phase, recomputed from the
   ONNX file, agree with the table (|d log|psi|| < 1e-3, |d phase| < 1e-3 rad, phase compared modulo 2 pi; float32
   runtimes agree to about 1e-5 on these rows, and a wrong export would be off by far more).
4. Symmetries built into the exported state, on 16 random Sz = 0 configurations: one-site translations in r and c and
   global spin flip leave psi unchanged; the C4v operations about site 0 multiply it by their B1 character (+1 for
   the 180-degree rotation and the two axis reflections, -1 for the 90-degree rotations and the two diagonal
   reflections).
5. Local energies, from a Hamiltonian written here from the VarBench definition (Pauli convention, periodic 10 x 10,
   J1 = 1, J2 = 0.9, each bond once), of the first NREF saved configurations (final chain states of measurement S2,
   verify-it-yourself/ref_configs.npz) reproduce the values recorded by the PyTorch model during S2:
   |mean difference| < 2e-4 and max |difference| < 1e-2 (float32 runtimes differ by about 1e-5 on average).
Prints PASS or FAIL as its last line.
"""
import csv, hashlib, os, sys
import numpy as np

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(PKG, 'verify-it-yourself')
ONNX = os.path.join(PKG, 'object', 'r10_J0.9_B1.onnx')
TABLE = os.path.join(PKG, 'object', 'r10_J0.9_B1.reference_values.csv')
L, N, J1, J2 = 10, 100, 1.0, 0.9
NREF = int(os.environ.get('NREF', '256'))


def fail(msg):
    print('check failed:', msg); print('FAIL'); sys.exit(1)


exp = {}
for line in open(os.path.join(V, 'expected_sha256.txt')):
    h, f = line.split(None, 1); exp[f.strip()] = h
shipped = sorted(os.path.relpath(os.path.join(r, f), PKG) for r, _, fs in os.walk(os.path.join(PKG, 'object')) for f in fs)
if shipped != sorted(exp):
    fail('object/ holds %s, expected %s' % (shipped, sorted(exp)))
for f, h in sorted(exp.items()):
    if hashlib.sha256(open(os.path.join(PKG, f), 'rb').read()).hexdigest() != h:
        fail('sha256 mismatch for ' + f)
print('1. object hashes: ok (%d files)' % len(exp))

import onnxruntime as ort
so = ort.SessionOptions(); so.intra_op_num_threads = int(os.environ.get('THREADS', '2')); so.inter_op_num_threads = 1
sess = ort.InferenceSession(ONNX, so, providers=['CPUExecutionProvider'])
ins = [(i.name, i.shape, i.type) for i in sess.get_inputs()]
outs = [o.name for o in sess.get_outputs()]
if len(ins) != 1 or ins[0][0] != 'spins' or ins[0][1][1] != N or ins[0][2] != 'tensor(float)' \
        or outs != ['log_abs_psi', 'phase']:
    fail('unexpected ONNX signature %s -> %s' % (ins, outs))


def logpsi(x, chunk=512):
    x = np.asarray(x, np.float32); la, ph = [], []
    for i in range(0, len(x), chunk):
        a, p = sess.run(None, {'spins': x[i:i + chunk]}); la.append(a); ph.append(p)
    return np.concatenate(la).astype(np.float64), np.concatenate(ph).astype(np.float64)


def angdiff(a, b):
    return np.abs(np.angle(np.exp(1j * (a - b))))


for bs in (1, 3):
    a, p = logpsi(np.ones((bs, N)) * np.where(np.arange(N) % 2, 1, -1))
    if a.shape != (bs,) or p.shape != (bs,):
        fail('batch size %d gives output shapes %s, %s' % (bs, a.shape, p.shape))
print('2. ONNX signature: ok (spins [batch, %d] float32 -> log_abs_psi [batch], phase [batch])' % N)

rows = list(csv.DictReader(open(TABLE)))
x = np.array([[1.0 if ch == 'u' else -1.0 for ch in r['spins']] for r in rows])
if len(rows) != 100 or x.shape != (100, N) or any(set(r['spins']) - set('ud') for r in rows) or (x.sum(1) != 0).any():
    fail('reference table is not 100 Sz = 0 configurations of %d sites' % N)
la, ph = logpsi(x)
dla = np.abs(la - np.array([float(r['log_abs_psi']) for r in rows])).max()
dph = angdiff(ph, np.array([float(r['phase']) for r in rows])).max()
print('3. reference table (100 rows): max |d log|psi|| %.2e, max |d phase| %.2e rad' % (dla, dph))
if not (dla < 1e-3 and dph < 1e-3):
    fail('the ONNX file does not reproduce the reference table')

r, c = np.meshgrid(np.arange(L), np.arange(L), indexing='ij')
idx = lambda rr, cc: ((rr % L) * L + (cc % L)).reshape(-1)       # (g s)[k] = s[idx[k]]
OPS = {'translate r': (idx(r + 1, c), 1), 'translate c': (idx(r, c + 1), 1),
       'rotate 90': (idx(c, -r), -1), 'rotate 180': (idx(-r, -c), 1), 'rotate 270': (idx(-c, r), -1),
       'reflect r': (idx(-r, c), 1), 'reflect c': (idx(r, -c), 1),
       'reflect diagonal': (idx(c, r), -1), 'reflect antidiagonal': (idx(-c, -r), -1)}
rng = np.random.default_rng(7)
s = np.array([rng.permutation(np.repeat([1.0, -1.0], N // 2)) for _ in range(16)])
la0, ph0 = logpsi(s)
worst = 0.0
for name, (p, chi) in list(OPS.items()) + [('spin flip', (None, 1))]:
    gs = -s if p is None else s[:, p]
    la1, ph1 = logpsi(gs)
    err = max(np.abs(la1 - la0).max(), angdiff(ph1, ph0 + (0.0 if chi > 0 else np.pi)).max())
    worst = max(worst, err)
    if err > 1e-3:
        fail('psi(g s) != %+d psi(s) for %s (error %.2e)' % (chi, name, err))
print('4. symmetries: ok (translations, spin flip, C4v with B1 characters; worst deviation %.1e)' % worst)

B = []                                                            # (i, j, W), each bond once
for k in range(N):
    rr, cc = divmod(k, L)
    for dr, dc, w in ((0, 1, J1), (1, 0, J1), (1, 1, J2), (1, -1, J2)):
        B.append((k, ((rr + dr) % L) * L + (cc + dc) % L, w))
BI, BJ, BW = (np.array(v) for v in zip(*B))
if len(B) != 4 * N or len(set(map(frozenset, zip(BI, BJ)))) != 4 * N:
    fail('bond list')


def eloc(x):
    """E_loc(s) = sum_b W_b s_i s_j + sum_{b: s_i != s_j} 2 W_b psi(s^b) / psi(s), real part (sigma.sigma = zz + 2 swap)."""
    la, ph = logpsi(x)
    out = (BW * x[:, BI] * x[:, BJ]).sum(1)
    for n in range(len(x)):
        anti = np.nonzero(x[n, BI] != x[n, BJ])[0]
        y = np.repeat(x[n:n + 1], len(anti), 0)
        y[np.arange(len(anti)), BI[anti]], y[np.arange(len(anti)), BJ[anti]] = x[n, BJ[anti]], x[n, BI[anti]]
        lb, pb = logpsi(y)
        out[n] += (2 * BW[anti] * np.exp(lb - la[n]) * np.cos(pb - ph[n])).sum()
    return out


ref = np.load(os.path.join(V, 'ref_configs.npz'))
xr = ref['configs'][:NREF].astype(np.float64)
if (xr.sum(1) != 0).any():
    fail('reference configurations are not Sz = 0')
d = eloc(xr) - ref['eloc'][:NREF]
print('5. local energies of %d saved configurations: mean diff %.2e, max |diff| %.2e, mean E_loc %.6f (recorded %.6f)'
      % (NREF, d.mean(), np.abs(d).max(), (d + ref['eloc'][:NREF]).mean(), ref['eloc'][:NREF].mean()))
if abs(d.mean()) >= 2e-4 or np.abs(d).max() >= 1e-2:
    fail('local energies differ from the recorded ones')
print('PASS')
