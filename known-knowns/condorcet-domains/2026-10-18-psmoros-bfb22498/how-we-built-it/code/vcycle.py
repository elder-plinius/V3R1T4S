"""V-cycle search (lens lns-high; idea imported from multigrid solvers): keep one best assignment per n in a shared
directory BEST/ (nN.npy + nN.txt holding its exact DP count), and alternate
  down pass  n = hi-1 .. lo : restrict best[n+1] to [n+1] \\ {v} for every v (lsx restrict), keep the best deletion;
                              if it beats best[n], adopt it and polish it (lsx dlns, S(n) seconds);
  up pass    n = lo .. hi-1 : clone-extend best[n] over x in n//2 +- W (lsx extend, node-capped exact B&B on the
                              mixed triples); offer the top-B raw results to n+1, polish the best raw one (dlns) and
                              offer it too.
Every offer is recounted by lsx count and adopted only if strictly larger (write to tmp + rename, so two drivers on
overlapping ranges can share BEST/).  One lsx process at a time, each under its own perl alarm.
Usage: python vcycle.py BEST OUT lo hi W BBCAP B STOP_EPOCH [SMUL]
"""
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LSX = os.path.join(HERE, "lsx")


def ts():
    return time.strftime("%H:%M:%S", time.gmtime())


def run(args, log, cap):
    cmd = ["nice", "-n", "10", "perl", "-e", "alarm shift; exec @ARGV", str(int(cap)), LSX] + [str(a) for a in args]
    with open(log, "a") as f:
        f.write("# %s %s\n" % (ts(), " ".join(cmd)))
        f.flush()
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    return open(log).read()


def count(n, path):
    out = subprocess.run([LSX, "count", str(n), path], capture_output=True, text=True).stdout.split()
    return int(out[3])


class Best:
    def __init__(self, d, summ):
        self.d, self.summ = d, summ

    def get(self, n):
        p = os.path.join(self.d, "n%d.npy" % n)
        if not os.path.exists(p):
            return None, None
        return int(open(os.path.join(self.d, "n%d.txt" % n)).read().split()[0]), p

    def offer(self, n, path, how):
        v = count(n, path)
        cur, _ = self.get(n)
        if cur is None or v > cur:
            tmp = os.path.join(self.d, "n%d.npy.tmp%d" % (n, os.getpid()))
            shutil.copy(path, tmp)
            os.rename(tmp, os.path.join(self.d, "n%d.npy" % n))
            with open(os.path.join(self.d, "n%d.txt.tmp%d" % (n, os.getpid())), "w") as f:
                f.write("%d %s %s\n" % (v, how, path))
            os.rename(os.path.join(self.d, "n%d.txt.tmp%d" % (n, os.getpid())), os.path.join(self.d, "n%d.txt" % n))
            self.summ.write("%s IMPROVED n %d %s -> %d via %s (%s)\n" % (ts(), n, cur, v, how, path))
            self.summ.flush()
            return True, v
        return False, v


def main():
    a = sys.argv
    bd, out, lo, hi, W, bbcap, B, stop = a[1], a[2], int(a[3]), int(a[4]), int(a[5]), int(a[6]), int(a[7]), float(a[8])
    smul = float(a[9]) if len(a) > 9 else 1.0
    os.makedirs(out, exist_ok=True)
    summ = open(os.path.join(out, "vcycle_summary.txt"), "a")
    best = Best(bd, summ)
    S = lambda n: smul * (40 + 4 * (n - 16))
    k = 0
    while time.time() < stop:
        k += 1
        summ.write("%s cycle %d down pass\n" % (ts(), k))
        summ.flush()
        for n in range(hi - 1, lo - 1, -1):
            if time.time() > stop:
                break
            v1, p1 = best.get(n + 1)
            if p1 is None:
                continue
            pre = os.path.join(out, "c%d_r%d" % (k, n))
            run(["restrict", n + 1, p1, pre], pre + ".log", 120)
            imp, v = best.offer(n, pre + ".npy", "restrict(n%d=%d)" % (n + 1, v1))
            if imp:
                pol = os.path.join(out, "c%d_r%d_pol" % (k, n))
                run(["dlns", n, pre + ".npy", pol, S(n), 1000 * k + n, "pp6", 4000, 3000], pol + ".log", S(n) + 90)
                best.offer(n, pol + ".npy", "restrict+dlns")
        summ.write("%s cycle %d up pass\n" % (ts(), k))
        summ.flush()
        for n in range(lo, hi):
            if time.time() > stop:
                break
            v0, p0 = best.get(n)
            if p0 is None:
                continue
            N = n + 1
            xlo, xhi = max(0, n // 2 - W), min(n - 1, n // 2 + W)
            pre = os.path.join(out, "c%d_e%d" % (k, N))
            txt = run(["extend", n, p0, pre, 2, "pp6", xlo, xhi, bbcap], pre + ".log", (xhi - xlo + 1) * 40 + 60)
            cands = {}
            for m in re.finditer(r"x (\d+) threshold (\d+) mixed-greedy (\d+) full-greedy (\d+)", txt):
                x, v = int(m.group(1)), int(m.group(4))
                if v not in cands:
                    cands[v] = x
            top = sorted(cands.items(), reverse=True)[:B]
            for v, x in top:
                best.offer(N, "%s_x%d.npy" % (pre, x), "extend(n%d=%d,x=%d)" % (n, v0, x))
            vb, pb = best.get(N)
            if top and top[0][0] >= vb * 0.995:
                x = top[0][1]
                pol = os.path.join(out, "c%d_e%d_x%d_pol" % (k, N, x))
                run(["dlns", N, "%s_x%d.npy" % (pre, x), pol, S(N), 1000 * k + N, "pp6", 4000, 3000], pol + ".log",
                    S(N) + 90)
                best.offer(N, pol + ".npy", "extend+dlns(x=%d)" % x)


if __name__ == "__main__":
    main()
