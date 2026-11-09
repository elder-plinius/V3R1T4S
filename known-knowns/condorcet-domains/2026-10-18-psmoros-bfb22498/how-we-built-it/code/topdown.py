"""Top-down polish + restriction cascade (lens lns-high).  Shares BEST/ with vcycle.py (same offer rule: recount
by lsx count, adopt only if strictly larger).
Loop over the top levels TOPS (comma list) in rotation:
  1. polish best[n] with lsx dlns for T seconds; offer the result;
  2. optionally extend best[n] to n+1 (if n+1 <= HI; x in n//2 +- W, B&B cap BBCAP) and offer the best raw clone,
     then polish it for S(n+1) seconds and offer;
  3. cascade down: for m = n-1 .. LO: restrict best[m+1] (every deletion), offer; if adopted, polish S(m) s, offer.
Usage: python topdown.py BEST OUT TOPS T LO HI W BBCAP STOP_EPOCH [SMUL]
"""
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vcycle import Best, run, ts  # noqa: E402


def main():
    a = sys.argv
    bd, out, tops, T, lo, hi = a[1], a[2], [int(x) for x in a[3].split(",")], float(a[4]), int(a[5]), int(a[6])
    W, bbcap, stop = int(a[7]), int(a[8]), float(a[9])
    smul = float(a[10]) if len(a) > 10 else 1.0
    S = lambda n: smul * (40 + 4 * (n - 16))
    os.makedirs(out, exist_ok=True)
    summ = open(os.path.join(out, "topdown_summary.txt"), "a")
    best = Best(bd, summ)
    k = 0
    while time.time() < stop:
        n = tops[k % len(tops)]
        k += 1
        v0, p0 = best.get(n)
        Tn = min(T, max(30, stop - time.time()))
        pol = os.path.join(out, "k%d_top%d" % (k, n))
        summ.write("%s round %d polish n %d from %d for %.0f s\n" % (ts(), k, n, v0, Tn))
        summ.flush()
        run(["dlns", n, p0, pol, Tn, 7000 + k, "pp6", 4000, 3000], pol + ".log", Tn + 90)
        best.offer(n, pol + ".npy", "topdown dlns")
        if n + 1 <= hi and time.time() < stop:
            v0, p0 = best.get(n)
            pre = os.path.join(out, "k%d_e%d" % (k, n + 1))
            xlo, xhi = max(0, n // 2 - W), min(n - 1, n // 2 + W)
            txt = run(["extend", n, p0, pre, 2, "pp6", xlo, xhi, bbcap], pre + ".log", (xhi - xlo + 1) * 40 + 60)
            c = [(int(m.group(4)), int(m.group(1))) for m in
                 re.finditer(r"x (\d+) threshold (\d+) mixed-greedy (\d+) full-greedy (\d+)", txt)]
            if c:
                v, x = max(c)
                best.offer(n + 1, "%s_x%d.npy" % (pre, x), "topdown extend(x=%d)" % x)
                vb, pb = best.get(n + 1)
                if v >= vb * 0.995 and time.time() < stop:
                    pp = os.path.join(out, "k%d_e%d_x%d_pol" % (k, n + 1, x))
                    run(["dlns", n + 1, "%s_x%d.npy" % (pre, x), pp, S(n + 1), 8000 + k, "pp6", 4000, 3000],
                        pp + ".log", S(n + 1) + 90)
                    best.offer(n + 1, pp + ".npy", "topdown extend+dlns(x=%d)" % x)
        top_down = min(hi, n + 1)
        for m in range(top_down - 1, lo - 1, -1):
            if time.time() > stop:
                break
            v1, p1 = best.get(m + 1)
            pre = os.path.join(out, "k%d_r%d" % (k, m))
            run(["restrict", m + 1, p1, pre], pre + ".log", 120)
            imp, v = best.offer(m, pre + ".npy", "topdown restrict(n%d=%d)" % (m + 1, v1))
            if imp and time.time() < stop:
                pp = os.path.join(out, "k%d_r%d_pol" % (k, m))
                run(["dlns", m, pre + ".npy", pp, S(m), 9000 + k, "pp6", 4000, 3000], pp + ".log", S(m) + 90)
                best.offer(m, pp + ".npy", "topdown restrict+dlns")


if __name__ == "__main__":
    main()
