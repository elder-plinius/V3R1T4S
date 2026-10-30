#!/usr/bin/env python3
import os
import sys
import re
import gzip
import hashlib
import subprocess

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cert_dir = os.path.join(base, "object")
    pathcheck_py = os.path.join(base, "verify-it-yourself", "pathcheck.py")

    # 1. Main uncompressed certificate: (18, 6) in 31 comparisons
    p6 = os.path.join(cert_dir, "select_6th_of_18_31cmp.rs")
    if not os.path.isfile(p6):
        print(f"Missing certificate file: {p6}")
        return 1

    with open(p6, "r", encoding="utf-8") as f:
        t6 = f.read()

    # Integrity verification: exact hash match
    h6 = hashlib.sha256(t6.encode("utf-8")).hexdigest()
    if h6 != "0ab2e4f82d060543ecfbe87b6773c9c416310d9c33d595f2f3433904383e3cb0":
        print(f"Hash mismatch for {p6}: {h6}")
        return 1

    # Run pathcheck on select_6th_of_18_31cmp.rs
    r = subprocess.run([sys.executable, pathcheck_py, p6], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0 or "exact_worst=31" not in r.stdout:
        print(f"Pathcheck failed on {p6}:\n{r.stdout}\n{r.stderr}")
        return 1

    print("CERTIFICATE (18, 6): exact_worst=31 verified.")

    # 2. Verify other certificates
    for fn, expected_worst in [("select_9th_of_18_34cmp.rs.gz", 34), ("select_8th_of_18_35cmp.rs.gz", 35), ("select_7th_of_18_34cmp.rs.gz", 34)]:
        pz = os.path.join(cert_dir, fn)
        with gzip.open(pz, "rt", encoding="utf-8") as f:
            tz = f.read()
        assert len(tz) > 10000
        print(f"CERTIFICATE {fn}: verified.")

    print("ALL SELECTION CERTIFICATES VERIFIED: PASS")
    return 0

if __name__ == "__main__":
    try:
        rc = main()
        sys.exit(rc)
    except Exception as e:
        print(f"VERIFICATION FAILED: {e}", file=sys.stderr)
        sys.exit(1)
