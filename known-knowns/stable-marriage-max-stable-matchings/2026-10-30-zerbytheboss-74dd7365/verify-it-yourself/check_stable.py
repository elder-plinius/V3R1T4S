#!/usr/bin/env python3
"""Standalone checker for stable-marriage-max-stable-matchings (n=19)."""
import os
import sys
import hashlib
import subprocess
import tempfile

pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECTED_SHA = "74dd73657f01b9ab73fabca46ed2d2835be4909b3d8bb8c06fdc6379a71af617"
EXPECTED_COUNT = 642696

def check():
    obj_path = os.path.join(pkg_dir, "object", "instance_n19.txt")
    v_dir = os.path.join(pkg_dir, "verify-it-yourself")

    if not os.path.isfile(obj_path):
        print(f"FAIL: Object file missing: {obj_path}")
        return False

    with open(obj_path, "rb") as f:
        data_bytes = f.read()

    actual_sha = hashlib.sha256(data_bytes).hexdigest()
    if actual_sha != EXPECTED_SHA:
        print(f"FAIL: SHA256 mismatch: expected {EXPECTED_SHA}, got {actual_sha}")
        return False

    text = data_bytes.decode("utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]
    if len(lines) != 38:
        print(f"FAIL: Expected 38 lines (19 men + 19 women), got {len(lines)}")
        return False

    for i, line in enumerate(lines):
        try:
            row = [int(x) for x in line.split()]
        except ValueError:
            print(f"FAIL: Non-integer token on line {i+1}")
            return False
        if sorted(row) != list(range(1, 20)):
            print(f"FAIL: Line {i+1} is not a valid permutation of 1..19")
            return False

    # Compile smcount3 in a temporary directory to avoid package pollution
    smcount3_src = os.path.join(v_dir, "smcount3.c")
    with tempfile.TemporaryDirectory() as tmpdir:
        smcount3_bin = os.path.join(tmpdir, "smcount3")
        res = subprocess.run(["cc", "-O3", "-o", smcount3_bin, smcount3_src, "-lm"], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"FAIL: Could not compile smcount3.c: {res.stderr}")
            return False

        # Run dual counting
        res = subprocess.run([smcount3_bin, "count", obj_path, "1"], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"FAIL: smcount3 execution failed: {res.stderr}")
            return False

        stdout = res.stdout
        if "agree: yes" not in stdout or f"count_lattice_verified: {EXPECTED_COUNT}" not in stdout:
            print(f"FAIL: smcount3 count did not match expected {EXPECTED_COUNT} or counters did not agree:\n{stdout}")
            return False

    print(f"Verified instance_n19.txt strict permutation properties and dual independent counts ({EXPECTED_COUNT}).")
    print("PASS")
    return True

if __name__ == "__main__":
    if check():
        sys.exit(0)
    else:
        sys.exit(1)
