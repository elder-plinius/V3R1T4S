import numpy as np, packlib, opt, time, os, json, sys
from scipy.optimize import linprog


def blockA(U):
    m, n, N = U.shape
    return np.transpose(U, (0, 2, 1)).reshape(m, n * N)


def overlap_mat(U):
    m, n, N = U.shape
    A = blockA(U)
    G = A.T @ A
    Gb = G.reshape(N, n, N, n)
    f = np.einsum('ijkl->ik', Gb ** 2)
    return f


def mind(U):
    f = overlap_mat(U)
    iu = np.triu_indices(U.shape[2], 1)
    return U.shape[1] - f[iu].max()


def pgrad(U, p):
    m, n, N = U.shape
    f = overlap_mat(U)
    iu = np.triu_indices(N, 1)
    fi = f[iu]
    fp = fi ** p
    S = fp.sum()
    F = S ** (1.0 / p)
    C = np.zeros((N, N))
    C[iu] = fi ** (p - 1)
    C = (C + C.T) / (F ** (p - 1))
    A = blockA(U)
    Gfull = A.T @ A
    CW = np.kron(C, np.ones((n, n)))
    H = CW * Gfull
    Gall = A @ H
    grads = 2.0 * np.transpose(Gall.reshape(m, N, n), (0, 2, 1))
    return F, grads


def descend(U, pseq, iters, lr=None):
    U = U.copy()
    N = U.shape[2]
    iu = np.triu_indices(N, 1)
    best = U.copy()
    bestmax = overlap_mat(U)[iu].max()
    for p in pseq:
        mo = np.zeros_like(U); vo = np.zeros_like(U)
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
            U = orth_frames(U)
        fm = overlap_mat(U)[iu].max()
        if fm < bestmax:
            bestmax = fm; best = U.copy()
    return best


def orth_frames(U):
    out = np.empty_like(U)
    for k in range(U.shape[2]):
        q, _ = np.linalg.qr(U[:, :, k])
        out[:, :, k] = q
    return out


def lp_polish(U, tol=1e-5, max_iter=20, r0=0.05, n_active=2500, deadline=None):
    import scipy.sparse as sp
    m, n, N = U.shape
    U = U.copy()
    iu = np.triu_indices(N, 1)
    r = r0
    D = n * (m - n)
    Q = np.empty((m, m - n, N))
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
        rows = []
        for a in active:
            rows.append((iu[0][a], iu[1][a]))
        A_ub = np.zeros((len(rows), nv))
        b_ub = -fi[active]
        for row, (i, j) in enumerate(rows):
            Sij = 2.0 * Q[:, :, i].T @ U[:, :, j] @ U[:, :, j].T @ U[:, :, i]
            Sji = 2.0 * Q[:, :, j].T @ U[:, :, i] @ U[:, :, i].T @ U[:, :, j]
            A_ub[row, i * D:(i + 1) * D] = Sij.ravel()
            A_ub[row, j * D:(j + 1) * D] = Sji.ravel()
        A_ub[:, -1] = -1.0
        c = np.zeros(nv); c[-1] = 1.0
        bounds = [(-r, r)] * (N * D) + [(0, None)]
        res = linprog(c, A_ub=sp.csr_matrix(A_ub), b_ub=b_ub,
                      bounds=bounds, method='highs')
        if not res.success:
            r *= 0.5; continue
        dB = res.x[:-1].reshape(N, D)
        Unew = U.copy()
        for k in range(N):
            Bk = dB[k].reshape(m - n, n)
            q, _ = np.linalg.qr(U[:, :, k] + Q[:, :, k] @ Bk)
            Unew[:, :, k] = q
        fnew = overlap_mat(Unew)[iu].max()
        if fnew < fmax - 1e-12:
            U = Unew; r = min(r * 1.5, 0.2)
        else:
            r *= 0.5
            if r < 1e-9:
                break
    return U


def perturb(U, rng, mag=None, kfrac=0.15):
    m, n, N = U.shape
    if mag is None:
        mag = 10 ** rng.uniform(-1.5, -0.2)
    Un = U.copy()
    K = max(1, int(round(kfrac * N)))
    idx = rng.choice(N, size=K, replace=False)
    for k in idx:
        H = rng.standard_normal((m, n))
        H = H - U[:, :, k] @ (U[:, :, k].T @ H)
        nrm = np.linalg.norm(H)
        if nrm > 0:
            H = H / nrm * mag
        q, _ = np.linalg.qr(U[:, :, k] + H)
        Un[:, :, k] = q
    return Un


def optimize(m, n, N, U0, budget, seed=0, iters=250,
             pseq=(8, 16, 32, 64), lp_iters=15, tag=None):
    rng = np.random.default_rng(seed)
    t0 = time.time()
    nv = N * n * (m - n) + 1
    lp_it0 = 20 if nv < 1200 else 10
    lp_it_tr = 9 if nv < 1200 else 6
    nact = 1600 if nv < 1200 else 1200

    def save(best):
        if tag:
            os.makedirs('results', exist_ok=True)
            np.save(f'results/{tag}.npy', best)

    # start from polished seed
    U0p = lp_polish(U0, tol=1e-5, max_iter=lp_it0, n_active=nact)
    best = U0p.copy(); bestd = mind(U0p)
    save(best)
    pool = [(bestd, U0p)]
    trials = 0
    while time.time() - t0 < budget:
        trials += 1
        if trials % 6 == 0:
            Up = orth_frames(rng.standard_normal((m, n, N)))
        else:
            Up = perturb(best, rng)
        Ud = descend(Up, pseq=pseq, iters=iters)
        d = mind(Ud)
        if d > bestd - 1e-5:
            Ud = lp_polish(Ud, tol=1e-5, max_iter=lp_it_tr, n_active=nact)
            d = mind(Ud)
            pool.append((d, Ud))
            if d > bestd + 1e-11:
                bestd = d; best = Ud.copy()
                save(best)
                print(json.dumps(dict(trials=trials, d=d, t=round(time.time()-t0,1))), flush=True)
    # final full polish on the best config
    best = lp_polish(best, tol=1e-6, max_iter=30 if nv < 1200 else 12, r0=0.03,
                     n_active=2500 if nv < 1200 else 1200)
    bestd = mind(best)
    save(best)
    pool.sort(key=lambda x: -x[0])
    return best, bestd, trials


if __name__ == '__main__':
    # args: m n N budget seed [workerid]
    m, n, N = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    budget = float(sys.argv[4]); seed = int(sys.argv[5])
    path = f'grass/txts/grassc.{m}.{n}.{N}.txt'
    if os.path.exists(path):
        U0 = packlib.orth(packlib.load_flat(path, m, n, N))
    else:
        rng = np.random.default_rng(seed)
        U0 = orth_frames(rng.standard_normal((m, n, N)))
    iters = 250 if N <= 60 else 150
    tag = f'{m}-{n}-{N}.{seed}'
    best, bd, tr = optimize(m, n, N, U0, budget, seed=seed, iters=iters, tag=tag)
    np.save(f'results/{tag}.npy', best)
    print(json.dumps(dict(m=m, n=n, N=N, d=bd, trials=tr, seed=seed)))
