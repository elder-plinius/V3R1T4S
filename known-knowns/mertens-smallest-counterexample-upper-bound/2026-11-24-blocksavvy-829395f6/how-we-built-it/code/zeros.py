"""Certified zeta zeros rho_n = 1/2 + i gamma_n (FLINT/Arb acb.zeta_zeros: index-rigorous isolation) and zeta'(rho_n).
Usage: python zeros.py START END CHUNK WORKERS OUTDIR [PREC]   (needs python-flint >= 0.9)"""
import sys, os, json, time
from multiprocessing import Pool
from flint import acb, acb_series, ctx
def chunk(args):
    n0, cnt, outdir, prec = args
    fn = os.path.join(outdir, "z_%08d_%05d.jsonl" % (n0, cnt))
    if os.path.exists(fn): return fn, 0.0
    ctx.prec = prec; t = time.time()
    zs = acb.zeta_zeros(n0, cnt); lines = []
    for i, r in enumerate(zs):
        d = acb_series([r, 1], prec=2).zeta().coeffs()[1]
        # Plain arb str (no `more`): Arb guarantees that parsing the string back gives a ball containing the value.
        lines.append(json.dumps({"n": n0 + i, "g": r.imag.str(radius=True, n=85),
            "re": r.real.str(radius=True, n=10),
            "dr": d.real.str(radius=True, n=75), "di": d.imag.str(radius=True, n=75)}))
    open(fn + ".tmp", "w").write("\n".join(lines) + "\n"); os.replace(fn + ".tmp", fn)
    return fn, time.time() - t
if __name__ == "__main__":
    a, b, c, w, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    prec = int(sys.argv[6]) if len(sys.argv) > 6 else 256
    os.makedirs(out, exist_ok=True)
    with Pool(w) as p:
        for fn, dt in p.imap_unordered(chunk, [(n, min(c, b - n + 1), out, prec) for n in range(a, b + 1, c)]):
            print(os.path.basename(fn), "%.1fs" % dt, flush=True)
