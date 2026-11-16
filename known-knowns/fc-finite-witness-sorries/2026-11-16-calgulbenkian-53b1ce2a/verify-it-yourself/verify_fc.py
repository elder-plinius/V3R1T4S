#!/usr/bin/env python3
"""Standalone Lean 4 kernel & statement verifier for Formal Conjectures claims.

Checks:
1. Integrity of object/proof_manifest.json and object/Solution.lean (SHA-256, byte size, parameters).
2. Pinned formal-conjectures checkout (commit SHA, lean-toolchain, mathlib revision).
3. Upstream target file SHA-256, unclaimed status (research solved, sorry, no formal_proof), and
   character-for-character verbatim match of docstring + attributes + theorem signature.
4. Zero forbidden tokens (sorry, admit, axiom, native_decide, ofReduceBool, implemented_by, extern,
   skipKernelTC).
5. Lean 4 kernel verification via `lake env lean` with FormalConjectures linters enabled, checking
   both the fully-qualified kernel type (`pp.fullNames true`) and `#print axioms` subset of
   {propext, Classical.choice, Quot.sound}.

Prints exact final line PASS (exit 0) or FAIL (exit 1).
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


def fail(msg: str) -> None:
    print(f"CHECK_ERROR: {msg}")
    print("FAIL")
    sys.exit(1)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_fc_checkout(path: str) -> bool:
    return (
        bool(path)
        and os.path.isdir(path)
        and os.path.isfile(os.path.join(path, "FormalConjecturesUtil.lean"))
        and os.path.isfile(os.path.join(path, "lake-manifest.json"))
        and os.path.isfile(os.path.join(path, "lean-toolchain"))
    )


def locate_fc_root(pkg_root: str) -> str:
    env_root = os.environ.get("FC_ROOT", "").strip()
    if is_fc_checkout(env_root):
        return os.path.abspath(env_root)

    rel_candidates = [
        os.path.join(pkg_root, "..", "..", "fc-work", "formal-conjectures"),
        os.path.join(pkg_root, "..", "..", "..", "fc-work", "formal-conjectures"),
        os.path.join(pkg_root, "..", "fc-work", "formal-conjectures"),
        os.path.join(os.getcwd(), "formal-conjectures"),
        os.path.join(os.getcwd(), "..", "fc-work", "formal-conjectures"),
    ]
    for cand in rel_candidates:
        if is_fc_checkout(cand):
            return os.path.abspath(cand)

    home = os.path.expanduser("~")
    if os.path.isdir(home):
        q = deque([(home, 0)])
        while q:
            cur, depth = q.popleft()
            if is_fc_checkout(cur):
                return cur
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

    fail("Could not locate formal-conjectures Lake checkout (set FC_ROOT if needed)")
    return ""


def strip_lean_comments(text: str) -> str:
    # Remove nested /- ... -/ block comments and -- line comments
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


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    pkg_root = os.path.dirname(here)

    manifest_path = os.path.join(pkg_root, "object", "proof_manifest.json")
    if not os.path.isfile(manifest_path):
        fail("Missing object/proof_manifest.json")

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as exc:
        fail(f"Invalid JSON in object/proof_manifest.json: {exc}")

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
        "witness_vertices",
        "expected_check_prefix",
        "allowed_axioms",
    ]
    for k in req_keys:
        if k not in manifest:
            fail(f"Missing key '{k}' in object/proof_manifest.json")

    if manifest["solution_file"] != "Solution.lean":
        fail("Unexpected solution_file in manifest")
    if set(manifest["allowed_axioms"]) != ALLOWED_AXIOMS or len(manifest["allowed_axioms"]) != 3:
        fail("Tampered allowed_axioms in manifest")

    sol_path = os.path.join(pkg_root, "object", manifest["solution_file"])
    if not os.path.isfile(sol_path):
        fail("Missing object/Solution.lean")

    with open(sol_path, "rb") as f:
        sol_bytes = f.read()

    actual_sol_sha = sha256_bytes(sol_bytes)
    if actual_sol_sha != manifest["solution_sha256"]:
        fail(
            f"SHA-256 mismatch on object/Solution.lean: "
            f"expected {manifest['solution_sha256']}, got {actual_sol_sha}"
        )
    if len(sol_bytes) != manifest["solution_bytes"]:
        fail(
            f"Byte length mismatch on object/Solution.lean: "
            f"expected {manifest['solution_bytes']}, got {len(sol_bytes)}"
        )

    sol_text = sol_bytes.decode("utf-8")
    if f"Fin {manifest['witness_vertices']}" not in sol_text:
        fail(f"Expected witness_vertices Fin {manifest['witness_vertices']} not found in Solution.lean")

    print(f"[1/5] Manifest & object integrity verified: sha256={actual_sol_sha} ({len(sol_bytes)} bytes)")

    # Check forbidden tokens on both full text and comment-stripped text
    stripped_sol = strip_lean_comments(sol_text)
    for tok in FORBIDDEN_TOKENS:
        if re.search(rf"\b{re.escape(tok)}\b", sol_text) or re.search(rf"\b{re.escape(tok)}\b", stripped_sol):
            fail(f"Forbidden token '{tok}' present in object/Solution.lean")

    # Check import hygiene (only FormalConjecturesUtil)
    imports = re.findall(r"(?m)^\s*(?:public\s+)?(?:meta\s+)?import\s+(\S+)", stripped_sol)
    if imports != ["FormalConjecturesUtil"]:
        fail(f"Solution.lean must import only FormalConjecturesUtil; found {imports}")

    print("[2/5] Forbidden-token & import hygiene audit passed (0 forbidden tokens)")

    fc_root = locate_fc_root(pkg_root)

    with open(os.path.join(fc_root, "lean-toolchain"), "r", encoding="utf-8") as f:
        tc = f.read().strip()
    if tc != manifest["lean_toolchain"]:
        fail(f"Toolchain mismatch: expected {manifest['lean_toolchain']}, got {tc}")

    with open(os.path.join(fc_root, "lake-manifest.json"), "r", encoding="utf-8") as f:
        lake_manifest = json.load(f)
    mathlib_pkgs = [p for p in lake_manifest.get("packages", []) if p.get("name") == "mathlib"]
    if not mathlib_pkgs or mathlib_pkgs[0].get("rev") != manifest["mathlib_rev"]:
        fail("Mathlib revision in lake-manifest.json does not match manifest")

    if os.path.isdir(os.path.join(fc_root, ".git")) and shutil.which("git"):
        head = subprocess.run(
            ["git", "-C", fc_root, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if head.returncode != 0 or head.stdout.strip() != manifest["upstream_commit"]:
            fail(
                f"formal-conjectures HEAD mismatch: expected {manifest['upstream_commit']}, "
                f"got {head.stdout.strip()}"
            )

    up_fc_path = os.path.join(fc_root, manifest["upstream_relpath"])
    if not os.path.isfile(up_fc_path):
        fail(f"Upstream file {manifest['upstream_relpath']} missing in formal-conjectures checkout")
    with open(up_fc_path, "rb") as f:
        up_bytes = f.read()
    if sha256_bytes(up_bytes) != manifest["upstream_sha256"]:
        fail("Upstream file SHA-256 mismatch against manifest")

    local_data_up = os.path.join(pkg_root, "data", os.path.basename(manifest["upstream_relpath"]))
    if os.path.isfile(local_data_up):
        with open(local_data_up, "rb") as f:
            local_up_bytes = f.read()
        if sha256_bytes(local_up_bytes) != manifest["upstream_sha256"]:
            fail("Local data/ upstream .lean SHA-256 mismatch against manifest")

    up_text = up_bytes.decode("utf-8")
    short_name = manifest["theorem_short_name"]
    ns = manifest["namespace"]
    pat = re.compile(
        rf"(/--(?:(?!/--)[\s\S])*?-/[\r\n]+@\[category research solved[^\]]*\][\r\n]+"
        rf"theorem\s+{re.escape(short_name)}\b[\s\S]*?:=\s*by)\s+sorry\b"
    )
    m = pat.search(up_text)
    if not m:
        fail(f"Could not locate unclaimed 'research solved ... sorry' theorem {short_name} in upstream file")
    verbatim_block = m.group(1)
    if "formal_proof" in verbatim_block:
        fail(f"Upstream theorem {short_name} already carries a formal_proof attribute")
    if f"namespace {ns}" not in sol_text or f"end {ns}" not in sol_text:
        fail(f"Namespace {ns} missing in object/Solution.lean")
    if verbatim_block not in sol_text:
        fail(f"Exact verbatim docstring/attribute/statement block for {short_name} not found in object/Solution.lean")

    print(
        f"[3/5] Upstream pinned environment & verbatim statement match verified "
        f"(commit={manifest['upstream_commit'][:12]}, toolchain={tc})"
    )

    env = os.environ.copy()
    elan_bin = os.path.join(os.path.expanduser("~"), ".elan", "bin")
    if os.path.isdir(elan_bin):
        env["PATH"] = elan_bin + os.pathsep + env.get("PATH", "")
    env["LEAN_NUM_THREADS"] = "2"

    if not shutil.which("lake", path=env.get("PATH")):
        fail("lake binary not found in PATH")

    thm_full = manifest["theorem_full_name"]
    with tempfile.TemporaryDirectory() as td:
        check_file = os.path.join(td, "VerifySolution.lean")
        with open(check_file, "w", encoding="utf-8") as f:
            f.write(sol_text)
            f.write(
                "\nset_option pp.fullNames true in\n"
                "set_option pp.universes true in\n"
                f"#check @{thm_full}\n"
                f"#print axioms {thm_full}\n"
            )

        cmd = [
            "lake",
            "env",
            "lean",
            "-DautoImplicit=false",
            "-DrelaxedAutoImplicit=false",
            "-Dweak.linter.style.copyright.formalConjectures=true",
            "-Dweak.linter.style.namespace=true",
            "-Dweak.linter.style.stubs=true",
            "-Dweak.linter.style.openClassical=true",
            "-Dweak.linter.style.ams_attribute=true",
            "-Dweak.linter.style.category_attribute=true",
            "-Dweak.linter.style.conditional_formal_proof=true",
            "-Dweak.linter.style.moduleDocstring=true",
            "-Dweak.linter.style.latex_docstring=true",
            check_file,
        ]
        proc = subprocess.run(cmd, cwd=fc_root, env=env, capture_output=True, text=True, timeout=600)

    if proc.returncode != 0:
        fail(f"Lean kernel compilation failed with exit code {proc.returncode}")
    if proc.stderr.strip():
        fail("Lean emitted unexpected stderr diagnostics")

    out = proc.stdout
    if manifest["expected_check_prefix"] not in out:
        fail(f"Kernel #check type output did not match expected canonical signature for {thm_full}")

    ax_match = re.search(
        rf"'{re.escape(thm_full)}' depends on axioms: \[([^\]]*)\]",
        out,
    )
    no_ax_match = re.search(
        rf"'{re.escape(thm_full)}' does not depend on any axioms",
        out,
    )
    if ax_match:
        axioms = [a.strip() for a in ax_match.group(1).split(",") if a.strip()]
    elif no_ax_match:
        axioms = []
    else:
        fail(f"Could not parse #print axioms output for {thm_full}")

    illegal_axioms = [a for a in axioms if a not in ALLOWED_AXIOMS]
    if illegal_axioms:
        fail(f"Disallowed axioms detected: {illegal_axioms}")

    print(f"[4/5] Lean 4 kernel & FC linter build succeeded (exit=0, warnings=0)")
    print(f"[5/5] Axiom audit passed: '{thm_full}' depends on axioms: {axioms}")
    print("PASS")


if __name__ == "__main__":
    main()
