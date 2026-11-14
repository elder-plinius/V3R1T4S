import numpy as np

def load_flat(path, m, n, N):
    """Load Sloane-style file: m*n*N lines, one coord per line.
    Ordering of basis vectors within the file varies; try both
    consecutive-block and interleaved groupings, keep the one that
    gives more-orthogonal within-subspace bases."""
    a = np.loadtxt(path).reshape(-1, m)
    cands = []
    # interleaved: v-th basis vector of subspace k at row v*N+k
    Ui = np.transpose(a.reshape(n, N, m), (2, 0, 1))
    cands.append(Ui)
    # consecutive: subspace k occupies rows k*n..k*n+n-1
    Uc = np.transpose(a.reshape(N, n, m), (2, 1, 0))
    cands.append(Uc)
    # column-major: each basis vector stored as a length-m column block
    # (seen in grassc.8.2.27 / grassc.7.3.27); non-orthonormal bases OK
    cands.append(a.reshape(-1).reshape(m, n, N, order='F'))
    errs = []
    for U in cands:
        err = 0.0
        for k in range(N):
            G = U[:, :, k].T @ U[:, :, k]
            err = max(err, np.abs(G - np.eye(n)).max())
        errs.append(err)
    i = int(np.argmin(errs))
    if errs[i] < 1e-6:
        return cands[i]
    # no orthonormal parse: return the candidate with the largest
    # post-orthonormalisation min-distance (the genuine layout)
    def _md(U):
        A = np.transpose(U, (0, 2, 1)).reshape(m, n * N)
        G = A.T @ A
        Gb = (G ** 2).reshape(N, n, N, n)
        f = np.einsum('ijkl->ik', Gb)
        iu = np.triu_indices(N, 1)
        return n - f[iu].max()
    best, bestd = None, -np.inf
    for U in cands:
        d = _md(orth(U))
        if d > bestd:
            best, bestd = U, d
    return best

def orth(U):
    """Re-orthonormalize each (m,n) frame via QR."""
    out = np.empty_like(U)
    for k in range(U.shape[2]):
        q, _ = np.linalg.qr(U[:, :, k])
        out[:, :, k] = q
    return out

def overlaps(U):
    """f_ij = ||U_i^T U_j||_F^2 for i<j; returns (i,j,f) arrays."""
    m, n, N = U.shape
    A = np.transpose(U, (0, 2, 1)).reshape(m, n * N)
    G = A.T @ A                     # (nN, nN)
    Gb = G.reshape(N, n, N, n)
    f = np.einsum('ijkl->ik', Gb**2)  # (N,N)
    iu = np.triu_indices(N, 1)
    return iu, f[iu]

def mindist(U):
    m, n, N = U.shape
    iu, f = overlaps(U)
    return n - f.max(), n - f.min()

def table():
    D = {}
    with open('/inputs/grassmannian_2026-11-04.tsv') as fh:
        for line in fh:
            if line.startswith('#') or line.startswith('m\t'):
                continue
            p = line.rstrip('\n').split('\t')
            if len(p) < 8:
                p += [''] * (8 - len(p))
            m, n, N = int(p[0]), int(p[1]), int(p[2])
            D[(m, n, N)] = dict(
                val=float(p[3]) if p[3] else None,
                bnd=float(p[4]) if p[4] else None,
                star=p[5] == 'yes', opt=p[6] == 'yes', cr=p[7])
    return D
