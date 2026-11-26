"""Multi-start polish (lens lns-high).  For each level n in LEVELS (in order): candidates = the R best one-alternative
deletions of best[n+1] (lsx restrict ... all) and the B best clones of best[n-1] (lsx extend, x in (n-1)//2 +- W);
polish each candidate with lsx dlns for S seconds (about one pair pass) in decreasing order of raw count, and offer
every result to the shared BEST/ (vcycle.Best: recount, adopt only if strictly larger).  After an adoption at n,
the R best deletions of the new best[n] are offered to n-1 (raw, no polish).
Usage: python multistart.py BEST OUT LEVELS R B W S STOP_EPOCH
"""
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vcycle import Best, run, ts  # noqa: E402


def main():
    a = sys.argv
    bd, out, levels, R, B, W, S, stop = a[1], a[2], [int(x) for x in a[3].split(",")], int(a[4]), int(a[5]), int(a[6]), \
        float(a[7]), float(a[8])
    os.makedirs(out, exist_ok=True)
    summ = open(os.path.join(out, "multistart_summary.txt"), "a")
    best = Best(bd, summ)
    for n in levels:
        if time.time() > stop:
            break
        cands = []
        v1, p1 = best.get(n + 1)
        if p1:
            pre = os.path.join(out, "L%d_r" % n)
            txt = run(["restrict", n + 1, p1, pre, "all"], pre + ".log", 300)
            rs = sorted(((int(m.group(2)), int(m.group(1))) for m in
                         re.finditer(r"delete (\d+) -> n \d+ count (\d+)", txt)), reverse=True)
            seen = set()
            for v, d in rs:
                if v in seen:
                    continue
                seen.add(v)
                cands.append((v, "%s_v%d.npy" % (pre, d), "restrict(n%d,del %d)" % (n + 1, d)))
                if len(seen) >= R:
                    break
        v0, p0 = best.get(n - 1)
        if p0 and B > 0:
            m_ = n - 1
            xlo, xhi = max(0, m_ // 2 - W), min(m_ - 1, m_ // 2 + W)
            pre = os.path.join(out, "L%d_e" % n)
            txt = run(["extend", m_, p0, pre, 2, "pp6", xlo, xhi, 3000], pre + ".log", (xhi - xlo + 1) * 40 + 60)
            es = {}
            for m in re.finditer(r"x (\d+) threshold (\d+) mixed-greedy (\d+) full-greedy (\d+)", txt):
                es.setdefault(int(m.group(4)), int(m.group(1)))
            for v, x in sorted(es.items(), reverse=True)[:B]:
                cands.append((v, "%s_x%d.npy" % (pre, x), "extend(n%d,x %d)" % (m_, x)))
        cands.sort(reverse=True)
        summ.write("%s level %d candidates %s\n" % (ts(), n, " ".join("%d:%s" % (v, h) for v, f, h in cands)))
        summ.flush()
        for i, (v, f, how) in enumerate(cands):
            if time.time() > stop:
                break
            best.offer(n, f, how + " raw")
            Sn = min(S, max(20, stop - time.time()))
            pol = os.path.join(out, "L%d_c%d_pol" % (n, i))
            txt = run(["dlns", n, f, pol, Sn, 500 + 10 * n + i, "pp6", 4000, 3000], pol + ".log", Sn + 90)
            fin = re.findall(r"final dlns (\d+)", txt)
            summ.write("%s level %d cand %d %s raw %d polished %s\n" % (ts(), n, i, how, v, fin[-1] if fin else "?"))
            summ.flush()
            imp, _ = best.offer(n, pol + ".npy", how + " + dlns")
            if imp and n - 1 >= 14:
                vb, pb = best.get(n)
                pre = os.path.join(out, "L%d_c%d_down" % (n, i))
                run(["restrict", n, pb, pre], pre + ".log", 120)
                best.offer(n - 1, pre + ".npy", "restrict of new best n%d" % n)


if __name__ == "__main__":
    main()
