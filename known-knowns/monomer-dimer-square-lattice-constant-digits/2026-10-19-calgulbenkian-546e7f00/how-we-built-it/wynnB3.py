"""Method B3 (PREREG_B3.md, blind): e_m = L_m - L_{m-1} for ALL widths m = m0+1..mmax, Wynn epsilon at 70 digits.
usage: python -I wynnB2.py [m0=4]      reads out/hp_P0_m*.json (all widths available)
"""
import json, sys, glob
from mpmath import mp, mpf, nstr
mp.dps = 70
OUT = "{WORKDIR}/"
m0 = int(sys.argv[1]) if len(sys.argv) > 1 else 4
fam = sys.argv[2] if len(sys.argv) > 2 else "all"     # all | even
L = {}
for f in glob.glob(OUT + "hp_P0_m*.json"):
    d = json.load(open(f)); L[d["m"]] = mpf(d["ln_lambda"])
def wynn(seq):
    n = len(seq); prev = [mpf(0)] * (n + 1); cur = list(seq); cols = [cur]
    for k in range(1, n):
        new = []
        for i in range(len(cur) - 1):
            diff = cur[i + 1] - cur[i]
            new.append(prev[i + 1] + (1 / diff if diff != 0 else mpf(10) ** 60))
        prev, cur = cur, new; cols.append(cur)
        if len(cur) < 2: break
    best = None
    for k, c in enumerate(cols):
        if k % 2 == 0 and len(c) >= 1: best = (k, c[-1])
    return best
def common(vs):
    ss = [nstr(v, 60, strip_zeros=False) for v in vs]
    n = 0
    while n < min(len(x) for x in ss) and all(x[n] == ss[0][n] for x in ss): n += 1
    return max(n - 2, 0)
step = 1 if fam == "all" else 2
ms = [m for m in sorted(L)]
E = {}
for mmax in ms:
    seq_ms = list(range(m0 + step, mmax + 1, step))
    if any((m not in L) or (m - step not in L) for m in seq_ms) or len(seq_ms) < 8: continue
    seq = [(L[m] - L[m - step]) / step for m in seq_ms]
    k, e = wynn(seq); E[mmax] = e
    print("mmax %2d terms %2d eps_%-2d E = %s" % (mmax, len(seq), k, nstr(e, 48, strip_zeros=False)))
ks = sorted(E)
for i in range(3, len(ks)):
    w = ks[i - 3:i + 1]
    if all(w[j + 1] == w[j] + 1 for j in range(3)) or step == 2:
        print("window", w, "common decimals", common([E[x] for x in w]))
json.dump({str(k): nstr(v, 60, strip_zeros=False) for k, v in E.items()}, open(OUT + "wynnB3_m0_%d_%s.json" % (m0, fam), "w"), indent=1)
