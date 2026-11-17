#!/usr/bin/env python3
"""Standalone 5-gate Lean 4 kernel & statement referee for brownian-motion-project-sorries.

Target declaration: ProbabilityTheory.IsBrownianReal.reflection
Upstream file: BrownianMotion/Gaussian/IteratedLogarithm.lean (commit 8fd8dc52830cdd07cf9cc8eadd533e284425fa6f)

Prints PASS (exit 0) or FAIL (exit 1) as its final line, with zero host paths in stdout.
"""
from collections import deque
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

FORBIDDEN_TOKENS = [
    "sorry",
    "admit",
    "axiom",
    "native_decide",
    "ofReduceBool",
    "implemented_by",
    "extern",
    "skipKernelTC",
]

ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

EXPECTED_PUBLIC_IMPORTS = ["BrownianMotion.Gaussian.BrownianMotion"]
EXPECTED_PRIVATE_IMPORTS = [
    "Mathlib.Analysis.Calculus.LHopital",
    "Mathlib.Analysis.PSeries",
    "Mathlib.Probability.BorelCantelli",
]

EXPECTED_FULL_CHECK = (
    "@ProbabilityTheory.IsBrownianReal.reflection.{u_1} : ∀ {Ω : Type u_1} {mΩ : MeasurableSpace.{u_1} Ω}\n"
    "  {P : MeasureTheory.Measure.{u_1} Ω} {X : NNReal → Ω → ℝ},\n"
    "  ProbabilityTheory.IsBrownianReal.{u_1} X P →\n"
    "    ∀ {t : NNReal} {c : ℝ},\n"
    "      LT.lt.{0} 0 t →\n"
    "        LE.le.{0} 0 c →\n"
    "          Eq.{1}\n"
    "            (MeasureTheory.Measure.real.{u_1} P\n"
    "              (Set.ofPred.{u_1} fun ω ↦ LE.le.{0} (↑c) (⨆ s, ⨆ (_ : LE.le.{0} s t), ↑(X s ω))))\n"
    "            (HMul.hMul.{0, 0, 0} 2 (MeasureTheory.Measure.real.{u_1} P (Set.ofPred.{u_1} fun ω ↦ LE.le.{0} c (X t ω))))"
)

TAIL_MARKER = "\nlemma IsStandardGaussian.tail (hX : HasLaw X (gaussianReal 0 1) P) :"

EXPECTED_DECL_BLOCK = (
    "variable {Ω : Type*} {mΩ : MeasurableSpace Ω} {P : Measure Ω}\n"
    "variable {X}\n\n"
    "lemma IsBrownianReal.reflection (hX : IsBrownianReal X P) {t : ℝ≥0} {c : ℝ}\n"
    "    (ht : 0 < t) (hc : 0 ≤ c) :\n"
    "    P.real {ω | c ≤ ⨆ s ≤ t, (X s ω).toEReal} = 2 * P.real {ω | c ≤ X t ω} :="
)

SKIP_WALK_DIRS = {
    "Library",
    "Pictures",
    "Music",
    "Movies",
    "Applications",
    "Downloads",
    "Documents",
    "Desktop",
    "Public",
    ".Trash",
    ".elan",
    ".cache",
    ".npm",
    ".cargo",
    ".rustup",
    "node_modules",
    ".lake",
    ".git",
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


def is_bm_checkout(path: str) -> bool:
    return (
        bool(path)
        and os.path.isdir(path)
        and os.path.isfile(os.path.join(path, "BrownianMotion.lean"))
        and os.path.isfile(os.path.join(path, "BrownianMotion", "Gaussian", "IteratedLogarithm.lean"))
        and os.path.isfile(os.path.join(path, "lake-manifest.json"))
        and os.path.isfile(os.path.join(path, "lean-toolchain"))
    )


def locate_bm_root(pkg_root: str) -> str:
    env_root = os.environ.get("BROWNIAN_MOTION_ROOT", "").strip()
    if is_bm_checkout(env_root):
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
                ("fc-work", "brownian-motion"),
                ("v3r1t4s-hunt", "fc-work", "brownian-motion"),
                ("brownian-motion",),
            ):
                cand = os.path.join(cur, *sub)
                if is_bm_checkout(cand):
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
            if is_bm_checkout(cur):
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

    fail("Could not locate brownian-motion Lake checkout (set BROWNIAN_MOTION_ROOT if needed)")
    return ""


def walk_rel_files(root: str):
    out = []
    for dp, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".git"))
        for fn in sorted(files):
            full = os.path.join(dp, fn)
            out.append(os.path.relpath(full, root).replace(os.sep, "/"))
    return sorted(out)


def parse_axioms(output: str, thm_full: str):
    ax_match = re.search(r"'" + re.escape(thm_full) + r"' depends on axioms: \[([^\]]*)\]", output)
    no_ax_match = re.search(r"'" + re.escape(thm_full) + r"' does not depend on any axioms", output)
    if ax_match:
        return [a.strip() for a in ax_match.group(1).split(",") if a.strip()]
    if no_ax_match:
        return []
    fail("Could not parse #print axioms output for " + thm_full)
    return []


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    pkg_root = os.path.dirname(here)
    obj_root = os.path.join(pkg_root, "object")
    manifest_path = os.path.join(here, "proof_manifest.json")

    if not os.path.isfile(manifest_path):
        fail("Missing verify-it-yourself/proof_manifest.json")
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as exc:
        fail("Invalid JSON in proof_manifest.json: " + str(exc))

    req_keys = [
        "target_id",
        "solution_file",
        "solution_sha256",
        "solution_bytes",
        "theorem_full_name",
        "theorem_short_name",
        "namespace",
        "upstream_commit",
        "upstream_relpath",
        "upstream_sha256",
        "lean_toolchain",
        "mathlib_rev",
        "checkdecls_rev",
        "subverso_rev",
        "expected_check_prefix",
        "allowed_axioms",
    ]
    for k in req_keys:
        if k not in manifest:
            fail("Missing key " + k + " in proof_manifest.json")

    if manifest["target_id"] != "brownian-motion-project-sorries":
        fail("Unexpected target_id in proof_manifest.json")
    if manifest["solution_file"] != "IteratedLogarithm.lean":
        fail("Unexpected solution_file in proof_manifest.json")
    if set(manifest["allowed_axioms"]) != ALLOWED_AXIOMS or len(manifest["allowed_axioms"]) != 3:
        fail("Tampered allowed_axioms in proof_manifest.json")

    if not os.path.isdir(obj_root):
        fail("Missing object/ directory")
    obj_files = walk_rel_files(obj_root)
    if obj_files != ["IteratedLogarithm.lean"]:
        fail("object/ must contain exclusively IteratedLogarithm.lean, found: " + str(obj_files))

    sol_path = os.path.join(obj_root, "IteratedLogarithm.lean")
    with open(sol_path, "rb") as f:
        sol_bytes = f.read()
    try:
        sol_text = sol_bytes.decode("utf-8")
    except UnicodeDecodeError:
        fail("object/IteratedLogarithm.lean is not valid UTF-8")

    bm_root = locate_bm_root(pkg_root)

    with open(os.path.join(bm_root, "lean-toolchain"), "r", encoding="utf-8") as f:
        tc = f.read().strip()
    if tc != manifest["lean_toolchain"]:
        fail("lean-toolchain mismatch: expected " + manifest["lean_toolchain"] + ", got " + tc)

    with open(os.path.join(bm_root, "lake-manifest.json"), "r", encoding="utf-8") as f:
        lm = json.load(f)
    pkgs = {p["name"]: p["rev"] for p in lm.get("packages", [])}
    if pkgs.get("mathlib") != manifest["mathlib_rev"]:
        fail("mathlib revision mismatch in lake-manifest.json")
    if pkgs.get("checkdecls") != manifest["checkdecls_rev"]:
        fail("checkdecls revision mismatch in lake-manifest.json")
    if pkgs.get("subverso") != manifest["subverso_rev"]:
        fail("subverso revision mismatch in lake-manifest.json")

    head_proc = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=bm_root, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30
    )
    if head_proc.returncode != 0 or head_proc.stdout.strip() != manifest["upstream_commit"]:
        fail("brownian-motion git HEAD does not match pinned upstream_commit")

    status_pre = subprocess.run(
        ["git", "status", "--porcelain"], cwd=bm_root, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30
    )
    if status_pre.returncode != 0 or status_pre.stdout.strip():
        fail("brownian-motion checkout is dirty prior to verification")

    up_file = os.path.join(bm_root, *manifest["upstream_relpath"].split("/"))
    with open(up_file, "rb") as f:
        up_bytes = f.read()
    if sha256_bytes(up_bytes) != manifest["upstream_sha256"]:
        fail("Upstream BrownianMotion/Gaussian/IteratedLogarithm.lean SHA-256 mismatch")

    local_snap = os.path.join(pkg_root, "data", "IteratedLogarithm.lean")
    if os.path.isfile(local_snap):
        with open(local_snap, "rb") as f:
            if sha256_bytes(f.read()) != manifest["upstream_sha256"]:
                fail("data/IteratedLogarithm.lean SHA-256 mismatch against upstream")

    up_text = up_bytes.decode("utf-8")
    print("[1/5] Pinned checkout & manifest schema verified (commit=" + manifest["upstream_commit"][:12] + ", toolchain=" + tc + ")")

    if TAIL_MARKER not in up_text or TAIL_MARKER not in sol_text:
        fail("Missing IsStandardGaussian.tail boundary marker")

    up_prefix, up_suffix = up_text.split(TAIL_MARKER, 1)
    sol_prefix, sol_suffix = sol_text.split(TAIL_MARKER, 1)

    if sol_suffix != up_suffix:
        fail("Suffix from lemma IsStandardGaussian.tail through end ProbabilityTheory was modified")

    ns_marker = "namespace ProbabilityTheory\n"
    if ns_marker not in up_prefix:
        fail("Unexpected upstream header layout")
    up_header = up_prefix[: up_prefix.index(ns_marker) + len(ns_marker)]
    if not sol_prefix.startswith(up_header):
        fail("Module header / imports / docstring / namespace ProbabilityTheory modified from upstream")

    if EXPECTED_DECL_BLOCK not in sol_prefix:
        fail("IsBrownianReal.reflection variable context or declaration header modified from upstream")
    if EXPECTED_DECL_BLOCK not in up_prefix:
        fail("Internal check error: EXPECTED_DECL_BLOCK missing in upstream")

    stripped_prefix = strip_lean_comments(sol_prefix)
    for tok in FORBIDDEN_TOKENS:
        if re.search(r"\b" + re.escape(tok) + r"\b", sol_prefix) or re.search(r"\b" + re.escape(tok) + r"\b", stripped_prefix):
            fail("Forbidden token '" + tok + "' present in IsBrownianReal.reflection proof prefix")

    pub_imports = re.findall(r"(?m)^\s*public\s+import\s+(\S+)", stripped_prefix)
    if pub_imports != EXPECTED_PUBLIC_IMPORTS:
        fail("Public imports modified: " + str(pub_imports))
    priv_imports = re.findall(r"(?m)^\s*import\s+(\S+)", stripped_prefix)
    if priv_imports != EXPECTED_PRIVATE_IMPORTS:
        fail("Private imports modified: " + str(priv_imports))

    print("[2/5] Forbidden-token & verbatim statement/header/suffix diff audit passed")

    env = os.environ.copy()
    elan_bin = os.path.join(os.path.expanduser("~"), ".elan", "bin")
    if os.path.isdir(elan_bin):
        env["PATH"] = elan_bin + os.pathsep + env.get("PATH", "")
    env["LEAN_NUM_THREADS"] = "2"

    if not shutil.which("lake", path=env.get("PATH")):
        fail("lake binary not found in PATH")

    thm_full = manifest["theorem_full_name"]

    with tempfile.TemporaryDirectory() as td:
        prefix_check = os.path.join(td, "VerifyReflectionPrefix.lean")
        standalone_prefix = re.sub(r"(?m)^module\s*$", "", sol_prefix, count=1)
        standalone_prefix = re.sub(r"(?m)^public\s+import\s+", "import ", standalone_prefix)
        standalone_prefix = standalone_prefix.replace("@[expose] public section", "")
        with open(prefix_check, "w", encoding="utf-8") as f:
            f.write(standalone_prefix)
            f.write(
                "\nend ProbabilityTheory\n\n"
                "set_option pp.fullNames true in\n"
                "set_option pp.universes true in\n"
                "#check @" + thm_full + "\n"
                "#print axioms " + thm_full + "\n"
            )

        cmd_prefix = [
            "lake",
            "env",
            "lean",
            "-Dpp.unicode.fun=true",
            "-DautoImplicit=false",
            "-DrelaxedAutoImplicit=false",
            "-Dweak.linter.flexible=true",
            "-Dweak.linter.mathlibStandardSet=true",
            "-Dlinter.style.header=false",
            "-Dwarn.sorry=true",
            prefix_check,
        ]
        proc_p = subprocess.run(cmd_prefix, cwd=bm_root, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600)

    if proc_p.returncode != 0:
        fail("Lean 4 kernel/linter compilation of IsBrownianReal.reflection failed (exit " + str(proc_p.returncode) + ")")
    if proc_p.stderr.strip():
        fail("Lean emitted unexpected stderr during zero-warning prefix check")
    for ln in proc_p.stdout.splitlines():
        if ": warning:" in ln or ": error" in ln:
            fail("Lean linter/compiler diagnostic emitted during zero-warning prefix check")

    if manifest["expected_check_prefix"] not in proc_p.stdout:
        fail("Prefix kernel #check signature did not match exact canonical upstream type")
    axioms_p = parse_axioms(proc_p.stdout, thm_full)
    if any(a not in ALLOWED_AXIOMS for a in axioms_p):
        fail("Disallowed axioms in prefix check: " + str(axioms_p))

    artifact_patterns = [
        os.path.join(bm_root, ".lake", "build", "lib", "lean", "BrownianMotion", "Gaussian", "IteratedLogarithm.*"),
        os.path.join(bm_root, ".lake", "build", "ir", "BrownianMotion", "Gaussian", "IteratedLogarithm.*"),
    ]
    with tempfile.TemporaryDirectory() as backup_dir:
        saved_artifacts = []
        for pat in artifact_patterns:
            for p in sorted(glob.glob(pat)):
                if os.path.isfile(p):
                    bname = os.path.relpath(p, bm_root).replace(os.sep, "__")
                    bpath = os.path.join(backup_dir, bname)
                    shutil.copy2(p, bpath)
                    saved_artifacts.append((p, bpath))

        try:
            for orig_p, _ in saved_artifacts:
                if os.path.exists(orig_p):
                    os.remove(orig_p)
            with open(up_file, "wb") as f:
                f.write(sol_bytes)

            proc_build = subprocess.run(
                ["lake", "build"], cwd=bm_root, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=900
            )
            if proc_build.returncode != 0:
                fail("Full lake build failed with exit code " + str(proc_build.returncode))

            mod_check = os.path.join(backup_dir, "VerifyCompiledModule.lean")
            with open(mod_check, "w", encoding="utf-8") as f:
                f.write(
                    "import BrownianMotion.Gaussian.IteratedLogarithm\n"
                    "set_option pp.fullNames true in\n"
                    "set_option pp.universes true in\n"
                    "#check @" + thm_full + "\n"
                    "#print axioms " + thm_full + "\n"
                )
            proc_mod = subprocess.run(
                ["lake", "env", "lean", "-Dpp.unicode.fun=true", mod_check],
                cwd=bm_root,
                env=env,
                capture_output=True,
                text=True,
                timeout=300,
            )
            if proc_mod.returncode != 0:
                fail("Compiled module kernel check failed (exit " + str(proc_mod.returncode) + ")")
        finally:
            with open(up_file, "wb") as f:
                f.write(up_bytes)
            for pat in artifact_patterns:
                for p in glob.glob(pat):
                    if os.path.isfile(p):
                        os.remove(p)
            for orig_p, bpath in saved_artifacts:
                os.makedirs(os.path.dirname(orig_p), exist_ok=True)
                shutil.copy2(bpath, orig_p)

    status_post = subprocess.run(
        ["git", "status", "--porcelain"], cwd=bm_root, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30
    )
    if status_post.returncode != 0 or status_post.stdout.strip():
        fail("Failed to restore brownian-motion checkout git-clean")

    print("[3/5] Zero-warning prefix check & full repository lake build succeeded (LEAN_NUM_THREADS=2, git-clean)")

    if manifest["expected_check_prefix"] not in proc_mod.stdout or EXPECTED_FULL_CHECK not in proc_mod.stdout:
        fail("Compiled module #check signature mismatch")
    axioms_mod = parse_axioms(proc_mod.stdout, thm_full)
    illegal = [a for a in axioms_mod if a not in ALLOWED_AXIOMS]
    if illegal:
        fail("Disallowed axioms in compiled module: " + str(illegal))

    print("[4/5] Kernel signature & axiom audit passed: '" + thm_full + "' depends on axioms: " + str(axioms_mod))

    actual_sha = sha256_bytes(sol_bytes)
    if len(sol_bytes) != manifest["solution_bytes"] or actual_sha != manifest["solution_sha256"]:
        fail(
            "Object digest/size mismatch against proof_manifest.json: expected sha256="
            + manifest["solution_sha256"]
            + " ("
            + str(manifest["solution_bytes"])
            + " bytes), got sha256="
            + actual_sha
            + " ("
            + str(len(sol_bytes))
            + " bytes)"
        )

    print("[5/5] Object SHA-256 & byte-count verified: sha256=" + actual_sha + " (" + str(len(sol_bytes)) + " bytes)")
    print("PASS")


if __name__ == "__main__":
    main()
