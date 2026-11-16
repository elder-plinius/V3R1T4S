#!/opt/homebrew/bin/python3
"""
AMS-SVG (`ams_svg`): Adaptive Multi-Scale Spatially Variable Gene Scoring.

Pure-NumPy/SciPy, strictly gene-marginal and coordinate-isometry-invariant SVG
scoring operator (`score_svg(counts, coords)`).

Mathematical specification (frozen prior to blind holdout evaluation):
  1. Strictly Gene-Marginal Variance Stabilization (Zero Library-Size Coupling):
     Each gene column y = counts[:, g] >= 0 is transformed independently via two
     variance-stabilizing maps spanning the Poisson-to-Negative-Binomial dispersion
     spectrum without dividing by spot total counts L_s:
       - T_1(y) = log(1 + y)
       - T_2(y) = sqrt(y) + sqrt(y + 1) - 1   (Freeman-Tukey root)
  2. Multi-Scale Spatial Operators (Exact O(2) & Uniform-Scale Invariance):
     - Local/Meso Scales: Three tie-free self-tuning compactly supported biweight
       operators A_{ij}^{(k)} = max(0, 1 - ||x_i - x_j||^2 / (sigma_i^{(k)} sigma_j^{(k)}))^2
       (i != j) with sigma_i^{(k)} = d_{(k)}(i) for k in {clamp(N//15, 8, 24),
       clamp(round(0.025 N), 28, 120), clamp(round(0.075 N), 64, 320)}, symmetrically
       degree-normalized W^{(k)} = D^{-1/2} A^{(k)} D^{-1/2}. Because A_{ij} > 0 implies
       ||x_i - x_j|| < sigma_i or ||x_i - x_j|| < sigma_j strictly, union symmetrization
       recovers the exact all-pairs N x N kernel in O(N k) operations with zero kd-tree
       equidistant tie-breaking ambiguity.
     - Macro Scales: Three density-equalized O(2)-invariant low-rank Mercer polynomial-
       Gaussian operators (degree P = 26, bandwidth ratios beta in {0.14, 0.26, 0.50} of
       the 99th-percentile centroid radius R_99), evaluated in O(N M) BLAS operations
       without forming N x N matrices.
  3. Underflow-Free Analytical Permutation Standardization:
     For each transformed gene column z and symmetric zero-diagonal operator W, Moran's I
     is standardized by its exact Cliff & Ord (1981) permutation expectation E_perm[I] and
     sample-kurtosis-adjusted permutation variance Var_perm(I; b_2(z)) on the unbounded
     real line (avoiding IEEE-754 float64 p-value underflow ties), then averaged equally
     across all representation-scale pairs.
"""

from __future__ import annotations

import math
from typing import Sequence, Tuple, Union

import numpy as np
import scipy.sparse as sp
import scipy.spatial

SparseOrDense = Union[sp.spmatrix, np.ndarray]
OperatorTuple = Union[
    Tuple[sp.csr_matrix, dict],
    Tuple[np.ndarray, np.ndarray, dict],
]

# Precomputed polynomial index & factorial tables for P = 26 (M = 378 columns)
_MAX_DEG: int = 26
_A_IDX = np.array([a for m in range(_MAX_DEG + 1) for a in range(m + 1)], dtype=np.int32)
_B_IDX = np.array([m - a for m in range(_MAX_DEG + 1) for a in range(m + 1)], dtype=np.int32)
_COEF_VEC = np.array(
    [
        math.exp(-0.5 * (math.lgamma(int(a) + 1) + math.lgamma(int(b) + 1)))
        for a, b in zip(_A_IDX, _B_IDX)
    ],
    dtype=np.float64,
)


def build_self_tuning_biweight_knn_operator(
    coords: np.ndarray, k: int
) -> Tuple[sp.csr_matrix, dict]:
    """Builds exact tie-free self-tuning symmetric biweight operator in O(N k)."""
    n = int(coords.shape[0])
    if n < 5:
        raise ValueError(f"Expected at least 5 spatial locations, got {n}")
    k_eff = min(max(6, int(k)), max(6, n // 2))
    k_eff = min(k_eff, n - 1)

    tree = scipy.spatial.cKDTree(coords)
    dists, nbrs = tree.query(coords, k=k_eff + 1)
    dists = dists[:, 1:]
    nbrs = nbrs[:, 1:]

    sigma = dists[:, -1].copy()
    pos_mask = sigma > 0.0
    pos_med = float(np.median(sigma[pos_mask])) if np.any(pos_mask) else 1.0
    sigma = np.maximum(sigma, 1e-6 * pos_med)

    rows = np.repeat(np.arange(n, dtype=np.int32), k_eff)
    cols = nbrs.ravel().astype(np.int32)
    d_ij = dists.ravel()
    u2 = (d_ij * d_ij) / np.maximum(sigma[rows] * sigma[cols], 1e-30)
    w_dir = np.maximum(0.0, 1.0 - u2) ** 2

    keep = (rows != cols) & (w_dir > 0.0)
    a_dir = sp.csr_matrix((w_dir[keep], (rows[keep], cols[keep])), shape=(n, n))
    a_sym = a_dir.maximum(a_dir.T).tocsr()
    a_sym.setdiag(0.0)
    a_sym.eliminate_zeros()

    deg = np.asarray(a_sym.sum(axis=1)).ravel()
    inv_sqrt_deg = np.zeros_like(deg)
    np.divide(1.0, np.sqrt(deg), out=inv_sqrt_deg, where=deg > 0.0)
    d_inv_sqrt = sp.diags(inv_sqrt_deg)
    w_sym = (d_inv_sqrt @ a_sym @ d_inv_sqrt).tocsr()

    s0 = float(w_sym.sum())
    s1 = float(2.0 * np.sum(w_sym.data * w_sym.data))
    row_sums = np.asarray(w_sym.sum(axis=1)).ravel()
    s2 = float(4.0 * np.sum(row_sums * row_sums))
    return w_sym, {"type": "sparse", "n": n, "s0": s0, "s1": s1, "s2": s2}


def build_mercer_gaussian_lowrank_operator(
    coords: np.ndarray, beta: float
) -> Tuple[np.ndarray, np.ndarray, dict]:
    """Builds exact O(2)- & scale-invariant density-equalized Mercer operator in O(N M)."""
    n, d = coords.shape
    if d != 2:
        # Project isotropically via SVD only if non-2D coordinates are supplied
        c_raw = coords - np.mean(coords, axis=0, keepdims=True)
        _, _, vt = np.linalg.svd(c_raw, full_matrices=False)
        c = c_raw @ vt[:2].T if vt.shape[0] >= 2 else np.hstack([c_raw, np.zeros((n, 1))])
    else:
        c = coords - np.mean(coords, axis=0, keepdims=True)

    radii = np.linalg.norm(c, axis=1)
    r99 = float(np.percentile(radii, 99))
    if r99 <= 0.0:
        r99 = 1.0
    ell = float(beta) * r99

    u = c / ell
    u_norm = np.linalg.norm(u, axis=1, keepdims=True)
    cap = 3.6
    scale = np.where(
        u_norm > cap,
        cap * (1.0 + np.tanh((u_norm - cap) / cap)) / np.maximum(u_norm, 1e-30),
        1.0,
    )
    u = u * scale

    u1 = u[:, 0]
    u2 = u[:, 1]
    env = np.exp(-0.5 * (u1 * u1 + u2 * u2))

    p1 = np.ones((n, _MAX_DEG + 1), dtype=np.float64)
    p2 = np.ones((n, _MAX_DEG + 1), dtype=np.float64)
    for m in range(1, _MAX_DEG + 1):
        p1[:, m] = p1[:, m - 1] * u1
        p2[:, m] = p2[:, m - 1] * u2

    phi = (p1[:, _A_IDX] * p2[:, _B_IDX]) * (env[:, None] * _COEF_VEC[None, :])

    ones_n = np.ones(n, dtype=np.float64)
    deg = phi @ (phi.T @ ones_n)
    inv_sqrt_deg = 1.0 / np.sqrt(np.maximum(deg, 1e-30))
    u_mat = phi * inv_sqrt_deg[:, None]
    d_self = np.sum(u_mat * u_mat, axis=1)

    row_sums = (u_mat @ (u_mat.T @ ones_n)) - d_self
    s0 = float(np.sum(row_sums))
    utu = u_mat.T @ u_mat
    s1 = float(2.0 * (np.sum(utu * utu) - np.sum(d_self * d_self)))
    s2 = float(4.0 * np.sum(row_sums * row_sums))
    return u_mat, d_self, {"type": "lowrank", "n": n, "s0": s0, "s1": s1, "s2": s2}


def build_multiscale_spatial_operators(coords: np.ndarray) -> Sequence[OperatorTuple]:
    """Constructs the frozen 6-scale spatial operator bank from `coords` alone."""
    coords_f = np.asarray(coords, dtype=np.float64)
    if coords_f.ndim != 2 or coords_f.shape[0] < 5:
        raise ValueError(f"Invalid spatial coordinate array shape: {coords_f.shape}")
    n = int(coords_f.shape[0])

    k_scales = sorted(
        {
            min(24, max(8, n // 15)),
            min(120, max(28, int(round(0.025 * n)))),
            min(320, max(64, int(round(0.075 * n)))),
        }
    )
    ops: list[OperatorTuple] = [
        build_self_tuning_biweight_knn_operator(coords_f, k) for k in k_scales
    ]
    for beta in (0.14, 0.26, 0.50):
        ops.append(build_mercer_gaussian_lowrank_operator(coords_f, beta=beta))
    return ops


def _normalize_gene_columns(z_mat: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = int(z_mat.shape[0])
    zc = z_mat - np.mean(z_mat, axis=0, keepdims=True)
    ss = np.sum(zc * zc, axis=0)
    valid = ss > 1e-15
    inv_norm = np.zeros_like(ss)
    inv_norm[valid] = 1.0 / np.sqrt(ss[valid])
    z_hat = zc * inv_norm[None, :]
    b2 = n * np.sum((z_hat * z_hat) ** 2, axis=0)
    return z_hat, b2, valid


def cliff_ord_permutation_z(
    z_hat: np.ndarray, b2: np.ndarray, valid: np.ndarray, op: OperatorTuple
) -> np.ndarray:
    """Exact Cliff & Ord (1981) kurtosis-adjusted permutation Z-score per gene."""
    if len(op) == 2:
        w_sym, stats = op
        wz = w_sym @ z_hat
        rayleigh = np.sum(z_hat * wz, axis=0)
    else:
        u_mat, d_self, stats = op
        proj = u_mat.T @ z_hat
        rayleigh = np.sum(proj * proj, axis=0) - (d_self @ (z_hat * z_hat))

    n = float(stats["n"])
    s0, s1, s2 = stats["s0"], stats["s1"], stats["s2"]
    if s0 <= 1e-18 or n < 5.0:
        return np.zeros(z_hat.shape[1], dtype=np.float64)

    moran_i = (n / s0) * rayleigh
    ei = -1.0 / (n - 1.0)
    a_term = n * ((n * n - 3.0 * n + 3.0) * s1 - n * s2 + 3.0 * s0 * s0)
    b_term = (n * n - n) * s1 - 2.0 * n * s2 + 6.0 * s0 * s0
    denom = (n - 1.0) * (n - 2.0) * (n - 3.0) * (s0 * s0)
    var_i = np.maximum((a_term - b2 * b_term) / denom - ei * ei, 1e-18)
    return np.where(valid, (moran_i - ei) / np.sqrt(var_i), 0.0)


def score_svg(
    counts: SparseOrDense,
    coords: np.ndarray,
    batch_genes: int = 2048,
) -> np.ndarray:
    """
    Computes strictly gene-marginal AMS-SVG spatial variability scores from ONLY
    `(counts, coords)` with O(N k G) CPU complexity and bounded O(N * batch_genes) RAM.
    """
    coords_f = np.asarray(coords, dtype=np.float64)
    n_spots, n_genes = int(counts.shape[0]), int(counts.shape[1])
    if coords_f.shape[0] != n_spots:
        raise ValueError(
            f"Spot count mismatch: counts has {n_spots} rows, coords has {coords_f.shape[0]}"
        )

    ops = build_multiscale_spatial_operators(coords_f)
    n_terms = float(2 * len(ops))
    scores = np.zeros(n_genes, dtype=np.float64)

    for g0 in range(0, n_genes, batch_genes):
        g1 = min(n_genes, g0 + batch_genes)
        sub = counts[:, g0:g1]
        y = sub.toarray().astype(np.float64) if sp.issparse(sub) else np.asarray(sub, dtype=np.float64)
        y = np.maximum(y, 0.0)

        tr_log = _normalize_gene_columns(np.log1p(y))
        tr_ft = _normalize_gene_columns(np.sqrt(y) + np.sqrt(y + 1.0) - 1.0)

        acc = np.zeros(g1 - g0, dtype=np.float64)
        for tr in (tr_log, tr_ft):
            for op in ops:
                acc += cliff_ord_permutation_z(*tr, op)
        scores[g0:g1] = acc / n_terms

    return scores
