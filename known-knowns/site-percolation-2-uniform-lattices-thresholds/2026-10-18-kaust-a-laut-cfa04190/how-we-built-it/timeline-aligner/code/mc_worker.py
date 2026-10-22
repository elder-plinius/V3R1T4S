"""Run a list of nzwrap jobs one after another (one core). Resumable: nzwrap continues from its .state file.

usage: python mc_worker.py <lattice> <site|bond> <ratio_num> <ratio_den> <L2 list, comma separated> <blocks> <seed0> <outdir> [exe]
exe: nzwrap.exe (default, the frozen evaluator) or nzwrap2.exe (byte-identical output, PREREG.v3; run 2026-10-16-1714).
For each L2: L1 = L2 * ratio_den / ratio_num (the fixed aspect ratio L2 = (num/den) L1 of PREREG.md),
samples per block chosen so that a block takes about 3 minutes (about 4.5e9 / sites), seed = seed0 + L2.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EF = os.path.join(HERE, "..", "..", "evaluator-first")
EXE = os.path.join(EF, "code", "nzwrap.exe")
LATDIR = os.path.join(EF, "lat")
sys.path.insert(0, os.path.join(EF, "code"))
import lattices  # noqa: E402


def main():
    lat, mode, num, den, sizes, blocks, seed0, outdir = sys.argv[1:9]
    exe = os.path.join(EF, "code", sys.argv[9]) if len(sys.argv) > 9 else EXE
    num, den, blocks, seed0 = int(num), int(den), int(blocks), int(seed0)
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(LATDIR, exist_ok=True)
    tag = "".join(ch for ch in lat if ch.isalnum())
    latfile = os.path.join(LATDIR, tag + ".lat")
    L = lattices.get(lat)
    lattices.write_latfile(L, latfile)
    K, E = len(L["verts"]), len(L["edges"])
    for L2 in [int(x) for x in sizes.split(",")]:
        assert (L2 * den) % num == 0
        L1 = L2 * den // num
        M = L1 * L2 * (K if mode == "site" else E)
        spb = max(1000, int(round(4.5e9 / M / 1000.0)) * 1000)
        seed = seed0 + L2
        jtag = "%s_%s_L%dx%d_s%d" % (tag, mode, L1, L2, seed)
        with open(os.path.join(outdir, jtag + ".log"), "a") as lf:
            r = subprocess.run([exe, latfile, mode, str(L1), str(L2), str(spb), str(blocks), str(seed), outdir, jtag],
                               stdout=lf, stderr=lf)
        if r.returncode != 0:
            print("job %s failed with %d" % (jtag, r.returncode), file=sys.stderr)


if __name__ == "__main__":
    main()
