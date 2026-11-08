import numpy as np
from scipy.optimize import linprog
import packlib


def blockA(U):
    """(m, n*N) matrix with subspace k's n basis vectors at cols k*n..k*n+n-1."""
    m, n, N = U.shape
    return np.transpose(U, (0, 2, 1)).reshape(m, n * N)


def overlap_mat(U):
    m, n, N = U.shape
    A = blockA(U)
    G = A.T @ A
    Gb = G.reshape(N, n, N, n)
    f = np.einsum('ijkl->ik', Gb ** 2)
    return f


def pgrad(U, p):
    """Gradient of p-norm objective F=(sum f^p)^{1/p} w.r.t. each U_i.
    Returns F value and gradient array (m,n,N)."""
    m, n, N = U.shape
    f = overlap_mat(U)
    iu = np.triu_indices(N, 1)
    fi = f[iu]
    fp = fi ** p
    S = fp.sum()
    F = S ** (1.0 / p)
    # weights c_ij = f_ij^{p-1} / F^{p-1}
    C = np.zeros((N, N))
    C[iu] = fi ** (p - 1)
    C = (C + C.T) / (F ** (p - 1))
    # grad_i = 2 * sum_j c_ij U_j U_j^T U_i
    A = blockA(U)
    Gfull = A.T @ A                       # (nN, nN), k-major
    CW = np.kron(C, np.ones((n, n)))
    H = CW * Gfull
    Gall = A @ H                          # col j*n+w = sum_i c_ij U_i (U_i^T u_{j,w})
    grads = 2.0 * np.transpose(Gall.reshape(m, N, n), (0, 2, 1))
    return F, grads


def descend(U, pseq=(4, 8, 16, 32, 64, 128, 256), iters=1500, lr=None, seed_phase=False):
    """Projected-gradient (QR retract) minimization of p-norm of overlaps,
    with rising p. Adam-like scaling per step."""
    m, n, N = U.shape
    U = U.copy()
    best = U.copy()
    bestmax = overlap_mat(U)[np.triu_indices(N, 1)].max()
    for p in pseq:
        mo = np.zeros_like(U)
        vo = np.zeros_like(U)
        b1, b2, eps = 0.9, 0.999, 1e-8
        step = lr if lr else 0.02 / p ** 0.5
        t = 0
        for it in range(iters):
            F, G = pgrad(U, p)
            t += 1
            mo = b1 * mo + (1 - b1) * G
            vo = b2 * vo + (1 - b2) * G * G
            mh = mo / (1 - b1 ** t)
            vh = vo / (1 - b2 ** t)
            U = U - step * mh / (np.sqrt(vh) + eps)
            U = packlib.orth(U)
        iu = np.triu_indices(N, 1)
        fm = overlap_mat(U)[iu].max()
        if fm < bestmax:
            bestmax = fm
            best = U.copy()
    return best


def lp_polish(U, tol=1e-6, max_iter=60, r0=0.05, n_active=4000):
    """Sequential LP on tangent displacements B_i in R^{(m-n) x n}.
    Minimise max overlap. Returns improved U."""
    m, n, N = U.shape
    U = U.copy()
    iu = np.triu_indices(N, 1)
    r = r0
    D = n * (m - n)
    for it in range(max_iter):
        f = overlap_mat(U)
        fi = f[iu]
        fmax = fi.max()
        active = np.where(fi > fmax - tol)[0]
        if len(active) > n_active:
            active = active[np.argsort(fi[active])[-n_active:]]
        # bases Q_i of U_i^\perp
        Q = np.empty((m, m - n, N))
        for k in range(N):
            q, _ = np.linalg.qr(U[:, :, k])
            # complete basis: QR of [U, I]
            M = np.hstack([U[:, :, k], np.eye(m)])
            Qfull, _ = np.linalg.qr(M)
            Q[:, :, k] = Qfull[:, n:]
        # S_ij = Q_i^T P_j U_i  -> ((m-n), n) for each pair
        # Build LP: vars = B flat (N*D) + t
        nv = N * D + 1
        pairs = [(iu[0][a], iu[1][a]) for a in active]
        A_ub = np.zeros((len(pairs), nv))
        for row, (i, j) in enumerate(pairs):
            Sij = 2.0 * Q[:, :, i].T @ U[:, :, j] @ U[:, :, j].T @ U[:, :, i]
            Sji = 2.0 * Q[:, :, j].T @ U[:, :, i] @ U[:, :, i].T @ U[:, :, j]
            A_ub[row, i * D:(i + 1) * D] = Sij.ravel()
            A_ub[row, j * D:(j + 1) * D] = Sji.ravel()
        A_ub[:, -1] = -1.0
        b_ub = -fi[active]
        c = np.zeros(nv)
        c[-1] = 1.0
        bounds = [(-r, r)] * (N * D) + [(0, None)]
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds,
                      method='highs')
        if not res.success:
            r *= 0.5
            continue
        dB = res.x[:-1].reshape(N, D)
        Unew = U.copy()
        for k in range(N):
            Bk = dB[k].reshape(m - n, n)
            Uk = U[:, :, k] + Q[:, :, k] @ Bk
            q, _ = np.linalg.qr(Uk)
            Unew[:, :, k] = q
        fnew = overlap_mat(Unew)[iu].max()
        if fnew < fmax - 1e-12:
            U = Unew
            r = min(r * 1.5, 0.2)
        else:
            r *= 0.5
            if r < 1e-9:
                break
    return U


def polish_and_report(U, label=''):
    f = overlap_mat(U)
    iu = np.triu_indices(U.shape[2], 1)
    d = U.shape[1] - f[iu].max()
    return d
