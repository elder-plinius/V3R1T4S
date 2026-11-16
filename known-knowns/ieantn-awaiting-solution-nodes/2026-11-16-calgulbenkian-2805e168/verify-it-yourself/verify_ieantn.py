#!/usr/bin/env python3
"""Deterministic 6-gate referee for ieantn-awaiting-solution-nodes (ZetaHadamard.v1).

Gates (matching PREREG.md):
1. Object & Manifest Integrity (pinned manifest SHA-256 + exact per-file bytes & SHA-256).
2. Forbidden-Token & Import-Isolation Audit (raw + comment-stripped Lean sources).
3. Pinned Upstream IEANTN Environment & Statement Integrity (commit, toolchain, mathlib, node hashes).
4. Lake Build (LEAN_NUM_THREADS=2, offline package cache reuse, zero warnings/errors).
5. Lean Comparator Kernel Replay (leanprover/comparator against IEANTN.Nodes.ZetaHadamard.v1.Challenge).
6. Direct #print axioms Check & Clean Restoration (git status --porcelain empty).

Prints PASS (exit 0) or FAIL (exit 1) as its final line.
"""
from collections import deque
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

EXPECTED_MANIFEST_SHA256 = "0add02ce82202878aeba6671e7c4ab54c67b85a75d88ae1121949f115a7832b9"
EXPECTED_MANIFEST_BYTES = 4714

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


def fail(msg):
    print("CHECK_ERROR: " + str(msg))
    print("FAIL")
    sys.exit(1)


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def strip_lean_comments(text):
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


def is_ieantn_checkout(path):
    return (
        bool(path)
        and os.path.isdir(path)
        and os.path.isfile(os.path.join(path, "IEANTN.lean"))
        and os.path.isfile(
            os.path.join(path, "IEANTN", "Nodes", "ZetaHadamard", "v1", "Challenge.lean")
        )
        and os.path.isfile(os.path.join(path, "lake-manifest.json"))
        and os.path.isfile(os.path.join(path, "lean-toolchain"))
    )


def is_comparator_tools(path):
    comp_dir = os.path.join(path, "comparator") if path else ""
    return (
        bool(path)
        and os.path.isdir(comp_dir)
        and os.path.isfile(os.path.join(comp_dir, ".lake", "build", "bin", "comparator"))
        and os.path.isfile(
            os.path.join(
                comp_dir,
                ".lake",
                "packages",
                "lean4export",
                ".lake",
                "build",
                "bin",
                "lean4export",
            )
        )
    )


def bfs_find(predicate):
    home = os.path.expanduser("~")
    if not os.path.isdir(home):
        return ""
    q = deque([(home, 0)])
    while q:
        cur, depth = q.popleft()
        if predicate(cur):
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
    return ""


def locate_ieantn_root(pkg_root):
    env_root = os.environ.get("IEANTN_ROOT", "").strip()
    if is_ieantn_checkout(env_root):
        return os.path.abspath(env_root)

    for base in (pkg_root, os.getcwd()):
        cur = os.path.abspath(base)
        for _ in range(6):
            cand = os.path.join(cur, "fc-work", "IEANTN")
            if is_ieantn_checkout(cand):
                return os.path.abspath(cand)
            cand2 = os.path.join(cur, "IEANTN")
            if is_ieantn_checkout(cand2):
                return os.path.abspath(cand2)
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent

    found = bfs_find(is_ieantn_checkout)
    if found:
        return found
    fail("Could not locate IEANTN checkout (set IEANTN_ROOT if needed)")
    return ""


def locate_comparator_tools(pkg_root, ieantn_root):
    env_root = os.environ.get("COMPARATOR_TOOLS_ROOT", "").strip()
    if is_comparator_tools(env_root):
        return os.path.abspath(env_root)

    sibling = os.path.join(os.path.dirname(ieantn_root), "comparator-tools")
    if is_comparator_tools(sibling):
        return os.path.abspath(sibling)

    for base in (pkg_root, os.getcwd()):
        cur = os.path.abspath(base)
        for _ in range(6):
            cand = os.path.join(cur, "fc-work", "comparator-tools")
            if is_comparator_tools(cand):
                return os.path.abspath(cand)
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent

    found = bfs_find(is_comparator_tools)
    if found:
        return found
    fail("Could not locate comparator-tools directory (set COMPARATOR_TOOLS_ROOT if needed)")
    return ""


def walk_rel_files(root):
    out = []
    for dp, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".git"))
        for f in sorted(files):
            full = os.path.join(dp, f)
            rel_p = os.path.relpath(full, root).replace(os.sep, "/")
            out.append(rel_p)
    return sorted(out)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    pkg_root = os.path.dirname(here)
    obj_root = os.path.join(pkg_root, "object")
    manifest_path = os.path.join(here, "proof_manifest.json")

    if not os.path.isfile(manifest_path):
        fail("Missing verify-it-yourself/proof_manifest.json")

    with open(manifest_path, "rb") as f:
        manifest_bytes = f.read()

    actual_manifest_sha = sha256_bytes(manifest_bytes)
    if len(manifest_bytes) != EXPECTED_MANIFEST_BYTES or actual_manifest_sha != EXPECTED_MANIFEST_SHA256:
        fail(
            "Manifest integrity mismatch: expected sha256=%s (%d bytes), got sha256=%s (%d bytes)"
            % (
                EXPECTED_MANIFEST_SHA256,
                EXPECTED_MANIFEST_BYTES,
                actual_manifest_sha,
                len(manifest_bytes),
            )
        )

    try:
        manifest = json.loads(manifest_bytes.decode("utf-8"))
    except Exception as exc:
        fail("Invalid JSON in verify-it-yourself/proof_manifest.json: %s" % exc)

    req_keys = [
        "target_id",
        "node_version",
        "challenge_module",
        "conclusions_module",
        "solution_module",
        "theorem_name",
        "conclusion_def",
        "ieantn_commit",
        "lean_toolchain",
        "mathlib_rev",
        "conclusions_relpath",
        "conclusions_sha256",
        "challenge_relpath",
        "challenge_sha256",
        "permitted_axioms",
        "files",
    ]
    for k in req_keys:
        if k not in manifest:
            fail("Missing required key in manifest: " + k)

    if manifest["target_id"] != "ieantn-awaiting-solution-nodes":
        fail("Unexpected target_id in manifest")
    if manifest["node_version"] != "ZetaHadamard.v1":
        fail("Unexpected node_version in manifest")
    if set(manifest["permitted_axioms"]) != ALLOWED_AXIOMS or len(manifest["permitted_axioms"]) != 3:
        fail("Unexpected permitted_axioms in manifest")

    all_obj_files = walk_rel_files(obj_root)
    expected_files = sorted(entry["path"] for entry in manifest["files"])
    if all_obj_files != expected_files:
        fail("File inventory mismatch in object/ vs proof_manifest.json")

    required_cfg = {
        "Solutions/ZetaHadamard.v1/lean-toolchain",
        "Solutions/ZetaHadamard.v1/lakefile.toml",
        "Solutions/ZetaHadamard.v1/lake-manifest.json",
        "Solutions/ZetaHadamard.v1/comparator.json",
        "Solutions/ZetaHadamard.v1/Solution.lean",
    }
    if not required_cfg.issubset(set(expected_files)):
        fail("Missing required Lake or Comparator configuration files in object/Solutions/ZetaHadamard.v1")

    lean_entries = []
    total_sol_bytes = 0
    for entry in manifest["files"]:
        rel_p = entry["path"]
        if not rel_p.startswith("Solutions/ZetaHadamard.v1/"):
            fail("Unexpected path outside Solutions/ZetaHadamard.v1/: " + rel_p)
        fp = os.path.join(obj_root, *rel_p.split("/"))
        with open(fp, "rb") as f:
            b = f.read()
        h = sha256_bytes(b)
        if not rel_p.endswith(".lean"):
            if len(b) != entry["bytes"] or h != entry["sha256"]:
                fail("Configuration file integrity mismatch on " + rel_p)
        elif len(b) == 0:
            fail("Empty Lean source file: " + rel_p)
        total_sol_bytes += len(b)
        if rel_p.endswith(".lean"):
            lean_entries.append((rel_p, b.decode("utf-8")))

    comp_cfg_path = os.path.join(obj_root, "Solutions", "ZetaHadamard.v1", "comparator.json")
    with open(comp_cfg_path, "r", encoding="utf-8") as f:
        comp_cfg = json.load(f)
    if (
        comp_cfg.get("challenge_module") != "IEANTN.Nodes.ZetaHadamard.v1.Challenge"
        or comp_cfg.get("solution_module") != "Solution"
        or comp_cfg.get("theorem_names") != ["ZetaHadamard.v1.challenge_logDeriv_partial_fractions"]
        or not set(comp_cfg.get("permitted_axioms", [])).issubset(ALLOWED_AXIOMS)
        or comp_cfg.get("enable_nanoda") is not True
    ):
        fail("comparator.json does not match required Challenge/Solution specification")

    print(
        "[1/6] Object & manifest integrity verified: %d files (%d bytes), manifest_sha256=%s"
        % (len(manifest["files"]), total_sol_bytes, actual_manifest_sha)
    )

    # Gate 2: Forbidden-token & import-isolation audit
    local_modules = {os.path.splitext(os.path.basename(p))[0] for p, _ in lean_entries}
    for rel_p, raw_text in lean_entries:
        mod_name = os.path.splitext(os.path.basename(rel_p))[0]
        clean_text = strip_lean_comments(raw_text)
        for tok in FORBIDDEN_TOKENS:
            pat = r"\b" + re.escape(tok) + r"\b"
            if re.search(pat, raw_text) or re.search(pat, clean_text):
                fail("Forbidden token '%s' found in %s" % (tok, rel_p))
        imports = re.findall(r"(?m)^\s*(?:public\s+)?import\s+(\S+)", clean_text)
        for imp in imports:
            if imp.startswith("IEANTN.Nodes."):
                if imp != "IEANTN.Nodes.ZetaHadamard.v1.Conclusions" or mod_name != "Solution":
                    fail("Disallowed node import '%s' in %s" % (imp, rel_p))
            elif imp in local_modules or imp == "IEANTN.Vocabulary.Zeta" or imp.startswith("Mathlib."):
                continue
            else:
                fail("Unexpected import '%s' in %s" % (imp, rel_p))

    print(
        "[2/6] Forbidden-token & import-isolation audit passed (%d Lean modules, 0 forbidden tokens)"
        % len(lean_entries)
    )

    # Gate 3: Pinned upstream IEANTN environment & statement integrity
    ieantn_root = locate_ieantn_root(pkg_root)
    comp_tools_root = locate_comparator_tools(pkg_root, ieantn_root)

    with open(os.path.join(ieantn_root, "lean-toolchain"), "r", encoding="utf-8") as f:
        tc = f.read().strip()
    if tc != manifest["lean_toolchain"]:
        fail("IEANTN lean-toolchain mismatch: expected %s, got %s" % (manifest["lean_toolchain"], tc))

    with open(os.path.join(ieantn_root, "lake-manifest.json"), "r", encoding="utf-8") as f:
        ieantn_manifest = json.load(f)
    pkgs_by_name = {p.get("name"): p for p in ieantn_manifest.get("packages", [])}
    if pkgs_by_name.get("mathlib", {}).get("rev") != manifest["mathlib_rev"]:
        fail("IEANTN mathlib revision mismatch against manifest")

    if os.path.isdir(os.path.join(ieantn_root, ".git")) and shutil.which("git"):
        head = subprocess.run(
            ["git", "-C", ieantn_root, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=20,
        )
        if head.returncode != 0 or head.stdout.strip() != manifest["ieantn_commit"]:
            fail("IEANTN git HEAD mismatch against pinned commit")
        pre_status = subprocess.run(
            ["git", "-C", ieantn_root, "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=20,
        )
        if pre_status.returncode != 0 or pre_status.stdout.strip() != "":
            fail("IEANTN checkout is not clean before verification")

    concl_p = os.path.join(ieantn_root, *manifest["conclusions_relpath"].split("/"))
    chall_p = os.path.join(ieantn_root, *manifest["challenge_relpath"].split("/"))
    if not os.path.isfile(concl_p) or not os.path.isfile(chall_p):
        fail("Missing upstream ZetaHadamard.v1 Conclusions.lean or Challenge.lean")

    if sha256_bytes(open(concl_p, "rb").read()) != manifest["conclusions_sha256"]:
        fail("Upstream Conclusions.lean SHA-256 mismatch")
    if sha256_bytes(open(chall_p, "rb").read()) != manifest["challenge_sha256"]:
        fail("Upstream Challenge.lean SHA-256 mismatch")

    staged_dir = os.path.join(ieantn_root, "Solutions", "ZetaHadamard.v1")
    if os.path.exists(staged_dir):
        fail("Solutions/ZetaHadamard.v1 already exists in upstream IEANTN checkout")

    print(
        "[3/6] Pinned upstream IEANTN verified (commit=%s, toolchain=%s, mathlib=%s)"
        % (manifest["ieantn_commit"][:12], tc, manifest["mathlib_rev"][:12])
    )

    env = os.environ.copy()
    elan_bin = os.path.join(os.path.expanduser("~"), ".elan", "bin")
    if os.path.isdir(elan_bin):
        env["PATH"] = elan_bin + os.pathsep + env.get("PATH", "")
    env["LEAN_NUM_THREADS"] = "2"

    if not shutil.which("lake", path=env.get("PATH")):
        fail("lake binary not found in PATH")

    src_sol_dir = os.path.join(obj_root, "Solutions", "ZetaHadamard.v1")

    try:
        # Gate 4: Stage into IEANTN/Solutions/ZetaHadamard.v1 and run lake build
        shutil.copytree(src_sol_dir, staged_dir)
        os.makedirs(os.path.join(staged_dir, ".lake"), exist_ok=True)
        os.symlink(
            os.path.join("..", "..", "..", ".lake", "packages"),
            os.path.join(staged_dir, ".lake", "packages"),
        )

        build_proc = subprocess.run(
            ["lake", "build"],
            cwd=staged_dir,
            env=env,
            capture_output=True,
            text=True,
            timeout=900,
        )
        build_out = (build_proc.stdout or "") + "\n" + (build_proc.stderr or "")
        if build_proc.returncode != 0:
            fail("lake build failed with exit code %d" % build_proc.returncode)
        for ln in build_out.splitlines():
            if ": warning:" in ln or ": error" in ln or "declaration uses 'sorry'" in ln:
                fail("lake build emitted diagnostic: " + ln[:120])

        print("[4/6] Lake build succeeded cleanly (LEAN_NUM_THREADS=2, exit=0, warnings=0)")

        # Gate 5: Lean Comparator kernel replay
        comp_repo = os.path.join(comp_tools_root, "comparator")
        comp_bin = os.path.join(comp_repo, ".lake", "build", "bin", "comparator")
        export_bin = os.path.join(
            comp_repo, ".lake", "packages", "lean4export", ".lake", "build", "bin", "lean4export"
        )
        fake_landrun = os.path.join(comp_repo, "scripts", "fake-landrun.sh")

        comp_env = env.copy()
        comp_env["COMPARATOR_LEAN4EXPORT"] = export_bin
        real_landrun = shutil.which("landrun", path=comp_env.get("PATH"))
        real_nanoda = shutil.which("nanoda_bin", path=comp_env.get("PATH"))

        with tempfile.TemporaryDirectory() as td:
            if real_landrun and real_nanoda and sys.platform.startswith("linux"):
                comp_env["COMPARATOR_LANDRUN"] = real_landrun
                cfg_arg = os.path.join(staged_dir, "comparator.json")
            else:
                comp_env["COMPARATOR_LANDRUN"] = fake_landrun
                runtime_cfg = dict(comp_cfg)
                if not real_nanoda:
                    runtime_cfg["enable_nanoda"] = False
                cfg_arg = os.path.join(td, "comparator_runtime.json")
                with open(cfg_arg, "w", encoding="utf-8") as f:
                    json.dump(runtime_cfg, f, indent=2)

            comp_proc = subprocess.run(
                ["lake", "env", comp_bin, cfg_arg],
                cwd=staged_dir,
                env=comp_env,
                capture_output=True,
                text=True,
                timeout=900,
            )

        comp_out = (comp_proc.stdout or "") + "\n" + (comp_proc.stderr or "")
        if comp_proc.returncode != 0:
            fail("leanprover/comparator failed with exit code %d" % comp_proc.returncode)
        if (
            "Lean default kernel accepts the solution" not in comp_out
            or "Your solution is okay!" not in comp_out
        ):
            fail("leanprover/comparator output lacked acceptance confirmation")

        print(
            "[5/6] leanprover/comparator verified IEANTN.Nodes.ZetaHadamard.v1.Challenge vs Solution "
            "('Your solution is okay!')"
        )

        # Gate 6: Direct #print axioms check
        thm_name = manifest["theorem_name"]
        concl_def = manifest["conclusion_def"]
        with tempfile.TemporaryDirectory() as td:
            ax_file = os.path.join(td, "AxiomCheck.lean")
            with open(ax_file, "w", encoding="utf-8") as f:
                f.write("import Solution\n")
                f.write("#check @" + thm_name + "\n")
                f.write("#print axioms " + thm_name + "\n")

            ax_proc = subprocess.run(
                ["lake", "env", "lean", ax_file],
                cwd=staged_dir,
                env=env,
                capture_output=True,
                text=True,
                timeout=300,
            )

        if ax_proc.returncode != 0:
            fail("Direct Lean axiom check failed with exit code %d" % ax_proc.returncode)

        ax_out = (ax_proc.stdout or "") + "\n" + (ax_proc.stderr or "")
        if (thm_name + " : " + concl_def) not in ax_out:
            fail("Direct #check signature mismatch for " + thm_name)

        ax_match = re.search(
            r"'" + re.escape(thm_name) + r"' depends on axioms: \[([^\]]*)\]",
            ax_out,
        )
        no_ax_match = re.search(
            r"'" + re.escape(thm_name) + r"' does not depend on any axioms",
            ax_out,
        )
        if ax_match:
            axioms = [a.strip() for a in ax_match.group(1).split(",") if a.strip()]
        elif no_ax_match:
            axioms = []
        else:
            fail("Could not parse #print axioms output for " + thm_name)

        bad_ax = [a for a in axioms if a not in ALLOWED_AXIOMS]
        if bad_ax:
            fail("Disallowed axioms detected: " + ", ".join(bad_ax))
    finally:
        shutil.rmtree(staged_dir, ignore_errors=True)

    if os.path.exists(staged_dir):
        fail("Failed to remove staged Solutions/ZetaHadamard.v1 directory")

    if os.path.isdir(os.path.join(ieantn_root, ".git")) and shutil.which("git"):
        post_status = subprocess.run(
            ["git", "-C", ieantn_root, "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=20,
        )
        if post_status.returncode != 0 or post_status.stdout.strip() != "":
            fail("IEANTN git status --porcelain not clean after verification")

    print(
        "[6/6] Direct #print axioms check passed (%s) & IEANTN restored git-clean"
        % str(axioms)
    )
    print("PASS")


if __name__ == "__main__":
    main()
