#!/usr/bin/env python3
"""Make a negative control: perturb each coordinate by Gaussian noise (rms s, seed k) and renormalise."""
import sys, numpy as np
src, dst, s, k = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
x = np.array([[float(v) for v in l.split()[-3:]] for l in open(src) if len(l.split()) >= 3])
rng = np.random.default_rng(k)
x = x + s * rng.standard_normal(x.shape)
x /= np.linalg.norm(x, axis=1)[:, None]
np.savetxt(dst, x, fmt='%.20e')
