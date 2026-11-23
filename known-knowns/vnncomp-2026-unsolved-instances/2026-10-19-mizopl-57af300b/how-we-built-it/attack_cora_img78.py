import tempfile
from pathlib import Path
#!/usr/bin/env python3
"""
Focused CLSS Linear-Region Exact Vertex Seam Surgery + Fine-Scale Adam/Line-Search
on cora_2024 unsolved instance: cifar10-set-cifar10-img78 (and cifar10-img362 / cifar10-img346).
"""
import os
import time
import numpy as np
import onnxruntime as ort
import torch
from triage_relu_and_acopf import parse_vnnlib1, ONNXReluModel

torch.set_num_threads(8)


def solve_cora_instance(onnx_path, vnnlib_path, target_k=4, max_time=45.0):
    t0 = time.time()
    l_arr, u_arr, y_true = parse_vnnlib1(vnnlib_path)
    model = ONNXReluModel(onnx_path)
    sess = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
    inp_name = model.inp_name

    # Use float32 strict interior bounds via nextafter(l_arr, u_arr) + safety buffer
    l_t = torch.tensor(l_arr.reshape(1, -1), dtype=torch.float32)
    u_t = torch.tensor(u_arr.reshape(1, -1), dtype=torch.float32)
    # 5e-6 relative margin is ~50 ULPs inside (l, u) in float32
    lo_in = l_t + 5e-6 * (u_t - l_t)
    hi_in = u_t - 5e-6 * (u_t - l_t)
    mid_t = 0.5 * (l_t + u_t)
    rad_t = 0.5 * (u_t - l_t)

    # Double check strict inequality in float32
    assert bool(torch.all((lo_in > l_t) & (hi_in < u_t) & (lo_in < hi_in))), "Strict interior bounds failed!"

    batch_size = 256
    torch.manual_seed(20261019)
    np.random.seed(20261019)

    x = mid_t.repeat(batch_size, 1)
    with torch.no_grad():
        for b in range(1, batch_size):
            if b < 64:
                x[b : b + 1] = mid_t + (2.0 * torch.rand_like(mid_t) - 1.0) * (0.2 + 0.8 * (b / 64.0)) * rad_t
            elif b < 192:
                x[b : b + 1] = mid_t + torch.sign(torch.randn_like(mid_t)) * 0.9999 * rad_t
            else:
                x[b : b + 1] = mid_t + (2.0 * torch.rand_like(mid_t) - 1.0) * 0.9999 * rad_t
        x = torch.max(torch.min(x, hi_in), lo_in)

    best_gap = -1e9
    best_x = mid_t.clone()
    best_k = target_k

    # Phase 1: Multi-scale Line-Search Frank-Wolfe + Sign-PGD on target_k (and all k)
    for step in range(1, 501):
        if time.time() - t0 > max_time:
            break
        x_var = x.detach().requires_grad_(True)
        y = model(x_var)
        with torch.no_grad():
            g_all = y - y[:, y_true : y_true + 1]
            g_all[:, y_true] = -1e9
            m_vals, m_ks = g_all.max(dim=1)
            idx_b = int(m_vals.argmax())
            if float(m_vals[idx_b]) > best_gap:
                best_gap = float(m_vals[idx_b])
                best_k = int(m_ks[idx_b])
                best_x = x[idx_b : idx_b + 1].detach().clone()
                print(f"  [Step {step:3d} | {time.time()-t0:5.2f}s] best_gap = {best_gap:+.8f} (rival {best_k}, y_true={y_true})")
                if best_gap >= 2e-6:
                    cand_np = best_x.numpy().astype(np.float32)
                    ort_out = sess.run(None, {inp_name: cand_np})[0][0]
                    ort_margin = float(ort_out[best_k] - ort_out[y_true])
                    strict_ok = bool(np.all((cand_np.reshape(-1) > l_arr) & (cand_np.reshape(-1) < u_arr)))
                    print(f"  >>> ORT CHECK: ort_margin={ort_margin:+.8e} (Y_{best_k}={ort_out[best_k]:.8f}, Y_{y_true}={ort_out[y_true]:.8f}), strict_interior={strict_ok}")
                    if ort_margin >= 1e-6 and strict_ok:
                        return cand_np, best_k, ort_margin

        # Focus 80% of batch on target_k (or best_k), 20% on their own best_k
        k_vec = m_ks.clone()
        k_vec[: int(0.8 * batch_size)] = best_k
        obj = (y[torch.arange(batch_size), k_vec] - y[:, y_true]).sum()
        obj.backward()

        with torch.no_grad():
            grad = x_var.grad
            vertex = torch.where(grad >= 0, hi_in, lo_in)
            # Test 4 line-search scales per particle and greedily take the best!
            scales = [0.002, 0.01, 0.05, 0.20, 0.50] if step < 150 else [0.0002, 0.001, 0.005, 0.02, 0.08]
            curr_scores = y[torch.arange(batch_size), k_vec] - y[:, y_true]
            best_next_x = x.clone()
            best_next_s = curr_scores.clone()

            for alpha in scales:
                # Candidate 1: Frank-Wolfe step toward linear-region extreme vertex
                c1 = x + alpha * (vertex - x)
                c1 = torch.max(torch.min(c1, hi_in), lo_in)
                y1 = model(c1)
                s1 = y1[torch.arange(batch_size), k_vec] - y1[:, y_true]
                imp1 = s1 > best_next_s
                best_next_x = torch.where(imp1.unsqueeze(1), c1, best_next_x)
                best_next_s = torch.where(imp1, s1, best_next_s)

                # Candidate 2: Sign-PGD step
                c2 = torch.max(torch.min(x + alpha * rad_t * torch.sign(grad), hi_in), lo_in)
                y2 = model(c2)
                s2 = y2[torch.arange(batch_size), k_vec] - y2[:, y_true]
                imp2 = s2 > best_next_s
                best_next_x = torch.where(imp2.unsqueeze(1), c2, best_next_x)
                best_next_s = torch.where(imp2, s2, best_next_s)

            x = best_next_x
            # Every 20 steps, re-seed worst 64 particles around best_x with small random perturbations
            if step % 20 == 0:
                worst_idx = torch.argsort(best_next_s)[:64]
                for i, w_i in enumerate(worst_idx):
                    sigma = 0.002 * (1 + (i % 16))
                    noise = sigma * rad_t * torch.randn_like(best_x)
                    x[w_i : w_i + 1] = torch.max(torch.min(best_x + noise, hi_in), lo_in)

    return None, best_k, best_gap


if __name__ == "__main__":
    base = "{Path(__file__).resolve().parent.parent.parent}/data/cora_2024"
    out_dir = "{Path(__file__).resolve().parent.parent.parent}/attempts/lens1_unsolved_audit_and_linear_seam_surgery"
    for m, img, tk in [
        ("cifar10-set.onnx", "cifar10-img78.vnnlib", 4),
        ("cifar10-set.onnx", "cifar10-img362.vnnlib", 6),
        ("cifar10-trades.onnx", "cifar10-img346.vnnlib", 2),
        ("cifar10-set.onnx", "cifar10-img345.vnnlib", 0),
    ]:
        print(f"\n=== Attacking {m} | {img} (target_k={tk}) ===")
        cand, k, margin = solve_cora_instance(f"{base}/onnx/{m}", f"{base}/vnnlib/{img}", target_k=tk, max_time=40.0)
        if cand is not None:
            out_p = f"{out_dir}/cex_{m.replace('.onnx','')}_{img.replace('.vnnlib','')}.npy"
            np.save(out_p, cand)
            print(f"SUCCESSFULLY SAVED COUNTEREXAMPLE TO {out_p} (rival={k}, margin={margin:+.8e})")
