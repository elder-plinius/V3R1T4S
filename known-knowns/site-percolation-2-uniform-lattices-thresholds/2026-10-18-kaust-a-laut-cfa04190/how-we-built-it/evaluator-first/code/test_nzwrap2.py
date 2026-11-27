"""Regression net: nzwrap2.exe must write byte-identical .hist and .state files to the frozen nzwrap.exe.

For each case (lattice, mode, L1, L2, samples per block, blocks, seed) both programs run in fresh folders; every
output file is compared by sha256. One case also checks resuming: nzwrap2 runs 1 block, then is restarted for the
rest, and must still match nzwrap's uninterrupted run.

usage: python test_nzwrap2.py <work folder>
"""
import hashlib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lattices  # noqa: E402

REF = os.path.join(HERE, "nzwrap.exe")
NEW = os.path.join(HERE, "nzwrap2.exe")
CASES = [
    ("triangular", "site", 8, 8, 4000, 2, 11),
    ("triangular", "bond", 9, 7, 2000, 2, 12),
    ("square", "site", 16, 16, 2000, 2, 13),
    ("square", "bond", 12, 12, 1000, 2, 14),
    ("kagome", "site", 12, 12, 1000, 2, 15),
    ("kagome", "bond", 10, 10, 1000, 2, 16),
    ("honeycomb", "site", 10, 10, 1000, 2, 17),
    ("honeycomb", "bond", 10, 10, 1000, 2, 18),
    ("(3,12^2)", "site", 6, 6, 1000, 2, 19),
    ("(3^3,4^2)", "site", 16, 8, 1000, 2, 20),
    ("#23", "site", 32, 8, 1000, 2, 21),
    ("#23", "bond", 32, 8, 1000, 2, 22),
    ("#22", "site", 24, 8, 1000, 2, 23),
    ("#21", "site", 21, 8, 1000, 2, 24),
    ("#20", "site", 28, 8, 1000, 2, 25),
    ("#23", "site", 3, 3, 3000, 2, 26),     # smallest torus nzwrap2 allows
]


def digest(folder):
    out = {}
    for f in sorted(os.listdir(folder)):
        if f.endswith(".hist") or f.endswith(".state"):
            out[f] = hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
    return out


def run(exe, lat, mode, L1, L2, spb, blocks, seed, d, tag):
    r = subprocess.run([exe, lat, mode, str(L1), str(L2), str(spb), str(blocks), str(seed), d, tag],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("%s failed: %s" % (exe, r.stderr[-300:]))


def main():
    work = sys.argv[1]
    if os.path.isdir(work):
        shutil.rmtree(work)
    os.makedirs(work)
    fails = 0
    for i, (name, mode, L1, L2, spb, blocks, seed) in enumerate(CASES):
        latf = os.path.join(work, "case%02d.lat" % i)
        lattices.write_latfile(lattices.get(name), latf)
        a, b = os.path.join(work, "case%02d_ref" % i), os.path.join(work, "case%02d_new" % i)
        os.makedirs(a)
        os.makedirs(b)
        run(REF, latf, mode, L1, L2, spb, blocks, seed, a, "t")
        if i == 0:   # resume check: 1 block, then restart to the full count
            run(NEW, latf, mode, L1, L2, spb, 1, seed, b, "t")
            run(NEW, latf, mode, L1, L2, spb, blocks, seed, b, "t")
        else:
            run(NEW, latf, mode, L1, L2, spb, blocks, seed, b, "t")
        da, db = digest(a), digest(b)
        ok = da == db and len(da) == blocks + 1
        fails += not ok
        print("%-4s case %2d %-10s %s %3dx%-3d %5d samples x %d blocks: %d files, %s%s" % (
            "ok" if ok else "FAIL", i, name, mode, L1, L2, spb, blocks, len(da),
            "byte-identical" if ok else "DIFFERENT", " (resumed after block 1)" if i == 0 else ""))
    print("NZWRAP2 REGRESSION: %s (%d failures of %d cases)" % ("PASS" if fails == 0 else "FAIL", fails, len(CASES)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
