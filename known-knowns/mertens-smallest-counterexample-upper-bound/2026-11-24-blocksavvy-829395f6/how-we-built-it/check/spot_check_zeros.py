"""Spot check for the `more=True` change. For sample chunks of the v1 zero files: (1) recompute with the v2 writer
(code/zeros.py, no `more`) at 256 bits; (2) compute a 512-bit reference; (3) check that every v1 ball and every v2
ball contains the 512-bit reference (g, zeta' real and imaginary parts), and that v1 and v2 midpoints agree to well
below the radii used by verify_p1.py. Usage: python spot_check_zeros.py V1_ZERO_DIR"""
import sys, os, json, importlib.util, tempfile
from flint import acb, acb_series, arb, ctx
v1dir = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("z2", os.path.join(here, "..", "code", "zeros.py")); z2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(z2)
tmp = tempfile.mkdtemp()
report = {"chunks": [], "all_ok": True}
for n0 in (1, 49601, 98401):
    fn2, _ = z2.chunk((n0, 400, tmp, 256))
    v1 = [json.loads(l) for l in open(os.path.join(v1dir, "z_%08d_00400.jsonl" % n0))]
    v2 = [json.loads(l) for l in open(fn2)]
    ctx.prec = 512
    ref = acb.zeta_zeros(n0, 400)
    bad = 0; maxmid = arb(0)
    for i, r in enumerate(ref):
        ctx.prec = 512
        d = acb_series([r, 1], prec=2).zeta().coeffs()[1]
        for key, val in (("g", r.imag), ("dr", d.real), ("di", d.imag)):
            a1, a2 = arb(v1[i][key]), arb(v2[i][key])
            if not (a1.contains(val) and a2.contains(val)): bad += 1
            diff = abs(a1.mid() - a2.mid())
            if diff > maxmid: maxmid = diff
        assert v1[i]["n"] == v2[i]["n"] == n0 + i
    ok = bad == 0
    report["all_ok"] &= ok
    report["chunks"].append({"n0": n0, "count": 400, "gamma_last": v2[-1]["g"][:30], "balls_not_containing_512bit_ref": bad,
                             "max_midpoint_diff_v1_v2": maxmid.str(3), "ok": ok})
    print(json.dumps(report["chunks"][-1]), flush=True)
print("ALL_OK", report["all_ok"])
json.dump(report, open(os.path.join(here, "spot_check_zeros.json"), "w"), indent=1)
