#!/usr/bin/env python3
"""Unified Verification Script for Minimum-Comparison Selection (n=18) Claim p2.

Dual-verifies that certificates for (18, 9), (18, 8), (18, 7), and (18, 6)
pass both:
1. Cremer's static checker (verify_rs_algorithm.py)
2. Independent recursive path checker (pathcheck.py)
and strictly beat Gasarch-Kelly-Pugh 1996 Table 3 and Hadian-Sobel.
"""

import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREMER_CHECKER = os.path.join(BASE_DIR, "code", "verifier", "verify_rs_algorithm.py")
PATHCHECK = os.path.join(BASE_DIR, "code", "independent_checks", "checker", "pathcheck.py")

CASES = [
    {
        "n": 18,
        "i": 9,
        "claimed_worst": 34,
        "gkp_table3": 37,
        "hadian_sobel": 41,
        "cert": os.path.join(BASE_DIR, "certificates", "select_9th_of_18_34cmp.rs"),
    },
    {
        "n": 18,
        "i": 8,
        "claimed_worst": 35,
        "gkp_table3": 37,
        "hadian_sobel": 38,
        "cert": os.path.join(BASE_DIR, "certificates", "select_8th_of_18_35cmp.rs"),
    },
    {
        "n": 18,
        "i": 7,
        "claimed_worst": 34,
        "gkp_table3": 35,
        "hadian_sobel": 35,
        "cert": os.path.join(BASE_DIR, "certificates", "select_7th_of_18_34cmp.rs"),
    },
    {
        "n": 18,
        "i": 6,
        "claimed_worst": 31,
        "gkp_table3": 32,
        "hadian_sobel": 32,
        "cert": os.path.join(BASE_DIR, "certificates", "select_6th_of_18_31cmp.rs"),
    },
]

def main():
    print("=" * 70)
    print("MINIMUM COMPARISON SELECTION (n=18): DUAL CHECKER VERIFICATION")
    print("=" * 70)

    all_passed = True

    for c in CASES:
        name = f"({c['n']}, {c['i']}) {c['claimed_worst']} cmp"
        if not os.path.isfile(c["cert"]):
            print(f"[FAIL] {name}: certificate file not found at {c['cert']}")
            all_passed = False
            continue

        # 1. Cremer checker
        cmd1 = [
            sys.executable,
            "-I",
            CREMER_CHECKER,
            c["cert"],
            "--expect-n",
            str(c["n"]),
            "--expect-i",
            str(c["i"]),
            "--expect-worst",
            str(c["claimed_worst"]),
        ]
        r1 = subprocess.run(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if r1.returncode != 0 or "ACCEPT" not in r1.stdout:
            print(f"[FAIL] {name}: Cremer checker rejected:")
            print(r1.stdout)
            print(r1.stderr)
            all_passed = False
            continue

        # 2. Pathcheck
        cmd2 = [sys.executable, "-I", PATHCHECK, c["cert"]]
        r2 = subprocess.run(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if r2.returncode != 0 or f"exact_worst={c['claimed_worst']}" not in r2.stdout:
            print(f"[FAIL] {name}: pathcheck rejected:")
            print(r2.stdout)
            print(r2.stderr)
            all_passed = False
            continue

        # 3. Baseline comparison checks
        beat_gkp = c["gkp_table3"] - c["claimed_worst"]
        beat_hs = c["hadian_sobel"] - c["claimed_worst"]
        if beat_gkp <= 0 or beat_hs <= 0:
            print(f"[FAIL] {name}: did not beat baselines (GKP diff {beat_gkp}, HS diff {beat_hs})")
            all_passed = False
            continue

        print(f"[PASS] {name}: Cremer checker ACCEPT, Pathcheck exact_worst={c['claimed_worst']}")
        print(f"       Beats GKP Table 3 ({c['gkp_table3']}) by {beat_gkp} cmp; beats Hadian-Sobel ({c['hadian_sobel']}) by {beat_hs} cmp")

    print("=" * 70)
    if all_passed:
        print("VERIFICATION RESULT: ALL CHECKS PASSED (CLAIM p2 CONFIRMED)")
        print("=" * 70)
        return 0
    else:
        print("VERIFICATION RESULT: FAILURES DETECTED")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
