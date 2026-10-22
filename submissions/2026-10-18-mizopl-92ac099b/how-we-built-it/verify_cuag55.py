#!/usr/bin/env python3
"""
Exact verification, 30-digit mpmath polish, and 3N x 3N analytical Hessian check
for the 8 improved Cu_n Ag_{55-n} nanoalloy structures in CuAg_55.rar.
"""
import glob
import os
import numpy as np
from scipy.optimize import minimize
import mpmath as mp

# Exact Cu-Ag Gupta parameters (Rapallo, Rossi, Ferrando 2005 / Wu, Cai, Shao 2009 / Lai, Huang, Xu 2011)
# Type 0 = Cu-Cu, Type 1 = Cu-Ag, Type 2 = Ag-Ag
PARAMS = {
    0: (0.0894, 1.2799, 10.550, 2.430, 2.556),
    1: (0.0980, 1.2274, 10.700, 2.805, 2.72405),
    2: (0.1031, 1.1895, 10.850, 3.180, 2.8921),
}

A_ARR  = np.array([PARAMS[0][0], PARAMS[1][0], PARAMS[2][0]], dtype=np.float64)
XI_ARR = np.array([PARAMS[0][1], PARAMS[1][1], PARAMS[2][1]], dtype=np.float64)
P_ARR  = np.array([PARAMS[0][2], PARAMS[1][2], PARAMS[2][2]], dtype=np.float64)
Q_ARR  = np.array([PARAMS[0][3], PARAMS[1][3], PARAMS[2][3]], dtype=np.float64)
R0_ARR = np.array([PARAMS[0][4], PARAMS[1][4], PARAMS[2][4]], dtype=np.float64)

def load_cuag_file(path):
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    e_hdr = None
    sp = []
    coords = []
    for l in lines:
        if "E=" in l:
            for tok in l.split():
                if tok.startswith("E="):
                    e_hdr = float(tok.split("=")[1])
            continue
        if l.startswith("type") or l.startswith("NA("):
            continue
        parts = l.split()
        if len(parts) < 4:
            continue
        s_tok = parts[0]
        if s_tok in ("0", "Cu"):
            sp.append(0)
        elif s_tok in ("1", "Ag"):
            sp.append(1)
        else:
            continue
        coords.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return e_hdr, np.array(sp, dtype=np.int32), np.array(coords, dtype=np.float64)

def energy_and_grad(x_flat, sp):
    n = len(sp)
    coords = x_flat.reshape(n, 3)
    diff = coords[:, None, :] - coords[None, :, :]
    r = np.sqrt(np.sum(diff**2, axis=-1))
    np.fill_diagonal(r, 1.0)
    tp = sp[:, None] + sp[None, :]
    A = A_ARR[tp]
    xi = XI_ARR[tp]
    p = P_ARR[tp]
    q = Q_ARR[tp]
    r0 = R0_ARR[tp]

    u = r / r0 - 1.0
    rep = A * np.exp(-p * u)
    phi = (xi**2) * np.exp(-2.0 * q * u)
    np.fill_diagonal(rep, 0.0)
    np.fill_diagonal(phi, 0.0)

    rho = np.sum(phi, axis=1)
    sqrt_rho = np.sqrt(rho)
    E = float(np.sum(np.sum(rep, axis=1) - sqrt_rho))

    # dE/dr_ij for i != j (symmetric pair contribution):
    # In E = sum_i sum_{j!=i} rep_ij - sum_i sqrt(sum_{j!=i} phi_ij),
    # each unordered pair {i,j} contributes 2 * rep_ij to the repulsive sum,
    # and phi_ij contributes to both rho_i and rho_j.
    inv_sqrt = 1.0 / sqrt_rho
    dE_dr_half = (-p / r0) * rep + (0.5 * (inv_sqrt[:, None] + inv_sqrt[None, :])) * (q / r0) * phi
    np.fill_diagonal(dE_dr_half, 0.0)
    # Since both (i,j) and (j,i) appear in sum_j, grad_i = 2 * sum_j dE_dr_half_ij * (r_i - r_j)/r_ij
    coeff = 2.0 * dE_dr_half / r
    np.fill_diagonal(coeff, 0.0)
    grad = np.sum(coeff[:, :, None] * diff, axis=1)
    return E, grad.reshape(-1)

def analytical_hessian(coords, sp):
    n = len(sp)
    diff = coords[:, None, :] - coords[None, :, :]
    r = np.sqrt(np.sum(diff**2, axis=-1))
    np.fill_diagonal(r, 1.0)
    tp = sp[:, None] + sp[None, :]
    A = A_ARR[tp]
    xi = XI_ARR[tp]
    p = P_ARR[tp]
    q = Q_ARR[tp]
    r0 = R0_ARR[tp]

    u = r / r0 - 1.0
    rep = A * np.exp(-p * u)
    phi = (xi**2) * np.exp(-2.0 * q * u)
    np.fill_diagonal(rep, 0.0)
    np.fill_diagonal(phi, 0.0)

    rho = np.sum(phi, axis=1)
    sqrt_rho = np.sqrt(rho)

    # First and second derivatives of rep_ij and phi_ij w.r.t. r_ij
    b = p / r0
    d = 2.0 * q / r0
    rep1 = -b * rep
    rep2 = (b**2) * rep
    phi1 = -d * phi
    phi2 = (d**2) * phi
    np.fill_diagonal(rep1, 0.0)
    np.fill_diagonal(rep2, 0.0)
    np.fill_diagonal(phi1, 0.0)
    np.fill_diagonal(phi2, 0.0)

    # Unit vectors e_ij = (r_i - r_j)/r_ij
    e_vec = diff / r[:, :, None]
    for i in range(n):
        e_vec[i, i, :] = 0.0

    H = np.zeros((3 * n, 3 * n), dtype=np.float64)

    # Pairwise terms: E_rep = sum_{i != j} rep_ij, and the direct second-derivative part of -sum_i sqrt(rho_i)
    # Wait: -sqrt(rho_i) has first derivative w.r.t. r_k: -(1/(2 sqrt(rho_i))) d(rho_i)/dr_k
    # and second derivative w.r.t. r_k, r_l:
    # -(1/(2 sqrt(rho_i))) d^2(rho_i)/(dr_k dr_l) + (1/(4 rho_i^(3/2))) (d(rho_i)/dr_k)(d(rho_i)/dr_l)^T
    inv_2sqrt = 0.5 / sqrt_rho
    inv_4rho32 = 0.25 / (rho * sqrt_rho)

    # 1) Pairwise radial terms: for each ordered pair (i, j) with i != j,
    # f(r_ij) = 2 * rep_ij - (inv_2sqrt[i] + inv_2sqrt[j]) * phi_ij
    # contributes 0.5 * f(r_ij) per ordered pair -> sum_{i < j} f(r_ij)
    f1 = 2.0 * rep1 - (inv_2sqrt[:, None] + inv_2sqrt[None, :]) * phi1
    f2 = 2.0 * rep2 - (inv_2sqrt[:, None] + inv_2sqrt[None, :]) * phi2
    for i in range(n):
        for j in range(i + 1, n):
            eij = e_vec[i, j]
            P_par = np.outer(eij, eij)
            P_perp = (np.eye(3) - P_par) / r[i, j]
            block = f2[i, j] * P_par + f1[i, j] * P_perp
            H[3*i:3*i+3, 3*i:3*i+3] += block
            H[3*j:3*j+3, 3*j:3*j+3] += block
            H[3*i:3*i+3, 3*j:3*j+3] -= block
            H[3*j:3*j+3, 3*i:3*i+3] -= block

    # 2) Three-body term from + sum_i (1/(4 rho_i^(3/2))) grad(rho_i) grad(rho_i)^T
    # For each atom i, rho_i = sum_{j != i} phi_ij(r_ij).
    # Let g_ij = phi1[i, j] * e_vec[i, j] (3-vector).
    # Then d(rho_i)/dr_j = -g_ij for j != i, and d(rho_i)/dr_i = sum_{j != i} g_ij.
    for i in range(n):
        G_i = np.zeros((3 * n, 3), dtype=np.float64)
        g_sum = np.zeros(3, dtype=np.float64)
        for j in range(n):
            if i == j:
                continue
            g_ij = phi1[i, j] * e_vec[i, j]
            G_i[3*j:3*j+3, :] = -g_ij[:, None] if False else np.diag(-g_ij) # wait: G_i is a 3N-vector!
        # Let's build the 3N gradient vector grad_rho_i of rho_i:
        grad_rho_i = np.zeros(3 * n, dtype=np.float64)
        for j in range(n):
            if i == j:
                continue
            g_ij = phi1[i, j] * e_vec[i, j]
            grad_rho_i[3*j:3*j+3] = -g_ij
            g_sum += g_ij
        grad_rho_i[3*i:3*i+3] = g_sum
        H += inv_4rho32[i] * np.outer(grad_rho_i, grad_rho_i)

    return H

def mpmath_polish_and_eval(coords, sp, dps=30):
    mp.mp.dps = dps
    # First polish tightly in float64 using L-BFGS-B + BFGS
    res1 = minimize(energy_and_grad, coords.reshape(-1), args=(sp,), method="L-BFGS-B", jac=True,
                    options={"ftol": 1e-15, "gtol": 1e-14, "maxiter": 10000, "maxfun": 50000})
    res2 = minimize(energy_and_grad, res1.x, args=(sp,), method="BFGS", jac=True,
                    options={"gtol": 1e-14, "maxiter": 5000})
    x_best = res2.x if res2.fun <= res1.fun else res1.x
    # Now do Newton-Raphson steps in 30-digit mpmath on the 3N-6 internal coordinates (or damped Newton with 1e-16 shift in 30-digit mpmath, or conjugate-gradient / Barzilai-Borwein in mpmath)
    n = len(sp)
    A_mp  = [mp.mpf(str(PARAMS[t][0])) for t in range(3)]
    xi_mp = [mp.mpf(str(PARAMS[t][1])) for t in range(3)]
    p_mp  = [mp.mpf(str(PARAMS[t][2])) for t in range(3)]
    q_mp  = [mp.mpf(str(PARAMS[t][3])) for t in range(3)]
    r0_mp = [mp.mpf(str(PARAMS[t][4])) for t in range(3)]

    X = [mp.mpf(repr(float(v))) for v in x_best]

    def mp_eg(X_vec):
        E_tot = mp.mpf(0)
        G = [mp.mpf(0)] * (3 * n)
        rho = [mp.mpf(0)] * n
        sqrt_rho = [mp.mpf(0)] * n
        inv_sqrt = [mp.mpf(0)] * n
        r_mat = [[mp.mpf(0)] * n for _ in range(n)]
        rep_mat = [[mp.mpf(0)] * n for _ in range(n)]
        phi_mat = [[mp.mpf(0)] * n for _ in range(n)]
        for i in range(n):
            xi_c, yi_c, zi_c = X_vec[3*i], X_vec[3*i+1], X_vec[3*i+2]
            for j in range(i + 1, n):
                dx = xi_c - X_vec[3*j]
                dy = yi_c - X_vec[3*j+1]
                dz = zi_c - X_vec[3*j+2]
                rij = mp.sqrt(dx*dx + dy*dy + dz*dz)
                r_mat[i][j] = r_mat[j][i] = rij
                t = int(sp[i] + sp[j])
                u = rij / r0_mp[t] - 1
                rep = A_mp[t] * mp.exp(-p_mp[t] * u)
                phi = (xi_mp[t]**2) * mp.exp(-2 * q_mp[t] * u)
                rep_mat[i][j] = rep_mat[j][i] = rep
                phi_mat[i][j] = phi_mat[j][i] = phi
                rho[i] += phi
                rho[j] += phi
                E_tot += 2 * rep
        for i in range(n):
            sr = mp.sqrt(rho[i])
            sqrt_rho[i] = sr
            inv_sqrt[i] = 1 / sr
            E_tot -= sr
        for i in range(n):
            for j in range(i + 1, n):
                t = int(sp[i] + sp[j])
                rij = r_mat[i][j]
                dE_dr = 2 * ((-p_mp[t] / r0_mp[t]) * rep_mat[i][j] + mp.mpf('0.5') * (inv_sqrt[i] + inv_sqrt[j]) * (q_mp[t] / r0_mp[t]) * phi_mat[i][j])
                c = dE_dr / rij
                dx = X_vec[3*i] - X_vec[3*j]
                dy = X_vec[3*i+1] - X_vec[3*j+1]
                dz = X_vec[3*i+2] - X_vec[3*j+2]
                G[3*i]   += c * dx; G[3*j]   -= c * dx
                G[3*i+1] += c * dy; G[3*j+1] -= c * dy
                G[3*i+2] += c * dz; G[3*j+2] -= c * dz
        gnorm = mp.sqrt(sum(g*g for g in G))
        return E_tot, G, gnorm

    # Use float64 pseudoinverse of analytical Hessian (excluding the 6 zero modes) to take 3 quasi-Newton steps in 30-digit mpmath!
    H = analytical_hessian(x_best.reshape(n, 3), sp)
    evals, evecs = np.linalg.eigh(H)
    # Keep modes with |lambda| > 1e-3
    mask = evals > 1e-3
    H_pinv = (evecs[:, mask] / evals[mask]) @ evecs[:, mask].T

    E_mp, G_mp, gnorm_mp = mp_eg(X)
    for step in range(6):
        if gnorm_mp < mp.mpf('1e-22'):
            break
        g_f64 = np.array([float(g) for g in G_mp], dtype=np.float64)
        dx_f64 = -H_pinv @ g_f64
        X_new = [X[k] + mp.mpf(repr(float(dx_f64[k]))) for k in range(3 * n)]
        E_new, G_new, gnorm_new = mp_eg(X_new)
        if gnorm_new < gnorm_mp:
            X, E_mp, G_mp, gnorm_mp = X_new, E_new, G_new, gnorm_new
        else:
            break

    coords_final = np.array([float(v) for v in X], dtype=np.float64).reshape(n, 3)
    H_final = analytical_hessian(coords_final, sp)
    evals_final = np.linalg.eigvalsh(H_final)
    return coords_final, X, E_mp, gnorm_mp, evals_final

if __name__ == "__main__":
    arch_dir = "CuAg55"
    imp_dir  = "bingupta_improved"
    # 1. Verify calibration across all 56 archive files
    max_cal_err = 0.0
    for fn in sorted(glob.glob(os.path.join(arch_dir, "Cu*Ag*.txt"))):
        eh, sp, c = load_cuag_file(fn)
        e_eval, _ = energy_and_grad(c.reshape(-1), sp)
        err = abs(e_eval - eh)
        if err > max_cal_err:
            max_cal_err = err
    print(f"Calibration across all 56 CuAg55 archive files: max_err = {max_cal_err:.3e} eV (requirement <= 1e-6 eV)")

    # 2. Verify all 8 improved structures
    for imp_path in sorted(glob.glob(os.path.join(imp_dir, "CuAg55_*.txt"))):
        base = os.path.basename(imp_path).replace("CuAg55_", "")
        arch_path = os.path.join(arch_dir, base)
        eh_arch, sp_arch, c_arch = load_cuag_file(arch_path)
        _, sp_imp, c_imp = load_cuag_file(imp_path)
        assert len(sp_arch) == 55 and len(sp_imp) == 55
        assert int(np.sum(sp_arch == 0)) == int(np.sum(sp_imp == 0)), "Composition mismatch!"

        e_arch_raw, _ = energy_and_grad(c_arch.reshape(-1), sp_arch)
        _, _, E_arch_pol, g_arch_pol, evals_arch = mpmath_polish_and_eval(c_arch, sp_arch)
        c_imp_pol, X_mp, E_imp_pol, g_imp_pol, evals_imp = mpmath_polish_and_eval(c_imp, sp_imp)

        n_zero = int(np.sum(np.abs(evals_imp) < 1e-6))
        n_neg  = int(np.sum(evals_imp <= -1e-6))
        min_pos = float(np.min(evals_imp[np.abs(evals_imp) >= 1e-6]))
        max_zero = float(np.max(np.abs(evals_imp[np.abs(evals_imp) < 1e-6])))
        dE_raw = float(E_imp_pol) - e_arch_raw
        dE_pol = float(E_imp_pol - E_arch_pol)
        print(f"{base:14s} | nCu={int(np.sum(sp_imp==0)):2d} | E_arch={e_arch_raw:14.8f} | E_arch_pol={float(E_arch_pol):14.8f} | E_imp={float(E_imp_pol):14.8f} | dE_pol={dE_pol:12.8f} | |g|_mp={float(g_imp_pol):.2e} | zero={n_zero} (max {max_zero:.2e}) | neg={n_neg} | min_pos={min_pos:.4e}")
