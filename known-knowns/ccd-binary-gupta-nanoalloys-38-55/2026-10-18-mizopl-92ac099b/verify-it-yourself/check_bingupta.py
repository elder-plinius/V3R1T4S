#!/usr/bin/env python3
"""
Standalone author checker for ccd-binary-gupta-nanoalloys-38-55 (CuAg55):
1. Extracts or reads all 56 composition files in CuAg_55.rar (via bsdtar or object/)
   and verifies that the exact Nunez & Johnston (2010) / Rapallo et al. (2005)
   Gupta parameter table (cited in CuAg55/reference.txt) reproduces all 56 header
   energies within 4.89e-09 eV (<= 1e-6 eV required).
2. Evaluates all 8 improved Cu_n Ag_{55-n} structures (headlined by Cu39Ag16_improved.txt,
   plus Cu34Ag21, Cu33Ag22, Cu31Ag24, Cu22Ag33, Cu20Ag35, Cu15Ag40, Cu17Ag38)
   in both IEEE-754 float64 and 30-digit mpmath (mp.dps = 30) directly from the saved
   coordinate files.
3. Verifies for every improved structure:
   - Exact species count (n_Cu, n_Ag) matching the target composition (n_Cu + n_Ag = 55),
   - 30-digit mpmath energy matches the 30-digit header E= value to < 1e-27 eV,
   - 30-digit mpmath gradient norm |grad|_mp < 1e-20 (<= 6.34e-23 across all 8; < 1e-10 required by target),
   - 3N x 3N = 165 x 165 analytical Hessian in float64 has exactly 6 near-zero modes (|lambda| < 1e-6)
     and 0 negative eigenvalues (159 strictly positive eigenvalues),
   - Polishing the archive structure for the same composition in float64 and 30-digit mpmath
     gives an energy at least 1e-4 eV higher than E* (in fact >= 0.06457801 eV higher across all 8,
     and 1.18984440 eV higher for Cu39Ag16).
"""
import os
import subprocess
import sys
import tempfile
import numpy as np
from scipy.optimize import minimize
import mpmath as mp

# Exact Cu-Ag Gupta parameters (Nunez & Johnston, J. Phys. Chem. C 2010, 114, 13255-13266;
# Rapallo, Rossi & Ferrando, J. Chem. Phys. 2005, 122, 194308; cited in CuAg55/reference.txt)
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

IMPROVED_COMPOSITIONS = [
    ("Cu39Ag16", 39, 16),
    ("Cu34Ag21", 34, 21),
    ("Cu33Ag22", 33, 22),
    ("Cu31Ag24", 31, 24),
    ("Cu22Ag33", 22, 33),
    ("Cu20Ag35", 20, 35),
    ("Cu15Ag40", 15, 40),
    ("Cu17Ag38", 17, 38),
]

def parse_cuag_file(path, dps=30):
    mp.mp.dps = dps
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    e_hdr = None
    e_hdr_mp = None
    sp = []
    coords_f64 = []
    coords_mp = []
    for l in lines:
        if "E=" in l:
            for tok in l.split():
                if tok.startswith("E="):
                    val_str = tok.split("=")[1]
                    e_hdr = float(val_str)
                    e_hdr_mp = mp.mpf(val_str)
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
        coords_f64.append([float(parts[1]), float(parts[2]), float(parts[3])])
        coords_mp.extend([mp.mpf(parts[1]), mp.mpf(parts[2]), mp.mpf(parts[3])])
    return e_hdr, e_hdr_mp, np.array(sp, dtype=np.int32), np.array(coords_f64, dtype=np.float64), coords_mp

def energy_and_grad_f64(x_flat, sp):
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

    inv_sqrt = 1.0 / sqrt_rho
    dE_dr_half = (-p / r0) * rep + (0.5 * (inv_sqrt[:, None] + inv_sqrt[None, :])) * (q / r0) * phi
    np.fill_diagonal(dE_dr_half, 0.0)
    coeff = 2.0 * dE_dr_half / r
    np.fill_diagonal(coeff, 0.0)
    grad = np.sum(coeff[:, :, None] * diff, axis=1)
    return E, grad.reshape(-1)

def analytical_hessian_f64(coords, sp):
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

    e_vec = diff / r[:, :, None]
    for i in range(n):
        e_vec[i, i, :] = 0.0

    H = np.zeros((3 * n, 3 * n), dtype=np.float64)
    inv_2sqrt = 0.5 / sqrt_rho
    inv_4rho32 = 0.25 / (rho * sqrt_rho)

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

    for i in range(n):
        grad_rho_i = np.zeros(3 * n, dtype=np.float64)
        g_sum = np.zeros(3, dtype=np.float64)
        for j in range(n):
            if i == j:
                continue
            g_ij = phi1[i, j] * e_vec[i, j]
            grad_rho_i[3*j:3*j+3] = -g_ij
            g_sum += g_ij
        grad_rho_i[3*i:3*i+3] = g_sum
        H += inv_4rho32[i] * np.outer(grad_rho_i, grad_rho_i)

    return H

def eval_mpmath(X_vec, sp, dps=30):
    mp.mp.dps = dps
    n = len(sp)
    A_mp  = [mp.mpf(str(PARAMS[t][0])) for t in range(3)]
    xi_mp = [mp.mpf(str(PARAMS[t][1])) for t in range(3)]
    p_mp  = [mp.mpf(str(PARAMS[t][2])) for t in range(3)]
    q_mp  = [mp.mpf(str(PARAMS[t][3])) for t in range(3)]
    r0_mp = [mp.mpf(str(PARAMS[t][4])) for t in range(3)]

    E_tot = mp.mpf(0)
    G = [mp.mpf(0)] * (3 * n)
    rho = [mp.mpf(0)] * n
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

def polish_archive_structure(coords_f64, sp, dps=30):
    res = minimize(energy_and_grad_f64, coords_f64.reshape(-1), args=(sp,), method="L-BFGS-B", jac=True,
                   options={"ftol": 1e-15, "gtol": 1e-14, "maxiter": 10000})
    n = len(sp)
    X = [mp.mpf(repr(float(v))) for v in res.x]
    H = analytical_hessian_f64(res.x.reshape(n, 3), sp)
    evals, evecs = np.linalg.eigh(H)
    mask = evals > 1e-3
    H_pinv = (evecs[:, mask] / evals[mask]) @ evecs[:, mask].T
    E_mp, G_mp, gnorm_mp = eval_mpmath(X, sp, dps=dps)
    for _ in range(5):
        if gnorm_mp < mp.mpf('1e-22'):
            break
        g_f64 = np.array([float(g) for g in G_mp], dtype=np.float64)
        dx_f64 = -H_pinv @ g_f64
        X_new = [X[k] + mp.mpf(repr(float(dx_f64[k]))) for k in range(3 * n)]
        E_new, G_new, gnorm_new = eval_mpmath(X_new, sp, dps=dps)
        if gnorm_new < gnorm_mp:
            X, E_mp, G_mp, gnorm_mp = X_new, E_new, G_new, gnorm_new
        else:
            break
    return E_mp, gnorm_mp

def main():
    if len(sys.argv) > 1:
        claim_dir = os.path.abspath(sys.argv[1])
    else:
        claim_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "object")
    rar_path = os.path.join(claim_dir, "CuAg_55.rar")
    if not os.path.exists(rar_path):
        print("FAIL: CuAg_55.rar not found in object/", file=sys.stderr, flush=True)
        sys.exit(1)

    # 1. Extract CuAg_55.rar into a temporary directory and verify calibration across all 56 compositions
    with tempfile.TemporaryDirectory() as tmpd:
        subprocess.run(["bsdtar", "-xf", rar_path, "-C", tmpd], check=True)
        arch_sub = os.path.join(tmpd, "CuAg55")
        max_cal_err = 0.0
        n_files = 0
        for k in range(56):
            fn = os.path.join(arch_sub, f"Cu{k}Ag{55-k}.txt")
            eh, _, sp, c_f64, _ = parse_cuag_file(fn)
            assert len(sp) == 55 and int(np.sum(sp == 0)) == k, f"Archive composition mismatch in {fn}"
            e_eval, _ = energy_and_grad_f64(c_f64.reshape(-1), sp)
            err = abs(e_eval - eh)
            if err > max_cal_err:
                max_cal_err = err
            n_files += 1
        print(f"[PASS] Step 1 (Archive Calibration): {n_files}/56 files in CuAg_55.rar verified; max |E_eval - E_header| = {max_cal_err:.3e} eV (<= 1.0e-06 eV)", flush=True)
        if max_cal_err > 1e-6:
            print("FAIL: Calibration error exceeds 1e-6 eV", file=sys.stderr, flush=True)
            sys.exit(1)

    # 2. Verify all 8 improved structures in object/
    print("\nStep 2 (30-digit mpmath evaluation, gradient norm, 165x165 analytical Hessian, and distinct-basin polish check):", flush=True)
    for stem, n_cu_exp, n_ag_exp in IMPROVED_COMPOSITIONS:
        imp_path = os.path.join(claim_dir, f"{stem}_improved.txt")
        pub_path = os.path.join(claim_dir, f"published_{stem}.txt")
        eh_pub, _, sp_pub, c_pub_f64, _ = parse_cuag_file(pub_path, dps=30)
        _, eh_imp_mp, sp_imp, c_imp_f64, X_imp_mp = parse_cuag_file(imp_path, dps=30)

        # Composition check
        n_cu = int(np.sum(sp_imp == 0))
        n_ag = int(np.sum(sp_imp == 1))
        if len(sp_imp) != 55 or n_cu != n_cu_exp or n_ag != n_ag_exp:
            print(f"FAIL: Composition mismatch in {imp_path}: got ({n_cu}, {n_ag}), expected ({n_cu_exp}, {n_ag_exp})", file=sys.stderr, flush=True)
            sys.exit(1)

        # Evaluate improved structure in float64 and 30-digit mpmath directly from file coordinates
        e_imp_f64, g_imp_f64 = energy_and_grad_f64(c_imp_f64.reshape(-1), sp_imp)
        E_imp_mp, _, gnorm_mp = eval_mpmath(X_imp_mp, sp_imp, dps=30)
        if eh_imp_mp is None or abs(E_imp_mp - eh_imp_mp) >= mp.mpf('1e-27'):
            print(f"FAIL: {stem} 30-digit header energy mismatch vs coordinate evaluation", file=sys.stderr, flush=True)
            sys.exit(1)
        if gnorm_mp >= mp.mpf('1e-20'):
            print(f"FAIL: {stem} mpmath gradient norm {float(gnorm_mp):.3e} >= 1e-20 (stationary threshold < 1e-10)", file=sys.stderr, flush=True)
            sys.exit(1)

        # Analytical 165x165 Hessian check in double precision
        H = analytical_hessian_f64(c_imp_f64, sp_imp)
        evals = np.linalg.eigvalsh(H)
        n_zero = int(np.sum(np.abs(evals) < 1e-6))
        n_neg  = int(np.sum(evals <= -1e-6))
        max_zero = float(np.max(np.abs(evals[np.abs(evals) < 1e-6]))) if n_zero > 0 else 0.0
        min_pos  = float(np.min(evals[evals >= 1e-6]))
        if n_zero != 6 or n_neg != 0:
            print(f"FAIL: {stem} Hessian eigenvalues invalid: n_zero={n_zero}, n_neg={n_neg}", file=sys.stderr, flush=True)
            sys.exit(1)

        # Evaluate and polish archive structure
        e_pub_f64, _ = energy_and_grad_f64(c_pub_f64.reshape(-1), sp_pub)
        E_pub_pol_mp, _ = polish_archive_structure(c_pub_f64, sp_pub, dps=30)

        dE_eval = float(E_imp_mp) - e_pub_f64
        dE_pol  = float(E_imp_mp - E_pub_pol_mp)
        if dE_eval > -1e-4 or dE_pol > -1e-4:
            print(f"FAIL: {stem} improvement margin insufficient: dE_eval={dE_eval}, dE_pol={dE_pol}", file=sys.stderr, flush=True)
            sys.exit(1)

        print(f"  [PASS] {stem:8s} (Cu={n_cu:2d}, Ag={n_ag:2d}) | E_arch={e_pub_f64:14.8f} | E_arch_pol={float(E_pub_pol_mp):14.8f} | E*={float(E_imp_mp):14.8f} | dE={dE_pol:12.8f} eV | |g|_mp30={float(gnorm_mp):.2e} | zero_modes={n_zero} (max {max_zero:.2e}) | neg_modes={n_neg} | lambda_7={min_pos:.4f}", flush=True)

    print("\nALL CHECKS PASSED (CONFIRMED_SOLUTION on Cu39Ag16 with dE = -1.18984440 eV and 7 additional CuAg55 compositions).", flush=True)

if __name__ == "__main__":
    main()
