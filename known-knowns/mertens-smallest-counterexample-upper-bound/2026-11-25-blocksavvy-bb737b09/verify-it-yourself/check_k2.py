"""Package checker for the p4 claim (Python standard library only; optional FLINT tier).
From the package folder: python3 verify-it-yourself/check_k2.py   (set FLINT=1 to also recompute chunks with python-flint)
Checks: object file hashes; every chunk record; index contiguity n = 1..2,325,573 with gamma increasing; the K2 ball
re-summed exactly in Decimal from the stored chunk balls minus the excluded n = 2,325,573 term; that ball equals the
stored one digit for digit, overlaps the stored arb ball, lies inside the certificate's K2 ball, and exceeds 1 + E
(E = the certificate's own 2.391e-11, not checked here); INDEX.csv row and sha256."""
import os, sys, json, hashlib, csv
from decimal import Decimal, Context, Inexact
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE); OBJ = os.path.join(PKG, "object")
CTX = Context(prec=2000, traps=[Inexact]); ok = True
def bad(msg):
    global ok; ok = False; print("FAIL:", msg)
def good(msg): print("ok:  ", msg)
def ball(s):
    s = s.strip()
    if s.startswith("["):
        b = s[1:-1].strip()
        if b.startswith("+/-"): return Decimal(0), Decimal(b[3:].strip())
        m, r = b.split("+/-"); return Decimal(m.strip()), Decimal(r.strip())
    return Decimal(s), Decimal(0)
R = json.load(open(os.path.join(OBJ, "k2_result.json")))
for fn, h in R["chunk_files_sha256"].items():
    got = hashlib.sha256(open(os.path.join(OBJ, fn), "rb").read()).hexdigest()
    (good if got == h else bad)("sha256 %s" % fn)
rows = []
for fn in ("chunks_head128.jsonl", "chunks_tail_1.jsonl", "chunks_tail_2.jsonl"):
    for line in open(os.path.join(OBJ, fn)):
        rows.append(json.loads(line))
n, last_g = 1, Decimal(0); prec_ok = True
for r in rows:
    if r["n0"] != n: bad("gap or overlap at n = %d (record n0 = %d)" % (n, r["n0"])); break
    gf, gr = ball(r["g_first"]); gl, _ = ball(r["g_last"])
    if not (gf - gr > last_g): bad("gamma not increasing at n0 = %d" % r["n0"]); break
    if r["n0"] <= 600000 and r["prec"] != 128: prec_ok = False
    if r["min_abs_zeta_prime"][0] <= 0: bad("zeta' ball touches 0 at n0 = %d" % r["n0"])
    last_g = gl; n += r["cnt"]
else:
    good("contiguous chunks n = 1..%d, gamma increasing, %d records" % (n - 1, len(rows)))
if n - 1 != 2325573: bad("last index %d, expected 2325573" % (n - 1))
(good if prec_ok else bad)("head chunks n <= 600,000 at 128 bits")
g1, r1 = ball(R["zeros"]["gamma_2325572"]); g2, r2 = ball(R["zeros"]["gamma_2325573"]); T0 = Decimal(1300000)
(good if (g1 + r1 < T0 < g2 - r2) and R["zeros"]["N_T0"] == 2325572 else bad)("boundary: gamma_2325572 < 1.3e6 < gamma_2325573, N(T0) = 2325572")
gl_last, _ = ball(rows[-1]["g_last"])
(good if abs(gl_last - g2) < Decimal("1e-9") else bad)("last stored zero is n = 2,325,573 (excluded from the sum)")
m, rad = Decimal(0), Decimal(0)
for r in rows:
    a, b = ball(r["S"]); m = CTX.add(m, a); rad = CTX.add(rad, b)
a, b = ball(R["excluded_term_n2325573_half"])
if abs(a) + b > Decimal("1e-100"): bad("excluded term not negligible")
m = CTX.multiply(CTX.subtract(m, a), 2); rad = CTX.multiply(CTX.add(rad, b), 2)
(good if str(m) == R["K2_decimal_mid"] and str(rad) == R["K2_decimal_rad"] else bad)("K2 re-summed exactly: mid %.20s..., rad %.6e" % (m, rad))
am, ar = ball(R["K2_arb"])
(good if abs(am - m) <= ar + rad else bad)("overlaps stored arb ball %s" % R["K2_arb"])
cm, cr = ball(R["certificate"]["K2"])
(good if (m - rad >= cm - cr and m + rad <= cm + cr) else bad)("inside the certificate's K2 ball %s" % R["certificate"]["K2"])
E = Decimal("2.391e-11"); margin = m - rad - 1 - E
(good if margin > 0 else bad)("lower(K2) - 1 - E = %.6e > 0 (E = certificate's own value, unchecked)" % margin)
mm, mr = ball(R["certificate"]["K2_main_n<=600000"])
hm, hr = ball(R["K2_head_arb"])
(good if abs(hm - mm) <= hr + mr else bad)("head n <= 600,000 overlaps the certificate's K2_main")
idx = list(csv.DictReader(open(os.path.join(PKG, "INDEX.csv"))))
if len(idx) == 1:
    h = hashlib.sha256(open(os.path.join(PKG, idx[0]["file"]), "rb").read()).hexdigest()
    (good if h == idx[0]["sha256"] and idx[0]["target_id"] == R["target_id"] else bad)("INDEX.csv row and sha256 of %s" % idx[0]["file"])
else: bad("INDEX.csv must have exactly one row")
if os.environ.get("FLINT") == "1":
    try:
        from flint import acb, arb, acb_series, ctx
    except ImportError:
        bad("FLINT=1 but python-flint is not installed")
    else:
        by = {r["n0"]: r for r in rows}
        for n0 in (1, 300001, 1462801, 2325201):
            r = by[n0]; ctx.prec = r["prec"]; S = arb(0)
            V = arb("3484971332733132396.5383341489440461"); K = arb("1.5e-10")
            for rho in acb.zeta_zeros(n0, r["cnt"]):
                g = rho.imag; zp = acb_series([rho, 1], prec=2).zeta().coeffs()[1]
                S += (-(K * g * g)).exp() * (acb(0, g * V).exp() / (rho * zp)).real
            (good if S.str(25, radius=True) == r["S"] else bad)("FLINT recompute of chunk n0 = %d" % n0)
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
