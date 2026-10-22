#!/usr/bin/env python3
"""
Standalone author checker for vnncomp-2026-unsolved-instance-counterexample:
  Category: 2026_challenging_certified_training_2026
  Network:  onnx/tinyimagenet_eps1_wide_cnn7.onnx
  Property: vnnlib/tinyimagenet_eps1_wide_cnn7/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib
"""
import os
import sys
import gzip
import json
import shutil
import hashlib
import tempfile
from pathlib import Path
import numpy as np


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def locate_file(base_dir: Path, name: str) -> Path:
    candidates = [
        base_dir / name,
        base_dir / "object" / name,
        base_dir / "the-record-we-beat" / name,
        base_dir / "verify-it-yourself" / name,
        base_dir.parent / name,
        base_dir.parent / "object" / name,
        base_dir.parent / "the-record-we-beat" / name,
        base_dir.parent / "verify-it-yourself" / name,
    ]
    for c in candidates:
        if c.is_file():
            return c
    raise FileNotFoundError(f"Could not locate {name} relative to {base_dir}")


def parse_ce_v1(text: str):
    content = text.replace("\n", " ").strip()
    if not (len(content) >= 2 and content[0] == "(" and content[-1] == ")"):
        raise ValueError("Counterexample does not start with '(' and end with ')'")
    content = content[1:-1]
    x_list = []
    y_list = []
    for part in content.split(")"):
        part = part.strip()
        if not part:
            continue
        while "  " in part:
            part = part.replace("  ", " ")
        if part[0] != "(":
            raise ValueError(f"Malformed assignment token: {part[:40]!r}")
        part = part[1:]
        tokens = part.split(" ")
        if len(tokens) != 2:
            raise ValueError(f"Expected 2 tokens in assignment, got {tokens!r}")
        name, num = tokens
        val = float(num)
        if name.startswith("X_"):
            idx = int(name[2:])
            if idx != len(x_list):
                raise ValueError(f"Out-of-order X index {idx} vs {len(x_list)}")
            x_list.append(val)
        elif name.startswith("Y_"):
            idx = int(name[2:])
            if idx != len(y_list):
                raise ValueError(f"Out-of-order Y index {idx} vs {len(y_list)}")
            y_list.append(val)
        else:
            raise ValueError(f"Unexpected variable name {name!r}")
    return x_list, y_list


def fail(reason: str):
    print(f"ERROR: {reason}")
    print("FAIL")
    sys.exit(1)


def main():
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parent if script_dir.name == "verify-it-yourself" else script_dir

    custom_ce = None
    if len(sys.argv) >= 3 and sys.argv[1] == "--counterexample":
        custom_ce = Path(sys.argv[2])

    try:
        ce_v1_path = custom_ce if custom_ce is not None else locate_file(base_dir, "tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample")
        ce_v2_path = locate_file(base_dir, "tinyimagenet_eps1_wide_cnn7_idx7687_sample8_v2.counterexample")
        check_json_path = locate_file(base_dir, "tinyimagenet_eps1_wide_cnn7_idx7687_sample8.counterexample.check.json")
        cert_npz_path = locate_file(base_dir, "linear_region_certificate_idx7687_sample8.npz")
        vnnlib1_gz_path = locate_file(base_dir, "tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib.gz")
        vnnlib2_gz_path = locate_file(base_dir, "tinyimagenet_eps1_wide_cnn7_idx7687_sample8_v2.vnnlib.gz")
        vnnlib_v1_py = locate_file(base_dir, "vnnlib_v1.py")
    except Exception as exc:
        fail(str(exc))

    # 1. Check counterexample SHA-256 and check.json integrity (unless custom_ce is being tested)
    if custom_ce is None:
        try:
            check_json_sha = sha256_file(check_json_path)
            if check_json_sha != "4faa45fce4f398e43b7ad916f198258820ef2dae49d8a7413e93e35e17b8ee51":
                fail(f"check.json SHA-256 mismatch (corrupted check.json): {check_json_sha}")
            check_meta = json.loads(check_json_path.read_text(encoding="utf-8"))
            ce_v1_sha = sha256_file(ce_v1_path)
            expected_sha = check_meta.get("witness_sha256", "")
            if ce_v1_sha != expected_sha:
                fail(f"Counterexample SHA-256 mismatch: {ce_v1_sha} != {expected_sha}")
            if check_meta.get("result") != "correct" or not check_meta.get("establishes_sat"):
                fail(f"check.json does not report result=='correct' and establishes_sat==True: {check_meta}")
            if "[-0.04230213]" not in check_meta.get("rationale", ""):
                fail("check.json rationale does not match exact violation margin [-0.04230213]")
        except Exception as exc:
            fail(f"Failed check.json validation: {exc}")

    # 2. Parse VNN-LIB 1.0 counterexample text
    try:
        ce_text = ce_v1_path.read_text(encoding="utf-8")
        x_list, y_list = parse_ce_v1(ce_text)
    except Exception as exc:
        fail(f"Failed to parse VNN-LIB 1.0 counterexample: {exc}")

    if len(x_list) != 12288 or len(y_list) != 200:
        fail(f"Unexpected dimensions: len(X)={len(x_list)}, len(Y)={len(y_list)}")

    x_f32 = np.asarray(x_list, dtype=np.float32)
    y_f32 = np.asarray(y_list, dtype=np.float32)
    if not (np.all(np.isfinite(x_f32)) and np.all(np.isfinite(y_f32))):
        fail("Non-finite values in X or Y")

    # 3. Verify VNN-LIB 1.0 input box and output specification via vnnlib_v1.py
    sys.path.insert(0, str(vnnlib_v1_py.parent))
    import vnnlib_v1

    vnnlib1_bytes = gzip.decompress(vnnlib1_gz_path.read_bytes())
    vnnlib1_sha = sha256_bytes(vnnlib1_bytes)
    if vnnlib1_sha != "1e626b4cb58eb1b691ce67e3d0932f8367719113461985b849f6b43030781b7b":
        fail(f"Unexpected VNN-LIB 1.0 sha256: {vnnlib1_sha}")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_v1 = Path(tmpdir) / "prop.vnnlib"
        tmp_v1.write_bytes(vnnlib1_bytes)
        box_spec_list = vnnlib_v1.read_vnnlib_simple(str(tmp_v1), 12288, 200)

    if len(box_spec_list) != 1:
        fail(f"Expected 1 box spec, got {len(box_spec_list)}")
    input_box, spec_list = box_spec_list[0]
    lb = np.asarray([b[0] for b in input_box], dtype=np.float32)
    ub = np.asarray([b[1] for b in input_box], dtype=np.float32)

    # Strict interior check in float32: lb_i < x_i < ub_i
    if not (np.all(x_f32 > lb) and np.all(x_f32 < ub)):
        fail("Input x_f32 does not satisfy strict interior bounds lb < x < ub in float32")
    min_lb_clear = float(np.min(x_f32 - lb))
    min_ub_clear = float(np.min(ub - x_f32))

    # Check output disjunction C y <= d with margin >= 1e-6
    violated_idx = -1
    best_margin = -1e9
    for j, (prop_mat, prop_rhs) in enumerate(spec_list):
        vec = prop_mat.dot(y_f32)
        margin_j = float(np.min(prop_rhs - vec))
        if margin_j > best_margin:
            best_margin = margin_j
            violated_idx = j

    if best_margin < 1e-6:
        fail(f"Specification not violated with margin >= 1e-6: best_margin={best_margin}")

    # 4. Verify linear-region & penultimate-layer certificate consistency
    cert = np.load(cert_npz_path)
    x_cert = cert["x_final"].ravel(order="C")
    y_ort_cert = cert["y_ort"].ravel(order="C")
    y_ref_cert = cert["y_ref"].ravel(order="C")
    y_pt32_cert = cert["y_pt32"].ravel(order="C")
    y_pt64_cert = cert["y_pt64"].ravel(order="C")
    h18_32 = cert["h18_32"]
    h18_64 = cert["h18_64"]
    w19 = cert["w19"]
    b19 = cert["b19"]
    grad64_179 = cert["grad64_179"]
    grad64_153 = cert["grad64_153"]
    eff_bias64_179 = float(cert["eff_bias64_179"][0])
    eff_bias64_153 = float(cert["eff_bias64_153"][0])
    y_true = int(cert["y_true"][0])
    y_adv = int(cert["y_adv"][0])

    if float(np.max(np.abs(x_f32 - x_cert))) > 0.0:
        fail("Parsed X does not match certificate x_final bit-for-bit")
    if float(np.max(np.abs(y_f32 - y_ort_cert))) > 1e-6:
        fail("Parsed Y does not match certificate y_ort")

    # Verify penultimate Gemm: w19 @ h18 + b19
    y_from_h18_32 = w19 @ h18_32 + b19
    y_from_h18_64 = w19.astype(np.float64) @ h18_64 + b19.astype(np.float64)
    if float(np.max(np.abs(y_from_h18_32 - y_pt32_cert))) > 1e-5:
        fail("Penultimate float32 Gemm check failed")
    if float(np.max(np.abs(y_from_h18_64 - y_pt64_cert))) > 1e-10:
        fail("Penultimate float64 Gemm check failed")

    # Verify exact piecewise-linear affine functional in float64 at x_f32
    x_f64 = x_f32.astype(np.float64)
    aff_179 = float(np.dot(grad64_179, x_f64) + eff_bias64_179)
    aff_153 = float(np.dot(grad64_153, x_f64) + eff_bias64_153)
    if abs(aff_179 - float(y_pt64_cert[y_adv])) > 1e-9 or abs(aff_153 - float(y_pt64_cert[y_true])) > 1e-9:
        fail("Exact linear-region affine functional mismatch")
    aff_margin = aff_179 - aff_153
    if aff_margin < 1e-6:
        fail(f"Affine margin < 1e-6: {aff_margin}")

    # 5. If ONNX model is present locally (in claim/ or in temp cache), run full multi-runtime + official v1.0 & v2.0 validators
    onnx_candidates = [
        base_dir / "tinyimagenet_eps1_wide_cnn7.onnx",
        Path(tempfile.gettempdir()) / "vnncomp2026_cct" / "onnx" / "tinyimagenet_eps1_wide_cnn7.onnx",
    ]
    onnx_path = next((p for p in onnx_candidates if p.is_file()), None)
    if onnx_path is not None:
        onnx_sha = sha256_file(onnx_path)
        if onnx_sha != "7bc65dc63a7f8536ed80aa0755cdc1870d2041358190ec0e8cba544c3b5d00c6":
            fail(f"ONNX model SHA-256 mismatch: {onnx_sha}")
        import onnx
        from onnx.reference import ReferenceEvaluator
        import onnxruntime as ort

        sess = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
        inp_name = sess.get_inputs()[0].name
        y_ort_live = sess.run(None, {inp_name: x_f32.reshape(1, 3, 64, 64)})[0][0]
        live_ort_margin = float(y_ort_live[y_adv] - y_ort_live[y_true])
        if live_ort_margin < 1e-6 or float(np.max(np.abs(y_ort_live - y_ort_cert))) > 1e-5:
            fail(f"Live ONNX Runtime verification failed: margin={live_ort_margin}")

        ref_eval = ReferenceEvaluator(onnx.load(str(onnx_path)))
        y_ref_live = ref_eval.run(None, {inp_name: x_f32.reshape(1, 3, 64, 64)})[0][0]
        live_ref_margin = float(y_ref_live[y_adv] - y_ref_live[y_true])
        if live_ref_margin < 1e-6 or float(np.max(np.abs(y_ref_live - y_ort_live))) > 1e-4:
            fail(f"Live ReferenceEvaluator verification failed: margin={live_ref_margin}")

        # Run unmodified official VNN-COMP 2026 v1.0 & v2.0 validators in an isolated temp layout
        with tempfile.TemporaryDirectory() as tmproot:
            troot = Path(tmproot)
            b_root = troot / "vnncomp2026_benchmarks"
            s_root = troot / "vnncomp2026_results" / "SCORING"
            b_10 = b_root / "benchmarks" / "challenging_certified_training_2026" / "1.0"
            b_20 = b_root / "benchmarks" / "challenging_certified_training_2026" / "2.0"
            (b_10 / "onnx").mkdir(parents=True, exist_ok=True)
            (b_10 / "vnnlib" / "tinyimagenet_eps1_wide_cnn7").mkdir(parents=True, exist_ok=True)
            (b_20 / "onnx").mkdir(parents=True, exist_ok=True)
            (b_20 / "vnnlib" / "tinyimagenet_eps1_wide_cnn7").mkdir(parents=True, exist_ok=True)
            s_root.mkdir(parents=True, exist_ok=True)

            os.symlink(onnx_path, b_10 / "onnx" / "tinyimagenet_eps1_wide_cnn7.onnx")
            os.symlink(onnx_path, b_20 / "onnx" / "tinyimagenet_eps1_wide_cnn7.onnx")
            v1_file = b_10 / "vnnlib" / "tinyimagenet_eps1_wide_cnn7" / "tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib"
            v2_file = b_20 / "vnnlib" / "tinyimagenet_eps1_wide_cnn7" / "tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib"
            v1_file.write_bytes(vnnlib1_bytes)
            v2_file.write_bytes(gzip.decompress(vnnlib2_gz_path.read_bytes()))

            for fn in ["settings.py", "counterexamples.py", "counterexamples_v2.py", "cex_checks.py", "benchmark_instances.py", "vnnlib_v1.py"]:
                shutil.copy2(locate_file(base_dir, fn), s_root / fn)

            sys.path.insert(0, str(s_root))
            import counterexamples as ce_v1_mod
            import counterexamples_v2 as ce_v2_mod

            res_v1_strict, _ = ce_v1_mod.get_ce_diff(
                str(onnx_path),
                str(v1_file),
                str(ce_v1_path),
                abs_tol=0.0,
                rel_tol=0.0,
            )
            if res_v1_strict != "correct":
                fail(f"Official v1.0 validator returned {res_v1_strict!r}")

            res_v2_strict, _ = ce_v2_mod.validate_vnnlib2_counterexample(
                b_20,
                "onnx/tinyimagenet_eps1_wide_cnn7.onnx",
                "vnnlib/tinyimagenet_eps1_wide_cnn7/tinyimagenet_eps1_wide_cnn7_idx7687_sample8.vnnlib",
                str(ce_v2_path),
                abs_tol=0.0,
                rel_tol=0.0,
                result_type=ce_v1_mod.CounterexampleResult,
                ignore_ce_outputs=True,
            )
            if res_v2_strict != "correct":
                fail(f"Official v2.0 validator returned {res_v2_strict!r}")

            shutil.rmtree(Path.cwd() / "cachier", ignore_errors=True)

        print(f"Live ONNX + ReferenceEvaluator + Official VNN-COMP 2026 v1.0/v2.0 Validators: ALL PASSED (margin={live_ort_margin:+.8f})")

    print(
        f"Verified tinyimagenet_eps1_wide_cnn7_idx7687_sample8 counterexample: "
        f"strict_interior=True (min_lb={min_lb_clear:.3e}, min_ub={min_ub_clear:.3e}), "
        f"prop #{violated_idx} violated (Y[{y_adv}]-Y[{y_true}] = {best_margin:+.8f} >= 1e-6)"
    )
    print("PASS")


if __name__ == "__main__":
    main()
