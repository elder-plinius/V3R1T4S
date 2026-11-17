#!/usr/bin/env python3
"""Check a candidate Lean proof of a frozen statement against Physlib. Python standard library only.

  python3 -I lean_claim_check.py --physlib DIR --spec SPEC.lean --candidate CANDIDATE.lean

SPEC.lean   defines `V3R1T4S.spec : Prop` (imports Physlib only). It is compiled first, on its own, so the
            statement's meaning (instances, notation) is fixed before the candidate is ever loaded.
CANDIDATE   imports V3R1T4SSpec (and Physlib/Mathlib) and proves `theorem V3R1T4S.claim : V3R1T4S.spec`.

PASS needs: both files compile with no error and no `sorry`; the candidate passes a source policy (no axioms,
instances, notation, meta code or kernel-check options); `theorem check : V3R1T4S.spec := V3R1T4S.claim`
elaborates in a fresh file; and `#print axioms check` lists only propext, Classical.choice, Quot.sound.
Last line: PASS or FAIL.
"""
import argparse, os, re, shutil, subprocess, sys, tempfile

ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
# words that let a file change the meaning of the statement or bypass the kernel; a plain proof needs none of them
FORBIDDEN = [r"\baxiom\b", r"\binstance\b", r"\battribute\b", r"\bnotation\b", r"\bmacro\b", r"\bsyntax\b",
             r"\belab\b", r"\brun_cmd\b", r"\brun_elab\b", r"\brun_meta\b", r"#eval", r"\binitialize\b",
             r"\bunsafe\b", r"\bimplemented_by\b", r"\bextern\b", r"\bopaque\b", r"native_decide",
             r"set_option\s+(debug|trust)", r"skipKernelTC", r"addDecl", r"\bsorry\b", r"\badmit\b",
             r"(def|abbrev|theorem|lemma)\s+V3R1T4S\.spec\b"]


def run(cmd, cwd, env=None, timeout=1800):
    r = subprocess.run(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def lean(physlib, tmp, args):
    # `lake env` supplies Physlib's LEAN_PATH; the temporary folder is prepended so V3R1T4SSpec/V3R1T4SClaim resolve
    script = 'LEAN_PATH="%s:$LEAN_PATH" exec lean --root="%s" "$@"' % (tmp, tmp)
    return run(["lake", "env", "sh", "-c", script, "lean"] + args, cwd=physlib)


def bad_output(out):
    return re.search(r"(?m)(^|\s)error(\(|:)", out) or "declaration uses 'sorry'" in out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--physlib", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--candidate", required=True)
    a = ap.parse_args()
    problems = []
    src = open(a.candidate, encoding="utf-8").read()
    code = re.sub(r"--[^\n]*|/-.*?-/", "", src, flags=re.S)          # policy applies to code, not comments
    for pat in FORBIDDEN:
        if re.search(pat, code):
            problems.append("candidate source uses forbidden construct /%s/" % pat)
    for imp in re.findall(r"(?m)^\s*(?:public\s+)?import\s+(\S+)", code):
        if not (imp == "V3R1T4SSpec" or imp.split(".")[0] in ("Physlib", "Mathlib", "QuantumInfo")):
            problems.append("candidate imports %s (only Physlib, Mathlib, QuantumInfo, V3R1T4SSpec)" % imp)
    scratch = os.path.join(os.path.dirname(os.path.abspath(a.physlib)), "tmp")   # lean/tmp, inside the workspace
    os.makedirs(scratch, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="claim_", dir=scratch)
    try:
        shutil.copy(a.spec, os.path.join(tmp, "V3R1T4SSpec.lean"))
        shutil.copy(a.candidate, os.path.join(tmp, "V3R1T4SClaim.lean"))
        rc, out = lean(a.physlib, tmp, ["-o", os.path.join(tmp, "V3R1T4SSpec.olean"), os.path.join(tmp, "V3R1T4SSpec.lean")])
        print("spec compile: exit %d" % rc)
        if rc != 0 or bad_output(out):
            print(out[-3000:])
            problems.append("spec does not compile cleanly")
        rc, out = lean(a.physlib, tmp, ["-o", os.path.join(tmp, "V3R1T4SClaim.olean"), os.path.join(tmp, "V3R1T4SClaim.lean")])
        print("candidate compile: exit %d" % rc)
        if rc != 0 or bad_output(out):
            print(out[-3000:])
            problems.append("candidate does not compile cleanly")
        if not problems:
            with open(os.path.join(tmp, "Check.lean"), "w") as f:
                f.write("import V3R1T4SSpec\nimport V3R1T4SClaim\n\n"
                        "theorem V3R1T4S_check : V3R1T4S.spec := V3R1T4S.claim\n\n#print axioms V3R1T4S_check\n")
            rc, out = lean(a.physlib, tmp, [os.path.join(tmp, "Check.lean")])
            print("check file: exit %d" % rc)
            print(out.strip()[-2000:])
            if rc != 0 or bad_output(out):
                problems.append("V3R1T4S.claim does not prove V3R1T4S.spec")
            else:
                m = re.search(r"depends on axioms: \[(.*?)\]", out, re.S)
                axioms = {x.strip() for x in m.group(1).split(",")} if m else set()
                if "does not depend on any axioms" in out:
                    axioms = set()
                elif not m:
                    problems.append("could not read #print axioms output")
                extra = sorted(axioms - ALLOWED_AXIOMS)
                print("axioms: %s" % (sorted(axioms) or "none"))
                if extra:
                    problems.append("non-standard axioms: %s" % ", ".join(extra))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for p in problems:
        print("problem: " + p)
    print("FAIL" if problems else "PASS")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
