import tempfile
from pathlib import Path
#!/usr/bin/env python3
"""
Lens 1: CLSS Pre-Softmax Logit Cauchy-STE + Penultimate Seam Potential +
Gradient-Guided Sparse/Patch Beam Surgery for VNN-COMP 2026 unsolved instances
in traffic_signs_recognition_2023.
"""
import os
import re
import time
import numpy as np
import onnx
from onnx import numpy_helper
import onnxruntime as ort
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.set_num_threads(8)


def parse_vnnlib1(path):
    with open(path) as f:
        txt = f.read()
    lo = {}
    hi = {}
    for m in re.finditer(r"\(\s*assert\s*\(\s*<=\s+X_(\d+)\s+([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*\)\s*\)", txt):
        hi[int(m.group(1))] = float(m.group(2))
    for m in re.finditer(r"\(\s*assert\s*\(\s*>=\s+X_(\d+)\s+([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*\)\s*\)", txt):
        lo[int(m.group(1))] = float(m.group(2))
    n = max(hi.keys()) + 1
    l_arr = np.array([lo[i] for i in range(n)], dtype=np.float32)
    u_arr = np.array([hi[i] for i in range(n)], dtype=np.float32)
    m_y = re.search(r">=\s+Y_(\d+)\s+Y_(\d+)", txt)
    y_true = int(m_y.group(2))
    return l_arr, u_arr, y_true


class CauchySTESign(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, temp=1.0):
        ctx.save_for_backward(x)
        ctx.temp = temp
        s1 = torch.sign(x)
        return torch.sign(s1 + 0.1)

    @staticmethod
    def backward(ctx, grad_output):
        (x,) = ctx.saved_tensors
        temp = ctx.temp
        scale = x.abs().mean(dim=tuple(range(1, x.ndim)), keepdim=True).clamp(min=1e-4)
        u = x / scale
        grad_u = temp / ((temp + u.abs()) ** 2)
        return grad_output * (grad_u / scale), None


def qsign_ste(x, temp=1.0):
    return CauchySTESign.apply(x, temp)


class ONNXQModel(nn.Module):
    def __init__(self, onnx_path):
        super().__init__()
        m = onnx.load(onnx_path)
        self.inits = {init.name: torch.tensor(numpy_helper.to_array(init)) for init in m.graph.initializer}
        self.nodes = list(m.graph.node)
        self.inp_name = m.graph.input[0].name
        inp_dims = [d.dim_value for d in m.graph.input[0].type.tensor_type.shape.dim]
        self.inp_shape = tuple(inp_dims)

    def forward_all(self, x, temp=1.0):
        env = {self.inp_name: x}
        env.update({k: v.to(x.device) for k, v in self.inits.items()})
        i = 0
        n = len(self.nodes)
        logits = None
        soft_logits = None
        last_u = None
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
                last_u = u
                out_name = self.nodes[i + 2].output[0]
                env[out_name] = qsign_ste(u, temp=temp)
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
                sh = tuple(env[nd.input[1]].long().tolist())
                env[nd.output[0]] = env[nd.input[0]].reshape(sh[0] if sh[0] != -1 else x.shape[0], *sh[1:])
            elif op == "MatMul":
                w = env[nd.input[1]]
                res = torch.matmul(env[nd.input[0]], w)
                env[nd.output[0]] = res
                logits = res
                if i == n - 2 and last_u is not None:
                    u_flat = last_u.reshape(x.shape[0], -1)
                    sc = u_flat.abs().mean(dim=1, keepdim=True).clamp(min=1e-4)
                    soft_act = torch.tanh(u_flat / (0.5 * sc))
                    soft_logits = torch.matmul(soft_act, w)
            elif op == "Softmax":
                logits = env[nd.input[0]]
                env[nd.output[0]] = F.softmax(logits, dim=-1)
            else:
                raise RuntimeError(f"Unsupported op {op}")
            i += 1
        return logits, soft_logits, env[self.nodes[-1].output[0]]


def check_bounds_strict(x_flat, l_arr, u_arr):
    return bool(np.all((x_flat > l_arr) & (x_flat < u_arr)))


def clamp_strict_interior(x, l_t, u_t, rel_margin=2e-3):
    width = u_t - l_t
    lo_in = l_t + rel_margin * width
    hi_in = u_t - rel_margin * width
    return torch.max(torch.min(x, hi_in), lo_in)


def attack_instance(onnx_path, vnnlib_path, max_time_sec=120.0, seed=42):
    t0 = time.time()
    torch.manual_seed(seed)
    np.random.seed(seed)

    l_arr, u_arr, y_true = parse_vnnlib1(vnnlib_path)
    print(f"\n[ATTACK] {os.path.basename(vnnlib_path)} | y_true={y_true} | min_width={(u_arr - l_arr).min():.6g} max_width={(u_arr - l_arr).max():.6g}")

    model = ONNXQModel(onnx_path)
    sess = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
    inp_name = model.inp_name
    shape = model.inp_shape
    H, W, C = shape[1], shape[2], shape[3]
    D = H * W * C

    l_t = torch.tensor(l_arr.reshape(1, H, W, C), dtype=torch.float32)
    u_t = torch.tensor(u_arr.reshape(1, H, W, C), dtype=torch.float32)
    lo_in = l_t + 2e-3 * (u_t - l_t)
    hi_in = u_t - 2e-3 * (u_t - l_t)
    mid_t = 0.5 * (l_t + u_t)
    rad_t = 0.5 * (u_t - l_t)

    with torch.no_grad():
        logits0, soft0, probs0 = model.forward_all(mid_t)
        ort_probs0 = sess.run(None, {inp_name: mid_t.numpy()})[0]
        max_ort_diff = float(np.max(np.abs(probs0.numpy() - ort_probs0)))
        z0 = logits0[0].clone()
        z0_true = float(z0[y_true])
        z0_masked = z0.clone()
        z0_masked[y_true] = -1e9
        top_vals, top_classes = torch.topk(z0_masked, k=6)
        print(f"  Clean logits: z_true({y_true})={z0_true:.1f}, top rivals={list(zip(top_classes.tolist(), [float(v) for v in top_vals]))}, ort_diff={max_ort_diff:.2e}")

    # Phase 1: Quick 40-step Batched Multi-Target Cauchy-STE warmup (batch=48) to reach deep seam basin
    warmup_batch = 48
    target_classes = [int(c) for c in top_classes[:4]]
    x = mid_t.repeat(warmup_batch, 1, 1, 1)
    with torch.no_grad():
        for b in range(1, warmup_batch):
            if b < 24:
                x[b : b + 1] = mid_t + (2.0 * torch.rand_like(mid_t) - 1.0) * 0.99 * rad_t
            else:
                x[b : b + 1] = mid_t + torch.sign(torch.randn_like(mid_t)) * 0.995 * rad_t
        x = clamp_strict_interior(x, l_t, u_t, rel_margin=2e-3)

    best_int_gap = -1e9
    best_score = -1e9
    best_x = mid_t.clone()
    best_k = target_classes[0]

    # Collect a diverse pool of top K=12 elites
    K = 12
    elite_x = x[:K].clone()
    elite_scores = torch.full((K,), -1e9)
    elite_ks = torch.full((K,), best_k, dtype=torch.long)

    for step in range(1, 36):
        temp = 0.4 + 0.8 * (1.0 - step / 36.0)
        x_var = x.detach().requires_grad_(True)
        logits, soft_logits, _ = model.forward_all(x_var, temp=temp)
        with torch.no_grad():
            int_gaps = logits - logits[:, y_true : y_true + 1]
            int_gaps[:, y_true] = -1e9
            soft_gaps = soft_logits - soft_logits[:, y_true : y_true + 1]
            soft_gaps[:, y_true] = -1e9
            combined = int_gaps + 0.05 * soft_gaps
            max_scores, max_ks = combined.max(dim=1)
            max_int_gaps = int_gaps[torch.arange(warmup_batch), max_ks]

            idx_best = int(max_scores.argmax())
            if float(max_int_gaps[idx_best]) > best_int_gap or (
                float(max_int_gaps[idx_best]) == best_int_gap and float(max_scores[idx_best]) > best_score
            ):
                best_int_gap = float(max_int_gaps[idx_best])
                best_score = float(max_scores[idx_best])
                best_x = x[idx_best : idx_best + 1].detach().clone()
                best_k = int(max_ks[idx_best])
                print(f"  [Warmup {step:2d} | {time.time()-t0:4.1f}s] int_gap={best_int_gap:+.1f} total_score={best_score:+.3f} (rival {best_k})")
                if best_int_gap >= 0.0:
                    cand_np = best_x.numpy().astype(np.float32)
                    ort_out = sess.run(None, {inp_name: cand_np})[0][0]
                    margin = float(ort_out[best_k] - ort_out[y_true])
                    if margin >= 1e-6 and check_bounds_strict(cand_np.reshape(-1), l_arr, u_arr):
                        return cand_np, best_k, best_int_gap, margin

        t_idx = torch.tensor([target_classes[b % len(target_classes)] for b in range(warmup_batch)], dtype=torch.long)
        loss = (
            (logits[torch.arange(warmup_batch), t_idx] - logits[:, y_true])
            + 0.2 * (soft_logits[torch.arange(warmup_batch), t_idx] - soft_logits[:, y_true])
        ).sum()
        loss.backward()
        with torch.no_grad():
            lr = (0.04 + 0.20 * (1.0 - step / 36.0)) * rad_t
            x = clamp_strict_interior(x + lr * torch.sign(x_var.grad), l_t, u_t, rel_margin=2e-3)

    # Seed the K=12 elites from the warmup population
    with torch.no_grad():
        logits, soft_logits, _ = model.forward_all(x)
        int_gaps = logits - logits[:, y_true : y_true + 1]
        int_gaps[:, y_true] = -1e9
        soft_gaps = soft_logits - soft_logits[:, y_true : y_true + 1]
        soft_gaps[:, y_true] = -1e9
        combined = int_gaps + 0.05 * soft_gaps
        max_scores, max_ks = combined.max(dim=1)
        order = torch.argsort(max_scores, descending=True)
        elite_x[0:1] = best_x.clone()
        elite_scores[0] = best_score
        elite_ks[0] = best_k
        pos = 1
        for idx in order:
            if pos >= K:
                break
            cand = x[idx : idx + 1]
            if (cand - elite_x[:pos]).abs().max() > 1e-4:
                elite_x[pos : pos + 1] = cand.clone()
                elite_scores[pos] = max_scores[idx]
                elite_ks[pos] = max_ks[idx]
                pos += 1
        while pos < K:
            elite_x[pos : pos + 1] = clamp_strict_interior(
                best_x + 0.1 * rad_t * torch.randn_like(best_x), l_t, u_t, rel_margin=2e-3
            )
            elite_scores[pos] = best_score - 10.0
            elite_ks[pos] = best_k
            pos += 1

    print(f"  Entering CLSS Gradient-Guided Sparse/Patch Beam Surgery (K={K}, best_int_gap={best_int_gap:+.1f}, rival={best_k})...")
    step = 0
    num_offspring = 96
    while time.time() - t0 < max_time_sec:
        step += 1
        # 1. Compute Cauchy-STE + Penultimate Seam gradients on the K elites
        temp = 0.25 + 0.75 * (0.5 * (1.0 + np.cos(step * 0.2)))
        e_var = elite_x.detach().requires_grad_(True)
        e_logits, e_soft, _ = model.forward_all(e_var, temp=temp)
        # Focus gradient on best_k (or each elite's assigned rival class)
        e_obj = (
            (e_logits[torch.arange(K), elite_ks] - e_logits[:, y_true])
            + 0.25 * (e_soft[torch.arange(K), elite_ks] - e_soft[:, y_true])
        ).sum()
        e_obj.backward()
        grad_e = e_var.grad.detach()  # shape (K, H, W, C)

        # 2. Generate 96 offspring using 4 complementary CLSS seam-surgery operators
        with torch.no_grad():
            cands = torch.empty((num_offspring, H, W, C), dtype=torch.float32)
            for b in range(num_offspring):
                parent_idx = 0 if (b % 3 == 0) else (b % K)
                parent = elite_x[parent_idx : parent_idx + 1]
                g = grad_e[parent_idx : parent_idx + 1]
                target_extreme = torch.where(g >= 0, hi_in, lo_in)
                room = (target_extreme - parent).abs()
                salience = (g.abs() * room).reshape(-1)

                op_type = b % 4
                if op_type == 0:
                    # Operator A: Gradient-guided sparse top-m coordinate flips (with stochastic masking)
                    m_list = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
                    m = m_list[(b // 4) % len(m_list)]
                    noisy_sal = salience * (0.5 + torch.rand_like(salience))
                    topk_idx = torch.topk(noisy_sal, k=m).indices
                    child = parent.reshape(-1).clone()
                    alpha = 1.0 if (b % 8 == 0) else (0.5 + 0.5 * np.random.rand())
                    t_flat = target_extreme.reshape(-1)
                    child[topk_idx] = child[topk_idx] + alpha * (t_flat[topk_idx] - child[topk_idx])
                    cands[b : b + 1] = child.reshape(1, H, W, C)

                elif op_type == 1:
                    # Operator B: Receptive-field spatial patch surgery (2x2, 3x3, 5x5) around high-gradient or random patches
                    ph = [1, 2, 3, 5][(b // 4) % 4]
                    if (b // 4) % 2 == 0:
                        # Center patch around one of the top-32 salient coordinates
                        top_coord = int(torch.topk(salience, k=32).indices[np.random.randint(0, 32)])
                        pix_idx = top_coord // C
                        r_center, c_center = pix_idx // W, pix_idx % W
                        r0 = int(np.clip(r_center - ph // 2, 0, H - ph))
                        c0 = int(np.clip(c_center - ph // 2, 0, W - ph))
                    else:
                        r0 = np.random.randint(0, H - ph + 1)
                        c0 = np.random.randint(0, W - ph + 1)
                    child = parent.clone()
                    if (b // 8) % 2 == 0:
                        # Move patch toward gradient-indicated extreme
                        alpha = 0.4 + 0.6 * np.random.rand()
                        child[0, r0 : r0 + ph, c0 : c0 + ph, :] += alpha * (
                            target_extreme[0, r0 : r0 + ph, c0 : c0 + ph, :] - child[0, r0 : r0 + ph, c0 : c0 + ph, :]
                        )
                    else:
                        # Random extreme assignment in patch
                        child[0, r0 : r0 + ph, c0 : c0 + ph, :] = (
                            mid_t[0, r0 : r0 + ph, c0 : c0 + ph, :]
                            + torch.sign(torch.randn(ph, ph, C)) * 0.995 * rad_t[0, r0 : r0 + ph, c0 : c0 + ph, :]
                        )
                    cands[b : b + 1] = child

                elif op_type == 2:
                    # Operator C: Fine-scale Cauchy-STE step + sparse random sign flips
                    alpha_list = [0.002, 0.005, 0.01, 0.02, 0.04, 0.08]
                    alpha = alpha_list[(b // 4) % len(alpha_list)]
                    child = parent + alpha * rad_t * torch.sign(g)
                    # Also flip 1..4 random coordinates
                    n_rand = 1 + ((b // 4) % 4)
                    r_idx = torch.randint(0, D, (n_rand,))
                    c_flat = child.reshape(-1)
                    ext_flat = (mid_t + torch.sign(torch.randn_like(mid_t)) * 0.995 * rad_t).reshape(-1)
                    c_flat[r_idx] = ext_flat[r_idx]
                    cands[b : b + 1] = c_flat.reshape(1, H, W, C)

                else:
                    # Operator D: Elite patch/mask crossover + sparse random corner flips
                    other_idx = (parent_idx + 1 + (b // 4)) % K
                    other = elite_x[other_idx : other_idx + 1]
                    child = parent.clone()
                    if (b // 4) % 2 == 0 and (other - parent).abs().max() > 1e-4:
                        # Copy a random spatial rectangle from other elite into parent
                        rh = np.random.randint(3, H // 2 + 1)
                        rw = np.random.randint(3, W // 2 + 1)
                        r0 = np.random.randint(0, H - rh + 1)
                        c0 = np.random.randint(0, W - rw + 1)
                        child[0, r0 : r0 + rh, c0 : c0 + rw, :] = other[0, r0 : r0 + rh, c0 : c0 + rw, :]
                    # Plus flip k_flip random coordinates toward their gradient extreme or random extreme
                    k_flip = [1, 2, 4, 8, 16, 32][(b // 4) % 6]
                    r_idx = torch.randint(0, D, (k_flip,))
                    c_flat = child.reshape(-1)
                    if b % 8 == 3:
                        t_flat = target_extreme.reshape(-1)
                        c_flat[r_idx] = t_flat[r_idx]
                    else:
                        ext_flat = (mid_t + torch.sign(torch.randn_like(mid_t)) * 0.995 * rad_t).reshape(-1)
                        c_flat[r_idx] = ext_flat[r_idx]
                    cands[b : b + 1] = c_flat.reshape(1, H, W, C)

            cands = clamp_strict_interior(cands, l_t, u_t, rel_margin=2e-3)

            # Evaluate all 96 candidates in a single forward pass
            logits, soft_logits, _ = model.forward_all(cands)
            int_gaps = logits - logits[:, y_true : y_true + 1]
            int_gaps[:, y_true] = -1e9
            soft_gaps = soft_logits - soft_logits[:, y_true : y_true + 1]
            soft_gaps[:, y_true] = -1e9
            combined = int_gaps + 0.05 * soft_gaps

            max_scores, max_ks = combined.max(dim=1)
            max_int_gaps = int_gaps[torch.arange(num_offspring), max_ks]

            batch_best_idx = int(max_scores.argmax())
            b_int = float(max_int_gaps[batch_best_idx])
            b_sc = float(max_scores[batch_best_idx])
            b_k = int(max_ks[batch_best_idx])

            if b_int > best_int_gap or (b_int == best_int_gap and b_sc > best_score + 1e-4):
                improved_int = b_int > best_int_gap
                best_int_gap = b_int
                best_score = b_sc
                best_x = cands[batch_best_idx : batch_best_idx + 1].clone()
                best_k = b_k
                if improved_int or (step % 15 == 0):
                    print(f"  [Beam {step:4d} | {time.time()-t0:5.1f}s] int_gap={best_int_gap:+.1f} total_score={best_score:+.3f} (rival {best_k})")
                if best_int_gap >= 0.0:
                    cand_np = best_x.numpy().astype(np.float32)
                    ort_out = sess.run(None, {inp_name: cand_np})[0][0]
                    margin = float(ort_out[best_k] - ort_out[y_true])
                    strict_ok = check_bounds_strict(cand_np.reshape(-1), l_arr, u_arr)
                    print(f"  >>> COUNTEREXAMPLE FOUND: int_gap={best_int_gap:+.1f}, ORT prob_margin={margin:+.6e}, strict_interior={strict_ok}")
                    if margin >= 1e-6 and strict_ok:
                        return cand_np, best_k, best_int_gap, margin

            # Merge elites + candidates and select top K diverse individuals
            all_x = torch.cat([elite_x, cands], dim=0)
            all_scores = torch.cat([elite_scores, max_scores], dim=0)
            all_ks = torch.cat([elite_ks, max_ks], dim=0)
            order = torch.argsort(all_scores, descending=True)

            new_elite_x = torch.empty_like(elite_x)
            new_elite_scores = torch.empty_like(elite_scores)
            new_elite_ks = torch.empty_like(elite_ks)

            pos = 0
            for idx in order:
                if pos >= K:
                    break
                cand = all_x[idx : idx + 1]
                if pos == 0 or (cand - new_elite_x[:pos]).abs().reshape(pos, -1).max(dim=1).values.min() > 1e-4:
                    new_elite_x[pos : pos + 1] = cand
                    new_elite_scores[pos] = all_scores[idx]
                    new_elite_ks[pos] = all_ks[idx]
                    pos += 1
            if pos == K:
                elite_x = new_elite_x
                elite_scores = new_elite_scores
                elite_ks = new_elite_ks

    return None, best_k, best_int_gap, 0.0


if __name__ == "__main__":
    base = "{Path(__file__).resolve().parent.parent.parent}/data/traffic_signs_recognition_2023"
    m30 = f"{base}/onnx/3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30.onnx"
    m48 = f"{base}/onnx/3_48_48_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_BN_Dense_256_BN_Dense_43_ep_30.onnx"
    m64 = f"{base}/onnx/3_64_64_QConv_32_5_MP_2_BN_QConv_64_5_MP_2_BN_QConv_64_3_MP_2_BN_Dense_1024_BN_Dense_43_ep_30.onnx"

    targets = [
        (m48, f"{base}/vnnlib/model_48_idx_6371_eps_3.00000.vnnlib", 90.0),
        (m30, f"{base}/vnnlib/model_30_idx_1703_eps_1.00000.vnnlib", 60.0),
        (m30, f"{base}/vnnlib/model_30_idx_178_eps_1.00000.vnnlib", 60.0),
        (m48, f"{base}/vnnlib/model_48_idx_6371_eps_1.00000.vnnlib", 60.0),
    ]
    out_dir = "{Path(__file__).resolve().parent.parent.parent}/attempts/lens1_unsolved_audit_and_linear_seam_surgery"
    for onnx_p, vnn_p, t_budget in targets:
        cand, k, gap, margin = attack_instance(onnx_p, vnn_p, max_time_sec=t_budget)
        if cand is not None:
            name = os.path.basename(vnn_p).replace(".vnnlib", "")
            np.save(f"{out_dir}/cex_{name}.npy", cand)
            print(f"SUCCESSFULLY SAVED COUNTEREXAMPLE for {name}: rival={k}, logit_gap={gap}, prob_margin={margin}")
            break
