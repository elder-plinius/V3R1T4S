import tempfile
from pathlib import Path
#!/usr/bin/env python3
"""
CLSS Linear-Region Seam & Momentum-FW Surgery on challenging_certified_training_2026:
1. Polish the discovered counterexample on tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib
2. Attack the remaining near-zero unsolved instances in challenging_certified_training_2026
"""
import os
import time
import numpy as np
import onnxruntime as ort
import torch
from triage_relu_and_acopf import parse_vnnlib1
from triage_cifar100_and_tiny import ONNXResNetModel

torch.set_num_threads(8)


def attack_cct_instance(onnx_path, vp, steps=180, batch_size=24):
    t0 = time.time()
    model = ONNXResNetModel(onnx_path)
    sess = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
    inp_name = model.inp_name
    shape = model.inp_shape

    l_arr, u_arr, y_true = parse_vnnlib1(vp)
    l_t = torch.tensor(l_arr.reshape(1, *shape[1:]), dtype=torch.float32)
    u_t = torch.tensor(u_arr.reshape(1, *shape[1:]), dtype=torch.float32)
    # Strict interior buffer: 1e-4 of interval width (or 2 ULPs if width is 0, though here all widths > 0)
    lo_in = l_t + 1e-4 * (u_t - l_t)
    hi_in = u_t - 1e-4 * (u_t - l_t)
    mid_t = 0.5 * (l_t + u_t)
    rad_t = 0.5 * (u_t - l_t)

    with torch.no_grad():
        y0 = model(mid_t)
        gaps0 = (y0[0] - y0[0, y_true]).clone()
        gaps0[y_true] = -1e9
        top_vals, top_ks = torch.topk(gaps0, k=min(8, gaps0.numel() - 1))

    rivals = [int(k) for k in top_ks]
    t_idx = torch.tensor([rivals[b % len(rivals)] for b in range(batch_size)], dtype=torch.long)

    torch.manual_seed(2026)
    x = mid_t.repeat(batch_size, 1, 1, 1)
    with torch.no_grad():
        for b in range(1, batch_size):
            if b < batch_size // 2:
                x[b : b + 1] = mid_t + torch.sign(torch.randn_like(mid_t)) * 0.99 * rad_t
            else:
                x[b : b + 1] = mid_t + torch.randn_like(mid_t) * 0.35 * rad_t
        x = torch.max(torch.min(x, hi_in), lo_in)

    mom = torch.zeros_like(x)
    best_gap = float(top_vals[0])
    best_k = rivals[0]
    best_x = mid_t.clone()
    saved_path = None

    for s in range(1, steps + 1):
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
                if best_gap >= 1e-6:
                    cand_np = best_x.numpy().astype(np.float32)
                    ort_out = sess.run(None, {inp_name: cand_np})[0][0]
                    ort_margin = float(ort_out[best_k] - ort_out[y_true])
                    strict_ok = bool(np.all((cand_np.reshape(-1) > l_arr) & (cand_np.reshape(-1) < u_arr)))
                    if ort_margin >= 1e-6 and strict_ok:
                        out_p = f"{Path(__file__).resolve().parent.parent.parent}/attempts/lens1_unsolved_audit_and_linear_seam_surgery/cex_{os.path.basename(vp).replace('.vnnlib','')}.npy"
                        np.save(out_p, cand_np)
                        saved_path = out_p
                        print(f"  >>> [step {s:3d}] VALID CEX on {os.path.basename(vp)}: gap={best_gap:+.6e}, ort_margin={ort_margin:+.6e}, rival={best_k}, strict={strict_ok}")

        obj = (y[torch.arange(batch_size), t_idx] - y[:, y_true]).sum()
        obj.backward()
        with torch.no_grad():
            grad = x_var.grad
            g_norm = grad / (grad.abs().mean(dim=(1, 2, 3), keepdim=True) + 1e-12)
            mom = 0.75 * mom + g_norm
            # First half of batch: pure Frank-Wolfe on raw grad; second half: Momentum-FW
            use_dir = torch.where(
                (torch.arange(batch_size) < batch_size // 2).view(-1, 1, 1, 1),
                grad,
                mom,
            )
            vertex = torch.where(use_dir >= 0, hi_in, lo_in)
            alpha = 0.001 + 0.35 * (0.5 * (1.0 + np.cos(s / steps * np.pi))) ** 1.5
            x = torch.max(torch.min(x + alpha * (vertex - x), hi_in), lo_in)

            if s in (30, 70, 110, 150):
                t_idx[:] = best_k
                _, order = torch.sort(m_vals)
                worst = order[: batch_size // 2]
                noise_scale = 0.08 if s == 30 else (0.03 if s == 70 else 0.008)
                for w_i in worst:
                    noise = torch.randn_like(best_x) * noise_scale * rad_t
                    x[w_i : w_i + 1] = torch.max(torch.min(best_x + noise, hi_in), lo_in)
                    mom[w_i : w_i + 1] = 0.0

    print(f"[{os.path.basename(vp):58s}] clean={float(top_vals[0]):+.5f} -> best={best_gap:+.6f} (rival {best_k}, cex={saved_path is not None}, {time.time()-t0:.1f}s)")
    return best_gap, best_k, saved_path


if __name__ == "__main__":
    cct = os.path.join(tempfile.gettempdir(), "vnncomp2026_cct")
    targets = [
        ("tinyimagenet_eps1_wide_cnn7", "tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib", 90, 16),
        ("cifar10_eps8_wide_cnn7", "cifar10_eps8_wide_cnn7_idx8397_sample9.vnnlib", 160, 24),
        ("cifar10_eps8_wide_cnn7", "cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib", 180, 24),
        ("cifar10_eps8_wide_cnn7", "cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib", 180, 24),
        ("cifar10_eps8_cnn7", "cifar10_eps8_cnn7_idx8072_sample9.vnnlib", 180, 24),
        ("cifar10_eps8_cnn7", "cifar10_eps8_cnn7_idx4688_sample8.vnnlib", 180, 24),
        ("tinyimagenet_eps1_cnn7", "tinyimagenet_eps1_cnn7_idx8561_sample7.vnnlib", 160, 20),
        ("cifar10_eps2_wide_cnn7", "cifar10_eps2_wide_cnn7_idx4519_sample7.vnnlib", 160, 24),
    ]
    for mname, vname, st, bs in targets:
        attack_cct_instance(f"{cct}/onnx/{mname}.onnx", f"{cct}/vnnlib/{mname}/{vname}", steps=st, batch_size=bs)
