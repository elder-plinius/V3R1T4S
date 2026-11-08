"""Exact diagonalisation of the L x L J1-J2 model in VarBench's Pauli convention.

H = J1 sum_<ij> sigma_i.sigma_j + J2 sum_<<ij>> sigma_i.sigma_j   (each bond once, see lattice.py)
sigma_i.sigma_j = s^z s^z + 2 (s^+_i s^-_j + s^-_i s^+_j): diagonal +1 parallel / -1 antiparallel,
off-diagonal +2 between a state and the state with the antiparallel pair (i, j) swapped.

Basis states are integers: bit k = site k, bit 1 = spin up (s = +1), bit 0 = spin down (s = -1).

Usage (library):  from ed import ground_state; E, v, basis, info = ground_state(4, 0.9)
Usage (script):   python ed.py OUTDIR      (runs R1, saves ground states and a JSON summary)
"""
import json, sys, time
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla
from lattice import j1j2_bonds


def popcount(x):
    x = np.asarray(x, dtype=np.int64)
    c = np.zeros_like(x)
    y = x.copy()
    while np.any(y):
        c += y & 1
        y >>= 1
    return c


def sz_basis(N, n_up=None):
    """Sorted integer basis with n_up up spins (default N/2); n_up=-1 -> full 2^N space."""
    x = np.arange(2 ** N, dtype=np.int64)
    if n_up == -1:
        return x
    if n_up is None:
        n_up = N // 2
    return x[popcount(x) == n_up]


def build_H(L, J1=1.0, J2=0.0, basis=None, pbc=True, bonds=None):
    """Sparse Hamiltonian (CSR, float64) on the given sorted integer basis (default Sz=0)."""
    N = L * L
    if basis is None:
        basis = sz_basis(N)
    if bonds is None:
        bonds = j1j2_bonds(L, J1, J2, pbc)
    bi, bj, bJ = bonds[0], bonds[1], bonds[2]
    D = len(basis)
    index = np.full(2 ** N, -1, dtype=np.int64)
    index[basis] = np.arange(D)
    diag = np.zeros(D)
    rows, cols, vals = [], [], []
    for i, j, J in zip(bi, bj, bJ):
        if J == 0.0:
            continue
        par = ((basis >> i) & 1) == ((basis >> j) & 1)
        diag += J * np.where(par, 1.0, -1.0)
        src = np.nonzero(~par)[0]
        tgt = index[basis[src] ^ ((1 << int(i)) | (1 << int(j)))]
        assert np.all(tgt >= 0), "exchange left the basis"
        rows.append(tgt); cols.append(src); vals.append(np.full(len(src), 2.0 * J))
    rows = np.concatenate(rows + [np.arange(D)]); cols = np.concatenate(cols + [np.arange(D)])
    vals = np.concatenate(vals + [diag])
    return sp.coo_matrix((vals, (rows, cols)), shape=(D, D)).tocsr(), basis


def lowest(H, k=4, seed=12345):
    rng = np.random.default_rng(seed)
    v0 = rng.standard_normal(H.shape[0])
    w, V = sla.eigsh(H, k=k, which='SA', v0=v0, tol=0, ncv=max(20, 2 * k + 1))
    o = np.argsort(w)
    return w[o], V[:, o]


def ground_state(L, J2, J1=1.0, pbc=True, k=4):
    H, basis = build_H(L, J1, J2, pbc=pbc)
    w, V = lowest(H, k=k)
    v = V[:, 0].copy()
    v /= np.linalg.norm(v)
    if v[np.argmax(np.abs(v))] < 0:
        v = -v
    Hv = H @ v
    rq = float(v @ Hv)
    info = dict(L=L, J1=J1, J2=J2, pbc=pbc, dim=int(len(basis)), lowest=[float(x) for x in w],
                rayleigh=rq, residual=float(np.linalg.norm(Hv - w[0] * v)), nnz=int(H.nnz))
    return float(w[0]), v, basis, info


def total_S2(L, v, basis):
    """<S_tot^2> (spin-1/2 units) of a vector on the Sz basis: S^2 = (3N + 2 sum_{i<j} sigma_i.sigma_j) / 4."""
    N = L * L
    ii, jj = np.triu_indices(N, 1)
    H, _ = build_H(L, basis=basis, bonds=(ii, jj, np.ones(len(ii))))
    return float((3 * N + 2 * (v @ (H @ v))) / 4)


def full_space_pauli_kron(L, J1, J2, pbc=True, k=6):
    """Independent check: H on the full 2^N space built from literal Pauli matrices by Kronecker products
    (sigma.sigma = XX + YY + ZZ, complex arithmetic), lowest k eigenvalues by eigsh."""
    N = L * L
    bi, bj, bJ, _ = j1j2_bonds(L, J1, J2, pbc)
    X = sp.csr_matrix(np.array([[0, 1], [1, 0]], dtype=complex))
    Y = sp.csr_matrix(np.array([[0, -1j], [1j, 0]], dtype=complex))
    Z = sp.csr_matrix(np.array([[1, 0], [0, -1]], dtype=complex))

    def two_site(A, i, B, j):
        if i > j:
            i, j, A, B = j, i, B, A
        out = sp.identity(2 ** i, dtype=complex, format='csr')
        out = sp.kron(out, A, format='csr')
        out = sp.kron(out, sp.identity(2 ** (j - i - 1), dtype=complex, format='csr'), format='csr')
        out = sp.kron(out, B, format='csr')
        out = sp.kron(out, sp.identity(2 ** (N - 1 - j), dtype=complex, format='csr'), format='csr')
        return out

    H = sp.csr_matrix((2 ** N, 2 ** N), dtype=complex)
    for i, j, J in zip(bi, bj, bJ):
        if J == 0.0:
            continue
        H = H + J * (two_site(X, i, X, j) + two_site(Y, i, Y, j) + two_site(Z, i, Z, j))
    max_imag = float(np.max(np.abs(H.data.imag))) if H.nnz else 0.0
    Hr = H.real.tocsr()
    herm = float(abs(Hr - Hr.T).max())
    w, _ = lowest(Hr, k=k)
    return [float(x) for x in w], dict(max_imag=max_imag, asym=herm, nnz=int(Hr.nnz))


def main(outdir):
    t0 = time.time()
    VB_05 = -33.83169340557936  # VarBench J1J2/square_16_P_0.5.md, exact diagonalisation row
    res = {}
    for J2 in (0.5, 0.55, 0.8, 0.9, 1.0, 0.25):
        E, v, basis, info = ground_state(4, J2)
        info['S2'] = total_S2(4, v, basis)
        res[str(J2)] = info
        np.savez(f"{outdir}/gs_4x4_J2_{J2}.npz", E0=E, psi=v, basis=basis, lowest=np.array(info['lowest']),
                 rayleigh=info['rayleigh'], residual=info['residual'], L=4, J1=1.0, J2=J2,
                 convention="Pauli; bit k = site k = y*L+x, bit 1 = up; Sz=0 sector")
        print(f"4x4 PBC J2={J2}: E0={E!r} lowest={info['lowest']} rayleigh={info['rayleigh']!r} "
              f"residual={info['residual']:.3e} S2={info['S2']:.12f} dim={info['dim']}", flush=True)
    # alternative conventions at J2 = 0.5 (each should FAIL to match VarBench)
    E05 = res['0.5']['lowest'][0]
    Eob, _, _, _ = ground_state(4, 0.5, pbc=False)
    alt = {
        'spin-1/2 operators (E/4)': E05 / 4,
        'diagonal bonds counted twice (= J2 1.0)': res['1.0']['lowest'][0],
        'NN bonds counted twice (= 2 * E(J2 0.25))': 2 * res['0.25']['lowest'][0],
        'open boundaries': Eob,
    }
    r1_pos = abs(E05 - VB_05)
    r1_neg = abs(res['0.55']['lowest'][0] - VB_05)
    r1 = dict(varbench_E=VB_05, E_J2_0_5=E05, absdiff_pos=r1_pos, pass_pos=bool(r1_pos < 1e-8),
              E_J2_0_55=res['0.55']['lowest'][0], absdiff_neg=r1_neg, pass_neg=bool(r1_neg > 1e-3),
              alternative_conventions={k: dict(E=v, absdiff=abs(v - VB_05)) for k, v in alt.items()})
    r1['PASS'] = r1['pass_pos'] and r1['pass_neg']
    print("R1:", json.dumps(r1, indent=1), flush=True)
    # independent full-space check with literal Pauli matrices
    full = {}
    for J2 in (0.5, 0.9):
        t1 = time.time()
        w, meta = full_space_pauli_kron(4, 1.0, J2)
        meta['lowest'] = w
        meta['diff_vs_sz0'] = w[0] - res[str(J2)]['lowest'][0]
        meta['seconds'] = time.time() - t1
        full[str(J2)] = meta
        print(f"full 2^16 Pauli-kron J2={J2}: lowest={w} diff_vs_sz0={meta['diff_vs_sz0']:.3e} "
              f"max_imag={meta['max_imag']} asym={meta['asym']} ({meta['seconds']:.1f} s)", flush=True)
    out = dict(R1=r1, sz0=res, full_space=full, seconds=time.time() - t0)
    with open(f"{outdir}/ed_results.json", "w") as f:
        json.dump(out, f, indent=1)
    print(f"total {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
