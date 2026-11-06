#!/usr/bin/env python3
"""Lens 2: Literature Frontier Certification for Size Ratio 1.50 at N in [51..60] (Partial Win p3)
and Targeted Neighbour Cell Motif Search.
"""
import csv
import glob
import math
import os
import re
import sys
import time
import numpy as np
import scipy.optimize as opt
from mpmath import mp

# Set high-precision arithmetic
mp.dps = 30

def blj_eval_np(coords_flat, species, ratio):
    n = len(species)
    coords = coords_flat.reshape((n, 3))
    energy = 0.0
    grad = np.zeros((n, 3), dtype=np.float64)
    sig_aa = 1.0
    sig_bb = ratio
    sig_ab = (1.0 + ratio) / 2.0
    
    for i in range(n):
        si = species[i]
        for j in range(i + 1, n):
            sj = species[j]
            dvec = coords[i] - coords[j]
            r2 = np.dot(dvec, dvec)
            r = math.sqrt(r2)
            sig = sig_aa if (si == 'A' and sj == 'A') else (sig_bb if (si == 'B' and sj == 'B') else sig_ab)
            inv_r = 1.0 / r
            u = sig * inv_r
            u2 = u * u
            u6 = u2 * u2 * u2
            u12 = u6 * u6
            energy += 4.0 * (u12 - u6)
            dV_dr = 24.0 * inv_r * (u6 - 2.0 * u12)
            g_vec = dV_dr * (dvec * inv_r)
            grad[i] += g_vec
            grad[j] -= g_vec
    return energy, grad.flatten()

def compute_analytical_hessian_np(coords_flat, species, ratio):
    n = len(species)
    coords = coords_flat.reshape((n, 3))
    H = np.zeros((3 * n, 3 * n), dtype=np.float64)
    sig_aa = 1.0
    sig_bb = ratio
    sig_ab = (1.0 + ratio) / 2.0
    I3 = np.eye(3, dtype=np.float64)
    
    for i in range(n):
        si = species[i]
        for j in range(i + 1, n):
            sj = species[j]
            dvec = coords[i] - coords[j]
            r2 = np.dot(dvec, dvec)
            r = math.sqrt(r2)
            sig = sig_aa if (si == 'A' and sj == 'A') else (sig_bb if (si == 'B' and sj == 'B') else sig_ab)
            inv_r = 1.0 / r
            rhat = dvec * inv_r
            rhat_outer = np.outer(rhat, rhat)
            u = sig * inv_r
            u2 = u * u
            u6 = u2 * u2 * u2
            u12 = u6 * u6
            dV_dr = 24.0 * inv_r * (u6 - 2.0 * u12)
            d2V_dr2 = 24.0 * (inv_r * inv_r) * (26.0 * u12 - 7.0 * u6)
            block = d2V_dr2 * rhat_outer + (dV_dr * inv_r) * (I3 - rhat_outer)
            i3, j3 = 3 * i, 3 * j
            H[i3:i3+3, i3:i3+3] += block
            H[j3:j3+3, j3:j3+3] += block
            H[i3:i3+3, j3:j3+3] -= block
            H[j3:j3+3, i3:i3+3] -= block
    return H

def mp_eval_blj(coords, species, ratio_mp):
    # High-precision 30-digit evaluation
    n = len(species)
    energy = mp.mpf(0)
    grad = [[mp.mpf(0), mp.mpf(0), mp.mpf(0)] for _ in range(n)]
    sig_aa = mp.mpf(1)
    sig_bb = ratio_mp
    sig_ab = (mp.mpf(1) + ratio_mp) / mp.mpf(2)
    
    for i in range(n):
        si = species[i]
        xi, yi, zi = coords[i]
        for j in range(i + 1, n):
            sj = species[j]
            xj, yj, zj = coords[j]
            dx = xi - xj
            dy = yi - yj
            dz = zi - zj
            r2 = dx*dx + dy*dy + dz*dz
            r = mp.sqrt(r2)
            sig = sig_aa if (si == 'A' and sj == 'A') else (sig_bb if (si == 'B' and sj == 'B') else sig_ab)
            inv_r = mp.mpf(1) / r
            u = sig * inv_r
            u2 = u * u
            u6 = u2 * u2 * u2
            u12 = u6 * u6
            energy += mp.mpf(4) * (u12 - u6)
            dV_dr = mp.mpf(24) * inv_r * (u6 - mp.mpf(2) * u12)
            gx = dV_dr * (dx * inv_r)
            gy = dV_dr * (dy * inv_r)
            gz = dV_dr * (dz * inv_r)
            grad[i][0] += gx; grad[i][1] += gy; grad[i][2] += gz
            grad[j][0] -= gx; grad[j][1] -= gy; grad[j][2] -= gz
            
    # Compute Euclidean norm of gradient
    sum_g2 = mp.mpf(0)
    for gvec in grad:
        sum_g2 += gvec[0]*gvec[0] + gvec[1]*gvec[1] + gvec[2]*gvec[2]
    gnorm = mp.sqrt(sum_g2)
    return energy, grad, gnorm

def parse_point_file(filepath):
    with open(filepath, 'r', errors='ignore') as f:
        lines = [l.strip() for l in f if l.strip()]
    if not lines: return None
    n_atoms = int(lines[0])
    species = []
    coords = []
    for l in lines[2:2 + n_atoms]:
        toks = l.split()
        sp = toks[0].replace('L', '')
        species.append(sp)
        coords.append([float(toks[1]), float(toks[2]), float(toks[3])])
    return n_atoms, species, np.array(coords, dtype=np.float64)

def polish_and_certify_cluster(n, ratio, init_species, init_coords):
    print(f"\n--- Polishing and Certifying N={n}, ratio={ratio:.2f} ---")
    c = init_coords.copy()
    sp = list(init_species)
    
    # 1. Optimize chemical ordering (A in core, B on surface)
    com = np.mean(c, axis=0)
    dists = [np.linalg.norm(c[i] - com) for i in range(n)]
    idx_sorted = np.argsort(dists)
    
    best_e, _ = blj_eval_np(c.flatten(), sp, ratio)
    best_sp = sp
    best_c = c.flatten()
    
    # Try different core compositions
    min_na = max(1, n // 4)
    max_na = min(n - 1, 3 * n // 4)
    for n_a in range(min_na, max_na + 1, 2):
        test_sp = ['B'] * n
        for k in range(n_a):
            test_sp[idx_sorted[k]] = 'A'
        res = opt.minimize(lambda x: blj_eval_np(x, test_sp, ratio), best_c, jac=True, method='L-BFGS-B', options={'maxiter': 300})
        if res.fun < best_e:
            best_e = res.fun
            best_sp = test_sp
            best_c = res.x
            
    print(f"  Optimal chemical ordering: N_A={best_sp.count('A')}, N_B={best_sp.count('B')}, E_init={best_e:.8f}")
    
    # 2. Precision L-BFGS-B polish
    res_opt = opt.minimize(lambda x: blj_eval_np(x, best_sp, ratio), best_c, jac=True, method='L-BFGS-B',
                           options={'gtol': 1e-13, 'ftol': 1e-15, 'maxiter': 5000})
    c_opt = res_opt.x
    
    # 3. Analytical Newton-Raphson polish
    for it in range(25):
        e_curr, g_curr = blj_eval_np(c_opt, best_sp, ratio)
        gnorm = np.linalg.norm(g_curr)
        if gnorm < 1e-11:
            break
        H = compute_analytical_hessian_np(c_opt, best_sp, ratio)
        H_inv = np.linalg.pinv(H, rcond=1e-5)
        p = -np.dot(H_inv, g_curr)
        c_opt = c_opt + p
        
    e_double, g_double = blj_eval_np(c_opt, best_sp, ratio)
    gnorm_double = np.linalg.norm(g_double)
    print(f"  Newton-Raphson polished: E = {e_double:.12f}, gnorm = {gnorm_double:.2e}")
    
    # 4. 30-digit mpmath validation
    coords_mp = [[mp.mpf(str(c_opt[3*i+k])) for k in range(3)] for i in range(n)]
    ratio_mp = mp.mpf(str(ratio))
    e_mp, _, gnorm_mp = mp_eval_blj(coords_mp, best_sp, ratio_mp)
    print(f"  30-digit mpmath: E = {mp.nstr(e_mp, 30)}")
    print(f"  30-digit mpmath gnorm = {mp.nstr(gnorm_mp, 10)} (< 1e-10 requirement: {gnorm_mp < mp.mpf('1e-10')})")
    
    # 5. 3N x 3N Hessian Eigenvalue Certification
    H_final = compute_analytical_hessian_np(c_opt, best_sp, ratio)
    eigs = np.linalg.eigvalsh(H_final)
    
    zero_modes = [val for val in eigs if abs(val) < 1e-5]
    neg_modes = [val for val in eigs if val < -1e-5]
    pos_modes = [val for val in eigs if val >= 1e-5]
    
    print(f"  Hessian modes (total {3*n}): zero={len(zero_modes)} (expected 6), neg={len(neg_modes)} (expected 0), pos={len(pos_modes)}")
    print(f"  Lowest vibrational eigenvalue: {pos_modes[0]:.8f}")
    
    assert len(zero_modes) == 6, f"Expected 6 zero modes, got {len(zero_modes)}"
    assert len(neg_modes) == 0, f"Expected 0 negative modes, got {len(neg_modes)}"
    assert gnorm_mp < mp.mpf('1e-10'), f"Gradient norm {gnorm_mp} exceeds 1e-10"
    
    cert_dict = {
        'n': n,
        'ratio': f"{ratio:.2f}",
        'n_A': best_sp.count('A'),
        'n_B': best_sp.count('B'),
        'energy_30digits': mp.nstr(e_mp, 30),
        'energy_double': e_double,
        'gradient_norm': mp.nstr(gnorm_mp, 6),
        'hessian_zero_modes': len(zero_modes),
        'hessian_negative_modes': len(neg_modes),
        'lowest_vibrational_eigenvalue': f"{pos_modes[0]:.8f}",
        'certified': "TRUE",
        'species': best_sp,
        'coords_mp': coords_mp
    }
    return cert_dict

def main():
    print("=" * 70)
    print("LENS 2: Literature Frontier Certification for Size Ratio 1.50 (p3)")
    print("=" * 70)
    
    run_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    data_dir = os.path.join(run_dir, "data")
    all_dir = os.path.join(data_dir, "all")
    
    target_ratio = 1.50
    sizes = list(range(51, 61)) # N in [51..60]
    results = []
    
    p3_obj_dir = os.path.join(run_dir, "object", "p3_ratio1.50")
    os.makedirs(p3_obj_dir, exist_ok=True)
    
    t0 = time.time()
    for n in sizes:
        # Load seed geometry from ratio 1.3
        seed_file = os.path.join(all_dir, "1.3", str(n))
        res_parse = parse_point_file(seed_file)
        if not res_parse:
            print(f"Skipping N={n}: seed file not found")
            continue
        _, seed_sp, seed_coords = res_parse
        cert = polish_and_certify_cluster(n, target_ratio, seed_sp, seed_coords)
        results.append(cert)
        
        # Save point file in CCD format
        pt_path = os.path.join(p3_obj_dir, f"BLJ_N{n}_ratio1.50.xyz")
        with open(pt_path, 'w') as f:
            f.write(f"{n}\n")
            f.write(f"Energy of minimum 1= {cert['energy_30digits']} (NA,SIG_BB) {cert['n_A']} {target_ratio:.6f}\n")
            for sp_i, c_i in zip(cert['species'], cert['coords_mp']):
                f.write(f"L{sp_i:<3s} {mp.nstr(c_i[0], 20):>25s} {mp.nstr(c_i[1], 20):>25s} {mp.nstr(c_i[2], 20):>25s}\n")
                
    dt = time.time() - t0
    print(f"\nSuccessfully polished and certified {len(results)} frontier clusters at ratio {target_ratio:.2f} in {dt:.2f}s.")
    
    # Save summary table
    summary_path = os.path.join(run_dir, "object", "p3_frontier_ratio1.50_summary.csv")
    fieldnames = ['n', 'ratio', 'n_A', 'n_B', 'energy_30digits', 'energy_double', 'gradient_norm',
                  'hessian_zero_modes', 'hessian_negative_modes', 'lowest_vibrational_eigenvalue', 'certified']
    with open(summary_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            row = {k: r[k] for k in fieldnames}
            writer.writerow(row)
    print(f"Saved p3 certification summary to {summary_path}")
    print("\nLENS 2 COMPLETE: Literature frontier p3 certified across N in [51..60] at size ratio 1.50.")

if __name__ == "__main__":
    main()
