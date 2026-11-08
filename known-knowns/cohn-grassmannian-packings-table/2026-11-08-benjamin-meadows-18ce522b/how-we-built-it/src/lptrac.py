import numpy as np, time
from scipy.optimize import linprog
from worker import overlap_mat

def lp_trace(U, tol=2e-5, max_iter=20, r0=0.1, n_active=1600, deadline=None,
             early=None, gapor_stop=None, noacc_stop=None,
             method='highs', lp_time=None, max_r=0.2, dstop=None):
    """lp_polish variant returning (U, trace). trace rows: (it, fmax, tstar, acc, r).
    gapor_stop: if set, abort when it>=5, last 5 iters unaccepted, and
    median(gap/r over last 3) < gapor_stop (phantom directions only).
    noacc_stop: abort if no accepted step has occurred by this iter.
    early: abort if `early` consecutive gaps all < 3e-12."""
    import scipy.sparse as sp
    m, n, N = U.shape
    U = U.copy()
    iu = np.triu_indices(N, 1)
    r = r0
    D = n * (m - n)
    Q = np.empty((m, m - n, N))
    trace = []
    ever_acc = False
    dry = 0
    for it in range(max_iter):
        if deadline is not None and time.time() > deadline:
            break
        f = overlap_mat(U)
        fi = f[iu]
        fmax = fi.max()
        active = np.where(fi > fmax - tol)[0]
        if len(active) > n_active:
            active = active[np.argsort(fi[active])[-n_active:]]
        for k in range(N):
            M = np.hstack([U[:, :, k], np.eye(m)])
            Qfull, _ = np.linalg.qr(M)
            Q[:, :, k] = Qfull[:, n:]
        nv = N * D + 1
        A_ub = np.zeros((len(active), nv))
        b_ub = -fi[active]
        for row, a in enumerate(active):
            i, j = iu[0][a], iu[1][a]
            Sij = 2.0 * Q[:, :, i].T @ U[:, :, j] @ U[:, :, j].T @ U[:, :, i]
            Sji = 2.0 * Q[:, :, j].T @ U[:, :, i] @ U[:, :, i].T @ U[:, :, j]
            A_ub[row, i * D:(i + 1) * D] = Sij.ravel()
            A_ub[row, j * D:(j + 1) * D] = Sji.ravel()
        A_ub[:, -1] = -1.0
        c = np.zeros(nv); c[-1] = 1.0
        bounds = [(-r, r)] * (N * D) + [(0, None)]
        res = linprog(c, A_ub=sp.csr_matrix(A_ub), b_ub=b_ub,
                      bounds=bounds, method=method,
                      options={'time_limit': lp_time} if lp_time else None)
        if not res.success:
            r *= 0.5; continue
        tstar = res.x[-1]
        dB = res.x[:-1].reshape(N, D)
        Unew = U.copy()
        for k in range(N):
            Bk = dB[k].reshape(m - n, n)
            q, _ = np.linalg.qr(U[:, :, k] + Q[:, :, k] @ Bk)
            Unew[:, :, k] = q
        fnew = overlap_mat(Unew)[iu].max()
        acc = fnew < fmax - 1e-12
        if acc:
            U = Unew; r = min(r * 1.5, max_r); ever_acc = True; dry = 0
        else:
            r *= 0.5
            dry = dry + 1 if not ever_acc else 0
        trace.append((it, fmax, tstar, acc, r))
        if dstop is not None and acc and fnew < dstop:
            break
        gaps = [t[1] - t[2] for t in trace]
        if early and len(gaps) >= early and max(gaps[-early:]) < 3e-12:
            break
        if gapor_stop and it >= 5:
            g = [t[1] - t[2] for t in trace[-3:]]
            rr = [t[4] for t in trace[-3:]]
            if (not any(t[3] for t in trace[-5:])) and \
               sorted(g[i] / rr[i] for i in range(3))[1] < gapor_stop:
                break
        if noacc_stop and it >= noacc_stop and not any(t[3] for t in trace):
            break
        if r < 1e-9:
            break
    return U, trace
