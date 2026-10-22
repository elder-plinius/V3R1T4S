"""Deep chain (lens lns-high): from an assignment on n0 alternatives, repeat
   (1) clone-extension n -> n+1 over x in [n//2 - W, n//2 + W] (lsx extend: thresholds + greedy + node-capped exact
       B&B on the n-1 mixed triples + greedy on all triples),
   (2) keep the top-B distinct extension values, polish each with lsx dlns for S1 seconds
       (sequenced pair-LNS, then triple-of-alternatives LNS),
   (3) polish the best one further for S2 seconds, and continue from it,
   up to n1.  Each lsx call runs under its own perl alarm (one C process per alarm); this driver only waits.
Usage: python dchain.py START.npy n0 n1 OUTDIR W BBCAP EXTSECS B S1 S2 PAIRCAP TRICAP [S0]
  S0 (optional): deep-polish the start for S0 seconds first.
"""
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LSX = os.path.join(HERE, "lsx")


def run(args, log, cap):
    cmd = ["nice", "-n", "10", "perl", "-e", "alarm shift; exec @ARGV", str(int(cap)), LSX] + [str(a) for a in args]
    with open(log, "a") as f:
        f.write("# %s %s\n" % (time.strftime("%H:%M:%S", time.gmtime()), " ".join(cmd)))
        f.flush()
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    return open(log).read()


def dlns(n, src, prefix, secs, seed, pcap, tcap):
    log = prefix + ".log"
    txt = run(["dlns", n, src, prefix, secs, seed, "pp6", pcap, tcap], log, secs + 90)
    m = re.findall(r"final dlns (\d+)", txt)
    if m:
        return int(m[-1]), prefix + ".npy"
    # killed by alarm: the .npy holds the best so far; recount it
    if os.path.exists(prefix + ".npy"):
        out = subprocess.run([LSX, "count", str(n), prefix + ".npy"], capture_output=True, text=True).stdout
        return int(out.split()[3]), prefix + ".npy"
    return None, None


def main():
    a = sys.argv
    start, n0, n1, out = a[1], int(a[2]), int(a[3]), a[4]
    W, bbcap, esec, B = int(a[5]), int(a[6]), float(a[7]), int(a[8])
    s1, s2, pcap, tcap = float(a[9]), float(a[10]), int(a[11]), int(a[12])
    s0 = float(a[13]) if len(a) > 13 else 0
    os.makedirs(out, exist_ok=True)
    summ = open(os.path.join(out, "chain_summary.txt"), "a")
    cur, n = start, n0
    if s0 > 0:
        v, f = dlns(n, cur, os.path.join(out, "n%d_start_pol" % n), s0, 3, pcap, tcap)
        summ.write("%s n %d start-polish %d file %s\n" % (time.strftime("%H:%M:%S", time.gmtime()), n, v, f))
        summ.flush()
        cur = f
    while n < n1:
        N = n + 1
        xlo, xhi = max(0, n // 2 - W), min(n - 1, n // 2 + W)
        elog = os.path.join(out, "n%d_extend.log" % N)
        txt = run(["extend", n, cur, os.path.join(out, "n%d" % N), esec, "pp6", xlo, xhi, bbcap], elog,
                  (xhi - xlo + 1) * (esec + 30) + 60)
        cands = {}
        for m in re.finditer(r"x (\d+) threshold (\d+) mixed-greedy (\d+) full-greedy (\d+)", txt):
            x, v = int(m.group(1)), int(m.group(4))
            if v not in cands:
                cands[v] = x
        if not cands:
            summ.write("n %d extend failed\n" % N)
            break
        top = sorted(cands.items(), reverse=True)[:B]
        res = []
        for i, (v, x) in enumerate(top):
            pv, pf = dlns(N, os.path.join(out, "n%d_x%d.npy" % (N, x)), os.path.join(out, "n%d_x%d_p1" % (N, x)), s1,
                          11 + i, pcap, tcap)
            res.append((pv if pv is not None else v, x, v, pf))
            summ.write("%s n %d cand x %d extend %d polish1 %s\n" % (time.strftime("%H:%M:%S", time.gmtime()), N, x, v, pv))
            summ.flush()
        res.sort(reverse=True)
        bv, bx, bext, bf = res[0]
        if s2 > 0:
            pv, pf = dlns(N, bf, os.path.join(out, "n%d_x%d_p2" % (N, bx)), s2, 101, pcap, tcap)
            if pv is not None and pv >= bv:
                bv, bf = pv, pf
        summ.write("%s n %d best-x %d extend %d final %d file %s\n" % (time.strftime("%H:%M:%S", time.gmtime()), N, bx,
                                                                     bext, bv, bf))
        summ.flush()
        cur, n = bf, N


if __name__ == "__main__":
    main()
