#!/usr/bin/env python3
"""Standalone Lean 4 kernel & statement verifier for LeanCamCombi BKR-Reimer claims.

Checks:
1. Integrity of object/proof_manifest.json and object/VanDenBergKesten.lean (SHA-256, byte size).
2. Zero forbidden tokens (sorry, admit, axiom, native_decide, ofReduceBool, implemented_by, extern,
   skipKernelTC) and public-import hygiene (exact 3 upstream public imports).
3. Pinned LeanCamCombi checkout (commit SHA, lean-toolchain, mathlib rev, AddCombi rev), upstream
   VanDenBergKesten.lean SHA-256, and character-for-character verbatim match of all upstream blocks
   (header/public imports, BooleanAlgebra section including Finset.certificator, and the exact
   Finset.card_certificator_le docstring + statement).
4. Lean 4 kernel compilation via `lake env lean` with all LeanCamCombi mathlibStandardSet linters
   enabled (exit code 0, zero warnings/errors).
5. Full kernel type check (`pp.fullNames true`, `pp.universes true`) and `#print axioms` subset of
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

EXPECTED_PUBLIC_IMPORTS = [
    "Mathlib.Data.Finset.Sups",
    "Mathlib.Data.Fintype.Basic",
    "Mathlib.Order.UpperLower.Basic",
]

EXPECTED_FULL_CHECK = (
    "@Finset.card_certificator_le.{u_2} : ∀ {α : Type u_2} [inst : DecidableEq.{u_2 + 1} α] "
    "[inst_1 : Fintype.{u_2} α]\n"
    "  {𝒜 ℬ : Finset.{u_2} (Finset.{u_2} α)},\n"
    "  LE.le.{0}\n"
    "    (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} 2 (Fintype.card.{u_2} α))\n"
    "      (Finset.card.{u_2} (Finset.certificator.{u_2} 𝒜 ℬ)))\n"
    "    (HMul.hMul.{0, 0, 0} (Finset.card.{u_2} 𝒜) (Finset.card.{u_2} ℬ))"
)

LAKE_MANIFEST_NOTICE_RE = re.compile(
    r"^warning: manifest out of date: git revision of dependency '(?:AddCombi|mathlib)' changed;"
    r" use `lake update (?:AddCombi|mathlib)` to update it$"
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
    print(f"CHECK_ERROR: {msg}")
    print("FAIL")
    sys.exit(1)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_lcc_checkout(path: str) -> bool:
    return (
        bool(path)
        and os.path.isdir(path)
        and os.path.isfile(os.path.join(path, "CamCombi.lean"))
        and os.path.isfile(os.path.join(path, "CamCombi", "PlainCombi", "VanDenBergKesten.lean"))
        and os.path.isfile(os.path.join(path, "lake-manifest.json"))
        and os.path.isfile(os.path.join(path, "lean-toolchain"))
    )


def locate_lcc_root(pkg_root: str) -> str:
    env_root = os.environ.get("LEANCAMCOMBI_ROOT", "").strip()
    if is_lcc_checkout(env_root):
        return os.path.abspath(env_root)

    rel_candidates = [
        os.path.join(pkg_root, "..", "..", "fc-work", "LeanCamCombi"),
        os.path.join(pkg_root, "..", "..", "..", "fc-work", "LeanCamCombi"),
        os.path.join(pkg_root, "..", "fc-work", "LeanCamCombi"),
        os.path.join(os.getcwd(), "LeanCamCombi"),
        os.path.join(os.getcwd(), "..", "fc-work", "LeanCamCombi"),
    ]
    for cand in rel_candidates:
        if is_lcc_checkout(cand):
            return os.path.abspath(cand)

    home = os.path.expanduser("~")
    if os.path.isdir(home):
        q = deque([(home, 0)])
        while q:
            cur, depth = q.popleft()
            if is_lcc_checkout(cur):
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

    fail("Could not locate LeanCamCombi Lake checkout (set LEANCAMCOMBI_ROOT if needed)")
    return ""


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
        "addcombi_rev",
        "expected_check_prefix",
        "allowed_axioms",
    ]
    for k in req_keys:
        if k not in manifest:
            fail(f"Missing key '{k}' in object/proof_manifest.json")

    if manifest["target_id"] != "leancamcombi-bkr-reimer-inequality":
        fail("Unexpected target_id in manifest")
    if manifest["solution_file"] != "VanDenBergKesten.lean":
        fail("Unexpected solution_file in manifest")
    if set(manifest["allowed_axioms"]) != ALLOWED_AXIOMS or len(manifest["allowed_axioms"]) != 3:
        fail("Tampered allowed_axioms in manifest")

    sol_path = os.path.join(pkg_root, "object", manifest["solution_file"])
    if not os.path.isfile(sol_path):
        fail("Missing object/VanDenBergKesten.lean")

    with open(sol_path, "rb") as f:
        sol_bytes = f.read()

    actual_sol_sha = sha256_bytes(sol_bytes)
    if actual_sol_sha != manifest["solution_sha256"]:
        fail(
            f"SHA-256 mismatch on object/VanDenBergKesten.lean: "
            f"expected {manifest['solution_sha256']}, got {actual_sol_sha}"
        )
    if len(sol_bytes) != manifest["solution_bytes"]:
        fail(
            f"Byte length mismatch on object/VanDenBergKesten.lean: "
            f"expected {manifest['solution_bytes']}, got {len(sol_bytes)}"
        )

    sol_text = sol_bytes.decode("utf-8")
    print(f"[1/5] Manifest & object integrity verified: sha256={actual_sol_sha} ({len(sol_bytes)} bytes)")

    stripped_sol = strip_lean_comments(sol_text)
    for tok in FORBIDDEN_TOKENS:
        if re.search(rf"\b{re.escape(tok)}\b", sol_text) or re.search(rf"\b{re.escape(tok)}\b", stripped_sol):
            fail(f"Forbidden token '{tok}' present in object/VanDenBergKesten.lean")

    pub_imports = re.findall(r"(?m)^\s*public\s+import\s+(\S+)", stripped_sol)
    if pub_imports != EXPECTED_PUBLIC_IMPORTS:
        fail(f"Public imports changed from upstream: found {pub_imports}")

    priv_imports = re.findall(r"(?m)^\s*import\s+(\S+)", stripped_sol)
    for imp in priv_imports:
        if not imp.startswith("Mathlib."):
            fail(f"Disallowed non-Mathlib private import: {imp}")

    print("[2/5] Forbidden-token & public-import hygiene audit passed (0 forbidden tokens)")

    lcc_root = locate_lcc_root(pkg_root)

    with open(os.path.join(lcc_root, "lean-toolchain"), "r", encoding="utf-8") as f:
        tc = f.read().strip()
    if tc != manifest["lean_toolchain"]:
        fail(f"Toolchain mismatch: expected {manifest['lean_toolchain']}, got {tc}")

    with open(os.path.join(lcc_root, "lake-manifest.json"), "r", encoding="utf-8") as f:
        lake_manifest = json.load(f)
    pkgs_by_name = {p.get("name"): p for p in lake_manifest.get("packages", [])}
    if pkgs_by_name.get("mathlib", {}).get("rev") != manifest["mathlib_rev"]:
        fail("mathlib revision in lake-manifest.json does not match manifest")
    if pkgs_by_name.get("AddCombi", {}).get("rev") != manifest["addcombi_rev"]:
        fail("AddCombi revision in lake-manifest.json does not match manifest")

    if os.path.isdir(os.path.join(lcc_root, ".git")) and shutil.which("git"):
        head = subprocess.run(
            ["git", "-C", lcc_root, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if head.returncode != 0 or head.stdout.strip() != manifest["upstream_commit"]:
            fail(
                f"LeanCamCombi HEAD mismatch: expected {manifest['upstream_commit']}, "
                f"got {head.stdout.strip()}"
            )

    up_lcc_path = os.path.join(lcc_root, manifest["upstream_relpath"])
    if not os.path.isfile(up_lcc_path):
        fail(f"Upstream file {manifest['upstream_relpath']} missing in LeanCamCombi checkout")
    with open(up_lcc_path, "rb") as f:
        up_bytes = f.read()
    if sha256_bytes(up_bytes) != manifest["upstream_sha256"]:
        fail("Upstream VanDenBergKesten.lean SHA-256 mismatch against manifest")

    local_data_up = os.path.join(pkg_root, "data", "VanDenBergKesten.lean")
    if os.path.isfile(local_data_up):
        with open(local_data_up, "rb") as f:
            local_up_bytes = f.read()
        if sha256_bytes(local_up_bytes) != manifest["upstream_sha256"]:
            fail("Local data/VanDenBergKesten.lean SHA-256 mismatch against manifest")

    up_text = up_bytes.decode("utf-8")
    if "lemma card_certificator_le : 2 ^ Fintype.card α * #(𝒜 □ ℬ) ≤ #𝒜 * #ℬ := sorry" not in up_text:
        fail("Upstream VanDenBergKesten.lean does not contain unclaimed 'card_certificator_le := sorry'")

    # Verbatim diff checks of all three upstream blocks
    b1_end = up_text.index("\n/-!")
    if not sol_text.startswith(up_text[:b1_end]):
        fail("Header / module / public imports do not match upstream verbatim")

    b2_start = up_text.index("/-!")
    b2_end = up_text.index("end BooleanAlgebra") + len("end BooleanAlgebra")
    if up_text[b2_start:b2_end] not in sol_text:
        fail("Module docstring or BooleanAlgebra section (certificator definition & lemmas) modified")

    b3_start = up_text.index("open scoped FinsetFamily", b2_end)
    b3_end = up_text.index(":= sorry", b3_start) + 2
    if up_text[b3_start:b3_end] not in sol_text:
        fail("card_certificator_le docstring or statement signature modified from upstream")

    if not sol_text.rstrip().endswith("end Finset"):
        fail("Solution file must end with 'end Finset'")

    print(
        f"[3/5] Upstream pinned environment & verbatim diff verified "
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
        check_file = os.path.join(td, "VerifyVanDenBergKesten.lean")
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
            "-Dpp.unicode.fun=true",
            "-DautoImplicit=false",
            "-DrelaxedAutoImplicit=false",
            "-Dweak.linter.mathlibStandardSet=true",
            "-Dweak.linter.style.header=false",
            "-Dwarn.sorry=true",
            check_file,
        ]
        proc = subprocess.run(cmd, cwd=lcc_root, env=env, capture_output=True, text=True, timeout=600)

    if proc.returncode != 0:
        fail(f"Lean kernel compilation failed with exit code {proc.returncode}")

    unexpected_stderr = [
        ln for ln in proc.stderr.splitlines()
        if ln.strip() and not LAKE_MANIFEST_NOTICE_RE.match(ln.strip())
    ]
    if unexpected_stderr:
        fail(f"Lean emitted unexpected stderr diagnostics: {unexpected_stderr[0][:120]}")

    out = proc.stdout
    for diag_line in out.splitlines():
        if ": warning:" in diag_line or ": error" in diag_line:
            fail(f"Lean compiler/linter diagnostic present: {diag_line[:120]}")

    if manifest["expected_check_prefix"] not in out or EXPECTED_FULL_CHECK not in out:
        fail(f"Kernel #check type output did not match exact canonical signature for {thm_full}")

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

    print("[4/5] Lean 4 kernel & mathlibStandardSet linter build succeeded (exit=0, warnings=0)")
    print(f"[5/5] Axiom audit passed: '{thm_full}' depends on axioms: {axioms}")
    print("PASS")


if __name__ == "__main__":
    main()
