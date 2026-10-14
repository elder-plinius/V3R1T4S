"""High-precision Thomson certification: MPFR (gmpy2) gradient/Hessian, mpmath dps-30 energy,
tangent-space Newton with float64 direction solves, Weyl-bounded eigenvalue certificate.
usage: python hp.py POINTS_FILE OUT_PREFIX [--hessian] [--newton K] [--workers 8]"""
import sys, os, re, time, json, argparse
for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS"): os.environ.setdefault(v, "8")
import numpy as np, gmpy2, mpmath
from gmpy2 import mpfr
from multiprocessing import Pool
PREC = 170  # bits, ~51 decimal digits
gmpy2.get_context().precision = PREC
P = None  # list of (x,y,z) mpfr, normalized
NCH = 96

def load(f):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from ptload import tokens
    toks = tokens(f)
    out = []
    for k in range(0, len(toks), 3):
        x, y, z = (mpfr(t) for t in toks[k:k+3]); r = gmpy2.sqrt(x*x+y*y+z*z); out.append((x/r, y/r, z/r))
    return out

def _gchunk(c):
    gmpy2.get_context().precision = PREC
    n = len(P); G = {}; E = mpfr(0)
    Gl = [[mpfr(0)]*3 for _ in range(n)]
    for i in range(c, n, NCH):
        xi, yi, zi = P[i]; gx = gy = gz = mpfr(0)
        for j in range(i+1, n):
            xj, yj, zj = P[j]; dx = xi-xj; dy = yi-yj; dz = zi-zj
            r2 = dx*dx+dy*dy+dz*dz; ir = gmpy2.rec_sqrt(r2); ir3 = ir*ir*ir; E += ir
            gx -= dx*ir3; gy -= dy*ir3; gz -= dz*ir3
            g = Gl[j]; g[0] += dx*ir3; g[1] += dy*ir3; g[2] += dz*ir3
        g = Gl[i]; g[0] += gx; g[1] += gy; g[2] += gz
    return E, Gl

def egrad(pts, workers):
    global P; P = pts; n = len(P)
    with Pool(workers) as pool: res = pool.map(_gchunk, range(NCH))
    E = mpfr(0); G = [[mpfr(0)]*3 for _ in range(n)]
    for e, Gl in res:
        E += e
        for i in range(n):
            for k in range(3): G[i][k] += Gl[i][k]
    # Riemannian (tangent) gradient
    T = []; lam = []
    for i in range(n):
        x = P[i]; d = G[i][0]*x[0]+G[i][1]*x[1]+G[i][2]*x[2]; lam.append(d)
        T.append([G[i][k]-d*x[k] for k in range(3)])
    gn = gmpy2.sqrt(sum(t*t for v in T for t in v))
    return E, G, T, lam, gn

def _echunk(c):
    mpmath.mp.dps = 30; n = len(P); s = []
    Q = [[mpmath.mpf(str(v)) for v in p] for p in P]
    for p in Q:
        r = mpmath.sqrt(p[0]**2+p[1]**2+p[2]**2); p[0] /= r; p[1] /= r; p[2] /= r
    for i in range(c, n, NCH):
        a = Q[i]
        for j in range(i+1, n):
            b = Q[j]; s.append(1/mpmath.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2))
    return str(mpmath.fsum(s))

def energy_mpmath30(pts, workers):
    """criterion statistic: mpmath dps=30, coordinates passed as 50-digit decimal strings then renormalized at dps 30"""
    global P; P = pts
    with Pool(workers) as pool: parts = pool.map(_echunk, range(NCH))
    mpmath.mp.dps = 30; return mpmath.fsum(mpmath.mpf(p) for p in parts)

def tbasis(x):
    """orthonormal tangent basis (e1,e2) at unit x, float64"""
    a = np.array([1.0, 0, 0]) if abs(x[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(x, a); e1 /= np.linalg.norm(e1); e2 = np.cross(x, e1); return e1, e2

def tangent_hessian_f64(X, lam):
    """2N x 2N Riemannian Hessian in float64 (numba-free, vectorized by row blocks)."""
    n = len(X); B = np.array([np.stack(tbasis(x), 1) for x in X])  # n x 3 x 2
    A = np.zeros((2*n, 2*n)); Hd = np.zeros((n, 3, 3)); I3 = np.eye(3)
    for i in range(n):
        d = X[i]-X; d[i] = 1; r = np.linalg.norm(d, axis=1); r[i] = 1
        H = 3*np.einsum('ja,jb->jab', d, d)/r[:, None, None]**5 - I3/r[:, None, None]**3  # d2(1/r)/dxi2 contribution
        H[i] = 0; Hd[i] = H.sum(0)
        Bl = np.einsum('ak,jab,jbl->jkl', B[i], -H, B)  # off-diagonal blocks B_i^T H_ij B_j, H_ij = -H
        A[2*i:2*i+2, :] = Bl.transpose(1, 0, 2).reshape(2, 2*n)
        A[2*i:2*i+2, 2*i:2*i+2] = B[i].T@Hd[i]@B[i] - lam[i]*np.eye(2)
    return 0.5*(A+A.T), B

def rot_modes(X, B):
    n = len(X); R = []
    for ax in np.eye(3):
        v = np.cross(ax, X)  # n x 3
        R.append(np.einsum('nk,nkl->nl', v, B).ravel())
    Q, _ = np.linalg.qr(np.array(R).T); return Q

def newton_step(pts, T, lam):
    X = np.array([[float(v) for v in p] for p in pts]); A, B = tangent_hessian_f64(X, np.array([float(l) for l in lam]))
    g = np.array([[float(sum(T[i][k]*B[i][k, l] for k in range(3))) for l in range(2)] for i in range(len(pts))]).ravel()
    R = rot_modes(X, B); Ap = A + 10.0*R@R.T
    delta = -np.linalg.solve(Ap, g); delta -= R@(R.T@delta)
    new = []
    for i, p in enumerate(pts):
        st = B[i]@delta[2*i:2*i+2]
        x, y, z = p[0]+mpfr(float(st[0])), p[1]+mpfr(float(st[1])), p[2]+mpfr(float(st[2]))
        r = gmpy2.sqrt(x*x+y*y+z*z); new.append((x/r, y/r, z/r))
    return new, float(np.linalg.norm(delta))

def save(pts, f):
    with open(f, 'w') as o:
        for p in pts: o.write(' '.join(gmpy2.mpfr(v).__format__('.40f') for v in p)+'\n')

def _hchunk(c):
    """exact-ish (170-bit) tangent Hessian blocks for rows i in chunk; returns off-diagonal 2x2 blocks (as float64)
    + their rounding error, and 3x3 diagonal accumulators in mpfr."""
    gmpy2.get_context().precision = PREC
    n = len(P); Bm = BM; out = []; Hd = [[mpfr(0)]*9 for _ in range(n)]; err2 = mpfr(0)
    for i in range(c, n, NCH):
        xi = P[i]; Bi = Bm[i]; row = np.zeros((2, 2*n))
        for j in range(i+1, n):
            xj = P[j]; d = (xi[0]-xj[0], xi[1]-xj[1], xi[2]-xj[2]); r2 = d[0]*d[0]+d[1]*d[1]+d[2]*d[2]
            ir = gmpy2.rec_sqrt(r2); ir3 = ir*ir*ir; ir5 = ir3*ir*ir
            H = [3*d[a]*d[b]*ir5 - (ir3 if a == b else 0) for a in range(3) for b in range(3)]  # d2(1/r)/dxi dxi
            hi, hj = Hd[i], Hd[j]
            for k in range(9): hi[k] += H[k]; hj[k] += H[k]
            Bj = Bm[j]
            for k in range(2):
                for l in range(2):  # B_i^T (-H) B_j
                    v = -sum(Bi[a][k]*H[3*a+b]*Bj[b][l] for a in range(3) for b in range(3))
                    f = float(v); row[k, 2*j+l] = f; e = v-f; err2 += e*e
        out.append((i, row))
    return out, Hd, err2

def mp_basis(x):
    a = (mpfr(1), mpfr(0), mpfr(0)) if abs(x[0]) < 0.9 else (mpfr(0), mpfr(1), mpfr(0))
    cr = lambda u, v: (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
    e1 = cr(x, a); r = gmpy2.sqrt(sum(t*t for t in e1)); e1 = tuple(t/r for t in e1); e2 = cr(x, e1)
    return [[e1[a], e2[a]] for a in range(3)]  # 3x2

def hessian_cert(pts, lam, workers):
    global P, BM; P = pts; n = len(pts); BM = [mp_basis(x) for x in pts]
    with Pool(workers) as pool: res = pool.map(_hchunk, range(NCH))
    A = np.zeros((2*n, 2*n)); Hd = [[mpfr(0)]*9 for _ in range(n)]; err2 = mpfr(0)
    for out, hd, e2 in res:
        err2 += e2
        for i, row in out: A[2*i:2*i+2, :] += row
        for i in range(n):
            for k in range(9): Hd[i][k] += hd[i][k]
    for i in range(n):
        Bi = BM[i]
        for k in range(2):
            for l in range(2):
                v = sum(Bi[a][k]*Hd[i][3*a+b]*Bi[b][l] for a in range(3) for b in range(3)) - (lam[i] if k == l else 0)
                f = float(v); A[2*i+k, 2*i+l] = f; e = v-f; err2 += e*e
    A = np.triu(A, 1); A = A + A.T + np.diag(np.diag(A)) * 0  # upper blocks only were filled for i<j
    # refill diagonal blocks (triu(.,1) dropped the lower entry of each 2x2 diagonal block's diagonal)
    for i in range(n):
        Bi = BM[i]
        for k in range(2):
            for l in range(2):
                v = sum(Bi[a][k]*Hd[i][3*a+b]*Bi[b][l] for a in range(3) for b in range(3)) - (lam[i] if k == l else 0)
                A[2*i+k, 2*i+l] = float(v)
    offerr_F = float(gmpy2.sqrt(2*err2))  # Frobenius norm of (exact - rounded), off-diag counted twice (upper bound)
    X = np.array([[float(v) for v in p] for p in pts]); Bf = np.array([[[float(Bi[a][k]) for k in range(2)] for a in range(3)] for Bi in BM])
    R = rot_modes(X, Bf); Qf, _ = np.linalg.qr(np.c_[R, np.random.default_rng(0).normal(size=(2*n, 2*n-3))])
    Qc = Qf[:, 3:]  # orthonormal complement of rotation modes (float64)
    Ar = Qc.T@A@Qc; Ar = 0.5*(Ar+Ar.T)
    w = np.linalg.eigvalsh(Ar); wA = np.linalg.eigvalsh(A)
    nrm = float(max(abs(w[0]), abs(w[-1]))); m = Ar.shape[0]; u = 2.0**-53
    # error budget: rounding of A (Frobenius, from MPFR), matmul Qc^T A Qc (~ 2*m*u*||A||), eigvalsh backward error (10*m*u*||A||),
    # non-orthonormality of Qc (||Qc^TQc - I||*||A||)
    orth = float(np.linalg.norm(Qc.T@Qc - np.eye(m), 2))
    bound = offerr_F + 2*m*u*nrm + 10*m*u*nrm + 2*orth*nrm
    chol_ok = True
    try: np.linalg.cholesky(Ar - (w[0]/2)*np.eye(m))
    except np.linalg.LinAlgError: chol_ok = False
    return dict(dim_tangent=2*n, dim_nonrot=m, lowest6_full=[float(v) for v in wA[:6]], lowest3_nonrot=[float(v) for v in w[:3]],
                max_eig=float(w[-1]), err_rounding_F=offerr_F, orth_defect=orth, weyl_bound=bound, certified_min=float(w[0]-bound),
                num_nonpositive_nonrot=int((w <= bound).sum()), cholesky_half_shift_ok=chol_ok)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('f'); ap.add_argument('out'); ap.add_argument('--newton', type=int, default=8)
    ap.add_argument('--hessian', action='store_true'); ap.add_argument('--workers', type=int, default=8); ap.add_argument('--gtol', type=float, default=1e-20)
    ap.add_argument('--prepolish', action='store_true', help='float64 L-BFGS gtol 1e-12 first (tools/fastpol.py)')
    a = ap.parse_args(); t0 = time.time(); rec = dict(file=a.f)
    pts = load(a.f); rec['N'] = len(pts)
    E0 = energy_mpmath30(pts, a.workers); rec['E_raw_mpmath30'] = mpmath.nstr(E0, 25); print('E_raw_mpmath30', rec['E_raw_mpmath30'], flush=True)
    if a.prepolish:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fastpol as F
        X = np.array([[float(v) for v in p] for p in pts]); Q, Ef = F.fine(X); rec['E_lbfgs_f64'] = Ef
        pts = [tuple(mpfr(repr(float(v))) for v in q) for q in Q]
        pts = [tuple(v/gmpy2.sqrt(p[0]**2+p[1]**2+p[2]**2) for v in p) for p in pts]; print('prepolish f64', Ef, flush=True)
    hist = []
    for k in range(a.newton+1):
        E, G, T, lam, gn = egrad(pts, a.workers); hist.append(dict(step=k, E_mpfr170=gmpy2.mpfr(E).__format__('.30f'), grad2=float(gn)))
        print('newton', k, hist[-1], round(time.time()-t0), flush=True)
        if gn < a.gtol or k == a.newton: break
        pts, dn = newton_step(pts, T, lam); hist[-1]['step_norm'] = dn
    rec['newton'] = hist; rec['grad2_final'] = float(gn); rec['grad_max_final'] = float(max(abs(t) for v in T for t in v))
    save(pts, a.out+'.txt')
    Ef = energy_mpmath30(load(a.out+'.txt'), a.workers); rec['E_final_mpmath30'] = mpmath.nstr(Ef, 25); print('E_final_mpmath30', rec['E_final_mpmath30'], flush=True)
    rec['E_change_raw_minus_final'] = mpmath.nstr(E0-Ef, 6)
    if a.hessian:
        pts2 = load(a.out+'.txt'); E, G, T, lam, gn = egrad(pts2, a.workers); rec['grad2_saved_file'] = float(gn)
        rec['hessian'] = hessian_cert(pts2, lam, a.workers); print('hessian', rec['hessian'], flush=True)
    rec['secs'] = round(time.time()-t0, 1); json.dump(rec, open(a.out+'.json', 'w'), indent=1); print('DONE', json.dumps(rec), flush=True)
