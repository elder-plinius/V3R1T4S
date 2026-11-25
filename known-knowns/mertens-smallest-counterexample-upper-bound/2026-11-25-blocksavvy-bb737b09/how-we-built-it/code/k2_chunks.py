"""K2 at the bzyzz point over zeros n = A..B (arb balls at the PREC argument: 128 for chunks_head128, 96 for chunks_head and chunks_tail), chunked and resumable.
Per chunk stores S = sum exp(-k g^2) Re(exp(i g v)/(rho zeta'(rho))) (WITHOUT the factor 2), the abs sum
sum exp(-k g^2)/|rho zeta'(rho)|, first/last gamma balls, min |zeta'|. Usage: k2_chunks.py A B CHUNK WORKERS OUTDIR PREC"""
import sys, os, json, time
from multiprocessing import Pool
from flint import acb, arb, acb_series, ctx
V = "3484971332733132396.5383341489440461"; K = "1.5e-10"
def run(args):
    n0, cnt, out, prec = args
    fn = os.path.join(out, "c_%08d_%05d.json" % (n0, cnt))
    if os.path.exists(fn): return fn, 0.0
    ctx.prec = prec; t = time.time()
    zs = acb.zeta_zeros(n0, cnt)
    v = arb(V); k = arb(K); S = arb(0); A = arb(0); mz = None
    for i, r in enumerate(zs):
        g = r.imag
        zp = acb_series([r, 1], prec=2).zeta().coeffs()[1]
        w = r * zp
        e = (-(k * g * g)).exp()
        S += e * (acb(0, g * v).exp() / w).real
        A += e / abs(w)
        az = abs(zp).lower()
        if mz is None or az < mz[0]: mz = (float(az), n0 + i)
    res = {"n0": n0, "cnt": cnt, "prec": prec, "g_first": zs[0].imag.str(30, radius=True),
           "g_last": zs[-1].imag.str(30, radius=True), "S": S.str(25, radius=True), "Abs": A.str(12, radius=True),
           "min_abs_zeta_prime": mz}
    json.dump(res, open(fn + ".tmp", "w")); os.replace(fn + ".tmp", fn)
    return fn, time.time() - t
if __name__ == "__main__":
    a, b, c, w, out, prec = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], int(sys.argv[6])
    os.makedirs(out, exist_ok=True)
    jobs = [(n, min(c, b - n + 1), out, prec) for n in range(a, b + 1, c)]
    with Pool(w) as p:
        for fn, dt in p.imap_unordered(run, jobs):
            print(time.strftime("%H:%M:%S"), os.path.basename(fn), "%.1fs" % dt, flush=True)
