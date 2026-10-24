"""Standalone check of the claimed VarBench state (run from the package folder: sh verify-it-yourself/run_checks.sh).

1. sha256 of every file in object/ equals verify-it-yourself/expected_sha256.txt.
2. The checkpoint's config is the claimed one (L = 10, ResNet 16 channels x 3 blocks, kernel 3, stripe prior, irrep B1,
   spin flip, C4v symmetrisation) with 14114 parameters.
3. The local energy (estimator2.py: Hamiltonian written from the VarBench definition, Pauli convention, periodic 10 x 10,
   J1 = 1, J2 = 0.9) of 2048 saved configurations (the final chain states of measurement S2) reproduces the values
   recorded during S2: |mean difference| < 1e-5 and max |difference| < 1e-2.
4. A short fresh plain Monte Carlo estimate (1024 chains, 30 thermalisation sweeps, 16 rounds of 2 sweeps, seed 9001)
   lies within 4 of its sigma of the claimed E = -253.753424311 and below the bar -253.668 by more than 3 of its sigma.
   (A spot check: the claim's >= 1e5-sample measurements are reproduced by RUN_IT_YOURSELF.md, about an hour of GPU.)
Needs Python 3 with torch (CUDA) and numpy.  Prints PASS or FAIL as its last line.
"""
import hashlib, json, math, os, sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(PKG, 'verify-it-yourself')
CLAIM_E, BAR = -253.753424311, -253.668


def fail(msg):
    print('check failed:', msg); print('FAIL'); sys.exit(1)


exp = {}
for line in open(os.path.join(V, 'expected_sha256.txt')):
    h, f = line.split(None, 1); exp[f.strip()] = h
for f, h in sorted(exp.items()):
    p = os.path.join(PKG, f)
    if not os.path.isfile(p) or hashlib.sha256(open(p, 'rb').read()).hexdigest() != h:
        fail('sha256 mismatch for ' + f)
print('1. object hashes: ok (%d files)' % len(exp))

sys.path.insert(0, V)
import estimator2 as E2
import numpy as np, torch
if E2.DEV == 'cuda' and not torch.cuda.is_available():
    fail('no CUDA GPU visible to torch')
nqs, model, d = E2.load_nqs(os.path.join(PKG, 'object', 'r10_J0.9_B1.pt'), os.path.join(PKG, 'object', 'model'))
want = dict(L=10, net=dict(channels=16, blocks=3, kernel=3), prior='stripe', irrep='B1', flip=True, sym=True)
cfg = {k: model.cfg[k] for k in want}
npar = sum(p.numel() for p in model.parameters())
if cfg != want or npar != 14114:
    fail('config %s, %d parameters' % (json.dumps(cfg), npar))
print('2. config: ok (%s, %d parameters, step %s)' % (json.dumps(cfg), npar, d['opt_state']['step']))

ref = np.load(os.path.join(V, 'ref_configs.npz'))
x = torch.tensor(ref['configs'].astype(np.float32), device=E2.DEV)
if (x.sum(1) != 0).any():
    fail('reference configurations are not Sz = 0')
wave = E2.NQSWave(model); ham = E2.Ham(10, 1.0, 0.9)
with E2.Lock():
    lp, lq = wave.logs(x); El = ham.apply(wave, x, lp, lq)[0].real.cpu().numpy()
diff = El - ref['eloc']
print('3. local energies of %d saved configurations: mean diff %.3e, max |diff| %.3e, mean E_loc %.6f'
      % (len(El), diff.mean(), np.abs(diff).max(), El.mean()))
if abs(diff.mean()) >= 1e-5 or np.abs(diff).max() >= 1e-2:
    fail('local energies differ from the recorded ones')

st, _ = E2.run(wave, ham, 'plain', 1024, 30, 2.0, 16, 16, seed=9001, log=lambda s: None)
E, s = st['E'], st['sigma']
print('4. short fresh estimate (seed 9001, %d samples): E = %.6f +- %.6f; claimed %.6f; bar %.3f'
      % (st['n'], E, s, CLAIM_E, BAR))
if abs(E - CLAIM_E) >= 4 * s or not (E + 3 * s < BAR):
    fail('short estimate inconsistent with the claim or not below the bar')
print('PASS')
