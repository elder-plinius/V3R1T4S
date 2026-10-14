"""p3-style check on the mpfr-polished N=3552 file: float64 tangent Hessian, rotations deflated, ARPACK shift-invert smallest
eigenvalues + full dense eigvalsh for comparison."""
import sys, os, json, time; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, hp, scipy.sparse.linalg as sla
pts = hp.load(sys.argv[1]); E, G, T, lam, gn = hp.egrad(pts, 8)
X = np.array([[float(v) for v in p] for p in pts]); t = time.time()
A, B = hp.tangent_hessian_f64(X, np.array([float(l) for l in lam])); R = hp.rot_modes(X, B)
Ad = A + 100.0*R@R.T
w_arp = sla.eigsh(Ad, k=6, sigma=-1.0, which='LM', return_eigenvectors=False)
w_full = np.linalg.eigvalsh(A)
rec = dict(N=len(pts), grad2=float(gn), arpack_deflated_smallest6=sorted(float(v) for v in w_arp), full_lowest6=[float(v) for v in w_full[:6]],
           full_max=float(w_full[-1]), n_nonpos_beyond3=int((w_full[3:] <= 0).sum()), secs=round(time.time()-t, 1))
print(json.dumps(rec)); json.dump(rec, open(sys.argv[2], 'w'), indent=1)
