#!/usr/bin/env python3
"""Standalone 5-gate Lean 4 kernel & statement referee for leanapap-kelley-meka-integer-bound.

Target declaration: int in APAP/Integer.lean
Secondary verified declarations: BohrIter.zmod_prime_threeAPFree, BohrSet.regularity
Upstream commit: fb5cb9c4f594cbeeb160c715618d13640984c521

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
    "DummyPositivity",
    "FiniteField",
]

FORBIDDEN_IMPORT_MODULES = {
    "APAP.Prereqs.DummyPositivity",
    "APAP.Prereqs.Convolution.Order",
    "APAP.Physics.DRC",
    "APAP.FiniteField",
}

ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

EXPECTED_INTEGER_PUBLIC_IMPORTS = [
    "Mathlib.Analysis.SpecialFunctions.Pow.Real",
    "Mathlib.Combinatorics.Additive.AP.Three.Defs",
]

EXPECTED_REGULAR_PUBLIC_IMPORTS = ["APAP.Prereqs.Bohr.Basic"]

EXPECTED_INT_DECL = (
    "theorem int :\n"
    "    ∃ c > 0, ∃ C > 0, ∀ ⦃A : Finset ℕ⦄ ⦃N : ℕ⦄, A ⊆ range N → ThreeAPFree (α := ℕ) A →\n"
    "      (#A : ℝ) ≤ C * N / exp (c * log N ^ (12⁻¹ : ℝ)) :="
)

EXPECTED_CHECK_INT = (
    "int : ∃ c,\n"
    "  GT.gt.{0} c 0 ∧\n"
    "    ∃ C,\n"
    "      GT.gt.{0} C 0 ∧\n"
    "        ∀ ⦃A : Finset.{0} ℕ⦄ ⦃N : ℕ⦄,\n"
    "          A ⊆ Finset.range N →\n"
    "            ThreeAPFree.{0} ↑A →\n"
    "              LE.le.{0} (↑(Finset.card.{0} A))\n"
    "                (HDiv.hDiv.{0, 0, 0} (HMul.hMul.{0, 0, 0} C ↑N)\n"
    "                  (Real.exp (HMul.hMul.{0, 0, 0} c (HPow.hPow.{0, 0, 0} (Real.log ↑N) (Inv.inv.{0} 12)))))"
)

EXPECTED_CHECK_ZMOD = (
    "BohrIter.zmod_prime_threeAPFree : ∃ c,\n"
    "  GT.gt.{0} c 0 ∧\n"
    "    ∃ C,\n"
    "      GT.gt.{0} C 0 ∧\n"
    "        ∀ (q : ℕ) [inst : Fact (Nat.Prime q)],\n"
    "          LE.le.{0} 3 q →\n"
    "            ∀ (A₀ : Finset.{0} (ZMod q)),\n"
    "              ThreeAPFree.{0} ↑A₀ →\n"
    "                LE.le.{0} (↑(Finset.card.{0} A₀))\n"
    "                  (HDiv.hDiv.{0, 0, 0} (HMul.hMul.{0, 0, 0} C ↑q)\n"
    "                    (Real.exp (HMul.hMul.{0, 0, 0} c (HPow.hPow.{0, 0, 0} (Real.log ↑q) (Inv.inv.{0} 12)))))"
)

EXPECTED_CHECK_REGULAR = (
    "@BohrSet.regularity.{u_1} : ∀ {G : Type u_1} [inst : AddCommGroup.{u_1} G] [Finite.{u_1 + 1} G] (B : BohrSet.{u_1} G),\n"
    "  ∃ ρ, LE.le.{0} (Inv.inv.{0} 2) ρ ∧ LE.le.{0} ρ 1 ∧ BohrSet.IsRegular.{u_1} (HSMul.hSMul.{0, u_1, u_1} ρ B)"
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


def is_apap_checkout(path: str) -> bool:
    return (
        bool(path)
        and os.path.isdir(path)
        and os.path.isfile(os.path.join(path, "APAP.lean"))
        and os.path.isfile(os.path.join(path, "APAP", "Integer.lean"))
        and os.path.isfile(os.path.join(path, "APAP", "Prereqs", "Bohr", "Regular.lean"))
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


def walk_rel_files(root: str):
    out = []
    for dp, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".git"))
        for fn in sorted(files):
            full = os.path.join(dp, fn)
            out.append(os.path.relpath(full, root).replace(os.sep, "/"))
    return sorted(out)


def parse_axioms(output: str, thm_full: str):
    ax_match = re.search(
        r"'" + re.escape(thm_full) + r"' depends on axioms: \[([^\]]*)\]",
        output,
        re.S,
    )
    no_ax_match = re.search(
        r"'" + re.escape(thm_full) + r"' does not depend on any axioms",
        output,
    )
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
    manifest_v = os.path.join(here, "proof_manifest.json")
    manifest_o = os.path.join(obj_root, "proof_manifest.json")

    if not os.path.isfile(manifest_v):
        fail("Missing verify-it-yourself/proof_manifest.json")
    if not os.path.isfile(manifest_o):
        fail("Missing object/proof_manifest.json")

    with open(manifest_v, "rb") as f:
        mv_bytes = f.read()
    with open(manifest_o, "rb") as f:
        mo_bytes = f.read()
    if mv_bytes != mo_bytes:
        fail("object/proof_manifest.json does not match verify-it-yourself/proof_manifest.json")

    try:
        manifest = json.loads(mv_bytes.decode("utf-8"))
    except Exception as exc:
        fail("Invalid JSON in proof_manifest.json: " + str(exc))

    req_keys = [
        "target_id",
        "claim_scope",
        "solution_file",
        "solution_sha256",
        "solution_bytes",
        "theorem_full_name",
        "secondary_theorems",
        "upstream_commit",
        "upstream_relpath",
        "upstream_sha256",
        "upstream_bytes",
        "lean_toolchain",
        "mathlib_rev",
        "addcombi_rev",
        "checkdecls_rev",
        "allowed_axioms",
        "proof_files",
    ]
    for k in req_keys:
        if k not in manifest:
            fail("Missing key " + k + " in proof_manifest.json")

    if manifest["target_id"] != "leanapap-kelley-meka-integer-bound":
        fail("Unexpected target_id in proof_manifest.json")
    if manifest["solution_file"] != "Integer.lean" or manifest["theorem_full_name"] != "int":
        fail("Unexpected solution_file or theorem_full_name in proof_manifest.json")
    if set(manifest["allowed_axioms"]) != ALLOWED_AXIOMS or len(manifest["allowed_axioms"]) != 3:
        fail("Tampered allowed_axioms in proof_manifest.json")

    proof_files = manifest["proof_files"]
    if not isinstance(proof_files, list) or len(proof_files) != 6:
        fail("Expected exactly 6 proof_files entries in proof_manifest.json")

    expected_obj_files = sorted([pf["object_file"] for pf in proof_files] + ["proof_manifest.json"])
    actual_obj_files = walk_rel_files(obj_root)
    if actual_obj_files != expected_obj_files:
        fail("object/ file list mismatch: " + str(actual_obj_files))

    loaded_objects = {}
    for pf in proof_files:
        oname = pf["object_file"]
        opath = os.path.join(obj_root, oname)
        with open(opath, "rb") as f:
            obytes = f.read()
        try:
            otext = obytes.decode("utf-8")
        except UnicodeDecodeError:
            fail("object/" + oname + " is not valid UTF-8")
        loaded_objects[oname] = (pf, obytes, otext)

    apap_root = locate_apap_root(pkg_root)

    with open(os.path.join(apap_root, "lean-toolchain"), "r", encoding="utf-8") as f:
        tc = f.read().strip()
    if tc != manifest["lean_toolchain"]:
        fail("lean-toolchain mismatch: expected " + manifest["lean_toolchain"] + ", got " + tc)

    with open(os.path.join(apap_root, "lake-manifest.json"), "r", encoding="utf-8") as f:
        lm = json.load(f)
    pkgs = {p["name"]: p["rev"] for p in lm.get("packages", [])}
    if pkgs.get("mathlib") != manifest["mathlib_rev"]:
        fail("mathlib revision mismatch in lake-manifest.json")
    if pkgs.get("AddCombi") != manifest["addcombi_rev"]:
        fail("AddCombi revision mismatch in lake-manifest.json")
    if pkgs.get("checkdecls") != manifest["checkdecls_rev"]:
        fail("checkdecls revision mismatch in lake-manifest.json")

    head_proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=apap_root,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if head_proc.returncode != 0 or head_proc.stdout.strip() != manifest["upstream_commit"]:
        fail("LeanAPAP git HEAD does not match pinned upstream_commit")

    status_pre = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=apap_root,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if status_pre.returncode != 0 or status_pre.stdout.strip():
        fail("LeanAPAP checkout is dirty prior to verification")

    upstream_originals = {}
    for pf in proof_files:
        target_p = os.path.join(apap_root, *pf["repo_relpath"].split("/"))
        if pf["is_new"]:
            if os.path.exists(target_p):
                fail("New module unexpectedly pre-exists in clean checkout: " + pf["repo_relpath"])
        else:
            if not os.path.isfile(target_p):
                fail("Modified upstream module missing in checkout: " + pf["repo_relpath"])
            with open(target_p, "rb") as f:
                ubytes = f.read()
            if len(ubytes) != pf["upstream_bytes"] or sha256_bytes(ubytes) != pf["upstream_sha256"]:
                fail("Upstream SHA-256/size mismatch on " + pf["repo_relpath"])
            upstream_originals[pf["object_file"]] = (target_p, ubytes)
            snap_p = os.path.join(pkg_root, "data", pf["object_file"])
            if os.path.isfile(snap_p):
                with open(snap_p, "rb") as f:
                    if sha256_bytes(f.read()) != pf["upstream_sha256"]:
                        fail("data/" + pf["object_file"] + " SHA-256 mismatch against upstream")

    print(
        "[1/5] Pinned LeanAPAP checkout & manifest schema verified (commit="
        + manifest["upstream_commit"][:12]
        + ", toolchain="
        + tc
        + ")"
    )

    # Gate 2: Forbidden-token, import-hygiene & verbatim statement diff audit
    for oname, (pf, _, otext) in loaded_objects.items():
        stripped = strip_lean_comments(otext)
        for tok in FORBIDDEN_TOKENS:
            if re.search(r"\b" + re.escape(tok) + r"\b", otext) or re.search(
                r"\b" + re.escape(tok) + r"\b", stripped
            ):
                fail("Forbidden token '" + tok + "' present in object/" + oname)
        all_imps = re.findall(r"(?m)^\s*(?:public\s+)?import\s+(\S+)", stripped)
        for imp in all_imps:
            if imp in FORBIDDEN_IMPORT_MODULES:
                fail("Disallowed tainted import '" + imp + "' in object/" + oname)

    # Check Regular.lean verbatim preservation against upstream
    reg_up_text = upstream_originals["Regular.lean"][1].decode("utf-8")
    reg_sol_text = loaded_objects["Regular.lean"][2]
    reg_stripped = strip_lean_comments(reg_sol_text)
    reg_pub_imps = re.findall(r"(?m)^\s*public\s+import\s+(\S+)", reg_stripped)
    if reg_pub_imps != EXPECTED_REGULAR_PUBLIC_IMPORTS:
        fail("Regular.lean public imports modified from upstream")
    b1 = reg_up_text[: reg_up_text.index("\npublic section")]
    b2 = reg_up_text[reg_up_text.index("public section") : reg_up_text.index("\n/-- **Bohr Set Regularity**")]
    b3 = reg_up_text[reg_up_text.index("/-- **Bohr Set Regularity**") : reg_up_text.index(" := sorry")]
    if not reg_sol_text.startswith(b1) or b2 not in reg_sol_text or (b3 + " := by") not in reg_sol_text:
        fail("Regular.lean IsRegular / BohrSet.regularity statement modified from upstream")

    # Check Integer.lean verbatim header and corrected Kelley-Meka theorem statement
    int_up_text = upstream_originals["Integer.lean"][1].decode("utf-8")
    int_sol_text = loaded_objects["Integer.lean"][2]
    int_stripped = strip_lean_comments(int_sol_text)
    int_pub_imps = re.findall(r"(?m)^\s*public\s+import\s+(\S+)", int_stripped)
    if int_pub_imps != EXPECTED_INTEGER_PUBLIC_IMPORTS:
        fail("Integer.lean public imports modified from upstream: " + str(int_pub_imps))
    int_b1 = int_up_text[: int_up_text.index("\nopen Finset Real")]
    if not int_sol_text.startswith(int_b1):
        fail("Integer.lean module / public import header modified from upstream")
    if "\nopen Finset Real\n" not in int_stripped or "\npublic section\n" not in int_stripped:
        fail("Integer.lean missing 'open Finset Real' or 'public section'")
    pub_tail = int_stripped.split("\npublic section\n", 1)[1]
    if EXPECTED_INT_DECL not in pub_tail:
        fail("Integer.lean public section does not match verbatim Kelley-Meka theorem int statement")

    print("[2/5] Forbidden-token, import-hygiene & verbatim statement diff audit passed across all 6 files")

    # Gate 3: Cold staging, full repository lake build, zero-warning linter check, and restoration
    env = os.environ.copy()
    elan_bin = os.path.join(os.path.expanduser("~"), ".elan", "bin")
    if os.path.isdir(elan_bin):
        env["PATH"] = elan_bin + os.pathsep + env.get("PATH", "")
    env["LEAN_NUM_THREADS"] = "2"

    if not shutil.which("lake", path=env.get("PATH")):
        fail("lake binary not found in PATH")

    module_stems = [pf["repo_relpath"][:-5] for pf in proof_files] + ["APAP"]
    artifact_patterns = []
    for stem in module_stems:
        parts = stem.split("/")
        artifact_patterns.append(os.path.join(apap_root, ".lake", "build", "lib", "lean", *parts) + ".*")
        artifact_patterns.append(os.path.join(apap_root, ".lake", "build", "ir", *parts) + ".*")

    with tempfile.TemporaryDirectory() as backup_dir:
        saved_artifacts = []
        for pat in artifact_patterns:
            for p in sorted(glob.glob(pat)):
                if os.path.isfile(p):
                    bname = os.path.relpath(p, apap_root).replace(os.sep, "__")
                    bpath = os.path.join(backup_dir, bname)
                    shutil.copy2(p, bpath)
                    saved_artifacts.append((p, bpath))

        try:
            # Remove cached artifacts for all 6 proof modules + APAP to force cold source build
            for pat in artifact_patterns:
                for p in glob.glob(pat):
                    if os.path.isfile(p):
                        os.remove(p)

            # Stage all 6 proof files
            for pf in proof_files:
                dst = os.path.join(apap_root, *pf["repo_relpath"].split("/"))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(dst, "wb") as f:
                    f.write(loaded_objects[pf["object_file"]][1])

            proc_build = subprocess.run(
                ["lake", "build"],
                cwd=apap_root,
                env=env,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=900,
            )
            if proc_build.returncode != 0:
                fail("Full LeanAPAP lake build failed with exit code " + str(proc_build.returncode))

            # Run zero-warning mathlib standard linter check + warn.sorry=true on all 6 modules
            for pf in proof_files:
                cmd_lint = [
                    "lake",
                    "env",
                    "lean",
                    "-Dpp.unicode.fun=true",
                    "-DautoImplicit=false",
                    "-DrelaxedAutoImplicit=false",
                    "-Dweak.linter.mathlibStandardSet=true",
                    "-Dlinter.style.header=false",
                    "-Dwarn.sorry=true",
                    pf["repo_relpath"],
                ]
                proc_l = subprocess.run(
                    cmd_lint,
                    cwd=apap_root,
                    env=env,
                    stdin=subprocess.DEVNULL,
                    capture_output=True,
                    text=True,
                    timeout=600,
                )
                if proc_l.returncode != 0 or proc_l.stderr.strip():
                    fail("Linter/kernel check failed on " + pf["object_file"])
                for ln in proc_l.stdout.splitlines():
                    if ": warning:" in ln or ": error" in ln:
                        fail("Diagnostic emitted during zero-warning check on " + pf["object_file"])

            mod_check = os.path.join(backup_dir, "VerifyCompiledIntegerModule.lean")
            with open(mod_check, "w", encoding="utf-8") as f:
                f.write(
                    "import APAP.Integer\n"
                    "import APAP.BohrIter\n"
                    "import APAP.Prereqs.Bohr.Regular\n"
                    "set_option pp.fullNames true in\n"
                    "set_option pp.universes true in\n"
                    "#check @int\n"
                    "#print axioms int\n"
                    "set_option pp.fullNames true in\n"
                    "set_option pp.universes true in\n"
                    "#check @BohrIter.zmod_prime_threeAPFree\n"
                    "#print axioms BohrIter.zmod_prime_threeAPFree\n"
                    "set_option pp.fullNames true in\n"
                    "set_option pp.universes true in\n"
                    "#check @BohrSet.regularity\n"
                    "#print axioms BohrSet.regularity\n"
                )
            proc_mod = subprocess.run(
                ["lake", "env", "lean", "-Dpp.unicode.fun=true", mod_check],
                cwd=apap_root,
                env=env,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=300,
            )
            if proc_mod.returncode != 0:
                fail("Compiled LeanAPAP module kernel check failed (exit " + str(proc_mod.returncode) + ")")
        finally:
            # Remove newly staged files and restore modified upstream files
            for pf in proof_files:
                dst = os.path.join(apap_root, *pf["repo_relpath"].split("/"))
                if pf["is_new"]:
                    if os.path.exists(dst):
                        os.remove(dst)
                else:
                    orig_p, orig_b = upstream_originals[pf["object_file"]]
                    with open(orig_p, "wb") as f:
                        f.write(orig_b)
            for pat in artifact_patterns:
                for p in glob.glob(pat):
                    if os.path.isfile(p):
                        os.remove(p)
            for orig_p, bpath in saved_artifacts:
                os.makedirs(os.path.dirname(orig_p), exist_ok=True)
                shutil.copy2(bpath, orig_p)

    status_post = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=apap_root,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if status_post.returncode != 0 or status_post.stdout.strip():
        fail("Failed to restore LeanAPAP checkout git-clean")

    print(
        "[3/5] Cold 6-module compilation, zero-warning linter check & full LeanAPAP lake build succeeded (LEAN_NUM_THREADS=2, git-clean)"
    )

    # Gate 4: Kernel signature & axiom audit
    if EXPECTED_CHECK_INT not in proc_mod.stdout:
        fail("Compiled module #check @int signature mismatch against required canonical type")
    if EXPECTED_CHECK_ZMOD not in proc_mod.stdout:
        fail("Compiled module #check @BohrIter.zmod_prime_threeAPFree signature mismatch")
    if EXPECTED_CHECK_REGULAR not in proc_mod.stdout:
        fail("Compiled module #check @BohrSet.regularity signature mismatch")

    for thm in ["int", "BohrIter.zmod_prime_threeAPFree", "BohrSet.regularity"]:
        axs = parse_axioms(proc_mod.stdout, thm)
        illegal = [a for a in axs if a not in ALLOWED_AXIOMS]
        if illegal:
            fail("Disallowed axioms on " + thm + ": " + str(illegal))
        if thm == "int":
            int_axs = axs

    print("[4/5] Kernel signature & axiom audit passed: 'int' depends on axioms: " + str(int_axs))

    # Gate 5: Object SHA-256 & byte-count verification across all 6 proof files
    total_bytes = 0
    for pf in proof_files:
        oname = pf["object_file"]
        _, obytes, _ = loaded_objects[oname]
        osha = sha256_bytes(obytes)
        if len(obytes) != pf["bytes"] or osha != pf["sha256"]:
            fail("Object digest/size mismatch on object/" + oname)
        total_bytes += len(obytes)

    sol_bytes = loaded_objects["Integer.lean"][1]
    sol_sha = sha256_bytes(sol_bytes)
    if len(sol_bytes) != manifest["solution_bytes"] or sol_sha != manifest["solution_sha256"]:
        fail("Solution Integer.lean digest/size mismatch against top-level manifest fields")

    print(
        "[5/5] All 6 object files SHA-256 & byte-counts verified (Integer.lean sha256="
        + sol_sha
        + ", total_proof_bytes="
        + str(total_bytes)
        + ")"
    )
    print("PASS")


if __name__ == "__main__":
    main()
