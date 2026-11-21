#!/usr/bin/env python3
"""Regress candidate wrapper contracts using synthetic scientific test doubles.

Run: python3 known-knowns/tests/harness_contracts/run_regressions.py
Requirements: Python >= 3.9, a POSIX shell, standard local coreutils.
No network, dependencies, real checker execution, compilation, or repository edits.
"""
import argparse
import csv
import io
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3],
                    help="Repository root whose wrappers and helper should be tested")
parser.add_argument("--output", type=Path, help="Capture/result directory (default: bundle directory)")
parser.add_argument("--implementation", choices=("candidate", "baseline"), default="candidate")
options = parser.parse_args()
BASE = Path(__file__).resolve().parent
REPO = options.repo.resolve()
OUTPUT_BASE = (options.output or (BASE / ("results-" + options.implementation))).resolve()
OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
OUT = OUTPUT_BASE / "captures"
OUT.mkdir(exist_ok=True)
PROVENANCE = json.loads((BASE / "wrapper-provenance.json").read_text())
MOCK_BODY = (BASE / "mock_command.py").read_text()
RESULTS = []
TIMEOUT = 5


def put(root, relative, text):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture(root, family, variant):
    if family == "biggest-graphs":
        for filename in ["G_9_4_n1700.edges", "G_15_3_n1620.edges.txt",
                         "G_14_4_n8424.edges.txt", "G_15_4_n13365.edges", "G_13_4_n6630.edges"]:
            put(root, "graphs/" + filename, "SYNTHETIC GRAPH PLACEHOLDER\n")
        put(root, "how-we-built-it/13_4/near_miss_N6630_cost2.edges", "SYNTHETIC NEAR MISS\n")
    elif family == "bigger-codes":
        inventory = json.loads((BASE / "fixture_inventory.json").read_text())
        for category, index in [("codes", "INDEX.csv"), ("certificates", "INDEX_delsarte.csv")]:
            rows = []
            for entry in inventory[category]:
                row = dict(entry)
                row["cell"] = "A(" + ",".join(row[k] for k in ("n", "d", "w")) + ")"
                row["credit"] = "Synthetic, quoted-comma fixture"
                row["sha256"] = put(root, row["file"], "SYNTHETIC DATA " + row["file"] + "\n")
                rows.append(row)
            if category == "codes":
                if variant == "duplicate_index":
                    rows.append(dict(rows[0]))
                elif variant == "unsafe_index_path":
                    rows[-1]["file"] = "../outside.txt"
                elif variant == "missing_index_row":
                    rows.pop()
                elif variant == "metadata_mismatch":
                    rows[-1]["M"] = "999"
            out = io.StringIO(newline="")
            writer = csv.DictWriter(out, fieldnames=["cell", "n", "d", "w", "M", "credit", "file", "sha256"], lineterminator="\r\n" if variant == "crlf_inventory" else "\n")
            writer.writeheader(); writer.writerows(rows)
            put(root, index, out.getvalue())
        if variant == "contributed_sibling_package":
            # A contributed package is separate from the original 30+5 release.
            package = "2026-10-14-freelsgood-9e824e9f/"
            put(root, package + "codes/A27_6_10_13026.txt", "SYNTHETIC CONTRIBUTED CODE\n")
            put(root, package + "INDEX.csv", "SYNTHETIC SEPARATE PACKAGE INDEX\n")
        if variant == "missing_unrequired_code":
            (root / "codes/A25_6_11_8718.txt").unlink()
        if variant == "missing_indexed_certificate":
            (root / "certificates/cert_A32_12_16.json").unlink()
        if variant == "missing_required_code":
            (root / "codes/A29_6_11_41219.txt").unlink()
        if variant == "hash_mismatch":
            put(root, "codes/A25_6_11_8718.txt", "SYNTHETIC MODIFIED CODE\n")
        if variant == "unexpected_file":
            put(root, "codes/A7_4_3_7.txt", "SYNTHETIC EXTRA\n")
        if variant == "malformed_csv":
            with (root / "INDEX.csv").open("a") as f:
                f.write('"unterminated synthetic row')
        if variant == "missing_index":
            (root / "INDEX.csv").unlink()
        if variant == "symlink_index":
            (root / "INDEX.csv").rename(root / "INDEX-copy.csv")
            (root / "INDEX.csv").symlink_to("INDEX-copy.csv")
        if variant == "symlink_file":
            (root / "codes/A25_6_11_8718.txt").unlink()
            (root / "codes/A25_6_11_8718.txt").symlink_to("A25_6_12_9895.txt")
        if variant == "symlink_directory":
            (root / "codes").rename(root / "codes-original")
            (root / "codes").symlink_to("codes-original", target_is_directory=True)
    elif family == "faster-matrix-multiplication":
        files = ["13x14x14_r1558_Q.json", "13x14x15_r1677_Q.json", "14x14x15_r1716_Q.json",
                 "14x15x15_r1842_Q.json", "15x16x16_r2180_Q.json",
                 "14x15x15_r1843_Q.json", "15x16x16_r2196_Q.json"]
        lines = ["format,field,rank,path,sha256"]
        for name in files:
            digest = put(root, "schemes/" + name, '{"synthetic":"' + name + '"}\n')
            rank = name.split("_r")[1].split("_")[0]
            lines.append("synthetic,Q," + rank + ",schemes/" + name + "," + digest)
        put(root, "INDEX.csv", "\n".join(lines) + "\n")
    elif family == "vnncomp-2026-unsolved-instances":
        lines = ["path,sha256"]
        for idx in [1703, 178]:
            for kind in ["plain", "v2"]:
                name = f"witnesses/model_30_idx_{idx}_eps_1/witness_{kind}.txt"
                digest = put(root, name, "SYNTHETIC WITNESS " + name + "\n")
                lines.append(name + "," + digest)
        put(root, "INDEX.csv", "\n".join(lines) + "\n")
    else:
        raise AssertionError(family)


def run_case(family, variant, expected_exit, overrides=None, assertions=None):
    entry = next(e for e in PROVENANCE["wrappers"] if family in e["path"])
    baseline = (BASE / "baseline" / entry["path"]).read_bytes()
    assert hashlib.sha256(baseline).hexdigest() == entry["sha256"]
    assert hashlib.sha1(b"blob " + str(len(baseline)).encode() + b"\0" + baseline).hexdigest() == entry["git_blob_sha1"]
    source = ((REPO if options.implementation == "candidate" else BASE / "baseline") / entry["path"]).read_bytes()
    case = family + "__" + variant
    capture = OUT / case
    capture.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="veritas-synthetic-") as temporary:
        root = Path(temporary) / "known-knowns" / family
        root.mkdir(parents=True)
        if variant != "missing_shared_helper":
            shutil.copyfile(REPO / "known-knowns/check_harness_contract.py", root.parent / "check_harness_contract.py")
        fixture(root, family, variant)
        fixture_files = sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())
        fixture_indices = {p.name: p.read_text() for p in root.glob("INDEX*.csv")}
        wrapper = root / "verify-it-yourself/run_checks.sh"
        wrapper.parent.mkdir(exist_ok=True)
        wrapper.write_bytes(source)  # selected pinned baseline or separately patched candidate
        bindir = root / "bin"
        bindir.mkdir()
        mock = bindir / "mock-dispatch"
        mock.write_text("#!" + sys.executable + "\n" + MOCK_BODY)
        mock.chmod(0o700)
        # Only reviewed local utilities are visible; no network or actual
        # compiler/interpreter command is accessible through this PATH.
        allowed = ["dirname", "mkdir", "basename", "sed", "grep", "cut", "tail", "rm"]
        if family != "biggest-graphs":
            allowed.append("sha256sum")
        for utility in allowed:
            resolved = shutil.which(utility)
            if resolved is None:
                raise RuntimeError("Missing prerequisite: " + utility)
            (bindir / utility).symlink_to(resolved)
        (bindir / "python3").symlink_to(mock)
        if family == "biggest-graphs":
            (bindir / "cc").symlink_to(mock)
            (bindir / "sha256sum").symlink_to(mock)
        (root / "tmp").mkdir()
        tracefile = root / "mock-trace.jsonl"
        env = {"PATH": str(bindir), "HOME": str(root), "TMPDIR": str(root / "tmp"),
               "LC_ALL": "C", "BIG": "0", "OFFICIAL": "0", "THREADS": "1",
               "PROBE_ROOT": str(root), "PROBE_FAMILY": family,
               "PROBE_TRACE": str(tracefile), "PROBE_MOCK": str(mock)}
        env.update(overrides or {})
        shell = shutil.which("sh")
        if shell is None:
            raise RuntimeError("Missing prerequisite: sh")
        started = time.monotonic()
        process = subprocess.Popen([shell, str(wrapper)], cwd=root, env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, start_new_session=True)
        timed_out = False
        try:
            stdout, stderr = process.communicate(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            timed_out = True
            # Only the process group created immediately above is killed.
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
        duration = round(time.monotonic() - started, 4)
        stdout = stdout.replace(str(root), "<fixture>")
        stderr = stderr.replace(str(root), "<fixture>")
        trace = [json.loads(line) for line in tracefile.read_text().splitlines()] if tracefile.exists() else []
        checks = [{"check": "wrapper exit equals expected", "pass": process.returncode == expected_exit},
                  {"check": "completed within 5-second process timeout", "pass": not timed_out}]
        expected_summary = "ALL CHECKS PASSED" if expected_exit == 0 else "SOME CHECK FAILED"
        if expected_exit in (0, 1):
            checks.append({"check": "aggregate summary equals expected", "pass": expected_summary in stdout})
        for description, predicate in assertions or []:
            checks.append({"check": description, "pass": bool(predicate(stdout, stderr, trace))})
        result = {"case": case, "wrapper_source": entry["path"], "variant": variant,
                  "wrapper_sha256": hashlib.sha256(source).hexdigest(),
                  "contract_helper_sha256": hashlib.sha256((REPO / "known-knowns/check_harness_contract.py").read_bytes()).hexdigest(),
                  "expected_exit": expected_exit, "exit": process.returncode,
                  "duration_seconds": duration, "timeout_seconds": TIMEOUT,
                  "timed_out": timed_out, "environment_overrides": overrides or {},
                  "fixture_files": fixture_files, "fixture_indices": fixture_indices,
                  "assertions": checks, "all_assertions_passed": all(c["pass"] for c in checks),
                  "stdout": stdout, "stderr": stderr, "mock_calls": trace}
        (capture / "stdout.txt").write_text(stdout)
        (capture / "stderr.txt").write_text(stderr)
        (capture / "mock-trace.jsonl").write_text("".join(json.dumps(t, sort_keys=True) + "\n" for t in trace))
        (capture / "result.json").write_text(json.dumps(result, indent=2) + "\n")
        RESULTS.append(result)
        print(f"{'PASS' if result['all_assertions_passed'] else 'FAIL'} {case}: wrapper exit={process.returncode}", flush=True)


def controls_have(count, code):
    return lambda out, err, trace: len([t for t in trace if t["role"] == "negative-control"]) == count and all(
        t["exit"] == code for t in trace if t["role"] == "negative-control")


graphs = "biggest-graphs"
codes = "bigger-codes"
fmm = "faster-matrix-multiplication"
vnn = "vnncomp-2026-unsolved-instances"
fixed = options.implementation == "candidate"

# Original 21 scenario classes, preserving baseline comparison and expected fixes.
run_case(graphs, "expected_rejection", 0, assertions=[("six semantic controls rejected", controls_have(6, 1))])
run_case(graphs, "controls_accept_invalid", 1 if fixed else 0, {"CONTROL_MODE": "accept"})
run_case(graphs, "controls_infrastructure_error", 1 if fixed else 0, {"CONTROL_MODE": "infra"})
run_case(graphs, "positive_checker_failure", 1, {"POSITIVE_FAIL": "1"})
run_case(graphs, "hash_mismatch", 1, {"HASH_FAIL": "1"})
run_case(codes, "complete_synthetic_inventory", 0)
run_case(codes, "missing_unrequired_code", 1 if fixed else 0)
run_case(codes, "missing_indexed_certificate", 1 if fixed else 0)
run_case(codes, "missing_required_code", 2)
run_case(codes, "hash_mismatch", 1)
run_case(codes, "positive_checker_failure", 1, {"POSITIVE_FAIL": "1"})
run_case(fmm, "expected_rejection", 0, assertions=[("three semantic controls rejected", controls_have(3, 1))])
run_case(fmm, "controls_accept_invalid", 1, {"CONTROL_MODE": "accept"})
run_case(fmm, "controls_infrastructure_error", 1 if fixed else 0, {"CONTROL_MODE": "infra"})
run_case(fmm, "mutator_infrastructure_error", 1 if fixed else 0, {"MUTATE_FAIL": "1"},
         [("control checks skipped after mutation failure" if fixed else "missing mutants rejected by mock", controls_have(0 if fixed else 3, 2))])
run_case(fmm, "positive_checker_failure", 1, {"POSITIVE_FAIL": "1"})
run_case(vnn, "expected_rejection", 0, assertions=[("six semantic controls rejected", controls_have(6, 1))])
run_case(vnn, "controls_accept_invalid", 1, {"CONTROL_MODE": "accept"})
run_case(vnn, "controls_infrastructure_error", 1 if fixed else 0, {"CONTROL_MODE": "infra"})
run_case(vnn, "mutator_infrastructure_error", 1, {"MUTATE_FAIL": "1"},
         [("control checks skipped after mutation failure" if fixed else "missing mutants rejected by mock", controls_have(0 if fixed else 6, 2))])
run_case(vnn, "positive_checker_failure", 1, {"POSITIVE_FAIL": "1"})

if fixed:
    for family in (graphs, codes, fmm, vnn):
        run_case(family, "missing_shared_helper", 2, assertions=[
            ("missing dependency is explicit", lambda out, err, trace: "missing known-knowns/check_harness_contract.py" in out and not trace)])
    for mode in ("infra_exit1", "late_traceback", "early_invalid", "wrong_near_count", "zero_far", "bad_structure", "wrong_identity"):
        run_case(graphs, mode, 1, {"CONTROL_MODE": mode})
    run_case(codes, "crlf_inventory", 0)
    run_case(codes, "contributed_sibling_package", 0)
    for variant in ("duplicate_index", "unsafe_index_path", "missing_index_row", "metadata_mismatch", "unexpected_file", "malformed_csv", "missing_index", "symlink_index", "symlink_file", "symlink_directory"):
        run_case(codes, variant, 1, assertions=[
            ("inventory failure prevents every scientific checker", lambda out, err, trace: all(x["role"] == "contract-helper" for x in trace))])
    for mode in ("infra_exit1", "late_traceback", "incomplete_fail", "wrong_identity", "wrong_hash", "no_semantic_failure", "incomplete_mods", "missing_proof"):
        run_case(fmm, mode, 1, {"CONTROL_MODE": mode})
    run_case(fmm, "missing_mutant", 1, {"MUTATE_MISSING": "1"})
    for mode in ("infra_exit1", "late_traceback", "incomplete_fail", "wrong_identity", "wrong_hash", "wrong_witness", "hash_mismatch", "missing_pins", "f32_false", "no_semantic_failure"):
        run_case(vnn, mode, 1, {"CONTROL_MODE": mode})
    run_case(vnn, "missing_mutant", 1, {"MUTATE_MISSING": "1"})
    run_case(vnn, "optional_runtime_warning", 0, {"CONTROL_MODE": "optional_warning"})

summary = {"repository": PROVENANCE["repository"], "commit": PROVENANCE["commit"],
           "implementation": options.implementation,
           "method": "Synthetic scientific commands; only new stdlib orchestration parser executed",
           "case_count": len(RESULTS), "passed_assertion_cases": sum(r["all_assertions_passed"] for r in RESULTS),
           "all_assertions_passed": all(r["all_assertions_passed"] for r in RESULTS), "results": RESULTS}
(OUTPUT_BASE / "results.json").write_text(json.dumps(summary, indent=2) + "\n")
print(f"{summary['passed_assertion_cases']}/{len(RESULTS)} synthetic regression scenarios passed.")
sys.exit(0 if summary["all_assertions_passed"] else 1)
