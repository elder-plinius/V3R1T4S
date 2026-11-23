import tempfile
from pathlib import Path
#!/usr/bin/env python3
"""
CLSS Linear-Region Exact Vertex Seam Surgery triage for cifar100_2024 (40 unsolved instances)
and tinyimagenet_2024 (22 unsolved instances).
"""
import os
import glob
import time
import numpy as np
import onnx
from onnx import numpy_helper
import onnxruntime as ort
import torch
import torch.nn as nn
import torch.nn.functional as F
from triage_relu_and_acopf import parse_vnnlib1

torch.set_num_threads(8)


class ONNXResNetModel(nn.Module):
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
            if op == "Conv":
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
            elif op == "BatchNormalization":
                inp = env[nd.input[0]]
                sh_bn = (1, -1) + (1,) * (inp.ndim - 2)
                scale = env[nd.input[1]].view(*sh_bn)
                bias = env[nd.input[2]].view(*sh_bn)
                mean = env[nd.input[3]].view(*sh_bn)
                var = env[nd.input[4]].view(*sh_bn)
                eps = 1e-5
                for a in nd.attribute:
                    if a.name == "epsilon":
                        eps = a.f
                env[nd.output[0]] = (inp - mean) / torch.sqrt(var + eps) * scale + bias
            elif op == "Relu":
                env[nd.output[0]] = F.relu(env[nd.input[0]])
            elif op == "Add":
                env[nd.output[0]] = env[nd.input[0]] + env[nd.input[1]]
            elif op == "Sub":
                env[nd.output[0]] = env[nd.input[0]] - env[nd.input[1]]
            elif op == "Mul":
                env[nd.output[0]] = env[nd.input[0]] * env[nd.input[1]]
            elif op == "Flatten" or op == "Reshape":
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


def triage_model_instances(onnx_path, vnnlib_paths, steps=40, batch_size=16):
    model = ONNXResNetModel(onnx_path)
    sess = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
    inp_name = model.inp_name
    shape = model.inp_shape

    for vp in vnnlib_paths:
        t0 = time.time()
        l_arr, u_arr, y_true = parse_vnnlib1(vp)
        l_t = torch.tensor(l_arr.reshape(1, *shape[1:]), dtype=torch.float32)
        u_t = torch.tensor(u_arr.reshape(1, *shape[1:]), dtype=torch.float32)
        lo_in = l_t + 1e-4 * (u_t - l_t)
        hi_in = u_t - 1e-4 * (u_t - l_t)
        mid_t = 0.5 * (l_t + u_t)
        rad_t = 0.5 * (u_t - l_t)

        with torch.no_grad():
            y0 = model(mid_t)
            ort_y0 = sess.run(None, {inp_name: mid_t.numpy()})[0]
            ort_err = float(np.max(np.abs(y0.numpy() - ort_y0)))
            gaps0 = (y0[0] - y0[0, y_true]).clone()
            gaps0[y_true] = -1e9
            top_vals, top_ks = torch.topk(gaps0, k=4)

        rivals = [int(k) for k in top_ks]
        t_idx = torch.tensor([rivals[b % len(rivals)] for b in range(batch_size)], dtype=torch.long)
        x = mid_t.repeat(batch_size, 1, 1, 1)
        with torch.no_grad():
            for b in range(1, batch_size):
                x[b : b + 1] = mid_t + torch.sign(torch.randn_like(mid_t)) * 0.99 * rad_t
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
                        print(f"  >>> FOUND COUNTEREXAMPLE on {os.path.basename(vp)}: gap={best_gap:+.6e}, ort_margin={ort_margin:+.6e}, strict={strict_ok}")
                        if ort_margin >= 1e-6 and strict_ok:
                            out_p = f"{Path(__file__).resolve().parent.parent.parent}/attempts/lens1_unsolved_audit_and_linear_seam_surgery/cex_{os.path.basename(vp).replace('.vnnlib','')}.npy"
                            np.save(out_p, cand_np)
                            return out_p

            obj = (y[torch.arange(batch_size), t_idx] - y[:, y_true]).sum()
            obj.backward()
            with torch.no_grad():
                grad = x_var.grad
                vertex = torch.where(grad >= 0, hi_in, lo_in)
                alpha = 0.05 + 0.45 * (0.5 * (1.0 + np.cos(s / steps * np.pi)))
                x = torch.max(torch.min(x + alpha * (vertex - x), hi_in), lo_in)

        print(f"[{os.path.basename(vp):62s}] clean={float(top_vals[0]):+.5f} -> best={best_gap:+.5f} (rival {best_k}, ort_err={ort_err:.1e}, {time.time()-t0:.1f}s)")
    return None


if __name__ == "__main__":
    base = "{Path(__file__).resolve().parent.parent.parent}/data/cifar100_2024"
    v_files = sorted(glob.glob(f"{base}/vnnlib/CIFAR100_resnet_medium_*.vnnlib"))
    triage_model_instances(f"{base}/onnx/CIFAR100_resnet_medium.onnx", v_files, steps=35, batch_size=12)
