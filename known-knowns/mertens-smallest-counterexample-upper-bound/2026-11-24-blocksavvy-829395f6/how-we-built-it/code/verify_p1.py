"""Certified h_StR / h_P at Kim-Nguyen's published y values (inputs/Test-ST.txt, inputs/Test-Pinch.txt).
h(y) = 2 sum_{0<gamma<T} exp(-k gamma^2) Re( e^{i gamma y} / (rho zeta'(rho)) ),  rho = 1/2 + i gamma
     = 2 sum alpha exp(-k gamma^2) cos(gamma y - psi),  alpha = 1/|rho zeta'(rho)|, psi = arg(rho zeta'(rho)).
h_StR: k = 3e-9, T = 74000.  h_P: k = 1.5e-6, T = 14000.   Usage: python verify_p1.py ZERODIR > out.json"""
import sys, os, glob, json
from flint import arb, acb, ctx
HERE = os.path.dirname(os.path.abspath(__file__))
def load(zdir, cutoff):
    ctx.prec = 320
    rows = sorted((json.loads(l) for f in glob.glob(os.path.join(zdir, "z_*.jsonl")) for l in open(f) if l.strip()), key=lambda r: r["n"])
    out = []
    for i, r in enumerate(rows):
        assert r["n"] == i + 1, "gap in zero indices"
        g = arb(r["g"])
        if g < cutoff: out.append(r); continue
        assert g > cutoff; return out   # zero number len(out)+1 lies above the cutoff: list complete
    raise SystemExit("zero list does not reach the cutoff")
def h(y, k, rows, prec):
    ctx.prec = prec; Y = arb(y); K = arb(k); half = arb(1) / 2; s = arb(0)
    for r in rows:
        g = arb(r["g"]); w = acb(half, g) * acb(arb(r["dr"]), arb(r["di"]))
        s += (-(K * g * g)).exp() * (acb(0, g * Y).exp() / w).real
    return 2 * s
zd = sys.argv[1]
S = load(zd, 74000); P = load(zd, 14000)
res = {"N_gamma_lt_74000": len(S), "N_gamma_lt_14000": len(P), "values": []}
for fn, k, rows in (("Test-ST.txt", "3e-9", S), ("Test-Pinch.txt", "1.5e-6", P)):
    for y in open(os.path.join(HERE, "..", "inputs", fn)).read().split():
        a, b = h(y, k, rows, 256), h(y, k, rows, 320)
        res["values"].append({"file": fn, "y": y, "k": k, "h_256": a.str(20, radius=True), "h_320": b.str(20, radius=True),
                              "overlap": bool(a.overlaps(b)), "abs_minus_1_lower": (abs(b) - 1).lower().str(8)})
        print(json.dumps(res["values"][-1]), file=sys.stderr, flush=True)
print(json.dumps(res, indent=1))
