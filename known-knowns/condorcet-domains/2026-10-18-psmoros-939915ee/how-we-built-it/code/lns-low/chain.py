"""Chain-with-polish (hypothesis H4'): from a record assignment on n0 alternatives, repeat
   clone-extension n -> n+1 (lsearch extend: every x, thresholds + greedy + node-capped B&B on the n-1 mixed
   triples + greedy on all triples), keep the best x, then pair-LNS polish (lsearch lns), up to n1.
Each lsearch call runs under its own perl alarm (one C process per alarm); this driver only waits.
Usage: python chain.py START.npy n0 n1 OUTDIR EXT_SECS_PER_X BBCAP LNS_SECS LNS_NODECAP [XWIN]
  XWIN: if given, only x in [n//2 - XWIN, n//2 + XWIN] (0-based) are tried.
"""
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LS = os.path.join(HERE, "lsearch")


def run(args, log, cap):
    cmd = ["nice", "-n", "10", "perl", "-e", "alarm shift; exec @ARGV", str(cap), LS] + [str(a) for a in args]
    with open(log, "a") as f:
        f.write("# %s %s\n" % (time.strftime("%H:%M:%S", time.gmtime()), " ".join(cmd)))
        f.flush()
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    return open(log).read()


def main():
    start, n0, n1, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    esec, bbcap, lsec, lcap = float(sys.argv[5]), int(sys.argv[6]), float(sys.argv[7]), int(sys.argv[8])
    xwin = int(sys.argv[9]) if len(sys.argv) > 9 else None
    os.makedirs(out, exist_ok=True)
    summ = open(os.path.join(out, "chain_summary.txt"), "a")
    cur, n = start, n0
    while n < n1:
        N = n + 1
        if xwin is None:
            xlo, xhi = 0, n - 1
        else:
            xlo, xhi = max(0, n // 2 - xwin), min(n - 1, n // 2 + xwin)
        elog = os.path.join(out, "n%d_extend.log" % N)
        cap = int((xhi - xlo + 1) * (esec + 20) + 60)
        txt = run(["extend", n, cur, os.path.join(out, "n%d" % N), esec, "pp6", xlo, xhi, bbcap], elog, cap)
        best = None
        for m in re.finditer(r"x (\d+) threshold (\d+) mixed-greedy (\d+) full-greedy (\d+)", txt):
            x, v = int(m.group(1)), int(m.group(4))
            if best is None or v > best[1]:
                best = (x, v)
        if best is None:
            summ.write("n %d extend failed\n" % N)
            break
        ext = os.path.join(out, "n%d_x%d.npy" % (N, best[0]))
        llog = os.path.join(out, "n%d_lns.log" % N)
        lprefix = os.path.join(out, "n%d_lns" % N)
        txt = run(["lns", N, ext, lprefix, lsec, 11, "pp6", lcap], llog, int(lsec + 60))
        m = re.findall(r"final lns (\d+)", txt)
        v = int(m[-1]) if m else best[1]
        res = lprefix + ".npy" if m else ext
        summ.write("%s n %d best-x %d extend %d lns %d file %s\n" % (time.strftime("%H:%M:%S", time.gmtime()), N,
                                                                   best[0], best[1], v, res))
        summ.flush()
        cur, n = res, N


if __name__ == "__main__":
    main()
