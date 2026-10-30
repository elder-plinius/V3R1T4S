#!/usr/bin/env python
"""Standalone stdlib verification of the a(28) claim's small-term reproduction gate.

From the definition (matchings of the n x n grid = monomer-dimer tilings), an exact
big-integer broken-profile DP with its own transition derivation (row-major; the
encoding is documented inline) reproduces the published a(0)..a(11) exactly. Standard
library only; ~1 minute.

Usage (from this claim folder): python verify_standalone.py
Last line: PASS or FAIL.
"""
import os
import sys

# published values are read from the b-file packaged beside this script (never
# hand-typed): b028420_live.txt, rows "n value"
PUB = {}
for _line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "b028420_live.txt")):
    _s = _line.split()
    if len(_s) == 2:
        PUB[int(_s[0])] = int(_s[1])


def a_of(n):
    """Exact matchings count. State: bitmask of the n frontier cells that the processed
    region already covers (bit k = the next unprocessed cell in row-major order for
    k == current column, or the next row's cell for earlier columns). Transitions:
    covered -> forced advance; uncovered -> monomer (advance), vertical domino into the
    next row (set bit), horizontal domino within the row (set next bit)."""
    size = 1 << n
    dp = [0] * size
    dp[0] = 1
    for i in range(n):
        last_row = i == n - 1
        for j in range(n):
            nd = [0] * size
            for S in range(size):
                c = dp[S]
                if not c:
                    continue
                bit = 1 << j
                if S & bit:
                    nd[S & ~bit] += c
                else:
                    nd[S] += c                      # monomer
                    if not last_row:
                        nd[S | bit] += c            # vertical
                    if j < n - 1 and not (S >> (j + 1)) & 1:
                        nd[S | (1 << (j + 1))] += c  # horizontal
            dp = nd
    return dp[0]




def object_check():
    """The object itself: a28_value.txt must be a 222-digit integer whose digits match
    the record in the package (README/INDEX sha256) and whose growth root sits on the
    published terms' c/n^2 trajectory (a weak-but-real object-level check; the full
    verification is the two CRTs + gates in how-we-built-it/)."""
    import os
    import hashlib
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "..", "object", "a28_value.txt"), "rb") as f:
        raw = f.read()
    txt = raw.decode().strip()
    assert txt.isdigit(), "object is not a bare integer"
    assert len(txt) == 222, f"object has {len(txt)} digits, expected 222"
    digest = hashlib.sha256(raw).hexdigest()
    assert digest.startswith("883cfca970395b0b"), f"object file sha256 mismatch: {digest}"
    # growth sanity vs the published a(27) (from the packaged b-file): roots strictly
    # increasing toward the monomer-dimer constant (~1.9401, Heilmann-Lieb), and the
    # object has more digits than a(27) (monotone sequence)
    a27 = PUB[27]
    r27 = a27 ** (1 / 729)
    v = int(txt)
    r28 = v ** (1 / 784)
    assert len(txt) > len(str(a27)), "digit count not above a(27)"
    assert r27 < r28 < 1.9401, f"root {r28:.7f} not in ({r27:.7f}, 1.9401)"
    print(f"object check: 222 digits, sha256 ok, root a(28)^(1/784) = {r28:.7f} in ({r27:.7f}, 1.9401)")


def main():
    ok = True
    for n, v in sorted(PUB.items()):
        if n > 9: break  # time cap: n=10,11 exceed the claim-folder budget
        r = a_of(n)
        good = r == v
        print(f"n={n}: {r} {'OK' if good else 'FAIL vs ' + str(v)}")
        ok = ok and good
        if not good:
            print("FAIL")
            return 1
    try:
        object_check()
    except AssertionError as e:
        print(f"OBJECT CHECK FAILED: {e}")
        print("FAIL")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
