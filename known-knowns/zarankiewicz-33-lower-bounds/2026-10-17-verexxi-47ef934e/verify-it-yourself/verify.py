"""Verify object/z_16x19_142.txt: 16 x 19, at least 142 ones, no all-ones 3 x 3 submatrix, file hash as claimed.
Uses check_matrix.py (two independent methods) from this folder. Prints the details, then a last line PASS or FAIL.
Exit status 0 on PASS, 1 on FAIL. Python standard library only."""
import hashlib
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import check_matrix as cm

PATH = os.path.join(here, "..", "object", "z_16x19_142.txt")
EXPECTED_SHA256 = "47ef934e67f7931526d0f9b57fbd617a7ea8100c4efdeccf765c4f29286f3fa8"


def main():
    ok = True
    try:
        data = open(PATH, "rb").read()
    except OSError as e:
        print("cannot read the object: %s" % e)
        print("FAIL")
        return 1
    h = hashlib.sha256(data).hexdigest()
    print("object sha256 %s %s" % (h, "matches the claimed hash" if h == EXPECTED_SHA256 else "DIFFERS from the claimed hash"))
    ok &= h == EXPECTED_SHA256
    try:
        M = cm.load(PATH)
    except (OSError, ValueError) as e:
        print("cannot parse the object: %s" % e)
        print("FAIL")
        return 1
    good, msgs = cm.check(M, rows=16, cols=19, ones=142)
    for s in msgs:
        print(s)
    ok &= good
    st = cm.selftest()
    print("checker self-test (known positive and negatives): %s" % ("ok" if st else "WRONG"))
    ok &= st
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
