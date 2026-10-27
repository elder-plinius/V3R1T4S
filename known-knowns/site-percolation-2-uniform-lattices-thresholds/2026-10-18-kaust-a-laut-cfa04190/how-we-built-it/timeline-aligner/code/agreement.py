"""Decision rules of PREREG.md for one lattice: TM extrapolation, MC FSS fit, agreement (a), table check (b).

usage: python agreement.py <tm site series> <mc site dir> <table site value> <table sigma>
"""
import io
import math
import os
import sys
import contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "exact-polynomial", "code"))
import extrapolate  # noqa: E402
import fss_mc  # noqa: E402


def mc_primary(d):
    buf = io.StringIO()
    argv = sys.argv
    sys.argv = ["fss_mc.py", d]
    with contextlib.redirect_stdout(buf):
        fss_mc.main()
    sys.argv = argv
    txt = buf.getvalue()
    p = s = None
    stable = None
    for line in txt.splitlines():
        if line.startswith("primary L2>=16"):
            t = line.split()
            p, s = float(t[3]), float(t[5])
        if line.startswith("stability:"):
            stable = "STABLE" in line and "UNSTABLE" not in line
    return p, s, stable, txt


def main():
    series, mcdir, ptab, stab = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    vals = extrapolate.read_series(series)
    with contextlib.redirect_stdout(io.StringIO()):
        med, sig, eloc, ests = extrapolate.extrapolate(vals)
    p_tm, s_tm = float(med), float(sig)
    p_mc, s_mc, stable, txt = mc_primary(mcdir)
    print(txt.rstrip())
    print("TM: n_max %d  p_TM %.10f +- %.2e   (local exponent %.3f)" % (max(vals), p_tm, s_tm, eloc or float("nan")))
    if p_mc is None:
        print("MC: no primary fit yet")
        return
    comb = math.sqrt(s_tm ** 2 + s_mc ** 2)
    print("MC: p_MC %.10f +- %.2e  stability %s" % (p_mc, s_mc, stable))
    print("(a) |TM - MC| = %.3e  vs 3 combined sigma %.3e -> %s" % (abs(p_tm - p_mc), 3 * comb,
                                                                     "AGREE" if abs(p_tm - p_mc) <= 3 * comb else "DISAGREE"))
    cb = math.sqrt(s_tm ** 2 + stab ** 2)
    print("(b) |TM - table| = %.3e vs 3 sigma %.3e -> %s" % (abs(p_tm - ptab), 3 * cb, "WITHIN" if abs(p_tm - ptab) <= 3 * cb else "OUTSIDE"))
    print("requirements: sigma_TM <= 2e-7: %s; sigma_MC <= 2e-6: %s" % (s_tm <= 2e-7, s_mc <= 2e-6))


if __name__ == "__main__":
    main()
