#!/usr/bin/env python3
"""Deterministic structural & dependency audit of Solutions/ZetaHadamard.v1."""
import hashlib
import json
import os
import re
import sys

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


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    attack_root = os.path.abspath(os.path.join(here, "..", "..", ".."))
    obj_root = os.path.join(attack_root, "object")
    manifest_path = os.path.join(obj_root, "proof_manifest.json")

    with open(manifest_path, "rb") as f:
        mbytes = f.read()
    msha = hashlib.sha256(mbytes).hexdigest()
    manifest = json.loads(mbytes.decode("utf-8"))

    print("=== Constructor Lens Audit: Solutions/ZetaHadamard.v1 ===")
    print("Manifest SHA-256: %s (%d bytes)" % (msha, len(mbytes)))
    print("Target theorem  : %s" % manifest["theorem_name"])
    print("Challenge module: %s" % manifest["challenge_module"])
    print("Lean toolchain  : %s" % manifest["lean_toolchain"])
    print("Mathlib rev     : %s" % manifest["mathlib_rev"])
    print()

    sol_dir = os.path.join(obj_root, "Solutions", "ZetaHadamard.v1")
    local_modules = set()
    for entry in manifest["files"]:
        rel_p = entry["path"]
        full_p = os.path.join(obj_root, rel_p)
        data = open(full_p, "rb").read()
        sha = hashlib.sha256(data).hexdigest()
        assert len(data) == entry["bytes"], "Byte mismatch on " + rel_p
        assert sha == entry["sha256"], "SHA-256 mismatch on " + rel_p
        if rel_p.endswith(".lean"):
            local_modules.add(os.path.splitext(os.path.basename(rel_p))[0])

    total_lines = 0
    total_decls = 0
    dag_edges = {}
    print("%-22s %6s %6s %6s  %s" % ("Module", "Lines", "Bytes", "Decls", "SHA-256 (prefix)"))
    print("-" * 72)

    for entry in manifest["files"]:
        rel_p = entry["path"]
        if not rel_p.endswith(".lean"):
            continue
        mod = os.path.splitext(os.path.basename(rel_p))[0]
        full_p = os.path.join(obj_root, rel_p)
        raw = open(full_p, "r", encoding="utf-8").read()
        clean = strip_lean_comments(raw)

        for tok in FORBIDDEN_TOKENS:
            if re.search(r"\b" + re.escape(tok) + r"\b", raw) or re.search(
                r"\b" + re.escape(tok) + r"\b", clean
            ):
                print("FAIL: forbidden token %s in %s" % (tok, rel_p))
                sys.exit(1)

        imports = re.findall(r"(?m)^\s*import\s+(\S+)", clean)
        local_deps = []
        for imp in imports:
            if imp in local_modules:
                local_deps.append(imp)
            elif imp == "IEANTN.Nodes.ZetaHadamard.v1.Conclusions":
                assert mod == "Solution", "Only Solution may import Conclusions"
            elif imp == "IEANTN.Vocabulary.Zeta" or imp.startswith("Mathlib."):
                pass
            else:
                print("FAIL: disallowed import %s in %s" % (imp, rel_p))
                sys.exit(1)
        dag_edges[mod] = local_deps

        lines = len(raw.splitlines())
        decls = len(
            re.findall(
                r"(?m)^\s*(?:private\s+|noncomputable\s+|protected\s+)*(?:lemma|theorem|def|abbrev)\s+",
                clean,
            )
        )
        total_lines += lines
        total_decls += decls
        print("%-22s %6d %6d %6d  %s" % (mod + ".lean", lines, entry["bytes"], decls, entry["sha256"][:16]))

    # Verify acyclicity of local module DAG
    visiting = set()
    visited = set()

    def dfs(u):
        assert u not in visiting, "Cycle in local module imports at " + u
        if u in visited:
            return
        visiting.add(u)
        for v in dag_edges.get(u, []):
            dfs(v)
        visiting.remove(u)
        visited.add(u)

    for m in sorted(local_modules):
        dfs(m)

    sol_clean = strip_lean_comments(open(os.path.join(sol_dir, "Solution.lean"), "r", encoding="utf-8").read())
    assert "theorem ZetaHadamard.v1.challenge_logDeriv_partial_fractions" in sol_clean

    print("-" * 72)
    print("Lean modules    : %d (DAG acyclic: True)" % len(local_modules))
    print("Total Lean lines: %d" % total_lines)
    print("Total decls     : %d" % total_decls)
    print("Forbidden tokens: 0")
    print("Audit verdict   : PASS")


if __name__ == "__main__":
    main()
