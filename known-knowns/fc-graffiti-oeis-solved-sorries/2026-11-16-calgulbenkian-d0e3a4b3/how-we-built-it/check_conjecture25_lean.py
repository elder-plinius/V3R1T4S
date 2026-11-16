#!/usr/bin/env python3
"""Run the standalone Lean 4 kernel & linter verifier for GraphConjecture25."""
import os
import subprocess
import sys
import time


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    attack_root = os.path.abspath(os.path.join(here, "..", "..", ".."))
    checker = os.path.join(attack_root, "verify-it-yourself", "run_checks.sh")
    t0 = time.monotonic()
    proc = subprocess.run(["sh", checker], cwd=attack_root, capture_output=True, text=True)
    elapsed = time.monotonic() - t0
    sys.stdout.write(proc.stdout)
    print(f"elapsed_seconds = {elapsed:.2f}")
    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
