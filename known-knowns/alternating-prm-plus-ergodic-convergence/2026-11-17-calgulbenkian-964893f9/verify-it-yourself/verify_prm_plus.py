#!/usr/bin/env python3
"""Standalone 5-gate Lean 4 kernel & statement referee for alternating-prm-plus-ergodic-convergence (p2).

Prints PASS (exit 0) or FAIL (exit 1) as its final line, with zero host paths in stdout.
"""
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from decimal import Decimal, getcontext
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time

getcontext().prec = 80

FORBIDDEN_TOKENS = [
    "sorry",
    "admit",
    "axiom",
    "native_decide",
    "ofReduceBool",
    "implemented_by",
    "extern",
    "skipKernelTC",
    "DummyPositivity",
]

ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

REQUIRED_DEFS_SNIPPETS = [
    "def Simplex (d : ℕ) (x : Fin d → ℝ) : Prop :=",
    "def vecPosPart {d : ℕ} (v : Fin d → ℝ) : Fin d → ℝ :=",
    "noncomputable def normalize {d : ℕ} (z : Fin d → ℝ) : Fin d → ℝ :=",
    "if l1Norm z = 0 then fun _ => (1 : ℝ) / (d : ℝ)",
    "def negInstRegret {d : ℕ} (x ℓ : Fin d → ℝ) : Fin d → ℝ :=",
    "noncomputable def DualGap {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ)",
    "sSup { v : ℝ | ∃ y' : Fin d₂ → ℝ, Simplex d₂ y' ∧ v = bilinearPayoff A x y' } -",
    "sInf { v : ℝ | ∃ x' : Fin d₁ → ℝ, Simplex d₁ x' ∧ v = bilinearPayoff A x' y }",
    "noncomputable def initState (d₁ d₂ : ℕ) : RMState d₁ d₂ :=",
    "noncomputable def alg1Step {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ) (s : RMState d₁ d₂) :",
    "noncomputable def alg2Step {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ) (s : RMState d₁ d₂) :",
    "let Rx' := vecPosPart (fun i => s.Rx i - fx i)",
    "let Ry' := vecPosPart (fun j => s.Ry j + fy j)",
    "let px := vecPosPart (fun i => Rx' i - fx i)",
    "let py := vecPosPart (fun j => Ry' j + fy j)",
    "noncomputable def alg7Step {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ) (s : RMState d₁ d₂) :",
    "noncomputable def alg8Step {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ) (s : RMState d₁ d₂) :",
    "noncomputable def alg2Iter {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ) : ℕ → RMState d₁ d₂",
    "| 0, 0 =>  3 | 0, 1 => 0 | 0, 2 => -3",
    "| 1, 0 =>  0 | 1, 1 => 3 | 1, 2 => -4",
    "| 2, 0 =>  0 | 2, 1 => 0 | 2, 2 =>  1",
]

SKIP_WALK_DIRS = {
    "Library", "Pictures", "Music", "Movies", "Applications", "Downloads",
    "Documents", "Desktop", "Public", ".Trash", ".elan", ".cache", ".npm",
    ".cargo", ".rustup", "node_modules", ".lake", ".git",
}


def fail(msg: str) -> None:
    print("CHECK_ERROR: " + str(msg))
    print("FAIL")
    sys.exit(1)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strip_lean_comments(text: str) -> str:
    out = []
    i = 0
    n = len(text)
    depth = 0
    while i < n:
        if i + 1 < n and text[i] == "/" and text[i + 1] == "-":
            depth += 1
            i += 2
            continue
        if depth > 0 and i + 1 < n and text[i] == "-" and text[i + 1] == "/":
            depth -= 1
            i += 2
            continue
        if depth == 0:
            if i + 1 < n and text[i] == "-" and text[i + 1] == "-":
                while i < n and text[i] != "\n":
                    i += 1
                continue
            out.append(text[i])
        elif text[i] == "\n":
            out.append("\n")
        i += 1
    return "".join(out)


def is_apap_checkout(path: str) -> bool:
    return (
        bool(path)
        and os.path.isdir(path)
        and os.path.isfile(os.path.join(path, "APAP.lean"))
        and os.path.isfile(os.path.join(path, "lake-manifest.json"))
        and os.path.isfile(os.path.join(path, "lean-toolchain"))
    )


def locate_apap_root(pkg_root: str) -> str:
    env_root = os.environ.get("LEANAPAP_ROOT", "").strip()
    if is_apap_checkout(env_root):
        return os.path.abspath(env_root)

    seeds = [
        pkg_root,
        os.getcwd(),
        sys.executable,
        os.environ.get("VIRTUAL_ENV", ""),
        os.environ.get("XDG_CACHE_HOME", ""),
    ]
    for seed in seeds:
        if not seed:
            continue
        cur = os.path.abspath(seed)
        for _ in range(8):
            for sub in (
                ("fc-work", "LeanAPAP"),
                ("v3r1t4s-hunt", "fc-work", "LeanAPAP"),
                ("LeanAPAP",),
            ):
                cand = os.path.join(cur, *sub)
                if is_apap_checkout(cand):
                    return os.path.abspath(cand)
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent

    home = os.path.expanduser("~")
    if os.path.isdir(home):
        q = deque([(home, 0)])
        while q:
            cur, depth = q.popleft()
            if is_apap_checkout(cur):
                return os.path.abspath(cur)
            if depth >= 7:
                continue
            try:
                entries = sorted(os.scandir(cur), key=lambda e: e.name)
            except OSError:
                continue
            for entry in entries:
                if not entry.is_dir(follow_symlinks=False):
                    continue
                if entry.name in SKIP_WALK_DIRS:
                    continue
                q.append((entry.path, depth + 1))

    fail("Could not locate LeanAPAP Lake checkout (set LEANAPAP_ROOT if needed)")
    return ""


def parse_axioms(output: str, thm_full: str):
    m = re.search(rf"'{re.escape(thm_full)}' depends on axioms: \[([^\]]*)\]", output)
    if m:
        return [a.strip() for a in m.group(1).split(",") if a.strip()]
    if re.search(rf"'{re.escape(thm_full)}' does not depend on any axioms", output):
        return []
    fail("Could not parse #print axioms output for " + thm_full)
    return []


def main() -> None:
    viy_dir = os.path.dirname(os.path.abspath(__file__))
    pkg_root = os.path.dirname(viy_dir)
    obj_dir = os.path.join(pkg_root, "object")
    manifest_path = os.path.join(obj_dir, "proof_manifest.json")

    if not os.path.isfile(manifest_path):
        fail("Missing object/proof_manifest.json")

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as exc:
        fail("Malformed object/proof_manifest.json: " + type(exc).__name__)

    expected_b = 60 * (1 << 80)
    if manifest.get("target_id") != "alternating-prm-plus-ergodic-convergence":
        fail("Unexpected target_id in proof_manifest.json")
    if manifest.get("claimed_partial_win") != "p2":
        fail("Unexpected claimed_partial_win in proof_manifest.json")
    if manifest.get("B_nat_str") != str(expected_b):
        fail("B_nat_str mismatch in proof_manifest.json")
    if manifest.get("T0") != 13203 or manifest.get("k_slabs") != 256:
        fail("T0 or k_slabs mismatch in proof_manifest.json")
    if manifest.get("game_matrix") != [[3, 0, -3], [0, 3, -4], [0, 0, 1]]:
        fail("game_matrix mismatch in proof_manifest.json")
    if manifest.get("duality_gap_lower_bound") != "1/20":
        fail("duality_gap_lower_bound mismatch in proof_manifest.json")

    files_list = manifest.get("files", [])
    if not isinstance(files_list, list) or len(files_list) != 119 or manifest.get("file_count") != 119:
        fail("Expected exactly 119 Lean files in proof_manifest.json")

    actual_prm_files = sorted(
        "PRMPlus/" + fn
        for fn in os.listdir(os.path.join(obj_dir, "PRMPlus"))
        if not fn.startswith(".")
    )
    listed_paths = [e.get("path") for e in files_list]
    if actual_prm_files != listed_paths:
        fail("object/PRMPlus file list does not match proof_manifest.json")

    file_texts = {}
    sum_bytes = 0
    for entry in files_list:
        rel_p = entry["path"]
        full_p = os.path.join(obj_dir, *rel_p.split("/"))
        if not os.path.isfile(full_p):
            fail("Missing Lean source file " + rel_p)
        with open(full_p, "rb") as f:
            raw = f.read()
        if len(raw) != entry.get("bytes"):
            fail("Byte size mismatch on " + rel_p)
        h = sha256_bytes(raw)
        if h != entry.get("sha256"):
            fail("SHA-256 mismatch on " + rel_p)
        sum_bytes += len(raw)
        file_texts[rel_p] = raw.decode("utf-8")

    if sum_bytes != manifest.get("total_lean_bytes"):
        fail("total_lean_bytes mismatch in proof_manifest.json")

    bundle_concat = "".join(f"{e['path']}:{e['bytes']}:{e['sha256']}\n" for e in files_list).encode("utf-8")
    if sha256_bytes(bundle_concat) != manifest.get("bundle_sha256"):
        fail("bundle_sha256 mismatch in proof_manifest.json")
    if next(e["sha256"] for e in files_list if e["path"] == "PRMPlus/Defs.lean") != manifest.get("defs_sha256"):
        fail("defs_sha256 mismatch in proof_manifest.json")
    if next(e["sha256"] for e in files_list if e["path"] == "PRMPlus/TubeSound.lean") != manifest.get("tubesound_sha256"):
        fail("tubesound_sha256 mismatch in proof_manifest.json")
    if next(e["sha256"] for e in files_list if e["path"] == "PRMPlus/Main.lean") != manifest.get("main_sha256"):
        fail("main_sha256 mismatch in proof_manifest.json")

    print(
        f"[1/5] Manifest & 119-file object integrity verified: "
        f"bundle_sha256={manifest['bundle_sha256']} ({sum_bytes} bytes)"
    )

    token_re = re.compile(r"\b(" + "|".join(re.escape(t) for t in FORBIDDEN_TOKENS) + r")\b")
    for rel_p, txt in file_texts.items():
        stripped = strip_lean_comments(txt)
        m = token_re.search(stripped)
        if m:
            fail(f"Forbidden token '{m.group(1)}' found in {rel_p}")

    print("[2/5] Forbidden-token hygiene audit passed across all 119 Lean files (0 forbidden tokens)")

    defs_txt = file_texts["PRMPlus/Defs.lean"]
    for snip in REQUIRED_DEFS_SNIPPETS:
        if snip not in defs_txt:
            fail("Defs.lean missing required verbatim definition snippet: " + snip[:60])

    main_txt = file_texts["PRMPlus/Main.lean"]
    thm4_idx = main_txt.find("theorem alg2_caiGame_iter1000_bounds")
    if thm4_idx < 0:
        fail("Main.lean missing theorem alg2_caiGame_iter1000_bounds")
    thm4_block = main_txt[thm4_idx:]
    bound_pairs = re.findall(
        r"\(\(([0-9]+) : ℝ\) / \(B_nat : ℝ\) ≤ \(alg2Iter caiGameA 1000\)\.([xy]) ([012]) ∧ "
        r"\(alg2Iter caiGameA 1000\)\.[xy] [012] ≤ \(([0-9]+) : ℝ\) / \(B_nat : ℝ\)\)",
        thm4_block,
    )
    if len(bound_pairs) != 6:
        fail("Could not parse all 6 rational coordinate bounds from alg2_caiGame_iter1000_bounds")

    A_f = [[3.0, 0.0, -3.0], [0.0, 3.0, -4.0], [0.0, 0.0, 1.0]]
    rx, ry = [0.0] * 3, [0.0] * 3
    xf, yf = [1.0 / 3.0] * 3, [1.0 / 3.0] * 3
    for _ in range(1000):
        ay = [sum(A_f[i][j] * yf[j] for j in range(3)) for i in range(3)]
        xAy = sum(xf[i] * ay[i] for i in range(3))
        fx = [ay[i] - xAy for i in range(3)]
        atx = [sum(A_f[i][j] * xf[i] for i in range(3)) for j in range(3)]
        yATx = sum(yf[j] * atx[j] for j in range(3))
        fy = [atx[j] - yATx for j in range(3)]
        rx = [max(0.0, rx[i] - fx[i]) for i in range(3)]
        ry = [max(0.0, ry[j] + fy[j]) for j in range(3)]
        px = [max(0.0, rx[i] - fx[i]) for i in range(3)]
        py = [max(0.0, ry[j] + fy[j]) for j in range(3)]
        sx, sy = sum(px), sum(py)
        xf = [1.0 / 3.0] * 3 if sx == 0.0 else [v / sx for v in px]
        yf = [1.0 / 3.0] * 3 if sy == 0.0 else [v / sy for v in py]

    A_d = [[Decimal(3), Decimal(0), Decimal(-3)], [Decimal(0), Decimal(3), Decimal(-4)], [Decimal(0), Decimal(0), Decimal(1)]]
    rxd, ryd = [Decimal(0)] * 3, [Decimal(0)] * 3
    xd, yd = [Decimal(1) / Decimal(3)] * 3, [Decimal(1) / Decimal(3)] * 3
    for _ in range(1000):
        ay = [sum(A_d[i][j] * yd[j] for j in range(3)) for i in range(3)]
        xAy = sum(xd[i] * ay[i] for i in range(3))
        fx = [ay[i] - xAy for i in range(3)]
        atx = [sum(A_d[i][j] * xd[i] for i in range(3)) for j in range(3)]
        yATx = sum(yd[j] * atx[j] for j in range(3))
        fy = [atx[j] - yATx for j in range(3)]
        rxd = [max(Decimal(0), rxd[i] - fx[i]) for i in range(3)]
        ryd = [max(Decimal(0), ryd[j] + fy[j]) for j in range(3)]
        px = [max(Decimal(0), rxd[i] - fx[i]) for i in range(3)]
        py = [max(Decimal(0), ryd[j] + fy[j]) for j in range(3)]
        sx, sy = sum(px), sum(py)
        xd = [Decimal(1) / Decimal(3)] * 3 if sx == 0 else [v / sx for v in px]
        yd = [Decimal(1) / Decimal(3)] * 3 if sy == 0 else [v / sy for v in py]

    max_width = Decimal(0)
    max_f64_err = 0.0
    b_dec = Decimal(expected_b)
    for lo_s, xy_tag, idx_s, hi_s in bound_pairs:
        idx = int(idx_s)
        lo_v = Decimal(int(lo_s)) / b_dec
        hi_v = Decimal(int(hi_s)) / b_dec
        val_d = xd[idx] if xy_tag == "x" else yd[idx]
        val_f = xf[idx] if xy_tag == "x" else yf[idx]
        if not (lo_v <= val_d <= hi_v):
            fail(f"1,000-iteration Decimal {xy_tag}[{idx}] fell outside Lean Theorem 4 interval")
        max_width = max(max_width, hi_v - lo_v)
        max_f64_err = max(max_f64_err, abs(val_f - float(val_d)))
    if max_width > Decimal("1e-12") or max_f64_err > 1e-13:
        fail("1,000-iteration precision threshold exceeded")

    print(
        f"[3/5] Defs.lean paper-update diff & 1,000-iteration float64/Decimal cross-check passed "
        f"(interval_width={float(max_width):.3e}, float64_err={max_f64_err:.3e})"
    )

    apap_root = locate_apap_root(pkg_root)
    with open(os.path.join(apap_root, "lean-toolchain"), "r", encoding="utf-8") as f:
        tc = f.read().strip()
    if tc != manifest["lean_toolchain"]:
        fail("LeanAPAP toolchain mismatch: expected " + manifest["lean_toolchain"] + ", got " + tc)

    with open(os.path.join(apap_root, "lake-manifest.json"), "r", encoding="utf-8") as f:
        lake_man = json.load(f)
    pkg_revs = {p["name"]: p["rev"] for p in lake_man.get("packages", [])}
    if pkg_revs.get("mathlib") != manifest["mathlib_rev"]:
        fail("LeanAPAP mathlib revision mismatch")
    if pkg_revs.get("AddCombi") != manifest["addcombi_rev"]:
        fail("LeanAPAP AddCombi revision mismatch")

    env = os.environ.copy()
    elan_bin = os.path.join(os.path.expanduser("~"), ".elan", "bin")
    if os.path.isdir(elan_bin):
        env["PATH"] = elan_bin + os.pathsep + env.get("PATH", "")
    if not shutil.which("lake", path=env.get("PATH")):
        fail("lake binary not found in PATH")

    lean_bin = subprocess.check_output(
        ["lake", "env", "which", "lean"], cwd=apap_root, env=env, text=True, timeout=60
    ).strip()
    apap_lp = subprocess.check_output(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=apap_root, env=env, text=True, timeout=60
    ).strip()

    t_build0 = time.time()
    with tempfile.TemporaryDirectory() as td:
        work_prm = os.path.join(td, "PRMPlus")
        os.makedirs(work_prm, exist_ok=True)
        for rel_p, txt in file_texts.items():
            with open(os.path.join(td, *rel_p.split("/")), "w", encoding="utf-8") as f:
                f.write(txt)

        env_lean = env.copy()
        env_lean["LEAN_PATH"] = td + os.pathsep + apap_lp
        env_lean["LEAN_NUM_THREADS"] = "1"

        def build_one(mod_rel: str) -> None:
            src_f = os.path.join(td, mod_rel + ".lean")
            out_f = os.path.join(td, mod_rel + ".olean")
            p = subprocess.run(
                [lean_bin, "-R", td, "-Dwarn.sorry=true", "-o", out_f, src_f],
                env=env_lean,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=300,
            )
            if p.returncode != 0:
                raise RuntimeError(f"Lean kernel build failed on {mod_rel} (exit {p.returncode})")
            diag = (p.stdout + "\n" + p.stderr).strip()
            for ln in diag.splitlines():
                if ": warning:" in ln or ": error" in ln:
                    raise RuntimeError(f"Diagnostic emitted on {mod_rel}")

        for core_mod in (
            "PRMPlus/Defs",
            "PRMPlus/Aff12Sound",
            "PRMPlus/ReachSound",
            "PRMPlus/Aff15Arith",
            "PRMPlus/TubeSound",
            "PRMPlus/Params",
        ):
            try:
                build_one(core_mod)
            except Exception as exc:
                fail(str(exc))

        cert_jobs = [f"PRMPlus/Reach{i:02d}" for i in range(1, 49)] + [f"PRMPlus/Tube{i:02d}" for i in range(1, 65)]
        slot_lock = threading.Lock()
        seen_threads = {}

        def build_cert(mod_rel: str) -> None:
            tid = threading.get_ident()
            delay = 0.0
            with slot_lock:
                if tid not in seen_threads:
                    idx = len(seen_threads)
                    seen_threads[tid] = idx
                    delay = 4.0 * idx
            if delay > 0.0:
                time.sleep(delay)
            build_one(mod_rel)

        try:
            with ThreadPoolExecutor(max_workers=int(os.environ.get("PRM_LEAN_JOBS", "6"))) as pool:
                futs = [pool.submit(build_cert, m) for m in cert_jobs]
                for fut in as_completed(futs):
                    fut.result()
            build_one("PRMPlus/Main")
        except Exception as exc:
            fail(str(exc))

        build_elapsed = time.time() - t_build0
        print(
            f"[4/5] Clean-room Lean 4 kernel build of all 119 modules succeeded "
            f"(exit=0, warnings=0, {build_elapsed:.1f}s)"
        )

        audit_f = os.path.join(td, "VerifyAudit.lean")
        audit_lines = ["import PRMPlus.Main"]
        for thm in manifest["main_theorems"]:
            audit_lines.append("set_option pp.fullNames true in")
            audit_lines.append("set_option pp.universes true in")
            audit_lines.append("#check @" + thm["full_name"])
            audit_lines.append("#print axioms " + thm["full_name"])
        with open(audit_f, "w", encoding="utf-8") as f:
            f.write("\n".join(audit_lines) + "\n")

        p_aud = subprocess.run(
            [lean_bin, "-R", td, audit_f],
            env=env_lean,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if p_aud.returncode != 0 or p_aud.stderr.strip():
            fail("Kernel signature/axiom audit failed")

        aud_out = p_aud.stdout
        all_axs = {}
        for thm in manifest["main_theorems"]:
            fn = thm["full_name"]
            if "expected_check" in thm and thm["expected_check"] not in aud_out:
                fail("Kernel #check signature mismatch for " + fn)
            if "expected_check_prefix" in thm and thm["expected_check_prefix"] not in aud_out:
                fail("Kernel #check prefix mismatch for " + fn)
            axs = parse_axioms(aud_out, fn)
            illegal = [a for a in axs if a not in ALLOWED_AXIOMS]
            if illegal:
                fail(f"Disallowed axioms on {fn}: {illegal}")
            all_axs[fn] = axs

    print(
        "[5/5] Kernel signature & axiom audit passed on all 4 theorems: axioms="
        + str(all_axs["PRMPlus.alg2_caiGame_liminf_dualityGap_pos"])
    )
    print("PASS")


if __name__ == "__main__":
    main()
