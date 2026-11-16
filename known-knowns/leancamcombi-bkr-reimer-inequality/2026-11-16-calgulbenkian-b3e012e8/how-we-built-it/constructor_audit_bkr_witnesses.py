#!/usr/bin/env python3
"""Audit upstream Finset.certificator semantics on monotone/non-monotone families and run checker."""
import os
import random
import subprocess
import sys


def certificator(n: int, fam_a: set, fam_b: set) -> set:
    mask_all = (1 << n) - 1
    out = set()
    for a in fam_a & fam_b:
        found = False
        for x in range(1 << n):
            y = mask_all ^ x
            if all((b in fam_a) for b in range(1 << n) if (a & x) == (b & x)) and all(
                (b in fam_b) for b in range(1 << n) if (a & y) == (b & y)
            ):
                found = True
                break
        if found:
            out.add(a)
    return out


def main() -> None:
    rng = random.Random(342000)
    # 1. Non-monotone parity example where |A cap B| * 2^n > |A|*|B| yet 2^n * |A □ B| <= |A|*|B|
    n = 3
    even_sets = {s for s in range(1 << n) if bin(s).count("1") % 2 == 0}
    cert_even = certificator(n, even_sets, even_sets)
    assert len(even_sets) == 4
    assert len(cert_even) == 0
    print(f"Parity non-monotone test (n=3): |A|=|B|=4, |A cap B|=4, |A □ B|={len(cert_even)} (0 <= 16)")

    # 2. Subcube cylinder tightness test where 2^n * |A □ B| == |A| * |B|
    cyl_a = {s for s in range(1 << n) if (s & 0b011) == 0b011}  # 2 elements
    cyl_b = {s for s in range(1 << n) if (s & 0b100) == 0}      # 4 elements
    cert_cyl = certificator(n, cyl_a, cyl_b)
    assert (1 << n) * len(cert_cyl) == len(cyl_a) * len(cyl_b)
    print(f"Cylinder equality test (n=3): 2^3 * |A □ B| = 8 * {len(cert_cyl)} == {len(cyl_a)} * {len(cyl_b)}")

    # 3. Random arbitrary (non-monotone) family sweep across n = 0..4
    for n in range(0, 5):
        trials = 1 if n == 0 else 200
        max_ratio = 0.0
        for _ in range(trials):
            p_a = rng.uniform(0.1, 0.9)
            p_b = rng.uniform(0.1, 0.9)
            fam_a = {s for s in range(1 << n) if rng.random() < p_a}
            fam_b = {s for s in range(1 << n) if rng.random() < p_b}
            cert = certificator(n, fam_a, fam_b)
            lhs = (1 << n) * len(cert)
            rhs = len(fam_a) * len(fam_b)
            assert lhs <= rhs
            if rhs > 0:
                max_ratio = max(max_ratio, lhs / rhs)
        print(f"Random general family sweep n={n} ({trials} trials): 2^n*|A □ B| <= |A|*|B| holds (max ratio={max_ratio:.3f})")

    # 4. Run standalone Lean 4 referee
    here = os.path.dirname(os.path.abspath(__file__))
    run_root = os.path.abspath(os.path.join(here, "..", "..", ".."))
    proc = subprocess.run(
        ["sh", "verify-it-yourself/run_checks.sh"],
        cwd=run_root,
        capture_output=True,
        text=True,
        timeout=600,
    )
    sys.stdout.write(proc.stdout)
    if proc.returncode != 0:
        sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
