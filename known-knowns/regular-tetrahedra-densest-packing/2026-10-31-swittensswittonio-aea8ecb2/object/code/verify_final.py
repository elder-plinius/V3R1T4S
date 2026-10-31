"""verify_final.py -- independent re-certification of everything stored by fullchain.py.
Reads rho_cert.json and scheme_best_<Q>.json (stored next to this file), re-checks base values, every state of the table (Lemma R) and the scheme
(Claims 1-3) with Arb balls, and prints the final bound as the LAST line.
Usage: python verify_final.py [Q=40] [EPSDEN=1000]   (EPSDEN: K4' constant is (3/sqrt2)(1+1/EPSDEN); must be a constant proved by k4_bb.py)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fullchain as F
Q = int(sys.argv[1]) if len(sys.argv) > 1 else 40
EPSDEN = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
rho = F.load_rho(os.path.join(HERE, "rho_cert.json"))
print("alpha = %s" % F.AL)
print("1-alpha >= %.12g ; 1/2-alpha >= %.12g ; Lemma A: rho(c>=2,1) >= sqrt2/(3 pi) >= %.12g ; F <= %.12g" % (F.down(F.ONE_MINUS_AL), F.down(F.HMA), F.down(F.S2 / (3 * F.PI)), F.up(F.FCAP)))
nd, nj = F.recertify(rho)
for k in [(1, 2), (0, 3), (2, 2), (1, 3), (0, 4), (3, 2), (2, 3), (1, 4), (0, 5), (0, 6), (0, 10), (0, 40)]:
    if k in rho: print("rho%s >= %.6e" % (k, rho[k]))
best = json.load(open(os.path.join(HERE, "scheme_best_%d.json" % Q)))
o = F.scheme_cert(best["Q"], best["k"], best["u"], rho, EPSDEN)
assert o["ok"], o
print("scheme (Q=%d, k=%d, u=%s, K4' eps=1/%d): gamma_Q=%.6f r_v=%.6f d=%.5f q=%d (multiplicity) q_v=%d (area count; K2-count would be %d) m_v=%d good/tet=%d" % (
    o["Q"], o["k"], o["u"], EPSDEN, o["gamma_Q"], o["r_v"], o["d"], o["q"], o["qv"], o["qv_old"], o["mv"], o["good"]))
print("checks:", {k: v for k, v in o.items() if isinstance(v, bool)})
print("rho(0,Q) used = %.6e ; b >= %.6e" % (o["rho_Q"], o["b_lb"]))
print("CERTIFIED (Arb, modulo the Residual trust list) density <= 1 - %.6e" % o["density_deficit_lb"])
