import tempfile
from pathlib import Path
#!/usr/bin/env python3
"""
Focused CLSS Linear-Region Seam & Momentum-PGD / Frank-Wolfe Surgery on the top near-zero
unsolved ResNet instances in TinyImageNet_2024 and CIFAR100_2024.
"""
import os
import time
import numpy as np
import onnxruntime as ort
import torch
from triage_relu_and_acopf import parse_vnnlib1
from triage_cifar100_and_tiny import ONNXResNetModel

torch.set_num_threads(8)


def strict_interior_bounds(l_arr, u_arr, shape):
    # 2 float32 ULPs inside (l_arr, u_arr) so lo < x_i < hi holds strictly in float32
    lo_np = np.nextafter(np.nextafter(l_arr, u_arr), u_arr).reshape(1, *shape[1:])
    hi_np = np.nextafter(np.nextafter(u_arr, l_arr), l_arr).reshape(1, *shape[1:])
    return torch.tensor(lo_np, dtype=torch.float32), torch.tensor(hi_np, dtype=torch.float32)


def attack_instance(model, sess, vp, l_arr, u_arr, y_true, target_k=None, batch_size=32, steps=200):
    t0 = time.time()
    shape = model.inp_shape
    inp_name = model.inp_name
    lo_in, hi_in = strict_interior_bounds(l_arr, u_arr, shape)
    mid_t = 0.5 * (lo_in + hi_in)
    rad_t = 0.5 * (hi_in - lo_in)

    # First quick 15-step probe if target_k not given
    if target_k is None:
        with torch.no_grad():
            y0 = model(mid_t)
            gaps0 = (y0[0] - y0[0, y_true]).clone()
            gaps0[y_true] = -1e9
            _, top_ks = torch.topk(gaps0, k=8)
        rivals = [int(k) for k in top_ks]
    else:
        rivals = [target_k]

    t_idx = torch.tensor([rivals[b % len(rivals)] for b in range(batch_size)], dtype=torch.long)

    # Initialize batch: particle 0 at midpoint, others with different random corners / Gaussian perturbations
    torch.manual_seed(42)
    x = mid_t.repeat(batch_size, 1, 1, 1)
    with torch.no_grad():
        for b in range(1, batch_size):
            scale = 0.2 + 0.8 * ((b % 8) / 7.0)
            x[b : b + 1] = mid_t + torch.sign(torch.randn_like(mid_t)) * scale * rad_t
        x = torch.max(torch.min(x, hi_in), lo_in)

    mom = torch.zeros_like(x)
    best_gap = -1e9
    best_k = rivals[0]
    best_x = mid_t.clone()

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
                    print(f"  >>> [step {s}] FOUND COUNTEREXAMPLE on {os.path.basename(vp)}: gap={best_gap:+.6e}, ort_margin={ort_margin:+.6e}, strict={strict_ok}")
                    if ort_margin >= 1e-6 and strict_ok:
                        out_p = f"{Path(__file__).resolve().parent.parent.parent}/attempts/lens1_unsolved_audit_and_linear_seam_surgery/cex_{os.path.basename(vp).replace('.vnnlib','')}.npy"
                        np.save(out_p, cand_np)
                        return best_gap, best_k, out_p

        obj = (y[torch.arange(batch_size), t_idx] - y[:, y_true]).sum()
        obj.backward()
        with torch.no_grad():
            grad = x_var.grad
            g_norm = grad / (grad.abs().mean(dim=(1, 2, 3), keepdim=True) + 1e-12)
            mom = 0.75 * mom + g_norm
            lr = 0.002 + 0.25 * (0.5 * (1.0 + np.cos(s / steps * np.pi)))
            vertex = torch.where(mom >= 0, hi_in, lo_in)
            x = torch.max(torch.min(x + lr * (vertex - x), hi_in), lo_in)

            if s == 25:
                t_idx[:] = best_k
                _, order = torch.sort(m_vals)
                worst = order[: batch_size // 2]
                for w_i in worst:
                    noise = torch.randn_like(best_x) * 0.05 * rad_t
                    x[w_i : w_i + 1] = torch.max(torch.min(best_x + noise, hi_in), lo_in)
                    mom[w_i : w_i + 1] = 0.0
            elif s in (60, 100, 140):
                _, order = torch.sort(m_vals)
                worst = order[: batch_size // 2]
                for w_i in worst:
                    noise = torch.randn_like(best_x) * (0.02 if s < 120 else 0.005) * rad_t
                    x[w_i : w_i + 1] = torch.max(torch.min(best_x + noise, hi_in), lo_in)
                    mom[w_i : w_i + 1] = 0.0

        if s % 40 == 0 or s == steps:
            print(f"  [{os.path.basename(vp)}] step {s:3d}/{steps}: best_gap={best_gap:+.6f} (rival {best_k}, {time.time()-t0:.1f}s)")

    return best_gap, best_k, None


if __name__ == "__main__":
    base_t = "{Path(__file__).resolve().parent.parent.parent}/data/tinyimagenet_2024"
    onnx_t = f"{base_t}/onnx/TinyImageNet_resnet_medium.onnx"
    model_t = ONNXResNetModel(onnx_t)
    sess_t = ort.InferenceSession(onnx_t, providers=["CPUExecutionProvider"])

    tiny_cands = [
        ("TinyImageNet_resnet_medium_prop_idx_6402_sidx_6736_eps_0.0039.vnnlib", 7),
        ("TinyImageNet_resnet_medium_prop_idx_378_sidx_1732_eps_0.0039.vnnlib", 159),
        ("TinyImageNet_resnet_medium_prop_idx_4303_sidx_2935_eps_0.0039.vnnlib", 157),
        ("TinyImageNet_resnet_medium_prop_idx_4464_sidx_4786_eps_0.0039.vnnlib", 74),
    ]
    for vname, rk in tiny_cands:
        vp = f"{base_t}/vnnlib/{vname}"
        l_arr, u_arr, y_true = parse_vnnlib1(vp)
        attack_instance(model_t, sess_t, vp, l_arr, u_arr, y_true, target_k=rk, batch_size=24, steps=160)

    base_c = "{Path(__file__).resolve().parent.parent.parent}/data/cifar100_2024"
    onnx_cm = f"{base_c}/onnx/CIFAR100_resnet_medium.onnx"
    model_cm = ONNXResNetModel(onnx_cm)
    sess_cm = ort.InferenceSession(onnx_cm, providers=["CPUExecutionProvider"])
    for vname, rk in [
        ("CIFAR100_resnet_medium_prop_idx_3805_sidx_6219_eps_0.0039.vnnlib", 47),
        ("CIFAR100_resnet_medium_prop_idx_4259_sidx_275_eps_0.0039.vnnlib", 96),
    ]:
        vp = f"{base_c}/vnnlib/{vname}"
        l_arr, u_arr, y_true = parse_vnnlib1(vp)
        attack_instance(model_cm, sess_cm, vp, l_arr, u_arr, y_true, target_k=rk, batch_size=24, steps=160)

    onnx_cl = f"{base_c}/onnx/CIFAR100_resnet_large.onnx"
    model_cl = ONNXResNetModel(onnx_cl)
    sess_cl = ort.InferenceSession(onnx_cl, providers=["CPUExecutionProvider"])
    for vname, rk in [
        ("CIFAR100_resnet_large_prop_idx_5454_sidx_5540_eps_0.0039.vnnlib", 73),
        ("CIFAR100_resnet_large_prop_idx_1397_sidx_345_eps_0.0039.vnnlib", 54),
        ("CIFAR100_resnet_large_prop_idx_6771_sidx_1674_eps_0.0039.vnnlib", 3),
        ("CIFAR100_resnet_large_prop_idx_7836_sidx_6290_eps_0.0039.vnnlib", 11),
        ("CIFAR100_resnet_large_prop_idx_2441_sidx_6205_eps_0.0039.vnnlib", 19),
    ]:
        vp = f"{base_c}/vnnlib/{vname}"
        l_arr, u_arr, y_true = parse_vnnlib1(vp)
        attack_instance(model_cl, sess_cl, vp, l_arr, u_arr, y_true, target_k=rk, batch_size=24, steps=160)
