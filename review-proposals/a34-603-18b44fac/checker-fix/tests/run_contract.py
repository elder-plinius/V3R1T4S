#!/usr/bin/env python3
"""Frozen independent tests for public leak_scan; no candidate implementation imported at freeze time."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import types


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scan(module, case):
    with tempfile.TemporaryDirectory(prefix="include-contract-") as directory:
        target = Path(directory) / case["file"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(case["text"], encoding="utf-8")
        checker = module.Checker(quiet=True)
        module.leak_scan(checker, directory, "fixture")
        return not checker.fails, checker.fails


def weak_module(original):
    # Deliberately weaker interpretation: disable placeholders in every C++ file.
    # Other checks remain the original real leak_scan, so this is an executable
    # counterexample, rather than an asserted hypothetical result.
    source = original.read_text(encoding="utf-8")
    needle = 'and not r.endswith((".py", ".sh")):'
    assert source.count(needle) == 1, "Original baseline structure changed"
    source = source.replace(needle, 'and not r.endswith((".py", ".sh", ".cpp", ".hpp")):')
    module = types.ModuleType("weaker_skip_all_cpp")
    module.__file__ = str(original)
    exec(compile(source, str(original) + "::weaker", "exec"), module.__dict__)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("original", type=Path)
    parser.add_argument("candidate", nargs="?", type=Path)
    args = parser.parse_args()
    fixture_path = Path(__file__).with_name("fixtures.json")
    spec = json.loads(fixture_path.read_text(encoding="utf-8"))
    print("fixtures_sha256=" + hashlib.sha256(fixture_path.read_bytes()).hexdigest())
    print("runner_sha256=" + hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    original = load(args.original, "original_checker")
    weaker = weak_module(args.original)
    by_id = {case["id"]: case for case in spec["cases"]}
    assert len(by_id) == len(spec["cases"])
    errors = []
    regression_count = 0
    for case in spec["cases"]:
        accepted, fails = scan(original, case)
        ok = accepted == case["original_accept"]
        print(json.dumps({"phase":"original", "case":case["id"], "accepted":accepted, "baseline_matches":ok, "desired_accept":case["accept"], "fails":fails}))
        if not ok:
            errors.append("Original baseline mismatch: " + case["id"])
        regression_count += accepted != case["accept"]
    old_witness = by_id[spec["old_rejects_new_accepts"]]
    weak_witness = by_id[spec["weak_accepts_new_rejects"]]
    assert old_witness["accept"] and not scan(original, old_witness)[0]
    assert not weak_witness["accept"] and scan(weaker, weak_witness)[0]
    print("META original-rejects/desired-accepts: PASS " + old_witness["id"])
    print("META weaker-accepts/desired-rejects: PASS " + weak_witness["id"])
    print("ORIGINAL regression mismatches: %d/%d" % (regression_count, len(spec["cases"])))
    if args.candidate:
        candidate = load(args.candidate, "candidate_checker")
        for case in spec["cases"]:
            accepted, fails = scan(candidate, case)
            ok = accepted == case["accept"]
            required = case.get("required_fail")
            if required and not any(required in message for message in fails):
                ok = False
            print(json.dumps({"phase":"candidate", "case":case["id"], "accepted":accepted, "passed":ok, "fails":fails}))
            if not ok:
                errors.append("Candidate mismatch: " + case["id"])
        meta_old = scan(candidate, old_witness)[0]
        meta_weak = not scan(candidate, weak_witness)[0]
        print("META candidate accepts old-rejection witness: " + str(meta_old))
        print("META candidate rejects weaker-acceptance witness: " + str(meta_weak))
        if not (meta_old and meta_weak):
            errors.append("Candidate fails meta-contract")
    for error in errors:
        print("FAIL: " + error)
    print("CONTRACT: " + ("FAIL" if errors else "PASS"))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
