import tempfile
from pathlib import Path
#!/usr/bin/env python3
"""
Lens 2: Dual-Runtime (onnxruntime CPU + onnx.reference.ReferenceEvaluator + PyTorch float32/float64),
Exact Linear-Region Vertex Polishing, and Unmodified Official VNN-COMP 2026 Validator Certification
(SCORING/counterexamples.py v1.0 + SCORING/counterexamples_v2.py v2.0 + SCORING/cex_checks.py)
for the unsolved VNN-COMP 2026 instance:
  Category: 2026_challenging_certified_training_2026
  Network:  onnx/tinyimagenet_eps1_wide_cnn7.onnx
  Property: vnnlib/tinyimagenet_eps1_wide_cnn7/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib
"""
import os
import sys
import json
import gzip
import shutil
import hashlib
from pathlib import Path
import numpy as np
import onnx
from onnx import numpy_helper
from onnx.reference import ReferenceEvaluator
import onnxruntime as ort
import torch
import torch.nn.functional as F

RUN_DIR = Path(str(Path(__file__).resolve().parent.parent.parent))
DATA_DIR = RUN_DIR / "data"
LENS1_DIR = RUN_DIR / "attempts" / "lens1_unsolved_audit_and_linear_seam_surgery"
LENS2_DIR = RUN_DIR / "attempts" / "lens2_dual_runtime_and_official_validator_certification"

sys.path.insert(0, str(LENS1_DIR))
from triage_relu_and_acopf import parse_vnnlib1
from triage_cifar100_and_tiny import ONNXResNetModel


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def forward_with_relu_distances(model: ONNXResNetModel, x: torch.Tensor):
    """Run forward pass and return (logits, penultimate_post_relu_h18, min_abs_relu_preact)."""
    env = {model.inp_name: x}
    env.update({k: v.to(device=x.device, dtype=x.dtype) for k, v in model.inits.items()})
    min_abs_preact = float("inf")
    h18 = None
    for nd in model.nodes:
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
            pre = env[nd.input[0]]
            with torch.no_grad():
                m_abs = float(pre.abs().min())
                if m_abs < min_abs_preact:
                    min_abs_preact = m_abs
            out_r = F.relu(pre)
            env[nd.output[0]] = out_r
            if nd.output[0] == "/layers/layers.18/Relu_output_0":
                h18 = out_r
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
    return env[model.nodes[-1].output[0]], h18, min_abs_preact


def main():
    onnx_src = Path(tempfile.gettempdir()) / ("vnncomp2026_cct/onnx/tinyimagenet_eps1_wide_cnn7.onnx")
    vnnlib1_src = Path(tempfile.gettempdir()) / ("vnncomp2026_cct/vnnlib/tinyimagenet_eps1_wide_cnn7/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib")
    vnnlib2_src = Path(tempfile.gettempdir()) / ("vnncomp2026_cct/tinyimagenet_eps1_wide_cnn7_idx7687_sample8_v2.vnnlib")
    npy_src = LENS1_DIR / "cex_tinyimagenet_eps1_wide_cnn7_idx7687_sample8.npy"

    assert onnx_src.is_file(), f"Missing {onnx_src}"
    assert vnnlib1_src.is_file(), f"Missing {vnnlib1_src}"
    assert vnnlib2_src.is_file(), f"Missing {vnnlib2_src}"
    assert npy_src.is_file(), f"Missing {npy_src}"

    l_arr, u_arr, y_true = parse_vnnlib1(str(vnnlib1_src))
    y_adv = 179
    assert y_true == 153, f"Expected y_true=153, got {y_true}"

    x_cand = np.load(str(npy_src)).astype(np.float32)
    shape = (1, 3, 64, 64)
    assert x_cand.shape == shape

    # 1. Exact Linear-Region Vertex Polish in float32 / float64
    model = ONNXResNetModel(str(onnx_src))
    sess = ort.InferenceSession(str(onnx_src), providers=["CPUExecutionProvider"])
    inp_name = model.inp_name

    lo_in = torch.tensor((l_arr + 1e-4 * (u_arr - l_arr)).reshape(shape), dtype=torch.float32)
    hi_in = torch.tensor((u_arr - 1e-4 * (u_arr - l_arr)).reshape(shape), dtype=torch.float32)
    x_t = torch.tensor(x_cand, dtype=torch.float32)

    # Polish along exact linear-region vertex direction with fine line search
    for polish_step in range(15):
        x_var = x_t.detach().requires_grad_(True)
        y_out = model(x_var)
        margin = y_out[0, y_adv] - y_out[0, y_true]
        margin.backward()
        with torch.no_grad():
            grad = x_var.grad
            vertex = torch.where(grad >= 0, hi_in, lo_in)
            best_tau = 0.0
            best_m = float(margin)
            best_xt = x_t
            for tau in [1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3, 2e-3]:
                x_try = torch.max(torch.min(x_t + tau * (vertex - x_t), hi_in), lo_in)
                # Roundtrip through float32 string representation to ensure text stability
                x_try_np = np.array([float(f"{v:.9g}") for v in x_try.numpy().ravel()], dtype=np.float32).reshape(shape)
                if not np.all((x_try_np.ravel() > l_arr) & (x_try_np.ravel() < u_arr)):
                    continue
                ort_y = sess.run(None, {inp_name: x_try_np})[0][0]
                m_try = float(ort_y[y_adv] - ort_y[y_true])
                if m_try > best_m:
                    best_m = m_try
                    best_tau = tau
                    best_xt = torch.tensor(x_try_np, dtype=torch.float32)
            if best_tau == 0.0:
                break
            x_t = best_xt

    # Ensure exact round-trip representation through decimal strings formatted as %.9g
    x_raw_flat = x_t.numpy().ravel(order="C")
    x_strs = [f"{float(v):.9g}" for v in x_raw_flat]
    x_final_flat = np.array([float(s) for s in x_strs], dtype=np.float32)
    x_final = x_final_flat.reshape(shape, order="C")

    # Verify strict interior box constraints in float32
    strict_lo = bool(np.all(x_final_flat > l_arr))
    strict_hi = bool(np.all(x_final_flat < u_arr))
    min_lo_clearance = float(np.min(x_final_flat - l_arr))
    min_hi_clearance = float(np.min(u_arr - x_final_flat))
    min_box_width = float(np.min(u_arr - l_arr))
    print(f"Strict interior check: strict_lo={strict_lo}, strict_hi={strict_hi}")
    print(f"Min clearance from lb: {min_lo_clearance:.6e}, from ub: {min_hi_clearance:.6e} (min width={min_box_width:.6e})")
    assert strict_lo and strict_hi

    # 2. Multi-runtime evaluation:
    # (a) ONNX Runtime CPUExecutionProvider (float32)
    y_ort = sess.run(None, {inp_name: x_final})[0][0]
    margin_ort = float(y_ort[y_adv] - y_ort[y_true])

    # (b) ONNX ReferenceEvaluator (float32)
    onnx_proto = onnx.load(str(onnx_src))
    ref_eval = ReferenceEvaluator(onnx_proto)
    y_ref = ref_eval.run(None, {inp_name: x_final})[0][0]
    margin_ref = float(y_ref[y_adv] - y_ref[y_true])

    # (c) PyTorch float32 forward pass + exact linear-region Jacobian
    x_pt32 = torch.tensor(x_final, dtype=torch.float32, requires_grad=True)
    y_pt32_t, h18_32, min_pre32 = forward_with_relu_distances(model, x_pt32)
    y_pt32 = y_pt32_t.detach().numpy()[0]
    margin_pt32 = float(y_pt32[y_adv] - y_pt32[y_true])

    grad_179 = torch.autograd.grad(y_pt32_t[0, y_adv], x_pt32, retain_graph=True)[0].detach().numpy().ravel()
    grad_153 = torch.autograd.grad(y_pt32_t[0, y_true], x_pt32, retain_graph=True)[0].detach().numpy().ravel()

    # (d) PyTorch float64 (double precision) forward pass + exact linear-region Jacobian
    x_pt64 = torch.tensor(x_final.astype(np.float64), dtype=torch.float64, requires_grad=True)
    y_pt64_t, h18_64, min_pre64 = forward_with_relu_distances(model, x_pt64)
    y_pt64 = y_pt64_t.detach().numpy()[0]
    margin_pt64 = float(y_pt64[y_adv] - y_pt64[y_true])

    grad64_179 = torch.autograd.grad(y_pt64_t[0, y_adv], x_pt64, retain_graph=True)[0].detach().numpy().ravel()
    grad64_153 = torch.autograd.grad(y_pt64_t[0, y_true], x_pt64, retain_graph=True)[0].detach().numpy().ravel()
    eff_bias64_179 = float(y_pt64[y_adv] - np.dot(grad64_179, x_final_flat.astype(np.float64)))
    eff_bias64_153 = float(y_pt64[y_true] - np.dot(grad64_153, x_final_flat.astype(np.float64)))

    diff_ort_ref = float(np.max(np.abs(y_ort - y_ref)))
    diff_ort_pt32 = float(np.max(np.abs(y_ort - y_pt32)))
    diff_ort_pt64 = float(np.max(np.abs(y_ort.astype(np.float64) - y_pt64)))

    print(f"Runtime margins (Y[{y_adv}] - Y[{y_true}]):")
    print(f"  1. onnxruntime (CPU, float32):           {margin_ort:+.8f} (Y[{y_adv}]={y_ort[y_adv]:+.8f}, Y[{y_true}]={y_ort[y_true]:+.8f})")
    print(f"  2. onnx.reference.ReferenceEvaluator:    {margin_ref:+.8f} (max_diff vs ORT = {diff_ort_ref:.3e})")
    print(f"  3. PyTorch float32 independent forward:  {margin_pt32:+.8f} (max_diff vs ORT = {diff_ort_pt32:.3e})")
    print(f"  4. PyTorch float64 independent forward:  {margin_pt64:+.8f} (max_diff vs ORT = {diff_ort_pt64:.3e})")
    assert margin_ort >= 1e-6 and margin_ref >= 1e-6 and margin_pt32 >= 1e-6 and margin_pt64 >= 1e-6

    # 3. Write VNN-LIB 1.0 .counterexample file and VNN-LIB 2.0 assignment file
    y_strs = [f"{float(v):.9g}" for v in y_ort.ravel(order="C")]
    ce_v1_lines = ["((" + f"X_0 {x_strs[0]})"]
    for i in range(1, len(x_strs)):
        ce_v1_lines.append(f" (X_{i} {x_strs[i]})")
    for j in range(len(y_strs)):
        sfx = "))" if j == len(y_strs) - 1 else ")"
        ce_v1_lines.append(f" (Y_{j} {y_strs[j]}{sfx}")
    ce_v1_text = "\n".join(ce_v1_lines) + "\n"

    ce_v1_path = LENS2_DIR / "tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample"
    ce_v1_gz_path = LENS2_DIR / "tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample.gz"
    with open(ce_v1_path, "w", encoding="utf-8") as f:
        f.write(ce_v1_text)
    with gzip.open(ce_v1_gz_path, "wb") as f:
        f.write(ce_v1_text.encode("utf-8"))

    # VNN-LIB 2.0 textual assignment format
    ce_v2_lines = ["X float32 [1, 3, 64, 64]"] + x_strs + ["Y float32 [1, 200]"] + y_strs
    ce_v2_text = "\n".join(ce_v2_lines) + "\n"
    ce_v2_path = LENS2_DIR / "tinyimagenet_eps1_wide_cnn7_idx7687_sample8_v2.counterexample"
    with open(ce_v2_path, "w", encoding="utf-8") as f:
        f.write(ce_v2_text)

    # Save exact linear-region & penultimate-layer certificate (< 250 KB compressed)
    cert_npz_path = LENS2_DIR / "linear_region_certificate_idx7687_sample8.npz"
    w19 = model.inits["layers.19.weight"].numpy().astype(np.float32)
    b19 = model.inits["layers.19.bias"].numpy().astype(np.float32)
    np.savez_compressed(
        cert_npz_path,
        x_final=x_final,
        y_ort=y_ort.astype(np.float32),
        y_ref=y_ref.astype(np.float32),
        y_pt32=y_pt32.astype(np.float32),
        y_pt64=y_pt64.astype(np.float64),
        h18_32=h18_32.detach().numpy()[0].astype(np.float32),
        h18_64=h18_64.detach().numpy()[0].astype(np.float64),
        w19=w19,
        b19=b19,
        grad64_179=grad64_179.astype(np.float64),
        grad64_153=grad64_153.astype(np.float64),
        eff_bias64_179=np.array([eff_bias64_179], dtype=np.float64),
        eff_bias64_153=np.array([eff_bias64_153], dtype=np.float64),
        y_true=np.array([y_true], dtype=np.int32),
        y_adv=np.array([y_adv], dtype=np.int32),
    )

    # 4. Run unmodified official VNN-COMP 2026 validators (counterexamples.py, counterexamples_v2.py, cex_checks.py)
    # Prepare benchmark layout expected by Settings.BENCHMARK_REPOS["2026"] in the temporary benchmark root
    bench_root = Path(os.path.join(tempfile.gettempdir(), "vnncomp2026_bench_root/vnncomp2026_benchmarks")
    b_10 = bench_root / "benchmarks" / "challenging_certified_training_2026" / "1.0"
    b_20 = bench_root / "benchmarks" / "challenging_certified_training_2026" / "2.0"
    (b_10 / "onnx").mkdir(parents=True, exist_ok=True)
    (b_10 / "vnnlib" / "tinyimagenet_eps1_wide_cnn7").mkdir(parents=True, exist_ok=True)
    (b_20 / "onnx").mkdir(parents=True, exist_ok=True)
    (b_20 / "vnnlib" / "tinyimagenet_eps1_wide_cnn7").mkdir(parents=True, exist_ok=True)

    for dst_onnx in [b_10 / "onnx" / "tinyimagenet_eps1_wide_cnn7.onnx", b_20 / "onnx" / "tinyimagenet_eps1_wide_cnn7.onnx"]:
        if not dst_onnx.exists():
            os.symlink(onnx_src, dst_onnx)
    dst_v1 = b_10 / "vnnlib" / "tinyimagenet_eps1_wide_cnn7" / "tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib"
    if not dst_v1.exists():
        shutil.copy2(vnnlib1_src, dst_v1)
    dst_v2 = b_20 / "vnnlib" / "tinyimagenet_eps1_wide_cnn7" / "tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib"
    if not dst_v2.exists():
        shutil.copy2(vnnlib2_src, dst_v2)

    scoring_dir = Path(os.path.join(tempfile.gettempdir(), "vnncomp2026_bench_root/vnncomp2026_results/SCORING")
    scoring_dir.mkdir(parents=True, exist_ok=True)
    for fn in ["settings.py", "counterexamples.py", "counterexamples_v2.py", "cex_checks.py", "benchmark_instances.py", "vnnlib_v1.py"]:
        shutil.copy2(DATA_DIR / fn, scoring_dir / fn)

    sys.path.insert(0, str(scoring_dir))
    import settings as vnn_settings
    import counterexamples as ce_v1_mod
    import counterexamples_v2 as ce_v2_mod
    import cex_checks

    # Place a symlink with "2026" in the path so check_counterexample matches key "2026"
    ce_v1_2026_path = LENS2_DIR / "2026_tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample"
    shutil.copy2(ce_v1_path, ce_v1_2026_path)

    cat = "2026_challenging_certified_training_2026"
    net = "tinyimagenet_eps1_wide_cnn7"
    prop = "tinyimagenet_eps1_wide_cnn7_idx7687_sample8"
    onnx_rel = "onnx/tinyimagenet_eps1_wide_cnn7.onnx"
    vnnlib_rel = "vnnlib/tinyimagenet_eps1_wide_cnn7/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib"

    res_v1, msg_v1 = ce_v1_mod.check_counterexample(
        str(ce_v1_2026_path),
        cat,
        net,
        prop,
        benchmark_version="1.0",
        onnx_src=onnx_rel,
        vnnlib_src=vnnlib_rel,
    )
    print(f"Official VNN-LIB 1.0 check_counterexample result: {res_v1!r}")
    assert res_v1 == ce_v1_mod.CounterexampleResult.CORRECT

    # Also test get_ce_diff with strict 0.0 tolerances
    res_strict0, msg_strict0 = ce_v1_mod.get_ce_diff(
        str(onnx_src),
        str(vnnlib1_src),
        str(ce_v1_path),
        abs_tol=0.0,
        rel_tol=0.0,
    )
    print(f"Official get_ce_diff(abs_tol=0.0, rel_tol=0.0) result: {res_strict0!r}")
    assert res_strict0 == ce_v1_mod.CounterexampleResult.CORRECT

    # Write official .counterexample.check.json via cex_checks.get_or_create_check
    check_json_path = cex_checks.check_path_for(ce_v1_path)
    if check_json_path.exists():
        check_json_path.unlink()
    check_payload = cex_checks.get_or_create_check(
        ce_v1_path,
        cat=cat,
        net=onnx_rel,
        prop=vnnlib_rel,
        benchmark_version="1.0",
        row=[cat, onnx_rel, vnnlib_rel, "0.0", "sat", "0.0"],
        validator=lambda: (res_v1, msg_v1),
    )
    # Remove absolute witness_path from saved check.json so it is portable and leak-free
    check_data = json.loads(check_json_path.read_text(encoding="utf-8"))
    check_data["witness_path"] = "tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample"
    check_json_path.write_text(json.dumps(check_data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Also validate VNN-LIB 2.0 counterexample with abs_tol=0.0, rel_tol=0.0
    res_v2, msg_v2 = ce_v2_mod.validate_vnnlib2_counterexample(
        b_20,
        onnx_rel,
        vnnlib_rel,
        str(ce_v2_path),
        abs_tol=0.0,
        rel_tol=0.0,
        result_type=ce_v1_mod.CounterexampleResult,
        ignore_ce_outputs=True,
    )
    print(f"Official VNN-LIB 2.0 validate_vnnlib2_counterexample(atol=0.0, rtol=0.0) result: {res_v2!r} ({msg_v2})")
    assert res_v2 == ce_v1_mod.CounterexampleResult.CORRECT

    os.remove(ce_v1_2026_path)

    summary = {
        "category": cat,
        "network": onnx_rel,
        "property": vnnlib_rel,
        "onnx_sha256": sha256_file(onnx_src),
        "onnx_bytes": onnx_src.stat().st_size,
        "vnnlib1_sha256": sha256_file(vnnlib1_src),
        "vnnlib2_sha256": sha256_file(vnnlib2_src),
        "counterexample_v1_sha256": sha256_file(ce_v1_path),
        "counterexample_v1_bytes": ce_v1_path.stat().st_size,
        "counterexample_v1_gz_sha256": sha256_file(ce_v1_gz_path),
        "counterexample_v1_gz_bytes": ce_v1_gz_path.stat().st_size,
        "counterexample_v2_sha256": sha256_file(ce_v2_path),
        "counterexample_v2_bytes": ce_v2_path.stat().st_size,
        "certificate_npz_sha256": sha256_file(cert_npz_path),
        "certificate_npz_bytes": cert_npz_path.stat().st_size,
        "true_label": int(y_true),
        "adversarial_label": int(y_adv),
        "ort_y_adv": float(y_ort[y_adv]),
        "ort_y_true": float(y_ort[y_true]),
        "ort_margin": margin_ort,
        "ref_margin": margin_ref,
        "pt32_margin": margin_pt32,
        "pt64_margin": margin_pt64,
        "max_diff_ort_vs_ref": diff_ort_ref,
        "max_diff_ort_vs_pt32": diff_ort_pt32,
        "max_diff_ort_vs_pt64": diff_ort_pt64,
        "strict_interior_float32": bool(strict_lo and strict_hi),
        "min_lb_clearance_float32": min_lo_clearance,
        "min_ub_clearance_float32": min_hi_clearance,
        "official_v1_validator_result": res_v1,
        "official_v1_strict0_result": res_strict0,
        "official_v2_strict0_result": res_v2,
    }
    summary_path = LENS2_DIR / "certification_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("Saved certification_summary.json:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
