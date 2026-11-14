"""Spherical code optimizer: minimize max pairwise inner product on S^{d-1}."""
import numpy as np
import numba


@numba.njit(cache=True, fastmath=True)
def _grad_lse(X, beta):
    """Gradient of (1/beta)*logsumexp(beta*g_ij) wrt X (tangent-projected later)."""
    N, d = X.shape
    G = X @ X.T
    gmax = -1e18
    for i in range(N):
        for j in range(i + 1, N):
            if G[i, j] > gmax:
                gmax = G[i, j]
    # weights
    W = np.zeros((N, N))
    s = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            w = np.exp(beta * (G[i, j] - gmax))
            W[i, j] = w
            W[j, i] = w
            s += w
    grad = np.zeros((N, d))
    for i in range(N):
        gi = 0.0
        for k in range(d):
            acc = 0.0
            for j in range(N):
                if j != i:
                    acc += W[j, i] * X[j, k]
            grad[i, k] = acc / s
    return grad, gmax


@numba.njit(cache=True, fastmath=True)
def lse_optimize(X, betas, iters, lr, seed):
    """Adam on LSE objective; X normalized after each step. Returns best X seen."""
    np.random.seed(seed)
    N, d = X.shape
    m = np.zeros((N, d))
    v = np.zeros((N, d))
    b1, b2, eps = 0.9, 0.999, 1e-9
    t = 0
    best = X.copy()
    bestg = 1e18
    for bi in range(len(betas)):
        beta = betas[bi]
        for it in range(iters):
            t += 1
            grad, gmax = _grad_lse(X, beta)
            # project gradient to tangent of each row
            for i in range(N):
                dot = 0.0
                for k in range(d):
                    dot += grad[i, k] * X[i, k]
                for k in range(d):
                    grad[i, k] -= dot * X[i, k]
            m = b1 * m + (1 - b1) * grad
            v = b2 * v + (1 - b2) * grad * grad
            mh = m / (1 - b1 ** t)
            vh = v / (1 - b2 ** t)
            X = X - lr * mh / (np.sqrt(vh) + eps)
            # renormalize
            for i in range(N):
                nrm = 0.0
                for k in range(d):
                    nrm += X[i, k] ** 2
                nrm = np.sqrt(nrm)
                for k in range(d):
                    X[i, k] /= nrm
            if gmax < bestg:
                bestg = gmax
                best = X.copy()
    return best


def max_ip(X):
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    G = Xn @ Xn.T
    np.fill_diagonal(G, -9)
    return G.max()


def tangent_bases(X):
    """For each unit row x_i, return basis B_i (d x (d-1)) of x_i perp."""
    N, d = X.shape
    B = np.empty((N, d, d - 1))
    for i in range(N):
        # basis of hyperplane perpendicular to X[i] via QR of I - x x^T? Use SVD.
        # cheaper: full QR on [x]
        e = X[i]
        A = np.eye(d) - np.outer(e, e)
        # columns of A span x^perp; orthonormalize via QR
        q, _ = np.linalg.qr(A)
        B[i] = q[:, 1:]
    return B


def slp_polish(X, max_iter=60, rho0=0.02, delta0=3e-5, tol=1e-13, verbose=False):
    """Sequential LP: minimize t s.t. linearized active constraints <= t.
    Uses full-d perturbations u_i with x_i.u_i = 0."""
    from scipy.optimize import linprog
    X = X / np.linalg.norm(X, axis=1, keepdims=True)
    N, d = X.shape
    rho = rho0
    cur = max_ip(X)
    for it in range(max_iter):
        G = X @ X.T
        np.fill_diagonal(G, -9)
        gmax = G.max()
        # active pairs
        A = []
        delta = max(delta0, 8 * rho * max(1.0, abs(gmax)))
        iu = np.triu_indices(N, 1)
        vals = G[iu]
        act = np.where(vals > gmax - delta)[0]
        if len(act) > 2500:
            # too rigid a code for LP polish; keep only top pairs
            thr = np.partition(-vals, 2499)[2499]
            act = np.where(vals >= -thr)[0][:2500]
        pairs = [(iu[0][k], iu[1][k]) for k in act]
        nvar = N * d + 1
        nA = len(pairs)
        rows = np.zeros((nA + N, nvar))
        rhs = np.zeros(nA + N)
        for c, (i, j) in enumerate(pairs):
            rows[c, i * d:(i + 1) * d] = X[j]
            rows[c, j * d:(j + 1) * d] = X[i]
            rows[c, -1] = -1.0
            rhs[c] = -G[i, j]
        for i in range(N):
            rows[nA + i, i * d:(i + 1) * d] = X[i]
            rhs[nA + i] = 0.0
        from scipy.sparse import csr_matrix
        Asp = csr_matrix(rows)
        c = np.zeros(nvar); c[-1] = 1.0
        bounds = [(-rho, rho)] * (N * d) + [(None, gmax)]
        res = linprog(c, A_ub=Asp[:nA], b_ub=rhs[:nA],
                      A_eq=Asp[nA:], b_eq=rhs[nA:], bounds=bounds,
                      method='highs-ipm',
                      options={'time_limit': 20.0,
                               'ipm_iteration_limit': 60})
        if not res.success:
            rho *= 0.5
            if rho < 1e-9:
                break
            continue
        u = res.x[:-1].reshape(N, d)
        t_lp = res.x[-1]
        Xn = X + u
        Xn /= np.linalg.norm(Xn, axis=1, keepdims=True)
        new = max_ip(Xn)
        if verbose:
            print(f'  slp it={it} gmax={gmax:.12f} t_lp={t_lp:.12f} new={new:.12f} nA={nA} rho={rho:.3g}')
        if new < cur - 1e-15:
            X = Xn
            cur = new
            if new < gmax - (gmax - t_lp) * 0.5:
                rho = min(rho * 1.5, 0.2)
        else:
            rho *= 0.4
            if rho < 1e-11:
                break
    return X, cur


def run(X0, betas=None, iters=2000, lr=0.02, seed=0, slp=True, verbose=False):
    if betas is None:
        betas = np.array([2 ** k for k in range(5, 18)], dtype=np.float64)
    X = lse_optimize(np.ascontiguousarray(X0), betas, iters, lr, seed)
    if slp:
        X, cur = slp_polish(X, verbose=verbose)
        return X, cur
    return X, max_ip(X)


@numba.njit(cache=True, fastmath=True)
def hinge_optimize(X, iters, lr, margin0, seed):
    """Minimize sum relu(g_ij - (gmax-margin))^2 ; Adam; margin decays."""
    np.random.seed(seed)
    N, d = X.shape
    m = np.zeros((N, d))
    v = np.zeros((N, d))
    b1, b2, eps = 0.9, 0.999, 1e-9
    margin = margin0
    G = np.empty((N, N))
    for t in range(1, iters + 1):
        # G = X X^T
        for i in range(N):
            for j in range(N):
                s = 0.0
                for k in range(d):
                    s += X[i, k] * X[j, k]
                G[i, j] = s
        gmax = -1e18
        for i in range(N):
            for j in range(i + 1, N):
                if G[i, j] > gmax:
                    gmax = G[i, j]
        thr = gmax - margin
        grad = np.zeros((N, d))
        tot = 0.0
        for i in range(N):
            for j in range(i + 1, N):
                e = G[i, j] - thr
                if e > 0:
                    w = 2 * e
                    tot += e * e
                    for k in range(d):
                        grad[i, k] += w * X[j, k]
                        grad[j, k] += w * X[i, k]
        # project to tangent
        for i in range(N):
            dot = 0.0
            for k in range(d):
                dot += grad[i, k] * X[i, k]
            for k in range(d):
                grad[i, k] -= dot * X[i, k]
        nrm = np.sqrt((grad * grad).sum()) + 1e-18
        grad = grad / nrm
        m = b1 * m + (1 - b1) * grad
        v = b2 * v + (1 - b2) * grad * grad
        mh = m / (1 - b1 ** t)
        vh = v / (1 - b2 ** t)
        X = X - lr * mh / (np.sqrt(vh) + eps)
        for i in range(N):
            n2 = 0.0
            for k in range(d):
                n2 += X[i, k] ** 2
            n2 = np.sqrt(n2)
            for k in range(d):
                X[i, k] /= n2
        if t % 200 == 0 and margin > 1e-9:
            margin *= 0.7
    return X, gmax


def random_code(N, d, rng):
    X = rng.standard_normal((N, d))
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def lbfgs_lse(X0, beta, maxiter=200):
    """L-BFGS on (1/beta) logsumexp(beta*g_ij); X normalized inside objective."""
    from scipy.optimize import minimize
    N, d = X0.shape

    def fg(y):
        X = y.reshape(N, d)
        X = X / np.linalg.norm(X, axis=1, keepdims=True)
        G = X @ X.T
        iu = np.triu_indices(N, 1)
        v = G[iu]
        m = v.max()
        e = np.exp(beta * (v - m))
        s = e.sum()
        f = m + np.log(s) / beta
        w = e / s
        W = np.zeros((N, N))
        W[iu] = w
        W += W.T
        grad = W @ X
        # project each row to tangent (objective is scale-invariant)
        grad -= (grad * X).sum(1, keepdims=True) * X
        return f, grad.ravel()

    res = minimize(fg, X0.ravel(), jac=True, method='L-BFGS-B',
                   options={'maxiter': maxiter, 'ftol': 1e-18, 'gtol': 1e-12})
    X = res.x.reshape(N, d)
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def lbfgs_polish(X0, betas=None, iters=150):
    if betas is None:
        betas = [200, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000]
    X = X0 / np.linalg.norm(X0, axis=1, keepdims=True)
    for b in betas:
        X = lbfgs_lse(X, b, iters)
    return X


@numba.njit(cache=True, fastmath=True)
def _min_ip_to_core(C, iters, lr, seed):
    """Find unit x minimizing max_j x.C_j; Adam on LSE over core C."""
    np.random.seed(seed)
    M, d = C.shape
    best_x = np.empty(d)
    best_v = 1e18
    for trial in range(8):
        x = np.random.standard_normal(d)
        x /= np.sqrt((x ** 2).sum())
        m1 = np.zeros(d); v1 = np.zeros(d)
        b1, b2, eps = 0.9, 0.999, 1e-9
        t = 0
        for beta in (300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0):
            for it in range(iters):
                t += 1
                g = C @ x
                gm = g.max()
                w = np.exp(beta * (g - gm))
                s = w.sum()
                grad = (w[:, None] * C).sum(0) / s
                grad -= (grad @ x) * x
                m1 = b1 * m1 + (1 - b1) * grad
                v1 = b2 * v1 + (1 - b2) * grad * grad
                mh = m1 / (1 - b1 ** t)
                vh = v1 / (1 - b2 ** t)
                x = x - lr * mh / (np.sqrt(vh) + eps)
                x /= np.sqrt((x ** 2).sum())
        v = (C @ x).max()
        if v < best_v:
            best_v = v
            best_x = x.copy()
    return best_x, best_v


def reinsert(C, k_random=200, rng=None):
    """Greedily best single-point insertion minimizing max ip to C."""
    return _min_ip_to_core(np.ascontiguousarray(C), 60, 0.02, 0)
