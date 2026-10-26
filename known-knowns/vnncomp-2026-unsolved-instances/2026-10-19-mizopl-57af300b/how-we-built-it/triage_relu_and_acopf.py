import tempfile
from pathlib import Path
#!/usr/bin/env python3
"""
CLSS Linear-Region Exact Vertex Seam Surgery (Frank-Wolfe / Line-Search PGD)
for all 27 unsolved instances of cora_2024 and metaroom_2023.
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
    # Find y_true from (>= Y_k Y_true) or (<= Y_true Y_k)
    m_y = re.search(r"\(\s*>=\s+Y_(\d+)\s+Y_(\d+)\s*\)", txt)
    if m_y:
        y_true = int(m_y.group(2))
    else:
        m_y2 = re.search(r"\(\s*<=\s+Y_(\d+)\s+Y_(\d+)\s*\)", txt)
        y_true = int(m_y2.group(1))
    return l_arr, u_arr, y_true


class ONNXReluModel(nn.Module):
    def __init__(self, onnx_path):
        super().__init__()
        m = onnx.load(onnx_path)
        self.inits = {init.name: torch.tensor(numpy_helper.to_array(init)) for init in m.graph.initializer}
        for nd in m.graph.node:
            if nd.op_type == "Constant":
                for a in nd.attribute:
                    if a.name == "value":
                        self.inits[nd.output[0]] = torch.tensor(numpy_helper.to_array(a.t))
        self.nodes = [nd for nd in m.graph.node if nd.op_type != "Constant"]
        self.inp_name = m.graph.input[0].name
        inp_dims = [d.dim_value if d.dim_value > 0 else 1 for d in m.graph.input[0].type.tensor_type.shape.dim]
        self.inp_shape = tuple(inp_dims)

    def forward(self, x):
        env = {self.inp_name: x}
        env.update({k: v.to(x.device) for k, v in self.inits.items()})
        for nd in self.nodes:
            op = nd.op_type
            if op == "MatMul":
                env[nd.output[0]] = torch.matmul(env[nd.input[0]], env[nd.input[1]])
            elif op == "Add":
                env[nd.output[0]] = env[nd.input[0]] + env[nd.input[1]]
            elif op == "Sub":
                env[nd.output[0]] = env[nd.input[0]] - env[nd.input[1]]
            elif op == "Mul":
                env[nd.output[0]] = env[nd.input[0]] * env[nd.input[1]]
            elif op == "Relu":
                env[nd.output[0]] = F.relu(env[nd.input[0]])
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
            elif op == "Reshape":
                sh = tuple(env[nd.input[1]].long().tolist())
                env[nd.output[0]] = env[nd.input[0]].reshape(x.shape[0], -1)
            elif op == "Flatten":
                env[nd.output[0]] = env[nd.input[0]].reshape(x.shape[0], -1)
            elif op == "Gemm":
                A = env[nd.input[0]]
                B = env[nd.input[1]]
                C = env[nd.input[2]] if len(nd.input) > 2 else None
                transB = 0
                for a in nd.attribute:
                    if a.name == "transB":
                        transB = a.i
                res = torch.matmul(A, B.t() if transB else B)
                if C is not None:
                    res = res + C
                env[nd.output[0]] = res
            else:
                raise RuntimeError(f"Unsupported op {op}")
        return env[self.nodes[-1].output[0]]


def triage_instance(onnx_path, vnnlib_path, steps=150, batch_size=64):
    t0 = time.time()
    l_arr, u_arr, y_true = parse_vnnlib1(vnnlib_path)
    model = ONNXReluModel(onnx_path)
    sess = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
    inp_name = model.inp_name
    shape = model.inp_shape

    l_t = torch.tensor(l_arr.reshape(1, *shape[1:]), dtype=torch.float32)
    u_t = torch.tensor(u_arr.reshape(1, *shape[1:]), dtype=torch.float32)
    lo_in = l_t + 1e-3 * (u_t - l_t)
    hi_in = u_t - 1e-3 * (u_t - l_t)
    mid_t = 0.5 * (l_t + u_t)
    rad_t = 0.5 * (u_t - l_t)

    with torch.no_grad():
        y0 = model(mid_t)
        ort_y0 = sess.run(None, {inp_name: mid_t.numpy()})[0]
        ort_err = float(np.max(np.abs(y0.numpy() - ort_y0)))
        gaps0 = (y0[0] - y0[0, y_true]).clone()
        gaps0[y_true] = -1e9
        top_vals, top_ks = torch.topk(gaps0, k=min(6, len(gaps0) - 1))

    # Assign batch particles across top rival classes
    rivals = [int(k) for k in top_ks]
    t_idx = torch.tensor([rivals[b % len(rivals)] for b in range(batch_size)], dtype=torch.long)

    x = mid_t.repeat(batch_size, *([1] * (len(shape) - 1)))
    with torch.no_grad():
        for b in range(1, batch_size):
            if b < batch_size // 2:
                x[b : b + 1] = mid_t + (2.0 * torch.rand_like(mid_t) - 1.0) * 0.99 * rad_t
            else:
                x[b : b + 1] = mid_t + torch.sign(torch.randn_like(mid_t)) * 0.995 * rad_t
        x = torch.max(torch.min(x, hi_in), lo_in)

    best_gap = float(top_vals[0])
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
                    print(f"  >>> FOUND COUNTEREXAMPLE on {os.path.basename(vnnlib_path)}: gap={best_gap:+.6e}, ort_margin={ort_margin:+.6e}, strict={strict_ok}")
                    if ort_margin >= 1e-6 and strict_ok:
                        return cand_np, best_k, ort_margin

        obj = (y[torch.arange(batch_size), t_idx] - y[:, y_true]).sum()
        obj.backward()
        with torch.no_grad():
            grad = x_var.grad
            # Exact linear-region extreme vertex v(x)
            vertex = torch.where(grad >= 0, hi_in, lo_in)
            # Mix Frank-Wolfe convex step toward vertex and Sign-PGD step
            alpha = 0.02 + 0.45 * (0.5 * (1.0 + np.cos(s / steps * np.pi)))
            x_fw = x + alpha * (vertex - x)
            x_pgd = torch.max(torch.min(x + alpha * rad_t * torch.sign(grad), hi_in), lo_in)
            # Evaluate both and keep the better point per particle!
            y_fw = model(x_fw)
            y_pgd = model(x_pgd)
            score_fw = y_fw[torch.arange(batch_size), t_idx] - y_fw[:, y_true]
            score_pgd = y_pgd[torch.arange(batch_size), t_idx] - y_pgd[:, y_true]
            cond = (score_fw >= score_pgd).view(batch_size, *([1] * (len(shape) - 1)))
            x = torch.where(cond, x_fw, x_pgd)

    print(f"[{os.path.basename(onnx_path):25s} | {os.path.basename(vnnlib_path):32s}] clean_gap={float(top_vals[0]):+.5f} -> best_gap={best_gap:+.5f} (rival {best_k}, ort_err={ort_err:.1e}, {time.time()-t0:.1f}s)")
    return None, best_k, best_gap


if __name__ == "__main__":
    base = "{Path(__file__).resolve().parent.parent.parent}/data"
    tasks = [
        (f"{base}/metaroom_2023/onnx/6cnn_ry_39_6_no_custom_OP.onnx", f"{base}/metaroom_2023/vnnlib/spec_idx_119_eps_0.00000436.vnnlib"),
    ]
    for i in [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]:
        tasks.append((f"{base}/cora_2024/onnx/mnist-trades.onnx", f"{base}/cora_2024/vnnlib/mnist-img{i}.vnnlib"))
    for i in [9, 12]:
        tasks.append((f"{base}/cora_2024/onnx/mnist-point.onnx", f"{base}/cora_2024/vnnlib/mnist-img{i}.vnnlib"))
    for m, img in [
        ("cifar10-set.onnx", "cifar10-img78.vnnlib"),
        ("cifar10-point.onnx", "cifar10-img306.vnnlib"),
        ("cifar10-trades.onnx", "cifar10-img316.vnnlib"),
        ("cifar10-set.onnx", "cifar10-img345.vnnlib"),
        ("cifar10-trades.onnx", "cifar10-img346.vnnlib"),
        ("cifar10-set.onnx", "cifar10-img362.vnnlib"),
    ]:
        tasks.append((f"{base}/cora_2024/onnx/{m}", f"{base}/cora_2024/vnnlib/{img}"))

    for onnx_p, vnn_p in tasks:
        cand, k, gap = triage_instance(onnx_p, vnn_p, steps=120, batch_size=64)
        if cand is not None:
            out_p = f"{Path(__file__).resolve().parent.parent.parent}/attempts/lens1_unsolved_audit_and_linear_seam_surgery/cex_{os.path.basename(onnx_p)}_{os.path.basename(vnn_p)}.npy"
            np.save(out_p, cand)
            print("SAVED:", out_p)
