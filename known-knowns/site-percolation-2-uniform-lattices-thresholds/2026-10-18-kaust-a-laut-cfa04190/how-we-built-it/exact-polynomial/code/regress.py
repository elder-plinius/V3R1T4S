"""Regression net for tmcrit: published n x infinity sequences and exactly solvable thresholds.

Reference values: Jacobsen, arXiv:1507.03027, Table 2 (square-lattice site, n x infinity bases) and Table 3
(kagome bond), copied from the paper's text; exact values from the star-triangle / self-duality solutions.
"""
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sweep  # noqa: E402

EXE = os.path.join(HERE, "tmcrit.exe")
PROGS = os.path.join(HERE, "..", "progs")

TABLE2_SQUARE_SITE = {1: "0.5000000000000000000", 2: "0.5651977173836393964", 3: "0.5888806999178529980",
                      4: "0.5914171708531384818", 5: "0.5922358232050266776", 6: "0.5925073562056416791",
                      7: "0.5926196333998949002", 8: "0.5926727605746273160"}
TABLE3_KAGOME_BOND = {1: "0.5244297175212747935", 2: "0.5244060578960626342", 3: "0.5244050922187183914",
                      4: "0.5244050138823434507", 5: "0.5244050026660985340"}
s18 = math.sin(math.pi / 18)
EXACT = [("triangular", "site", 0.5), ("kagome", "site", 1 - 2 * s18), ("(3,12^2)", "site", math.sqrt(1 - 2 * s18)),
         ("square", "bond", 0.5), ("triangular", "bond", 2 * s18), ("honeycomb", "bond", 1 - 2 * s18)]


def run(lat, n, mode, lo, hi):
    os.makedirs(PROGS, exist_ok=True)
    path = os.path.join(PROGS, "%s_n%d.txt" % ("".join(ch for ch in lat if ch.isalnum()), n))
    prog = sweep.build_program(sweep.LATTICES[lat](), n)
    sweep.write_program(prog, path)
    out = subprocess.run([EXE, path, mode, str(lo), str(hi)], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr[-500:])
    tok = out.stdout.split()
    return float(tok[tok.index("pc") + 1])


def main():
    worst = 0.0
    fails = 0
    print("check                         n   computed               reference              |diff|")
    for n, ref in TABLE2_SQUARE_SITE.items():
        v = run("square", n, "site", 0.4, 0.7)
        d = abs(v - float(ref)); worst = max(worst, d); fails += d > 1e-12
        print("square site (Table 2)       %2d   %.16f     %s  %.1e" % (n, v, ref, d))
    for n, ref in TABLE3_KAGOME_BOND.items():
        v = run("kagome", n, "bond", 0.4, 0.7)
        d = abs(v - float(ref)); worst = max(worst, d); fails += d > 1e-12
        print("kagome bond (Table 3)       %2d   %.16f     %s  %.1e" % (n, v, ref, d))
    for lat, mode, ref in EXACT:
        for n in range(1, 5):
            v = run(lat, n, mode, 0.2, 0.95)
            d = abs(v - ref); worst = max(worst, d); fails += d > 1e-12
            print("%-12s %-4s exact      %2d   %.16f     %.16f  %.1e" % (lat, mode, n, v, ref, d))
    print("worst |diff| %.2e ; failures (> 1e-12): %d" % (worst, fails))
    print("REGRESSION: %s" % ("PASS" if fails == 0 else "FAIL"))


if __name__ == "__main__":
    main()
