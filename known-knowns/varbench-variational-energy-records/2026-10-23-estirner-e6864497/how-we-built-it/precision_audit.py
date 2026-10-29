"""PREREG.v2 I3'(c): on 2048 configurations from the final chains of a |psi|^2 measurement (S2), compare E_loc from
estimator2's measurement path (float32 network, float64 composition) and from nqs.py's all-float32 local energy with
an all-float64 evaluation of the same state.  Usage: precision_audit.py <ckpt> <nqs_dir> <S2 npz> <out json> [sigma_claim]"""
import os, sys, json, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estimator2 as E2
import numpy as np, torch
ck, nqd, npz, out = sys.argv[1:5]; sig = float(sys.argv[5]) if len(sys.argv) > 5 else None
if E2.DEV == 'cuda':
    torch.cuda.set_per_process_memory_fraction(5.0 / 16.0)
nqs, model, d = E2.load_nqs(ck, nqd)
m64 = copy.deepcopy(model).double()
w32, w64 = E2.NQSWave(model), E2.NQSWave(m64)
ham = E2.Ham(model.L, 1.0, 0.9); Href = nqs.Ham(model.L, 1.0, 0.9, E2.DEV)
x = torch.tensor(np.load(npz)['final_chains'][:2048].astype(np.float32), device=E2.DEV)
with E2.Lock():
    lp32, lq32 = w32.logs(x); El32 = ham.apply(w32, x, lp32, lq32)[0]
    x64 = x.double(); lp64, lq64 = w64.logs(x64); El64 = ham.apply(w64, x64, lp64, lq64)[0]
    Eq = nqs.local_energy(model, Href, x, max_images=65536)
d32 = (El32 - El64).real.cpu().numpy(); dq = (Eq - El64).real.cpu().numpy()
r = dict(n=int(x.shape[0]), sha256_npz=E2.sha256(npz), mean_E64=float(El64.real.mean()),
         est_path=dict(mean_diff=float(d32.mean()), max_abs_diff=float(np.abs(d32).max())),
         nqs_float32=dict(mean_diff=float(dq.mean()), max_abs_diff=float(np.abs(dq).max())), sigma_claim=sig)
if sig is not None:
    r['I3prime_c_pass'] = bool(abs(r['est_path']['mean_diff']) < sig / 10)
json.dump(r, open(out, 'w'), indent=1); print(json.dumps(r))
