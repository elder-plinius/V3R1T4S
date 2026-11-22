"""EXTENSION beyond the prereg stop (context only): chi = 32..48 warm-started from the chi=28 state. Original: PREREG ladder for Method A: chi = 12, 16, ..., 64 (warm-started), stop when the last four rungs agree on >= 28 decimals of h2 = ln kappa.
usage: python -I ctmchain.py   (run in out/)"""
import subprocess, os, sys, re, json
from mpmath import mp, mpf, log, nstr
mp.dps = 80
SRC = "{WORKDIR}/ctm_md.py"
PY = "python3"
env = dict(os.environ, VECLIB_MAXIMUM_THREADS="2", OMP_NUM_THREADS="2")
vals = {}
def common_decimals(vs):
    ss = [nstr(v, 60, strip_zeros=False) for v in vs]
    L = 0
    while L < min(len(x) for x in ss) and all(x[L] == ss[0][L] for x in ss): L += 1
    return max(L - 2, 0)
prev_state = "ctm_state_28.json"
chis = list(range(32, 52, 4))
for chi in chis:
    log_fn = "ctm_chi%d.log" % chi; st = "ctm_state_%d.json" % chi
    with open(log_fn, "w") as lf:
        subprocess.check_call([PY, "-I", SRC, "vertex", str(chi), "400", "256", prev_state, st], stdout=lf, env=env)
    lines = [l for l in open(log_fn).read().strip().split("\n") if re.match(r"^\d+ 1\.", l)]
    kap = mpf(lines[-1].split()[1])
    h = log(kap)
    vals[chi] = h
    conv = "converged" in open(log_fn).read()
    print("chi", chi, "iters", len(lines), "conv", conv, "h2", nstr(h, 50, strip_zeros=False), flush=True)
    json.dump({str(k): nstr(v, 70, strip_zeros=False) for k, v in vals.items()}, open("ctm_ladder_ext.json", "w"), indent=1)
    prev_state = st
    ks = sorted(vals)
    if len(ks) >= 4:
        last4 = [vals[k] for k in ks[-4:]]
        d = common_decimals(last4)
        print("   last four rungs", ks[-4:], "common decimals", d, flush=True)
