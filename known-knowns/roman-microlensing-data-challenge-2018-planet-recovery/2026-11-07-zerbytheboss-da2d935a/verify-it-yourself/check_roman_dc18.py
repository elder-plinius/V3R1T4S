#!/usr/bin/env python3
import ast
import ctypes
import gzip
import json
import math
import os
import subprocess
import sys
sys.dont_write_bytecode = True
import tempfile


def fail(msg):
    print(f"Verification error: {msg}")
    print("FAIL")
    sys.exit(1)


def main():
    pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    py_solver = os.path.join(pkg_root, "how-we-built-it", "solve_roman_dc18.py")
    c_kernel = os.path.join(pkg_root, "how-we-built-it", "binary_lens_kernel.c")
    obj_tsv = os.path.join(pkg_root, "object", "roman_dc18_predictions.tsv")
    obj_json = os.path.join(pkg_root, "object", "roman_dc18_solver_outputs.json.gz")
    ref_json = os.path.join(pkg_root, "verify-it-yourself", "data", "roman_dc18_eval_ref.json.gz")

    for p in [py_solver, c_kernel, obj_tsv, obj_json, ref_json]:
        if not os.path.isfile(p):
            fail(f"Missing required file: {p}")

    # 1. Static AST & zero-leakage audit on solve_roman_dc18.py and binary_lens_kernel.c
    src_py = open(py_solver, "r", encoding="utf-8").read()
    src_c = open(c_kernel, "r", encoding="utf-8").read()
    try:
        ast.parse(src_py)
    except SyntaxError as e:
        fail(f"SyntaxError in solve_roman_dc18.py: {e}")

    for forbidden in ["master_file.txt", "MASTER_PATH", "roman_dc18_eval_ref", "entries/entry"]:
        if forbidden in src_py or forbidden in src_c:
            fail(f"Zero-leakage audit failed: forbidden reference {forbidden} found in solver")

    # 2. Live compilation & physics unit test of binary_lens_kernel.c + self-contained import smoke test of solve_roman_dc18.py
    with tempfile.TemporaryDirectory() as tmpd:
        so_path = os.path.join(tmpd, "libbl_test.so")
        cmd = ["cc", "-O3", "-shared", "-fPIC", c_kernel, "-o", so_path, "-lm"]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            fail(f"Failed to compile binary_lens_kernel.c: {res.stderr}")
        lib = ctypes.CDLL(so_path)
        lib.bl_magnification_fs.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.POINTER(ctypes.c_double),
        ]
        u1 = (ctypes.c_double * 1)(0.5)
        u2 = (ctypes.c_double * 1)(0.0)
        out_m = (ctypes.c_double * 1)(0.0)
        lib.bl_magnification_fs(1, u1, u2, 2.0, 1e-6, 0.001, 0.45, out_m)
        if abs(out_m[0] - 2.1828206) > 0.01:
            fail(f"Binary-lens kernel q->0 PSPL limit check failed: {out_m[0]}")

    sys.path.insert(0, os.path.join(pkg_root, "how-we-built-it"))
    import solve_roman_dc18
    a_fspl = float(solve_roman_dc18.fspl_mag_exact([0.5], 0.001)[0])
    if abs(a_fspl - 2.1828206) > 0.01:
        fail(f"solve_roman_dc18.fspl_mag_exact smoke test failed: {a_fspl}")

    # 3. Independently recompute all 293 rows and verify exact match with object/roman_dc18_predictions.tsv
    with gzip.open(obj_json, "rt", encoding="utf-8") as f:
        solver_data = json.load(f)["events"]
    with gzip.open(ref_json, "rt", encoding="utf-8") as f:
        ref_data = json.load(f)
    truth = ref_data["truth"]

    with open(obj_tsv, "r", encoding="utf-8") as f:
        actual_lines = [l.rstrip("\n") for l in f if l.strip()]

    expected_header = (
        "event_id\tpred_class\tpred_s\tpred_q\thost_t0\thost_u0\thost_tE\thost_Fs\t"
        "anom_t\tanom_snr\tregime\ttrue_class\ttrue_s\ttrue_q\tdlog10_s\tdlog10_q\tis_3class_ok\tis_lowq_ok"
    )
    if not actual_lines or actual_lines[0] != expected_header:
        fail("Header mismatch in object/roman_dc18_predictions.tsv")

    if len(actual_lines) - 1 != 293 or len(solver_data) != 293:
        fail(f"Expected 293 event rows, found {len(actual_lines)-1}")

    n_3class = 0
    n_cv_ok = 0
    n_pspl_ok = 0
    n_usbl_ok = 0
    n_false_lowq = 0
    false_lowq_evs = []
    lowq_rec = []
    p3_rec = []
    p4_rec = []

    for idx, item in enumerate(solver_data):
        ev = int(item["event_id"])
        if ev != idx + 1:
            fail(f"Event ordering mismatch at index {idx}: {ev}")
        tr = truth[str(ev)]
        t_cls = tr["true_class"]
        t_s = float(tr["true_s"])
        t_q = float(tr["true_q"])
        is_low_q = bool(tr["is_low_q"])

        pred_cls = item["pred_class"]
        pred_s = float(item["pred_s"])
        pred_q = float(item["pred_q_str"])

        is_3c = 1 if pred_cls == t_cls else 0
        n_3class += is_3c
        if t_cls == "CV" and is_3c:
            n_cv_ok += 1
        elif t_cls == "PSPL" and is_3c:
            n_pspl_ok += 1
        elif t_cls == "USBL" and is_3c:
            n_usbl_ok += 1

        if pred_cls == "USBL" and pred_q < 0.03 and not is_low_q:
            n_false_lowq += 1
            false_lowq_evs.append(ev)

        if t_cls == "USBL" and pred_cls == "USBL" and pred_s > 0.0 and pred_q > 0.0 and t_s > 0.0 and t_q > 0.0:
            ds = min(
                abs(math.log10(pred_s) - math.log10(t_s)),
                abs(math.log10(1.0 / pred_s) - math.log10(t_s)),
            )
            dlq = abs(math.log10(pred_q) - math.log10(t_q))
        else:
            ds = 9.999999
            dlq = 9.999999

        is_lq_ok = 1 if (is_low_q and is_3c == 1 and ds <= 0.10 and dlq <= 0.30) else 0
        if is_lq_ok:
            lowq_rec.append(ev)
            if math.log10(t_q) < -5.0:
                p3_rec.append(ev)
            if t_s > 2.0:
                p4_rec.append(ev)

        exp_row = (
            f"{ev}\t{pred_cls}\t{item['pred_s']:.6f}\t{item['pred_q_str']}\t"
            f"{item['host_t0']:.5f}\t{item['host_u0']:.6f}\t{item['host_tE']:.5f}\t{item['host_Fs']:.6f}\t"
            f"{item['anom_t']:.5f}\t{item['anom_snr']:.3f}\t{item['regime']}\t"
            f"{t_cls}\t{t_s:.6f}\t{t_q:.8e}\t{ds:.6f}\t{dlq:.6f}\t{is_3c}\t{is_lq_ok}"
        )
        act_row = actual_lines[idx + 1]
        if act_row != exp_row:
            fail(f"Row {idx+2} mismatch in object/roman_dc18_predictions.tsv:\n  actual:   {act_row}\n  expected: {exp_row}")

    if not (len(lowq_rec) > 41 and len(lowq_rec) == 46):
        fail(f"win/p1 low-q recovery check failed: {len(lowq_rec)}/51 (expected 46 > 41)")
    if not (n_false_lowq <= 9 and n_false_lowq == 5):
        fail(f"win/p1 false low-q check failed: {n_false_lowq} (expected 5 <= 9)")
    if not (n_3class > 268 and n_3class == 280):
        fail(f"win/p2 3-class accuracy check failed: {n_3class}/293 (expected 280 > 268)")
    if not (len(p3_rec) >= 2 and p3_rec == [47, 131, 152]):
        fail(f"p3 check failed: ultra-low-q recovered = {p3_rec} (expected [47, 131, 152])")
    if not (len(p4_rec) >= 8 and len(p4_rec) == 10):
        fail(f"p4 check failed: wide s>2 recovered = {len(p4_rec)}/10 (expected 10/10 >= 8/10)")

    print(
        f"Verified 293 Roman DC18 events (WIN + p1 + p2 + p3 + p4): low-q={len(lowq_rec)}/51 (90.20% > 41/51), "
        f"false_lowq={n_false_lowq} <= 9 {false_lowq_evs}, 3-class={n_3class}/293 (95.56% > 268/293; CV={n_cv_ok}/93, "
        f"PSPL={n_pspl_ok}/74, USBL={n_usbl_ok}/126), p3 (log10 q < -5)={len(p3_rec)}/3 {p3_rec}, p4 (s > 2)={len(p4_rec)}/10 {p4_rec}"
    )
    print("PASS")


if __name__ == "__main__":
    main()
