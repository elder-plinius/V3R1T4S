#!/usr/bin/env python3
"""Standalone 5-gate Lean 4 kernel & statement referee for flt-imperial-unclaimed-prop-sorries.

Target declarations:
  - Group.subsingleton_of_pow_prime_eq_one
  - AddGroup.subsingleton_of_nsmul_prime_eq_zero
Upstream file: FLT/Patching/Utils/CompactHausdorffRings.lean (commit a3210204ad8876e851e32f73dd97d882bf1ccd0a)

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
    "knownin1980s",
    "Mazur_statement",
    "Odlyzko_statement",
]

ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

EXPECTED_PUBLIC_IMPORTS = [
    "Mathlib.GroupTheory.Divisible",
    "Mathlib.Topology.Algebra.Group.CompactOpen",
    "Mathlib.Data.Nat.Prime.Defs",
]

EXPECTED_GROUP_CHECK = (
    "Group.subsingleton_of_pow_prime_eq_one.{u_1} : ∀ (A : Type u_1) [inst : CommGroup.{u_1} A]\n"
    "  [inst_1 : TopologicalSpace.{u_1} A] [IsTopologicalGroup.{u_1} A] [ConnectedSpace.{u_1} A] [CompactSpace.{u_1} A]\n"
    "  [T2Space.{u_1} A] (p : ℕ),\n"
    "  Nat.Prime p → (∀ (a : A), Eq.{u_1 + 1} (HPow.hPow.{u_1, 0, u_1} a p) 1) → Subsingleton.{u_1 + 1} A"
)

EXPECTED_ADDGROUP_CHECK = (
    "AddGroup.subsingleton_of_nsmul_prime_eq_zero.{u_1} : ∀ (A : Type u_1) [inst : AddCommGroup.{u_1} A]\n"
    "  [inst_1 : TopologicalSpace.{u_1} A] [IsTopologicalAddGroup.{u_1} A] [ConnectedSpace.{u_1} A] [CompactSpace.{u_1} A]\n"
    "  [T2Space.{u_1} A] (p : ℕ),\n"
    "  Nat.Prime p → (∀ (a : A), Eq.{u_1 + 1} (HSMul.hSMul.{0, u_1, u_1} p a) 0) → Subsingleton.{u_1 + 1} A"
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


def is_flt_checkout(path: str) -> bool:
    return (
        bool(path)
        and os.path.isdir(path)
        and os.path.isfile(os.path.join(path, "FLT.lean"))
        and os.path.isfile(os.path.join(path, "FLT", "Patching", "Utils", "CompactHausdorffRings.lean"))
        and os.path.isfile(os.path.join(path, "lake-manifest.json"))
        and os.path.isfile(os.path.join(path, "lean-toolchain"))
    )


def locate_flt_root(pkg_root: str) -> str:
    env_root = os.environ.get("FLT_ROOT", "").strip()
    if is_flt_checkout(env_root):
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
                ("fc-work", "FLT"),
                ("v3r1t4s-hunt", "fc-work", "FLT"),
                ("FLT",),
            ):
                cand = os.path.join(cur, *sub)
                if is_flt_checkout(cand):
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
            if is_flt_checkout(cur):
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

    fail("Could not locate FLT Lake checkout (set FLT_ROOT if needed)")
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
    ax_match = re.search(r"'" + re.escape(thm_full) + r"' depends on axioms: \[([^\]]*)\]", output, re.S)
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
        "additive_theorem_full_name",
        "downstream_theorem_full_name",
        "upstream_commit",
        "upstream_relpath",
        "upstream_sha256",
        "lean_toolchain",
        "mathlib_rev",
        "checkdecls_rev",
        "allowed_axioms",
    ]
    for k in req_keys:
        if k not in manifest:
            fail("Missing key " + k + " in proof_manifest.json")

    if manifest["target_id"] != "flt-imperial-unclaimed-prop-sorries":
        fail("Unexpected target_id in proof_manifest.json")
    if manifest["solution_file"] != "CompactHausdorffRings.lean":
        fail("Unexpected solution_file in proof_manifest.json")
    if set(manifest["allowed_axioms"]) != ALLOWED_AXIOMS or len(manifest["allowed_axioms"]) != 3:
        fail("Tampered allowed_axioms in proof_manifest.json")

    if not os.path.isdir(obj_root):
        fail("Missing object/ directory")
    obj_files = walk_rel_files(obj_root)
    if obj_files != ["CompactHausdorffRings.lean"]:
        fail("object/ must contain exclusively CompactHausdorffRings.lean, found: " + str(obj_files))

    sol_path = os.path.join(obj_root, "CompactHausdorffRings.lean")
    with open(sol_path, "rb") as f:
        sol_bytes = f.read()
    try:
        sol_text = sol_bytes.decode("utf-8")
    except UnicodeDecodeError:
        fail("object/CompactHausdorffRings.lean is not valid UTF-8")

    flt_root = locate_flt_root(pkg_root)

    with open(os.path.join(flt_root, "lean-toolchain"), "r", encoding="utf-8") as f:
        tc = f.read().strip()
    if tc != manifest["lean_toolchain"]:
        fail("lean-toolchain mismatch: expected " + manifest["lean_toolchain"] + ", got " + tc)

    with open(os.path.join(flt_root, "lake-manifest.json"), "r", encoding="utf-8") as f:
        lm = json.load(f)
    pkgs = {p["name"]: p["rev"] for p in lm.get("packages", [])}
    if pkgs.get("mathlib") != manifest["mathlib_rev"]:
        fail("mathlib revision mismatch in lake-manifest.json")
    if pkgs.get("checkdecls") != manifest["checkdecls_rev"]:
        fail("checkdecls revision mismatch in lake-manifest.json")

    head_proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=flt_root,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if head_proc.returncode != 0 or head_proc.stdout.strip() != manifest["upstream_commit"]:
        fail("FLT git HEAD does not match pinned upstream_commit")

    status_pre = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=flt_root,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if status_pre.returncode != 0 or status_pre.stdout.strip():
        fail("FLT checkout is dirty prior to verification")

    up_file = os.path.join(flt_root, *manifest["upstream_relpath"].split("/"))
    with open(up_file, "rb") as f:
        up_bytes = f.read()
    if sha256_bytes(up_bytes) != manifest["upstream_sha256"]:
        fail("Upstream FLT/Patching/Utils/CompactHausdorffRings.lean SHA-256 mismatch")

    local_snap = os.path.join(pkg_root, "data", "CompactHausdorffRings.lean")
    if os.path.isfile(local_snap):
        with open(local_snap, "rb") as f:
            if sha256_bytes(f.read()) != manifest["upstream_sha256"]:
                fail("data/CompactHausdorffRings.lean SHA-256 mismatch against upstream")

    up_text = up_bytes.decode("utf-8")
    print("[1/5] Pinned FLT checkout & manifest schema verified (commit=" + manifest["upstream_commit"][:12] + ", toolchain=" + tc + ")")

    stripped_sol = strip_lean_comments(sol_text)
    if re.search(r"\bsorry\b", sol_text):
        fail("Forbidden token 'sorry' present in object/CompactHausdorffRings.lean")
    for tok in FORBIDDEN_TOKENS:
        if re.search(r"\b" + re.escape(tok) + r"\b", stripped_sol):
            fail("Forbidden token '" + tok + "' present in object/CompactHausdorffRings.lean")

    pub_imports = re.findall(r"(?m)^\s*public\s+import\s+(\S+)", stripped_sol)
    if pub_imports != EXPECTED_PUBLIC_IMPORTS:
        fail("Public imports modified from upstream: " + str(pub_imports))
    priv_imports = re.findall(r"(?m)^\s*import\s+(\S+)", stripped_sol)
    for imp in priv_imports:
        if not imp.startswith("Mathlib."):
            fail("Disallowed non-Mathlib private import: " + imp)

    # Verbatim block comparisons against upstream
    b1 = up_text[: up_text.index("\nimport ")]
    if not sol_text.startswith(b1):
        fail("Copyright / module / public imports header modified from upstream")

    b2 = up_text[up_text.index("\n/-!") : up_text.index("\n@[expose] public section")]
    if b2 not in sol_text:
        fail("Module docstring modified from upstream")

    b3 = up_text[up_text.index("@[expose] public section") : up_text.index("  sorry\n")]
    if b3 not in sol_text:
        fail("Group.subsingleton_of_pow_prime_eq_one docstring, attributes, or signature modified from upstream")

    suffix_anchor = "\n/-- A compact Hausdorff vector space over `𝔽_p` is totally disconnected. -/"
    b4 = up_text[up_text.index(suffix_anchor) :]
    if not sol_text.endswith(b4):
        fail("Downstream declarations in CompactHausdorffRings.lean modified from upstream")

    print("[2/5] Forbidden-token & verbatim upstream statement/downstream diff audit passed")

    env = os.environ.copy()
    elan_bin = os.path.join(os.path.expanduser("~"), ".elan", "bin")
    if os.path.isdir(elan_bin):
        env["PATH"] = elan_bin + os.pathsep + env.get("PATH", "")
    env["LEAN_NUM_THREADS"] = "2"

    if not shutil.which("lake", path=env.get("PATH")):
        fail("lake binary not found in PATH")

    thm_mul = manifest["theorem_full_name"]
    thm_add = manifest["additive_theorem_full_name"]
    thm_td = manifest["downstream_theorem_full_name"]

    with tempfile.TemporaryDirectory() as td:
        standalone = re.sub(r"(?m)^module\s*$", "", sol_text, count=1)
        standalone = re.sub(r"(?m)^public\s+import\s+", "import ", standalone)
        standalone = standalone.replace("@[expose] public section", "")
        check_p = os.path.join(td, "VerifyCHRStandalone.lean")
        with open(check_p, "w", encoding="utf-8") as f:
            f.write(standalone)
            f.write(
                "\nset_option pp.fullNames true in\nset_option pp.universes true in\n"
                "#check @" + thm_mul + "\n"
                "set_option pp.fullNames true in\nset_option pp.universes true in\n"
                "#check @" + thm_add + "\n"
                "#print axioms " + thm_mul + "\n"
                "#print axioms " + thm_add + "\n"
                "#print axioms " + thm_td + "\n"
            )
        cmd_s = [
            "lake",
            "env",
            "lean",
            "-Dpp.unicode.fun=true",
            "-DautoImplicit=false",
            "-DrelaxedAutoImplicit=false",
            "-DmaxSynthPendingDepth=3",
            "-Dweak.linter.flexible=true",
            "-Dweak.linter.mathlibStandardSet=true",
            "-Dlinter.style.header=false",
            "-Dwarn.sorry=true",
            check_p,
        ]
        proc_s = subprocess.run(
            cmd_s, cwd=flt_root, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600
        )

    if proc_s.returncode != 0:
        fail("Lean 4 kernel/linter compilation of CompactHausdorffRings.lean failed (exit " + str(proc_s.returncode) + ")")
    if proc_s.stderr.strip():
        fail("Lean emitted unexpected stderr during zero-warning check")
    for ln in proc_s.stdout.splitlines():
        if ": warning:" in ln or ": error" in ln:
            fail("Lean linter/compiler diagnostic emitted during zero-warning check")

    artifact_patterns = [
        os.path.join(flt_root, ".lake", "build", "lib", "lean", "FLT", "Patching", "Utils", "CompactHausdorffRings.*"),
        os.path.join(flt_root, ".lake", "build", "ir", "FLT", "Patching", "Utils", "CompactHausdorffRings.*"),
    ]
    with tempfile.TemporaryDirectory() as backup_dir:
        saved_artifacts = []
        for pat in artifact_patterns:
            for p in sorted(glob.glob(pat)):
                if os.path.isfile(p):
                    bname = os.path.relpath(p, flt_root).replace(os.sep, "__")
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
                ["lake", "build"],
                cwd=flt_root,
                env=env,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=900,
            )
            if proc_build.returncode != 0:
                fail("Full FLT lake build failed with exit code " + str(proc_build.returncode))

            mod_check = os.path.join(backup_dir, "VerifyCompiledFLTModule.lean")
            with open(mod_check, "w", encoding="utf-8") as f:
                f.write(
                    "import FLT.Patching.Utils.CompactHausdorffRings\n"
                    "set_option pp.fullNames true in\nset_option pp.universes true in\n"
                    "#check @" + thm_mul + "\n"
                    "set_option pp.fullNames true in\nset_option pp.universes true in\n"
                    "#check @" + thm_add + "\n"
                    "#print axioms " + thm_mul + "\n"
                    "#print axioms " + thm_add + "\n"
                    "#print axioms " + thm_td + "\n"
                )
            proc_mod = subprocess.run(
                ["lake", "env", "lean", "-Dpp.unicode.fun=true", mod_check],
                cwd=flt_root,
                env=env,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=300,
            )
            if proc_mod.returncode != 0:
                fail("Compiled FLT module kernel check failed (exit " + str(proc_mod.returncode) + ")")
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
        ["git", "status", "--porcelain"],
        cwd=flt_root,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if status_post.returncode != 0 or status_post.stdout.strip():
        fail("Failed to restore FLT checkout git-clean")

    print("[3/5] Zero-warning linter check & full FLT repository lake build succeeded (LEAN_NUM_THREADS=2, git-clean)")

    if EXPECTED_GROUP_CHECK not in proc_mod.stdout or EXPECTED_ADDGROUP_CHECK not in proc_mod.stdout:
        fail("Compiled module #check signature mismatch against upstream canonical type")

    for decl in (thm_mul, thm_add, thm_td):
        axs = parse_axioms(proc_mod.stdout, decl)
        illegal = [a for a in axs if a not in ALLOWED_AXIOMS]
        if illegal:
            fail("Disallowed axioms on " + decl + ": " + str(illegal))

    axs_mul = parse_axioms(proc_mod.stdout, thm_mul)
    axs_add = parse_axioms(proc_mod.stdout, thm_add)
    print(
        "[4/5] Kernel signature & axiom audit passed: "
        + thm_mul
        + "="
        + str(axs_mul)
        + ", "
        + thm_add
        + "="
        + str(axs_add)
    )

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
