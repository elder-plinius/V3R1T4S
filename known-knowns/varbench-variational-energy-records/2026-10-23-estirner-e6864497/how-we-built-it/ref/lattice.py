"""J1-J2 square-lattice bonds in VarBench's convention (shared by ed.py and estimator.py).

Site index: i = y * L + x  (x = column, y = row), 0 <= x, y < L.
Bonds (each counted once, periodic in x and y when pbc=True):
  J1: i -> i + x_hat, i -> i + y_hat                       (2N bonds for L >= 3)
  J2: i -> i + x_hat + y_hat, i -> i + x_hat - y_hat      (2N bonds for L >= 3)
With open boundaries, bonds that would wrap are dropped.
"""
import numpy as np


def site(x, y, L):
    return (y % L) * L + (x % L)


def j1j2_bonds(L, J1=1.0, J2=0.0, pbc=True):
    """Return (bi, bj, bJ, kind): int arrays of bond end points, float couplings, kind 1 (NN) or 2 (diagonal).

    Each bond appears exactly once. Raises if a bond would be duplicated (L <= 2 with pbc)."""
    bi, bj, bJ, kind = [], [], [], []
    for y in range(L):
        for x in range(L):
            i = site(x, y, L)
            for dx, dy, J, k in ((1, 0, J1, 1), (0, 1, J1, 1), (1, 1, J2, 2), (1, -1, J2, 2)):
                xx, yy = x + dx, y + dy
                if not pbc and not (0 <= xx < L and 0 <= yy < L):
                    continue
                j = site(xx, yy, L)
                bi.append(i); bj.append(j); bJ.append(J); kind.append(k)
    bi = np.array(bi, dtype=np.int64); bj = np.array(bj, dtype=np.int64)
    bJ = np.array(bJ, dtype=np.float64); kind = np.array(kind, dtype=np.int64)
    pairs = {(min(a, b), max(a, b)) for a, b in zip(bi.tolist(), bj.tolist())}
    if len(pairs) != len(bi) or np.any(bi == bj):
        raise ValueError(f"duplicate or self bonds for L={L}, pbc={pbc}")
    return bi, bj, bJ, kind


def nn_pairs(L, pbc=True):
    """Nearest-neighbour pairs (for local exchange proposals), shape (n, 2)."""
    bi, bj, _, kind = j1j2_bonds(L, 1.0, 1.0, pbc)
    m = kind == 1
    return np.stack([bi[m], bj[m]], axis=1)


def diag_pairs(L, pbc=True):
    bi, bj, _, kind = j1j2_bonds(L, 1.0, 1.0, pbc)
    m = kind == 2
    return np.stack([bi[m], bj[m]], axis=1)
