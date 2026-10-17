"""Synthetic test doubles only. Never imports or executes repository checker code."""
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import sys

name = Path(sys.argv[0]).name
args = sys.argv[1:]
family = os.environ["PROBE_FAMILY"]
root = os.environ["PROBE_ROOT"]


def finish(code, stdout="", stderr="", role=""):
    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)
    record = {
        "command": name,
        "args": [a.replace(root, "<fixture>") for a in args],
        "role": role,
        "exit": code,
        "stdout": stdout.replace(root, "<fixture>"),
        "stderr": stderr.replace(root, "<fixture>"),
    }
    with open(os.environ["PROBE_TRACE"], "a") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")
    sys.exit(code)


def control(kind):
    mode = os.environ.get("CONTROL_MODE", "reject")
    if mode == "accept":
        finish(0, f"{kind} PASS SYNTHETIC control unexpectedly accepted", role="negative-control")
    if mode in ("infra", "infra_exit1"):
        code = 2 if mode == "infra" else 1
        finish(code, stderr="Traceback (most recent call last):\nRuntimeError: synthetic infrastructure failure", role="negative-control")
    if kind == "DDCHECK":
        far = "2" if mode == "wrong_near_count" and "near_miss" in args[0] else "4"
        if mode == "zero_far":
            far = "0"
        file = args[0] + (".wrong" if mode == "wrong_identity" else "")
        loops = "1" if mode == "bad_structure" else "0"
        out = (f"file={file}\nN=3 edges=3 loops={loops} duplicates=0 unused_labels=0 mindeg=2 maxdeg=2 (DELTA={args[1]}, D={args[2]})\n"
               f"ordered_pairs_at_distance_gt_{args[2]}={far} (of 9)\nINVALID")
        if mode == "early_invalid":
            out = "no edges: INVALID"
    elif kind == "FMMCHECK":
        path = Path(args[1]); sha = hashlib.sha256(path.read_bytes()).hexdigest()
        file = path.name + (".wrong" if mode == "wrong_identity" else "")
        if mode == "wrong_hash":
            sha = "0" * 64
        bad = "0" if mode == "no_semantic_failure" else "1"
        primes = [1048573, 1048571, 1048559, 1048549]
        if mode == "incomplete_mods":
            primes.pop()
        out = "\n".join(f"  mod {prime}: violated Brent equations = {bad}" for prime in primes)
        if mode != "missing_proof":
            out += "\n  checked 182*210*195 = 7452900 Brent equations modulo 4 primes; log2(prod primes) = 80.0 > log2(2 L (S+1)) = 4.0"
        out += f"\nFMMCHECK FAIL file={file} format=<13,14,15> sorted=<13,14,15> terms=1 rank_nonzero_terms=1 sha256={sha}"
        if mode == "incomplete_fail":
            finish(1, "  mod 1048573: violated Brent equations = 1", "FMMCHECK FAIL non-exact floating point product", role="negative-control")
    else:
        idx = args[args.index("--instance") + 1]
        path = Path(args[args.index("--witness") + 1]); mode_name = path.stem
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        if mode == "wrong_hash":
            sha = "0" * 64
        show_idx = "178" if mode == "wrong_identity" and idx == "1703" else idx
        exact = "False" if mode == "f32_false" else "True"
        strict = "True" if mode_name == "centre" else "False"
        output = "False" if mode_name == "centre" else "True"
        if mode == "no_semantic_failure":
            strict = output = "True"
        pin = "MISMATCH" if mode == "hash_mismatch" else "(pinned)"
        out = "\n".join(f"  {label} sha256 {'a' * 64} {pin}" for label in ("onnx.gz", "onnx", "vnnlib.gz", "vnnlib"))
        if mode == "missing_pins":
            out = ""
        out += ("\n  property: 5400 input assertions, 1 output assertion(s); all 2700 coordinates bounded above and below: True"
                f"\n  witness sha256 {sha}; every value exactly representable in float32: {exact}"
                f"\n  input box, exact rationals, strict: {strict}; smallest distance to a bound = 0 = 0.0"
                f"\n  onnxruntime 1.0 CPU float32: output assertion holds at zero tolerance: {output}; margin 0.0; argmax 0")
        witness = os.path.relpath(path, root)
        if mode == "wrong_witness":
            witness += ".wrong"
        out += (f"\nVNNCHECK FAIL instance=3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30/model_30_idx_{show_idx}_eps_1.00000"
                f" margin=0.0 min_input_slack=0.0 witness={witness}")
        if mode == "incomplete_fail":
            out = "VNNCHECK FAIL"
    stderr = "Traceback (most recent call last):\nRuntimeError: synthetic late exception" if mode == "late_traceback" else ""
    if mode == "optional_warning":
        stderr = "onnxruntime warning: optional accelerator unavailable"
    finish(1, out, stderr, role="negative-control")


if name == "cc":
    # A compiler is NEVER invoked: copy this dispatcher as the fake executable.
    assert family == "biggest-graphs" and args[:2] == ["-O3", "-o"]
    dest = Path(args[2])
    assert dest.is_relative_to(Path(root))
    shutil.copyfile(os.environ["PROBE_MOCK"], dest)
    dest.chmod(0o700)
    finish(0, role="mock-compiler-copied-stub")

if name == "sha256sum":
    assert family == "biggest-graphs"
    # Graph wrapper has literal release hashes. Stub only this integrity layer,
    # so synthetic files can reach the exact unchanged control-flow branches.
    expected = {
        "G_9_4_n1700.edges": "d271a1e84aa9539ba47f8d036cd15e4a5a9ccc5a4752d0dacc94a9d35f17eebd",
        "G_15_3_n1620.edges.txt": "da9faa8c8a875ac789506ca3f91a45db37b3f1f3952b729c88199557caa792ce",
        "G_14_4_n8424.edges.txt": "71ef820b5804f77c626209fbcda3a8bd50c546a5fb70175cbe36a9f98f22f281",
        "G_15_4_n13365.edges": "2d36814028c63e32e527fc0f88ac08cbc70be134f8786de4867c58d748dae52f",
        "G_13_4_n6630.edges": "7c44e128901d6dd6b64e0574b90ff8aa21872462338fd267bab466cb268e10a4",
    }
    value = expected[Path(args[0]).name]
    if os.environ.get("HASH_FAIL") == "1":
        value = "0" * 64
    finish(0, value + "  " + Path(args[0]).name, role="mock-literal-release-hash")

if name == "ddcheck":
    basename = Path(args[0]).name
    positive_d = "3" if basename == "G_15_3_n1620.edges.txt" else "4"
    if basename.startswith("near_miss") or args[2] != positive_d:
        control("DDCHECK")
    if os.environ.get("POSITIVE_FAIL") == "1":
        finish(1, "INVALID synthetic positive failure", role="positive-check")
    finish(0, "VALID synthetic positive", role="positive-check")

assert name == "python3", name
script = Path(args[0]).name
if script == "check_harness_contract.py":
    assert Path(args[0]).resolve() == (Path(root).parent / "check_harness_contract.py").resolve()
    # Execute ONLY the new reviewed stdlib orchestration parser, never a scientific checker.
    sys.argv = args
    try:
        runpy.run_path(args[0], run_name="__main__")
    except SystemExit as exc:
        finish(int(exc.code or 0), role="contract-helper")
    finish(0, role="contract-helper")
if script == "ddcheck.py":
    finish(0, "VALID synthetic numpy-checker stub", role="positive-check")
if script in ("cwcheck.py", "delsarte_check.py"):
    if os.environ.get("POSITIVE_FAIL") == "1":
        finish(1, "INVALID synthetic positive failure", role="positive-check")
    finish(0, "VALID synthetic " + script, role="positive-check")
if script == "fmmcheck.py":
    path = Path(args[1])
    if path.parent.name == "schemes":
        rank = re.search(r"_r(\d+)_", path.name).group(1)
        code = int(os.environ.get("POSITIVE_FAIL") == "1")
        finish(code, "FMMCHECK " + ("FAIL" if code else "PASS") +
               f" synthetic rank_nonzero_terms={rank} sha256=synthetic", role="positive-check")
    if not path.is_file():
        finish(2, stderr="FileNotFoundError: synthetic mutant was not generated", role="negative-control")
    control("FMMCHECK")
if script == "vnncheck.py":
    if "--witness" in args:
        witness = Path(args[args.index("--witness") + 1])
        if not witness.is_file():
            finish(2, stderr="FileNotFoundError: synthetic mutant was not generated", role="negative-control")
        control("VNNCHECK")
    code = int(os.environ.get("POSITIVE_FAIL") == "1")
    finish(code, "VNNCHECK " + ("FAIL" if code else "PASS") + " synthetic positive", role="positive-check")
if script == "mutate.py":
    if os.environ.get("MUTATE_FAIL") == "1":
        finish(2, stderr="RuntimeError: synthetic mutation infrastructure failure", role="mutator")
    target = Path(args[-1])
    assert target.is_relative_to(Path(root))
    target.mkdir(parents=True, exist_ok=True)
    names = (["drop_term.json", "bump_coeff.json", "swap_vw.json"]
             if family == "faster-matrix-multiplication"
             else ["on_bound.txt", "outside.txt", "centre.txt"])
    for item in names:
        if os.environ.get("MUTATE_MISSING") == "1" and item == names[-1]:
            continue
        (target / item).write_text("SYNTHETIC MUTANT, NOT SCIENTIFIC DATA\n")
    finish(0, role="mutator")
raise AssertionError("Unreviewed mock command: " + script)
