"""Audit A1-A3: where Var(H) and the energy tail of the trained 4x4 NQS (r4_J0.9.pt) live, by exact enumeration of the
12870 Sz = 0 configurations (estimator2's local energy).  For thresholds t: weight of p < t, its share of Var(H), its
signed contribution to E (sum_{p<t} p (E_loc - E)), and the bias of a sampler blind to p < t
(E_trunc(t) - E, E_trunc = sum_{p>=t} p E_loc / sum_{p>=t} p)."""
import sys, os, json
sys.path.insert(0, sys.argv[1]); sys.path.insert(1, os.path.join(sys.argv[1], 'ref'))
import estimator2 as E2, checks
import numpy as np
nqs, model, d = E2.load_nqs(checks.R4, checks.NQS_DIR)
wave = E2.NQSWave(model); ham = E2.Ham(4, 1.0, 0.9)
x = checks.basis_configs(np.load(checks.GS)['basis'], 16)
lp, El, p, E = checks.enumerate_exact(wave, ham, x)
e = El.real
dev = e - E; var = float((p * dev ** 2).sum())
out = dict(E=E, Var=var, max_abs_dev=float(np.abs(dev).max()), rows=[])
for t in (1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9):
    m = p < t
    out['rows'].append(dict(t=t, n_conf=int(m.sum()), weight=float(p[m].sum()), var_share=float((p * dev ** 2)[m].sum() / var),
                            tail_mean_contrib=float((p * dev)[m].sum()),
                            tail_pos=float((p * np.clip(dev, 0, None))[m].sum()),
                            tail_neg=float((p * np.clip(dev, None, 0))[m].sum()),
                            blind_bias=float((p * e)[~m].sum() / p[~m].sum() - E)))
# with the 2048 samples per step of night-1 training, a config of probability p is seen in a step with prob ~2048 p
print(json.dumps(out, indent=1))
