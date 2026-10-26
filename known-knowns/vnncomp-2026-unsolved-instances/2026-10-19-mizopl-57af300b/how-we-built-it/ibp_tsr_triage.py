import tempfile
from pathlib import Path
#!/usr/bin/env python3
"""
Multi-Layer Exact Interval Bound Propagation (IBP) + IBP-Masked Chord-STE &
Layer-1 Active Seam Surgery for all 9 unsolved instances of traffic_signs_recognition_2023.
"""
import os
import time
import numpy as np
import onnx
from onnx import numpy_helper
import onnxruntime as ort
import torch
import torch.nn as nn
import torch.nn.functional as F
from solve_tsr_seam import parse_vnnlib1, check_bounds_strict, clamp_strict_interior

torch.set_num_threads(8)


class MaskedChordSTE(torch.autograd.Function):
    @staticmethod
    def forward(ctx, u, active_mask, chord_slope, temp=1.0):
        ctx.save_for_backward(u, active_mask, chord_slope)
        ctx.temp = temp
        return torch.sign(torch.sign(u) + 0.1)

    @staticmethod
    def backward(ctx, grad_output):
        u, active_mask, chord_slope = ctx.saved_tensors
        temp = ctx.temp
        # Only active (flippable) neurons transmit gradient!
        # Normalize u by active chord width (2 / chord_slope)
        rel_u = u * (0.5 * chord_slope)
        surrogate_deriv = (temp / ((temp + rel_u.abs()) ** 2)) * chord_slope * active_mask
        return grad_output * surrogate_deriv, None, None, None


class IBPQModel(nn.Module):
    def __init__(self, onnx_path, l_t, u_t):
        super().__init__()
        m = onnx.load(onnx_path)
        self.inits = {init.name: torch.tensor(numpy_helper.to_array(init)) for init in m.graph.initializer}
        self.nodes = list(m.graph.node)
        self.inp_name = m.graph.input[0].name
        inp_dims = [d.dim_value for d in m.graph.input[0].type.tensor_type.shape.dim]
        self.inp_shape = tuple(inp_dims)
        self.active_masks = {}
        self.chord_slopes = {}
        self._compute_ibp(l_t, u_t)

    def _compute_ibp(self, l_t, u_t):
        with torch.no_grad():
            env_lo = {self.inp_name: l_t}
            env_hi = {self.inp_name: u_t}
            i = 0
            n = len(self.nodes)
            layer_idx = 0
            while i < n:
                nd = self.nodes[i]
                op = nd.op_type
                if (
                    op == "Sign"
                    and i + 2 < n
                    and self.nodes[i + 1].op_type == "Add"
                    and self.nodes[i + 2].op_type == "Sign"
                ):
                    layer_idx += 1
                    lo = env_lo[nd.input[0]]
                    hi = env_hi[nd.input[0]]
                    out_name = self.nodes[i + 2].output[0]
                    # qsign(u) = +1 if u >= 0 else -1
                    b_lo = torch.where(lo >= 0, torch.ones_like(lo), -torch.ones_like(lo))
                    b_hi = torch.where(hi >= 0, torch.ones_like(hi), -torch.ones_like(hi))
                    active = (b_lo != b_hi).float()
                    width = (hi - lo).clamp(min=1e-5)
                    slope = (2.0 / width) * active
                    self.active_masks[out_name] = active
                    self.chord_slopes[out_name] = slope
                    n_act = int(active.sum().item())
                    n_tot = active.numel()
                    print(f"    IBP Layer {layer_idx} ({out_name}): active={n_act}/{n_tot} ({100.0*n_act/n_tot:.1f}%)")
                    env_lo[out_name] = b_lo
                    env_hi[out_name] = b_hi
                    i += 3
                    continue
                if op == "Transpose":
                    perm = list(nd.attribute[0].ints)
                    env_lo[nd.output[0]] = env_lo[nd.input[0]].permute(*perm)
                    env_hi[nd.output[0]] = env_hi[nd.input[0]].permute(*perm)
                elif op == "Conv":
                    lo = env_lo[nd.input[0]]
                    hi = env_hi[nd.input[0]]
                    w = self.inits[nd.input[1]]
                    b = self.inits[nd.input[2]] if len(nd.input) > 2 else None
                    strides = (1, 1)
                    pads = (0, 0, 0, 0)
                    for a in nd.attribute:
                        if a.name == "strides":
                            strides = tuple(a.ints)
                        elif a.name == "pads":
                            pads = tuple(a.ints)
                    if any(pads):
                        lo = F.pad(lo, (pads[1], pads[3], pads[0], pads[2]))
                        hi = F.pad(hi, (pads[1], pads[3], pads[0], pads[2]))
                    w_pos = torch.clamp(w, min=0.0)
                    w_neg = torch.clamp(w, max=0.0)
                    out_lo = F.conv2d(lo, w_pos, None, stride=strides) + F.conv2d(hi, w_neg, None, stride=strides)
                    out_hi = F.conv2d(hi, w_pos, None, stride=strides) + F.conv2d(lo, w_neg, None, stride=strides)
                    if b is not None:
                        out_lo = out_lo + b.view(1, -1, 1, 1)
                        out_hi = out_hi + b.view(1, -1, 1, 1)
                    env_lo[nd.output[0]] = out_lo
                    env_hi[nd.output[0]] = out_hi
                elif op == "MaxPool":
                    ks = (2, 2)
                    st = (2, 2)
                    for a in nd.attribute:
                        if a.name == "kernel_shape":
                            ks = tuple(a.ints)
                        elif a.name == "strides":
                            st = tuple(a.ints)
                    env_lo[nd.output[0]] = F.max_pool2d(env_lo[nd.input[0]], kernel_size=ks, stride=st)
                    env_hi[nd.output[0]] = F.max_pool2d(env_hi[nd.input[0]], kernel_size=ks, stride=st)
                elif op == "BatchNormalization":
                    lo = env_lo[nd.input[0]]
                    hi = env_hi[nd.input[0]]
                    scale = self.inits[nd.input[1]].view(1, -1, 1, 1)
                    bias = self.inits[nd.input[2]].view(1, -1, 1, 1)
                    mean = self.inits[nd.input[3]].view(1, -1, 1, 1)
                    var = self.inits[nd.input[4]].view(1, -1, 1, 1)
                    eps = 1e-5
                    for a in nd.attribute:
                        if a.name == "epsilon":
                            eps = a.f
                    factor = scale / torch.sqrt(var + eps)
                    v1 = (lo - mean) * factor + bias
                    v2 = (hi - mean) * factor + bias
                    env_lo[nd.output[0]] = torch.min(v1, v2)
                    env_hi[nd.output[0]] = torch.max(v1, v2)
                elif op == "Sub":
                    a_lo = env_lo.get(nd.input[0], self.inits.get(nd.input[0]))
                    a_hi = env_hi.get(nd.input[0], self.inits.get(nd.input[0]))
                    b_lo = env_lo.get(nd.input[1], self.inits.get(nd.input[1]))
                    b_hi = env_hi.get(nd.input[1], self.inits.get(nd.input[1]))
                    env_lo[nd.output[0]] = a_lo - b_hi
                    env_hi[nd.output[0]] = a_hi - b_lo
                elif op == "Add":
                    a_lo = env_lo.get(nd.input[0], self.inits.get(nd.input[0]))
                    a_hi = env_hi.get(nd.input[0], self.inits.get(nd.input[0]))
                    b_lo = env_lo.get(nd.input[1], self.inits.get(nd.input[1]))
                    b_hi = env_hi.get(nd.input[1], self.inits.get(nd.input[1]))
                    env_lo[nd.output[0]] = a_lo + b_lo
                    env_hi[nd.output[0]] = a_hi + b_hi
                elif op == "Mul":
                    a_lo = env_lo.get(nd.input[0], self.inits.get(nd.input[0]))
                    a_hi = env_hi.get(nd.input[0], self.inits.get(nd.input[0]))
                    b_lo = env_lo.get(nd.input[1], self.inits.get(nd.input[1]))
                    b_hi = env_hi.get(nd.input[1], self.inits.get(nd.input[1]))
                    p1, p2, p3, p4 = a_lo * b_lo, a_lo * b_hi, a_hi * b_lo, a_hi * b_hi
                    env_lo[nd.output[0]] = torch.min(torch.min(p1, p2), torch.min(p3, p4))
                    env_hi[nd.output[0]] = torch.max(torch.max(p1, p2), torch.max(p3, p4))
                elif op == "Sqrt":
                    env_lo[nd.output[0]] = torch.sqrt( self.inits[nd.input[0]] if nd.input[0] in self.inits else env_lo[nd.input[0]] )
                    env_hi[nd.output[0]] = torch.sqrt( self.inits[nd.input[0]] if nd.input[0] in self.inits else env_hi[nd.input[0]] )
                elif op == "Reciprocal":
                    v = self.inits[nd.input[0]] if nd.input[0] in self.inits else env_lo[nd.input[0]]
                    env_lo[nd.output[0]] = torch.reciprocal(v)
                    env_hi[nd.output[0]] = torch.reciprocal(v)
                elif op == "Reshape":
                    env_lo[nd.output[0]] = env_lo[nd.input[0]].reshape(1, -1)
                    env_hi[nd.output[0]] = env_hi[nd.input[0]].reshape(1, -1)
                elif op == "MatMul":
                    lo = env_lo[nd.input[0]]
                    hi = env_hi[nd.input[0]]
                    w = self.inits[nd.input[1]]
                    w_pos = torch.clamp(w, min=0.0)
                    w_neg = torch.clamp(w, max=0.0)
                    env_lo[nd.output[0]] = torch.matmul(lo, w_pos) + torch.matmul(hi, w_neg)
                    env_hi[nd.output[0]] = torch.matmul(hi, w_pos) + torch.matmul(lo, w_neg)
                elif op == "Softmax":
                    pass
                i += 1

    def forward_all(self, x, temp=1.0):
        env = {self.inp_name: x}
        env.update({k: v.to(x.device) for k, v in self.inits.items()})
        i = 0
        n = len(self.nodes)
        logits = None
        soft_logits = None
        last_u = None
        last_out_name = None
        while i < n:
            nd = self.nodes[i]
            op = nd.op_type
            if (
                op == "Sign"
                and i + 2 < n
                and self.nodes[i + 1].op_type == "Add"
                and self.nodes[i + 2].op_type == "Sign"
            ):
                u = env[nd.input[0]]
                out_name = self.nodes[i + 2].output[0]
                last_u = u
                last_out_name = out_name
                env[out_name] = MaskedChordSTE.apply(
                    u, self.active_masks[out_name], self.chord_slopes[out_name], temp
                )
                i += 3
                continue
            if op == "Transpose":
                perm = list(nd.attribute[0].ints)
                env[nd.output[0]] = env[nd.input[0]].permute(*perm)
            elif op == "Conv":
                inp = env[nd.input[0]]
                w = env[nd.input[1]]
                b = env[nd.input[2]] if len(nd.input) > 2 else None
                strides = (1, 1)
                pads = (0, 0, 0, 0)
                for a in nd.attribute:
                    if a.name == "strides":
                        strides = tuple(a.ints)
                    elif a.name == "pads":
                        pads = tuple(a.ints)
                if any(pads):
                    inp = F.pad(inp, (pads[1], pads[3], pads[0], pads[2]))
                env[nd.output[0]] = F.conv2d(inp, w, b, stride=strides)
            elif op == "MaxPool":
                inp = env[nd.input[0]]
                ks = (2, 2)
                st = (2, 2)
                for a in nd.attribute:
                    if a.name == "kernel_shape":
                        ks = tuple(a.ints)
                    elif a.name == "strides":
                        st = tuple(a.ints)
                env[nd.output[0]] = F.max_pool2d(inp, kernel_size=ks, stride=st)
            elif op == "BatchNormalization":
                inp = env[nd.input[0]]
                scale = env[nd.input[1]].view(1, -1, 1, 1)
                bias = env[nd.input[2]].view(1, -1, 1, 1)
                mean = env[nd.input[3]].view(1, -1, 1, 1)
                var = env[nd.input[4]].view(1, -1, 1, 1)
                eps = 1e-5
                for a in nd.attribute:
                    if a.name == "epsilon":
                        eps = a.f
                env[nd.output[0]] = (inp - mean) / torch.sqrt(var + eps) * scale + bias
            elif op == "Sub":
                env[nd.output[0]] = env[nd.input[0]] - env[nd.input[1]]
            elif op == "Add":
                env[nd.output[0]] = env[nd.input[0]] + env[nd.input[1]]
            elif op == "Mul":
                env[nd.output[0]] = env[nd.input[0]] * env[nd.input[1]]
            elif op == "Sqrt":
                env[nd.output[0]] = torch.sqrt(env[nd.input[0]])
            elif op == "Reciprocal":
                env[nd.output[0]] = torch.reciprocal(env[nd.input[0]])
            elif op == "Reshape":
                env[nd.output[0]] = env[nd.input[0]].reshape(x.shape[0], -1)
            elif op == "MatMul":
                w = env[nd.input[1]]
                res = torch.matmul(env[nd.input[0]], w)
                env[nd.output[0]] = res
                logits = res
                if i == n - 2 and last_u is not None:
                    u_flat = last_u.reshape(x.shape[0], -1)
                    slope_flat = self.chord_slopes[last_out_name].reshape(1, -1)
                    soft_act = torch.tanh(u_flat * (0.5 * slope_flat))
                    soft_logits = torch.matmul(soft_act, w)
            elif op == "Softmax":
                logits = env[nd.input[0]]
                env[nd.output[0]] = F.softmax(logits, dim=-1)
            i += 1
        return logits, soft_logits, env[self.nodes[-1].output[0]]


def run_ibp_triage(onnx_path, vnnlib_path, max_time_sec=25.0):
    t0 = time.time()
    l_arr, u_arr, y_true = parse_vnnlib1(vnnlib_path)
    print(f"\n=== [IBP-MASKED ATTACK] {os.path.basename(vnnlib_path)} (y_true={y_true}) ===")
    m_tmp = onnx.load(onnx_path)
    shape = tuple(d.dim_value for d in m_tmp.graph.input[0].type.tensor_type.shape.dim)
    H, W, C = shape[1], shape[2], shape[3]
    l_t = torch.tensor(l_arr.reshape(1, H, W, C), dtype=torch.float32)
    u_t = torch.tensor(u_arr.reshape(1, H, W, C), dtype=torch.float32)
    lo_in = l_t + 1e-4 * (u_t - l_t)
    hi_in = u_t - 1e-4 * (u_t - l_t)
    mid_t = 0.5 * (l_t + u_t)
    rad_t = 0.5 * (u_t - l_t)

    model = IBPQModel(onnx_path, l_t, u_t)
    sess = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
    inp_name = model.inp_name

    # First verify on known solved model_30_idx_6371_eps_1.00000 or unsolved instance
    batch_size = 64
    torch.manual_seed(42)
    np.random.seed(42)
    with torch.no_grad():
        z0, _, _ = model.forward_all(mid_t)
        z0_m = z0[0].clone()
        z0_m[y_true] = -1e9
        top_vals, top_ks = torch.topk(z0_m, k=4)
        print(f"    Clean z_true={float(z0[0, y_true]):.1f}, top rivals={list(zip(top_ks.tolist(), [float(v) for v in top_vals]))}")

    rivals = [int(k) for k in top_ks]
    t_idx = torch.tensor([rivals[b % len(rivals)] for b in range(batch_size)], dtype=torch.long)

    x = mid_t.repeat(batch_size, 1, 1, 1)
    with torch.no_grad():
        for b in range(1, batch_size):
            if b < 32:
                x[b : b + 1] = mid_t + (2.0 * torch.rand_like(mid_t) - 1.0) * 0.99 * rad_t
            else:
                x[b : b + 1] = mid_t + torch.sign(torch.randn_like(mid_t)) * 0.999 * rad_t
        x = torch.max(torch.min(x, hi_in), lo_in)

    best_gap = -1e9
    best_x = mid_t.clone()
    best_k = rivals[0]
    step = 0
    while time.time() - t0 < max_time_sec:
        step += 1
        temp = 0.2 + 0.8 * (0.5 * (1.0 + np.cos(step * 0.15)))
        x_var = x.detach().requires_grad_(True)
        logits, soft_logits, _ = model.forward_all(x_var, temp=temp)
        with torch.no_grad():
            gaps = logits - logits[:, y_true : y_true + 1]
            gaps[:, y_true] = -1e9
            m_vals, m_ks = gaps.max(dim=1)
            idx_b = int(m_vals.argmax())
            if float(m_vals[idx_b]) > best_gap:
                best_gap = float(m_vals[idx_b])
                best_k = int(m_ks[idx_b])
                best_x = x[idx_b : idx_b + 1].detach().clone()
                print(f"    [Step {step:4d} | {time.time()-t0:4.1f}s] best_int_gap = {best_gap:+.1f} (rival {best_k})")
                if best_gap >= 0.0:
                    cand_np = best_x.numpy().astype(np.float32)
                    ort_out = sess.run(None, {inp_name: cand_np})[0][0]
                    margin = float(ort_out[best_k] - ort_out[y_true])
                    strict_ok = check_bounds_strict(cand_np.reshape(-1), l_arr, u_arr)
                    print(f"    >>> COUNTEREXAMPLE: gap={best_gap:+.1f}, ort_margin={margin:+.6e}, strict={strict_ok}")
                    if margin >= 1e-6 and strict_ok:
                        return cand_np, best_k, best_gap, margin

        loss = (
            (logits[torch.arange(batch_size), t_idx] - logits[:, y_true])
            + 0.25 * (soft_logits[torch.arange(batch_size), t_idx] - soft_logits[:, y_true])
        ).sum()
        loss.backward()
        with torch.no_grad():
            g = x_var.grad
            vertex = torch.where(g >= 0, hi_in, lo_in)
            alpha = 0.01 + 0.25 * (0.5 * (1.0 + np.cos((step % 40) / 40.0 * np.pi)))
            x = torch.max(torch.min(x + alpha * (vertex - x), hi_in), lo_in)
            if step % 20 == 0:
                worst = torch.argsort(m_vals)[:24]
                for i, w_i in enumerate(worst):
                    base = best_x.clone()
                    mask = (torch.rand_like(base) < (0.002 * (1 + (i % 10)))).float()
                    ext = mid_t + torch.sign(torch.randn_like(base)) * 0.999 * rad_t
                    x[w_i : w_i + 1] = (1.0 - mask) * base + mask * ext
    return None, best_k, best_gap, 0.0


if __name__ == "__main__":
    base = "{Path(__file__).resolve().parent.parent.parent}/data/traffic_signs_recognition_2023"
    m30 = f"{base}/onnx/3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30.onnx"
    m48 = f"{base}/onnx/3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30.onnx"
    m64 = f"{base}/onnx/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx"

    # First test on known-SAT model_30_idx_6371_eps_1.00000 as a calibration check, then all 9 unsolved!
    instances = [
        (m30, f"{base}/vnnlib/model_30_idx_6371_eps_1.00000.vnnlib", 15.0),
        (m48, f"{base}/vnnlib/model_48_idx_6371_eps_3.00000.vnnlib", 20.0),
        (m48, f"{base}/vnnlib/model_48_idx_1703_eps_1.00000.vnnlib", 15.0),
        (m48, f"{base}/vnnlib/model_48_idx_178_eps_1.00000.vnnlib", 15.0),
        (m48, f"{base}/vnnlib/model_48_idx_6371_eps_1.00000.vnnlib", 15.0),
        (m64, f"{base}/vnnlib/model_64_idx_1703_eps_1.00000.vnnlib", 15.0),
        (m64, f"{base}/vnnlib/model_64_idx_6371_eps_1.00000.vnnlib", 15.0),
        (m64, f"{base}/vnnlib/model_64_idx_178_eps_1.00000.vnnlib", 15.0),
    ]
    for op, vp, tb in instances:
        cand, k, gap, margin = run_ibp_triage(op, vp, max_time_sec=tb)
        if cand is not None and "model_30_idx_6371_eps_1.00000" not in vp:
            out_p = f"{Path(__file__).resolve().parent.parent.parent}/attempts/lens1_unsolved_audit_and_linear_seam_surgery/cex_{os.path.basename(vp).replace('.vnnlib','')}.npy"
            np.save(out_p, cand)
            print("SAVED UNSOLVED COUNTEREXAMPLE:", out_p)
            break
