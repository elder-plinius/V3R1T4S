"""Method B data: high-precision ln beta(m) for periodic rows, via exact fixed-point (u128) power iteration.
For each m: double power iteration -> exact refine (cw, VECOUT) -> `hp` iterations; eigenvalue = sqrt(||Tx||^2/||x||^2) from exact sums.
usage: python -I hprun.py m_list(comma) [hp_iters]    environment P (default 1)
Writes out/hp_P{P}_m{m}.json with ln(lambda) at 60 digits for the last three iterations.
"""
import subprocess, sys, json, os, time, re
from mpmath import mp, mpf, log, sqrt, nstr
mp.dps = 90
BIN = "{WORKDIR}/"
OUT = "{WORKDIR}/"
ms = [int(x) for x in sys.argv[1].split(",")]
hpit = int(sys.argv[2]) if len(sys.argv) > 2 else 25
P = int(os.environ.get("P", "1"))
env = dict(os.environ, NTH="12")
def val(limbs): return sum(int(c) << (32 * k) for k, c in enumerate(limbs))
for m in ms:
    t0 = time.time()
    vd = OUT + "tmp_P%d_m%d.dbl" % (P, m); vx = OUT + "tmp_P%d_m%d.u128" % (P, m)
    subprocess.check_call([BIN + "mdtm_dbl", "pow", str(m), str(P), "80", vd], stdout=subprocess.DEVNULL, env=env)
    e2 = dict(env, VECOUT=vx)
    subprocess.check_call([BIN + "mdtm_ex", "cw", str(m), str(P), vd, "6"], stdout=subprocess.DEVNULL, env=e2)
    os.remove(vd)
    out = subprocess.check_output([BIN + "mdtm_ex", "hp", str(m), str(P), str(hpit), vx], text=True, env=env)
    os.remove(vx)
    ests = []
    for line in out.strip().split("\n"):
        mt = re.match(r"IT (\d+) XX (.*) YY (.*) ovf (\d+)", line)
        assert mt, line
        xx = val(mt.group(2).split()); yy = val(mt.group(3).split()); assert int(mt.group(4)) == 0
        ests.append(log(mpf(yy) / mpf(xx)) / 2)
    d = {"m": m, "P": P, "hp_iters": hpit, "ln_lambda_last3": [nstr(e, 70, strip_zeros=False) for e in ests[-3:]],
         "diff_last2": nstr(ests[-1] - ests[-2], 5), "ln_lambda": nstr(ests[-1], 70, strip_zeros=False)}
    json.dump(d, open(OUT + "hp_P%d_m%d.json" % (P, m), "w"), indent=1)
    print(m, d["ln_lambda"][:60], "diff_last2", d["diff_last2"], "%.1fs" % (time.time() - t0), flush=True)
