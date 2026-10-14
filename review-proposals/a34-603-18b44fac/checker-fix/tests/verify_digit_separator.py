#!/usr/bin/env python3
"""Targeted post-review reproduction; separate from the frozen 25-case suite."""
import hashlib
import importlib.util
from pathlib import Path
import sys
import tempfile

candidate = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("digit_separator_candidate", candidate)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
fixture = "constexpr int count = 1'000;\n#include <unordered_map>\n"
with tempfile.TemporaryDirectory(prefix="digit-separator-") as directory:
    Path(directory, "main.cpp").write_text(fixture, encoding="utf-8")
    checker = module.Checker(quiet=True)
    module.leak_scan(checker, directory, "digit-separator")
    print("candidate_sha256=" + hashlib.sha256(candidate.read_bytes()).hexdigest())
    print("fixture:", repr(fixture))
    print("expected_accept: True")
    print("actual_accept:", not checker.fails)
    print("failures:", repr(checker.fails))
    print("TARGETED CHECK: " + ("FAIL" if checker.fails else "PASS"))
    raise SystemExit(bool(checker.fails))
