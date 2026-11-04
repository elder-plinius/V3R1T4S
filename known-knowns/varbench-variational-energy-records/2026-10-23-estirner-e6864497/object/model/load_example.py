"""How to reload a saved state (for a stranger).
  python load_example.py ../ckpt/r6_J0.8_B1.pt  [J2]
The checkpoint holds state_dict + config (L, net channels/blocks/kernel, prior, irrep, flip, sym) + opt_state
(step, lr schedule; MinSR keeps no other optimizer state) + the sampler chains and RNG state.  The same file's
.config.json repeats the config.  log psi(s) for s in {-1,+1}^(L*L) (row-major, +1 = up) is model(s)[:, 0] + i model(s)[:, 1].
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nqs, torch
path = sys.argv[1]; J2 = float(sys.argv[2]) if len(sys.argv) > 2 else None
model, d = nqs.load_ckpt(path, nqs.DEVICE)
print('config', model.cfg, 'step', d['opt_state']['step'], 'params', nqs.nparams(model))
x = nqs.random_sz0(4, model.N, nqs.DEVICE)
print('log psi of 4 random Sz=0 configurations:', model(x).tolist())
if J2 is not None:
    H = nqs.Ham(model.L, 1.0, J2, nqs.DEVICE)
    print('E_loc of those configurations:', nqs.local_energy(model, H, x).tolist())
