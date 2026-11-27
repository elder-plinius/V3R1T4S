"""Build object/ for the outbox package from claim/: chunk sums as JSONL (head128 + tail, split under 1 MB per file),
plus k2_result.json (arb aggregate, the excluded n = 2,325,573 term, boundary zeros, and the stdlib-Decimal aggregate the
package checker reproduces exactly). Usage: python build_object.py CLAIM_DIR OUT_OBJECT_DIR"""
import sys, os, json, glob, hashlib
from flint import arb, acb, acb_series, ctx
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from k2lib import ball_sum
C, O = sys.argv[1], sys.argv[2]; os.makedirs(O, exist_ok=True)
def load(d):
    rows = [json.load(open(f)) for f in glob.glob(os.path.join(C, d, "c_*.json"))]
    rows.sort(key=lambda r: r["n0"]); return rows
head, tail = load("chunks_head128"), load("chunks_tail")
keys = ["n0", "cnt", "prec", "g_first", "g_last", "S", "Abs", "min_abs_zeta_prime"]
files = {"chunks_head128.jsonl": head, "chunks_tail_1.jsonl": tail[:2200], "chunks_tail_2.jsonl": tail[2200:]}
sums = {}
for fn, rows in files.items():
    with open(os.path.join(O, fn), "w") as f:
        for r in rows: f.write(json.dumps({k: r[k] for k in keys}, separators=(",", ":")) + "\n")
    sums[fn] = hashlib.sha256(open(os.path.join(O, fn), "rb").read()).hexdigest()
ctx.prec = 128
V = arb("3484971332733132396.5383341489440461"); K = arb("1.5e-10")
z = acb.zeta_zeros(2325572, 2); g1, g2 = z[0].imag, z[1].imag
zp = acb_series([z[1], 1], prec=2).zeta().coeffs()[1]
term = (-(K * g2 * g2)).exp() * (acb(0, g2 * V).exp() / (z[1] * zp)).real
agg = json.load(open(os.path.join(C, "result", "aggregate_claim.json")))
mid, rad = ball_sum([r["S"] for r in head + tail], term.str(10, radius=True))
res = {"target_id": "mertens-smallest-counterexample-upper-bound", "partial_win": "p4",
       "point": {"v": "3484971332733132396.5383341489440461", "k": "1.5e-10", "T0": "1300000"},
       "definition": "K2(v) = 2 * sum_{0<gamma<T0} exp(-k gamma^2) * Re(exp(i gamma v)/(rho zeta'(rho))), rho = 1/2 + i gamma",
       "zeros": {"N_T0": 2325572, "gamma_2325572": g1.str(22, radius=True), "gamma_2325573": g2.str(22, radius=True),
                 "source": "FLINT/Arb acb_dirichlet_zeta_zeros via python-flint 0.9.0 (same routine as the certificate)"},
       "excluded_term_n2325573_half": term.str(10, radius=True),
       "K2_arb": agg["K2"], "K2_head_arb": agg["K2_head"], "K2_tail_arb": agg["K2_tail"],
       "K2_decimal_mid": mid, "K2_decimal_rad": rad,
       "certificate": {"K2": "[1.0003052504 +/- 2.30e-11]", "K2_main_n<=600000": "[1.000305250386499012059 +/- 3.21e-22]",
                       "K2_tail_ball": "[+/- 9.43e-12]", "E": "2.391e-11 (certificate's own bound; not checked here)",
                       "source": "https://github.com/bzyzz/mertens_bound/blob/a0b267c2c7ff32a917732cf16ee860d705ca4a08/certification/k2_certificate.json"},
       "chunk_files_sha256": sums, "label": "NUMERICAL"}
json.dump(res, open(os.path.join(O, "k2_result.json"), "w"), indent=1)
print(json.dumps({"mid": mid, "rad": rad, "K2_arb": agg["K2"]}))
