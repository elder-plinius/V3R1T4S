#!/opt/homebrew/bin/python3
"""
AMS-SVG v2 (`ams_svg`): Variance-Stabilized Adaptive Multi-Scale Spatially Variable Gene
Scoring with Scale-Separated Empirical-Bayes Capture Deconfounding and Hilbert-Sphere
Riemannian Geodesic Scale Quadrature.

Pure-NumPy/SciPy, column-permutation-equivariant and coordinate-isometry-invariant SVG
scoring operator (`score_svg(counts, coords)`).

Mathematical specification (frozen prior to blind holdout evaluation):
  1. Scale-Separated Empirical-Bayes High-Pass Capture Deconfounding:
     Decomposes spot total transcription into smooth anatomical compartment structure
     versus sub-compartment technical capture variation relative to the meso-scale
     self-tuning biweight neighborhood expectation P_meso = D^{-1} A^{(k_meso)}:
       - High-pass log-rate residual: U = (I - P_meso) log(1 + Y), centered on 1^perp.
       - Bounded first-order capture sensitivity slope: a_g = E_s[Y_{sg} / (1 + Y_{sg})] in [0, 1),
         standardized by per-gene residual variance v_g = E_s[U_{sg}^2] so no high-count outlier
         gene can dominate spot capture estimation.
       - Deflated-spectral copula floor: projects U_std onto w_hat proportional to a_g / sqrt(v_g)
         (energy E_cap = ||q||_2^2) and computes the maximum singular value squared E_floor of the
         orthogonal complement U_std_perp via deterministic Newton-power-sum-seeded block subspace
         iteration in spot space (under O(2)-invariant canonical column ordering for exact 0-ULP
         column-permutation invariance in O(N G)). When E_cap <= 1.30 * max(E_floor, N) (intact
         counts without spot-wide capture dropout), shrinkage kappa = 0 identically. Above this
         floor, spot log-capture shifts delta_hat_s are shrunk by exact Gauss-Markov Wiener gain
         and removed multiplicatively via Y_corr = Y * exp(-delta_hat_s).
  2. Dual-Endpoint Variance Stabilization:
     Transforms Y_corr column-wise via log(1 + y) (overdispersed NB limit) and Freeman-Tukey
     sqrt(y) + sqrt(y + 1) - 1 (Poisson low-count limit), both strictly invariant to alpha-level
     spatial mixture variance shifts.
  3. Multi-Scale Spatial Operator Bank & Hilbert-Sphere Geodesic Quadrature:
     - Single cKDTree prefix-sliced construction of three tie-free locally density-adapted
       compactly supported biweight kNN operators k in {clamp(round(0.012 N), 14, 56),
       clamp(round(0.035 N), 36, 150), clamp(round(0.090 N), 80, 360)}, symmetrically normalized
       W = D^{-1/2} A D^{-1/2} (tie-free whenever coordinate multiplicity <= k_eff + 1).
     - Three O(2)- and scale-invariant density-equalized low-rank Mercer polynomial-Gaussian
       operators (degree P = 26, bandwidth ratios beta in {0.14, 0.26, 0.45} of R_99).
     - Exact O(N k M) adjacent Hilbert-sphere inner products R_{s, s+1} = tr(W_tilde^{(s)} W_tilde^{(s+1)}) /
       (||W_tilde^{(s)}||_F ||W_tilde^{(s+1)}||_F) on 1^perp, integrated across Cliff & Ord (1981)
       kurtosis-adjusted permutation Z-scores via intrinsic geodesic trapezoid quadrature weights
       d_theta = arccos(R_{s, s+1}) (provably invariant to duplicate scales).
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


def _biweight_from_knn_arrays(
    dists_k: np.ndarray, nbrs_k: np.ndarray, n: int, need_p_row: bool = False
) -> Tuple[sp.csr_matrix, dict, sp.csr_matrix | None]:
    """Constructs symmetric biweight operator from pre-queried k-NN distance/index slices."""
    k_eff = int(dists_k.shape[1])
    sigma = dists_k[:, -1].copy()
    pos_mask = sigma > 0.0
    pos_med = float(np.median(sigma[pos_mask])) if np.any(pos_mask) else 1.0
    sigma = np.maximum(sigma, 1e-6 * pos_med)

    rows = np.repeat(np.arange(n, dtype=np.int32), k_eff)
    cols = nbrs_k.ravel().astype(np.int32)
    d_ij = dists_k.ravel()
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
    w_sym = (sp.diags(inv_sqrt_deg) @ a_sym @ sp.diags(inv_sqrt_deg)).tocsr()

    p_row = None
    if need_p_row:
        inv_deg = np.zeros_like(deg)
        np.divide(1.0, deg, out=inv_deg, where=deg > 0.0)
        p_row = (sp.diags(inv_deg) @ a_sym).tocsr()

    s0 = float(w_sym.sum())
    s1 = float(2.0 * np.sum(w_sym.data * w_sym.data))
    row_sums = np.asarray(w_sym.sum(axis=1)).ravel()
    s2 = float(4.0 * np.sum(row_sums * row_sums))
    return w_sym, {"type": "sparse", "n": n, "s0": s0, "s1": s1, "s2": s2, "row_sums": row_sums}, p_row


def build_self_tuning_biweight_knn_operator(
    coords: np.ndarray, k: int
) -> Tuple[sp.csr_matrix, dict]:
    """Builds exact tie-free self-tuning symmetric biweight operator in O(N k)."""
    coords_f = np.asarray(coords, dtype=np.float64)
    n = int(coords_f.shape[0])
    if n < 5:
        raise ValueError(f"Expected at least 5 spatial locations, got {n}")
    k_eff = min(max(6, int(k)), max(6, n // 2))
    k_eff = min(k_eff, n - 1)
    tree = scipy.spatial.cKDTree(coords_f)
    dists, nbrs = tree.query(coords_f, k=k_eff + 1)
    w_sym, stats, _ = _biweight_from_knn_arrays(dists[:, 1:], nbrs[:, 1:], n, need_p_row=False)
    return w_sym, stats


def build_mercer_gaussian_lowrank_operator(
    coords: np.ndarray, beta: float
) -> Tuple[np.ndarray, np.ndarray, dict]:
    """Builds exact O(2)- & scale-invariant density-equalized Mercer operator in O(N M)."""
    n, d = coords.shape
    if d != 2:
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
    return u_mat, d_self, {"type": "lowrank", "n": n, "s0": s0, "s1": s1, "s2": s2, "row_sums": row_sums}


def _build_operators_and_meso_smoother(
    coords: np.ndarray,
) -> Tuple[list[OperatorTuple], sp.csr_matrix]:
    """Single-cKDTree construction of all 3 biweight kNN operators + 3 Mercer operators."""
    coords_f = np.asarray(coords, dtype=np.float64)
    if coords_f.ndim != 2 or coords_f.shape[0] < 5:
        raise ValueError(f"Invalid spatial coordinate array shape: {coords_f.shape}")
    n = int(coords_f.shape[0])

    raw_ks = sorted(
        {
            min(56, max(14, int(round(0.012 * n)))),
            min(150, max(36, int(round(0.035 * n)))),
            min(360, max(80, int(round(0.090 * n)))),
        }
    )
    k_effs = sorted({min(min(max(6, k), max(6, n // 2)), n - 1) for k in raw_ks})
    meso_idx = min(1, len(k_effs) - 1)

    tree = scipy.spatial.cKDTree(coords_f)
    dists_all, nbrs_all = tree.query(coords_f, k=k_effs[-1] + 1)

    ops: list[OperatorTuple] = []
    p_meso: sp.csr_matrix | None = None
    for idx_k, k_eff in enumerate(k_effs):
        w_sym, st, p_row = _biweight_from_knn_arrays(
            dists_all[:, 1 : k_eff + 1],
            nbrs_all[:, 1 : k_eff + 1],
            n,
            need_p_row=(idx_k == meso_idx),
        )
        ops.append((w_sym, st))
        if idx_k == meso_idx:
            p_meso = p_row

    for beta in (0.14, 0.26, 0.45):
        ops.append(build_mercer_gaussian_lowrank_operator(coords_f, beta=beta))

    assert p_meso is not None
    return ops, p_meso


def build_multiscale_spatial_operators(coords: np.ndarray) -> Sequence[OperatorTuple]:
    """Constructs the frozen 6-scale spatial operator bank from `coords` alone."""
    ops, _ = _build_operators_and_meso_smoother(coords)
    return ops


def _operator_pair_centered_inner_product(op_a: OperatorTuple, op_b: OperatorTuple) -> float:
    """Exact inner product tr(W_tilde^(a) W_tilde^(b)) on 1^perp without N x N matrices."""
    st_a, st_b = op_a[-1], op_b[-1]
    n = int(st_a["n"])
    ones_n = None
    rs_a = st_a.get("row_sums")
    if rs_a is None:
        if len(op_a) == 2:
            rs_a = np.asarray(op_a[0].sum(axis=1)).ravel()
        else:
            ones_n = np.ones(n, dtype=np.float64)
            rs_a = (op_a[0] @ (op_a[0].T @ ones_n)) - op_a[1]
    rs_b = st_b.get("row_sums")
    if rs_b is None:
        if len(op_b) == 2:
            rs_b = np.asarray(op_b[0].sum(axis=1)).ravel()
        else:
            if ones_n is None:
                ones_n = np.ones(n, dtype=np.float64)
            rs_b = (op_b[0] @ (op_b[0].T @ ones_n)) - op_b[1]

    if len(op_a) == 2 and len(op_b) == 2:
        tr_ab = float(op_a[0].multiply(op_b[0]).sum())
    elif len(op_a) == 2 and len(op_b) == 3:
        ub = op_b[0]
        tr_ab = float(np.sum(ub * (op_a[0] @ ub)))
    elif len(op_a) == 3 and len(op_b) == 2:
        ua = op_a[0]
        tr_ab = float(np.sum(ua * (op_b[0] @ ua)))
    else:
        ua, da, _ = op_a
        ub, db, _ = op_b
        ut_u = ua.T @ ub
        tr_ab = float(np.sum(ut_u * ut_u) - np.dot(da, db))

    c_s0 = (n - 2.0) / (float(n) * float(n) * (n - 1.0))
    return tr_ab - (2.0 / n) * float(np.dot(rs_a, rs_b)) + c_s0 * float(st_a["s0"]) * float(st_b["s0"])


def _operator_centered_norm_sq(op: OperatorTuple) -> float:
    """Analytical tr((W_tilde)^2) = 0.5*s1 - (0.5/N)*s2 + ((N-2)/(N^2(N-1)))*s0^2 in O(1)."""
    st = op[-1]
    n = float(st["n"])
    s0, s1, s2 = float(st["s0"]), float(st["s1"]), float(st["s2"])
    c_s0 = (n - 2.0) / (n * n * (n - 1.0))
    return max(0.5 * s1 - (0.5 / n) * s2 + c_s0 * s0 * s0, 1e-30)


def compute_operator_null_correlation_matrix(ops: Sequence[OperatorTuple]) -> np.ndarray:
    """Full S x S null correlation matrix R on 1^perp (for diagnostics & external callers)."""
    s_cnt = len(ops)
    norms = np.array([math.sqrt(_operator_centered_norm_sq(op)) for op in ops], dtype=np.float64)
    r_mat = np.eye(s_cnt, dtype=np.float64)
    for a in range(s_cnt):
        for b in range(a + 1, s_cnt):
            val = _operator_pair_centered_inner_product(ops[a], ops[b]) / (norms[a] * norms[b])
            val = float(np.clip(val, -1.0, 1.0))
            r_mat[a, b] = val
            r_mat[b, a] = val
    return r_mat


def compute_riemannian_arclength_weights(
    ops: Sequence[OperatorTuple], r_mat: np.ndarray | None = None
) -> np.ndarray:
    """
    Intrinsic Hilbert-sphere geodesic arc-length trapezoid quadrature weights across
    spatial operators ordered monotonically by null dispersion s1 / s0^2.
    Evaluates ONLY the S - 1 adjacent inner products along the ordered curve (1 sparse-Mercer
    product instead of 9, bit-exact identical weights).
    """
    s_cnt = len(ops)
    keys = np.array(
        [op[-1]["s1"] / max(op[-1]["s0"] * op[-1]["s0"], 1e-30) for op in ops],
        dtype=np.float64,
    )
    order = np.argsort(keys, kind="mergesort")
    if r_mat is not None:
        adj_corr = np.array(
            [r_mat[order[i], order[i + 1]] for i in range(s_cnt - 1)], dtype=np.float64
        )
    else:
        norms = [math.sqrt(_operator_centered_norm_sq(ops[idx])) for idx in order]
        adj_corr = np.empty(s_cnt - 1, dtype=np.float64)
        for i in range(s_cnt - 1):
            ia, ib = int(order[i]), int(order[i + 1])
            c_val = _operator_pair_centered_inner_product(ops[ia], ops[ib]) / (norms[i] * norms[i + 1])
            adj_corr[i] = float(np.clip(c_val, -1.0, 1.0))

    dtheta = np.arccos(np.clip(adj_corr, -1.0, 1.0))
    w_ord = np.zeros(s_cnt, dtype=np.float64)
    w_ord[:-1] += 0.5 * dtheta
    w_ord[1:] += 0.5 * dtheta
    tot = float(np.sum(w_ord))
    if tot <= 1e-15:
        w_ord[:] = 1.0 / s_cnt
    else:
        w_ord /= tot
    w = np.zeros(s_cnt, dtype=np.float64)
    w[order] = w_ord
    return w


def _canonical_column_order(
    u: np.ndarray, slopes: np.ndarray, spot_anchor_1: np.ndarray, spot_anchor_2: np.ndarray
) -> Tuple[np.ndarray, list[Tuple[int, int]]]:
    """
    Computes a deterministic O(2)- & scale-invariant canonical ordering of active columns in
    O(N G + G log G), returning (order, tied_ranges) so BLAS sums/products over columns are
    0-ULP invariant under arbitrary gene-column permutations without sorting N x G matrices.
    """
    k1 = np.round(slopes, 12)
    k2 = np.round(np.sum(u * u, axis=0), 10)
    k3 = np.round(spot_anchor_1 @ u, 10)
    k4 = np.round(spot_anchor_2 @ (u * u), 10)
    order = np.lexsort((k4, k3, k2, k1))

    # Identify any exact 4-key collision runs (typically 0 runs; if present, row-sort only that tiny slice)
    s1, s2, s3, s4 = k1[order], k2[order], k3[order], k4[order]
    same = (s1[1:] == s1[:-1]) & (s2[1:] == s2[:-1]) & (s3[1:] == s3[:-1]) & (s4[1:] == s4[:-1])
    ties: list[Tuple[int, int]] = []
    if np.any(same):
        m = len(order)
        idx = 0
        while idx < m - 1:
            if same[idx]:
                end = idx + 1
                while end < m - 1 and same[end]:
                    end += 1
                ties.append((idx, end + 1))
                idx = end + 1
            else:
                idx += 1
    return order, ties


def _canon_row_sum(mat_canon: np.ndarray, ties: Sequence[Tuple[int, int]]) -> np.ndarray:
    """Fast O(N G) row sum with exact tie-slice symmetrization if any duplicate columns exist."""
    if not ties:
        return np.sum(mat_canon, axis=1)
    # Sum untied and tied slices deterministically
    acc = np.sum(mat_canon, axis=1)
    for a, b in ties:
        sub = mat_canon[:, a:b]
        acc = acc - np.sum(sub, axis=1) + np.sum(np.sort(sub, axis=1), axis=1)
    return acc


def estimate_eb_capture_log_shift(
    counts: SparseOrDense,
    p_meso: sp.csr_matrix,
    spot_anchor_1: np.ndarray,
    spot_anchor_2: np.ndarray,
    safety_mult: float = 1.30,
) -> Tuple[np.ndarray, dict]:
    """
    Scale-separated Wiener + Deflated-Spectral Empirical-Bayes spot log-capture estimator.
    Preserves smooth compartment expression while deconfounding sub-compartment capture dropout.
    """
    n_spots, n_genes = int(counts.shape[0]), int(counts.shape[1])
    zero_shift = np.zeros(n_spots, dtype=np.float64)
    if n_genes < 8:
        return zero_shift, {"kappa": 0.0, "e_cap": 0.0, "e_floor": 0.0, "ratio": 0.0}

    # Build log1p(Y) and slopes directly without extra full-matrix copies
    if sp.issparse(counts):
        csc = counts.tocsc()
        dat = np.maximum(csc.data.astype(np.float64, copy=False), 0.0)
        slopes = np.zeros(n_genes, dtype=np.float64)
        ratio_dat = dat / (1.0 + dat)
        indptr = csc.indptr
        for g in range(n_genes):
            s_idx, e_idx = int(indptr[g]), int(indptr[g + 1])
            if e_idx > s_idx:
                slopes[g] = float(np.sum(ratio_dat[s_idx:e_idx])) / n_spots
        log_csc = sp.csc_matrix((np.log1p(dat), csc.indices, csc.indptr), shape=(n_spots, n_genes))
        x_log = log_csc.toarray()
    else:
        y_arr = np.maximum(np.asarray(counts, dtype=np.float64), 0.0)
        slopes = np.mean(y_arr / (1.0 + y_arr), axis=0)
        x_log = np.log1p(y_arr)

    active = slopes > 1e-4
    n_act = int(np.sum(active))
    if n_act < 8:
        return zero_shift, {"kappa": 0.0, "e_cap": 0.0, "e_floor": 0.0, "ratio": 0.0}

    # Restrict to active columns before dense smoothing & centering
    x_act = x_log[:, active] if n_act < n_genes else x_log
    slopes_act = slopes[active]

    has_nbrs = np.asarray(p_meso.sum(axis=1)).ravel() > 0.5
    u = x_act - (p_meso @ x_act)
    if not np.all(has_nbrs):
        u[~has_nbrs, :] = 0.0
    u -= np.mean(u, axis=0, keepdims=True)

    # Canonicalize column order for 0-ULP permutation invariance across all BLAS reductions
    canon_ord, ties = _canonical_column_order(u, slopes_act, spot_anchor_1, spot_anchor_2)
    u = np.ascontiguousarray(u[:, canon_ord])
    slopes_act = slopes_act[canon_ord]

    v_g = np.maximum(np.sum(u * u, axis=0) / max(n_spots, 1), 1e-4)
    inv_sqrt_v = 1.0 / np.sqrt(v_g)
    u *= inv_sqrt_v[None, :]  # In-place standardization: u is now U_std!

    w_dir = slopes_act * inv_sqrt_v
    w_sq_sum = float(np.sum(w_dir * w_dir))
    if w_sq_sum <= 1e-12:
        return zero_shift, {"kappa": 0.0, "e_cap": 0.0, "e_floor": 0.0, "ratio": 0.0}

    w_norm = math.sqrt(w_sq_sum)
    w_hat = w_dir / w_norm

    q = _canon_row_sum(u * w_hat[None, :], ties) if ties else (u @ w_hat)
    q -= float(np.mean(q))
    e_cap = float(np.dot(q, q))
    e_diag = float(n_spots)
    if e_cap <= max(1.05 * e_diag, 1e-12):
        return zero_shift, {
            "kappa": 0.0,
            "e_cap": e_cap,
            "e_floor": e_diag,
            "ratio": e_cap / max(e_diag, 1e-12),
        }

    # Newton power-sum spot seeds in O(N G) with zero N x G sorting
    u2 = u * u
    s1_vec = _canon_row_sum(u, ties)
    s2_vec = _canon_row_sum(u2, ties)
    s3_vec = _canon_row_sum(u2 * u, ties)
    s4_vec = _canon_row_sum(u2 * u2, ties)
    del u2

    b_seeds = np.column_stack([s1_vec, s2_vec, s3_vec, s4_vec])
    b_seeds -= np.mean(b_seeds, axis=0, keepdims=True)
    v_blk, _ = np.linalg.qr(b_seeds)
    for _ in range(10):
        ut_v = u.T @ v_blk - np.outer(w_hat, q @ v_blk)
        v_next = (u @ ut_v) - np.outer(q, w_hat @ ut_v)
        if np.max(np.linalg.norm(v_next, axis=0)) <= 1e-15:
            break
        v_blk, _ = np.linalg.qr(v_next)
    ut_v = u.T @ v_blk - np.outer(w_hat, q @ v_blk)
    e_floor = float(np.max(np.linalg.eigvalsh(ut_v.T @ ut_v)))

    denom_floor = max(e_floor, e_diag)
    ratio = e_cap / max(denom_floor, 1e-15)
    noise_bound = safety_mult * denom_floor
    if e_cap <= noise_bound:
        return zero_shift, {
            "kappa": 0.0,
            "e_cap": e_cap,
            "e_floor": e_floor,
            "ratio": ratio,
        }

    gate = 1.0 - noise_bound / e_cap
    sig2_delta = max(0.0, (e_cap - denom_floor) / (n_spots * w_sq_sum))
    wiener_gain = (w_sq_sum * sig2_delta) / (1.0 + w_sq_sum * sig2_delta)
    kappa = gate * wiener_gain
    delta_hat = np.clip(kappa * (q / w_norm), -2.5, 2.5)
    return delta_hat, {
        "kappa": float(kappa),
        "e_cap": e_cap,
        "e_floor": e_floor,
        "ratio": ratio,
    }


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


def _spatial_morton_order(coords_f: np.ndarray) -> np.ndarray:
    """2D Morton Z-order spot permutation maximizing CPU cache locality on large point clouds."""
    c = coords_f[:, :2] - np.mean(coords_f[:, :2], axis=0, keepdims=True)
    c_min = np.min(c, axis=0)
    c_ptp = np.maximum(np.ptp(c, axis=0), 1e-12)
    q = np.clip(((c - c_min) / c_ptp * 65535.0).astype(np.uint32), 0, 65535)

    def _part1by1(v: np.ndarray) -> np.ndarray:
        v = (v | (v << 8)) & np.uint32(0x00FF00FF)
        v = (v | (v << 4)) & np.uint32(0x0F0F0F0F)
        v = (v | (v << 2)) & np.uint32(0x33333333)
        v = (v | (v << 1)) & np.uint32(0x55555555)
        return v

    code = _part1by1(q[:, 0]) | (_part1by1(q[:, 1]) << np.uint32(1))
    return np.argsort(code, kind="mergesort")


def score_svg(
    counts: SparseOrDense,
    coords: np.ndarray,
    batch_genes: int = 2048,
    return_diagnostics: bool = False,
) -> Union[np.ndarray, Tuple[np.ndarray, dict]]:
    """
    Computes AMS-SVG v2 spatial variability scores from ONLY `(counts, coords)` with
    O(N k G) CPU complexity, exact column-permutation equivariance, and O(2)/scale invariance.
    """
    coords_f = np.asarray(coords, dtype=np.float64)
    n_spots, n_genes = int(counts.shape[0]), int(counts.shape[1])
    if coords_f.shape[0] != n_spots:
        raise ValueError(
            f"Spot count mismatch: counts has {n_spots} rows, coords has {coords_f.shape[0]}"
        )

    spot_order = None
    if n_spots >= 8192 and coords_f.shape[1] >= 2:
        spot_order = _spatial_morton_order(coords_f)
        coords_f = np.ascontiguousarray(coords_f[spot_order])
        counts = counts[spot_order, :]

    ops, p_meso = _build_operators_and_meso_smoother(coords_f)
    w_arc = compute_riemannian_arclength_weights(ops)

    # O(2)- & scale-invariant spot anchors from existing operators for canonical column ordering
    spot_anchor_1 = ops[0][-1]["row_sums"]
    spot_anchor_2 = ops[-1][1]  # Mercer d_self

    delta_hat, eb_diag = estimate_eb_capture_log_shift(
        counts, p_meso, spot_anchor_1, spot_anchor_2
    )
    has_shift = bool(np.any(delta_hat != 0.0))
    spot_mult = np.exp(-delta_hat)[:, None] if has_shift else None

    scores = np.zeros(n_genes, dtype=np.float64)
    for g0 in range(0, n_genes, batch_genes):
        g1 = min(n_genes, g0 + batch_genes)
        sub = counts[:, g0:g1]
        y = sub.toarray().astype(np.float64) if sp.issparse(sub) else np.asarray(sub, dtype=np.float64)
        y = np.maximum(y, 0.0)
        if spot_mult is not None:
            y = y * spot_mult

        tr_log = _normalize_gene_columns(np.log1p(y))
        tr_ft = _normalize_gene_columns(np.sqrt(y) + np.sqrt(y + 1.0) - 1.0)

        z_log = np.vstack([cliff_ord_permutation_z(*tr_log, op) for op in ops])
        z_ft = np.vstack([cliff_ord_permutation_z(*tr_ft, op) for op in ops])
        scores[g0:g1] = w_arc @ (0.5 * (z_log + z_ft))

    if return_diagnostics:
        if spot_order is not None:
            inv_spot = np.argsort(spot_order)
            eb_diag["delta_hat"] = delta_hat[inv_spot]
        eb_diag["scale_weights"] = w_arc.tolist()
        return scores, eb_diag
    return scores
