#!/usr/bin/env python3
"""Active-Set SQP Overlap Equalizer on CP^{d-1} with 40-digit mpmath verification.
Solves the Chebyshev minimax overlap problem on complex projective space.
"""

import os
import sys
import numpy as np
import mpmath
from scipy.optimize import linprog

def load_packing_np(path, d, n):
    with open(path, 'r') as f:
        vals = [float(line.strip()) for line in f if line.strip()]
    assert len(vals) == 2 * d * n, f"Expected {2*d*n} values, got {len(vals)}"
    reals = np.array(vals[:d*n], dtype=np.float64).reshape((n, d))
    imags = np.array(vals[d*n:], dtype=np.float64).reshape((n, d))
    V = reals + 1j * imags
    return V / np.linalg.norm(V, axis=1, keepdims=True)

def eval_coherence_numpy(V):
    G = np.abs(V @ V.conj().T)
    np.fill_diagonal(G, 0.0)
    return float(np.max(G))

def eval_coherence_mpmath(V):
    mpmath.mp.dps = 40
    n, d = V.shape
    vecs = []
    for j in range(n):
        v = [mpmath.mpc(mpmath.mpf(str(V[j, m].real)), mpmath.mpf(str(V[j, m].imag))) for m in range(d)]
        norm = mpmath.sqrt(sum(c.real**2 + c.imag**2 for c in v))
        vecs.append([c / norm for c in v])
    max_c = mpmath.mpf(0)
    for j in range(n):
        for k in range(j+1, n):
            ip = sum(vecs[j][m].conjugate() * vecs[k][m] for m in range(d))
            overlap = mpmath.sqrt(ip.real**2 + ip.imag**2)
            if overlap > max_c:
                max_c = overlap
    return max_c

def save_packing(V, path):
    n, d = V.shape
    V_norm = V / np.linalg.norm(V, axis=1, keepdims=True)
    reals = V_norm.real.ravel()
    imags = V_norm.imag.ravel()
    with open(path, 'w') as f:
        for val in reals:
            f.write(f"{val:.16e}\n")
        for val in imags:
            f.write(f"{val:.16e}\n")

def run_sqp_equalizer(V_init, d, n, max_steps=120, delta_bound=5e-5):
    cur_V = V_init.copy()
    cur_V = cur_V / np.linalg.norm(cur_V, axis=1, keepdims=True)
    c_start = eval_coherence_numpy(cur_V)
    print(f"Starting SQP equalizer: d={d}, n={n}, initial mu = {c_start:.10f}")
    
    cur_mu = c_start
    for it in range(max_steps):
        G = cur_V @ cur_V.conj().T
        U = np.abs(G)
        np.fill_diagonal(U, 0.0)
        mu = np.max(U)
        
        iu = np.triu_indices(n, k=1)
        sorted_u = np.sort(U[iu])[::-1]
        eps_active = max(1e-5, mu - sorted_u[min(len(sorted_u)-1, min(100, n*2))])
        
        active = []
        for j, k in zip(iu[0], iu[1]):
            if U[j, k] >= mu - eps_active:
                active.append((j, k, U[j, k], G[j, k]))
                
        num_vars = 2*n*d + 1
        z_idx = 2*n*d
        c = np.zeros(num_vars)
        c[z_idx] = 1.0
        
        A_ub = []
        b_ub = []
        for j, k, u_val, g_val in active:
            s = g_val / u_val
            row = np.zeros(num_vars)
            coeff_j = np.conj(s) * np.conj(cur_V[k])
            row[j*d : (j+1)*d] = coeff_j.real
            row[n*d + j*d : n*d + (j+1)*d] = -coeff_j.imag
            coeff_k = s * np.conj(cur_V[j])
            row[k*d : (k+1)*d] += coeff_k.real
            row[n*d + k*d : n*d + (k+1)*d] += -coeff_k.imag
            row[z_idx] = -1.0
            A_ub.append(row)
            b_ub.append(-u_val)
            
        A_eq = []
        b_eq = []
        for j in range(n):
            row_re = np.zeros(num_vars)
            row_re[j*d : (j+1)*d] = cur_V[j].real
            row_re[n*d + j*d : n*d + (j+1)*d] = cur_V[j].imag
            A_eq.append(row_re)
            b_eq.append(0.0)
            row_im = np.zeros(num_vars)
            row_im[j*d : (j+1)*d] = -cur_V[j].imag
            row_im[n*d + j*d : n*d + (j+1)*d] = cur_V[j].real
            A_eq.append(row_im)
            b_eq.append(0.0)
            
        bounds = [(-delta_bound, delta_bound) for _ in range(2*n*d)] + [(None, None)]
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        if not res.success:
            print(f"LP solver terminated at step {it}: {res.message}")
            break
            
        sol = res.x
        xi = sol[:n*d].reshape((n, d)) + 1j * sol[n*d : 2*n*d].reshape((n, d))
        
        best_cand = cur_V
        best_cand_mu = mu
        for t in [1.0, 0.7, 0.5, 0.3, 0.2, 0.1, 0.05, 0.01]:
            V_cand = cur_V + t * xi
            V_cand = V_cand / np.linalg.norm(V_cand, axis=1, keepdims=True)
            c_cand = eval_coherence_numpy(V_cand)
            if c_cand < best_cand_mu:
                best_cand_mu = c_cand
                best_cand = V_cand
                
        if best_cand_mu >= mu - 1e-12:
            print(f"Equalizer converged at step {it+1}")
            break
            
        cur_mu = best_cand_mu
        cur_V = best_cand
        if (it + 1) % 20 == 0:
            print(f"Iter {it+1:3d}: mu = {cur_mu:.10f}, drop = {c_start - cur_mu:.2e}")
            
    cur_V = cur_V / np.linalg.norm(cur_V, axis=1, keepdims=True)
    c_final = eval_coherence_numpy(cur_V)
    print(f"SQP finished: final mu = {c_final:.10f}, total reduction = {c_start - c_final:.2e}")
    return cur_V, c_final

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    run_dir = os.path.dirname(os.path.dirname(base_dir))
    data_dir = os.path.join(run_dir, "data")
    result_dir = os.path.join(base_dir, "result")
    os.makedirs(result_dir, exist_ok=True)
    
    # 1. Row (5, 49)
    d, n = 5, 49
    p5_49 = os.path.join(data_dir, "5x49_oai.txt")
    V0 = load_packing_np(p5_49, d, n)
    c0 = eval_coherence_numpy(V0)
    V_opt, c_final = run_sqp_equalizer(V0, d, n, max_steps=120)
    c_mp = eval_coherence_mpmath(V_opt)
    table_mu = mpmath.mpf("0.54164128")
    lb_mu = mpmath.mpf("0.50751922")
    drop = table_mu - c_mp
    print(f"\n--- Row (5, 49) mpmath 40-digit verification ---")
    print(f"Table Best Coherence : {table_mu}")
    print(f"Lower Bound          : {lb_mu}")
    print(f"V3R1T4S mpmath mu    : {c_mp}")
    print(f"Strict Improvement   : {drop} (>= 1e-8: {drop >= 1e-8})")
    assert drop >= 1e-8, f"Improvement {drop} is less than 1e-8"
    assert c_mp >= lb_mu, f"Coherence {c_mp} is below lower bound {lb_mu}"
    out_5_49 = os.path.join(result_dir, "5x49_v3r1t4s.txt")
    save_packing(V_opt, out_5_49)
    print(f"Saved verified packing to {out_5_49}")
    
    # 2. Row (6, 44)
    d, n = 6, 44
    p6_44 = os.path.join(data_dir, "6x44_oai.txt")
    V0 = load_packing_np(p6_44, d, n)
    V_opt, c_final = run_sqp_equalizer(V0, d, n, max_steps=80)
    c_mp = eval_coherence_mpmath(V_opt)
    table_mu = mpmath.mpf("0.44643020")
    lb_mu = mpmath.mpf("0.41585133")
    drop = table_mu - c_mp
    print(f"\n--- Row (6, 44) mpmath 40-digit verification ---")
    print(f"Table Best Coherence : {table_mu}")
    print(f"Lower Bound          : {lb_mu}")
    print(f"V3R1T4S mpmath mu    : {c_mp}")
    print(f"Strict Improvement   : {drop} (>= 1e-8: {drop >= 1e-8})")
    assert drop >= 1e-8
    out_6_44 = os.path.join(result_dir, "6x44_v3r1t4s.txt")
    save_packing(V_opt, out_6_44)
    print(f"Saved verified packing to {out_6_44}")
    
    # 3. Row (7, 29)
    d, n = 7, 29
    p7_29 = os.path.join(data_dir, "7x29_oai.txt")
    V0 = load_packing_np(p7_29, d, n)
    V_opt, c_final = run_sqp_equalizer(V0, d, n, max_steps=60)
    c_mp = eval_coherence_mpmath(V_opt)
    table_mu = mpmath.mpf("0.34064551")
    lb_mu = mpmath.mpf("0.33502970")
    drop = table_mu - c_mp
    print(f"\n--- Row (7, 29) mpmath 40-digit verification ---")
    print(f"Table Best Coherence : {table_mu}")
    print(f"Lower Bound          : {lb_mu}")
    print(f"V3R1T4S mpmath mu    : {c_mp}")
    print(f"Strict Improvement   : {drop} (>= 1e-8: {drop >= 1e-8})")
    assert drop >= 1e-8
    out_7_29 = os.path.join(result_dir, "7x29_v3r1t4s.txt")
    save_packing(V_opt, out_7_29)
    print(f"Saved verified packing to {out_7_29}")

if __name__ == "__main__":
    main()
