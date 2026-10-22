"""Run the certificate chain: for each link j, (p_j, q_j) with q_1 = 1/2 and q_j = p_{j-1}.
usage: python chain.py <counts file> <workdir> [q1=num/den] p_1 p_2 ... (each p as "num/den"; q_1 = 1/2 unless given)
Each link: cert.py intervals -> cert.exe laws -> cert.py check. Stops at the first failing link.
"""
import os
import subprocess
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
EXE = os.path.join(HERE, "cert", "cert.exe")


def run(cmd, log):
    t = time.time()
    out = subprocess.run(cmd, capture_output=True, text=True)
    log.write("$ %s\n%s%s(%.0f s, exit %d)\n" % (" ".join(cmd), out.stdout, out.stderr, time.time() - t, out.returncode))
    log.flush()
    if out.returncode != 0:
        raise SystemExit("command failed: %s\n%s" % (cmd, out.stderr))
    return out.stdout


def main():
    counts, wd = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]
    q = Fraction(1, 2)
    if args and args[0].startswith("q1="):
        q = Fraction(args.pop(0)[3:])
    ps = [Fraction(x) for x in args]
    os.makedirs(wd, exist_ok=True)
    with open(os.path.join(wd, "chain_log.txt"), "a", newline="\n") as log:
        for j, p in enumerate(ps, 1):
            tag = "link%d_p%d_%d" % (j, p.numerator, p.denominator)
            iv = os.path.join(wd, tag + "_intervals.txt")
            lw = os.path.join(wd, tag + "_laws.txt")
            run([PY, os.path.join(HERE, "cert.py"), "intervals", counts, str(p.numerator), str(p.denominator), iv], log)
            run([EXE, "3", "3", "3", "6", "6", "laws", iv, lw], log)
            out = run([PY, os.path.join(HERE, "cert.py"), "check", counts, lw, str(p.numerator), str(p.denominator),
                       str(q.numerator), str(q.denominator)], log)
            last = out.strip().splitlines()[-1]
            print("link %d: p = %s, q = %s: %s" % (j, p, q, last), flush=True)
            print(out.strip().splitlines()[-2], flush=True)
            if "PASS" not in last:
                print("chain stops at link %d" % j)
                return
            q = p
    print("chain complete: p_c^site(Z^3) <= %s (given Campanino-Russo's p_c < 1/2 for link 1)" % ps[-1])


if __name__ == "__main__":
    main()
