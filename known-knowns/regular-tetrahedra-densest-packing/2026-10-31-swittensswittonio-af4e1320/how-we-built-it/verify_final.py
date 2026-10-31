"""Independent re-verification (no searching): reads rho_cert.json and scheme_best.json, re-checks every inequality with Arb balls,
prints the final certified bound.  Run:  venv\\Scripts\\python.exe code\\verify_final.py   (from attempts/formalist-3)."""
import json, os, sys, math
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import rig_dp as R
import scheme as S
from flint import arb

rho = {tuple(map(int, k.split(','))): v for k, v in json.load(open(os.path.join(here, 'rho_cert.json'))).items()}
R.rho.clear(); R.rho.update(rho)

print("alpha =", R.AL, "\n1-alpha >= %.12g ; 1/2-alpha >= %.12g ; Lemma A: rho(c>=2,1) >= sqrt2/(3 pi) >= %.12g ; FCAP <= %.12g"
      % (R.down(R.ONE_MINUS_AL), R.down(R.HMA), R.down(R.S2 / (3 * R.PI)), R.up(R.FCAP)))
assert rho[(0, 1)] <= R.down(R.ONE_MINUS_AL) and rho[(1, 1)] <= R.down(R.HMA) and rho[(0, 2)] <= R.down(R.HMA)
for c in range(2, 12): assert rho[(c, 1)] <= R.down(R.S2 / (3 * R.PI))
states = sorted([k for k in rho if k[1] >= 2 and k != (0, 2)], key=lambda x: (x[0] + x[1], x[1]))
verified = set(); failed = []
for k in states:
    c, w = k; t = w * R.al_f + c / 2
    ok = R.cert_lt1(c, w, rho[k]) if t < 1 else R.cert_gt1(c, w, rho[k])
    if ok: verified.add(k)
    else: failed.append(k)
# monotone closure: rho(k) <= rho(k2) allowed only if k2 >= k (w2>=w, c2+w2>=c+w) is itself verified or a base value; then
# the class K(k2) contains K(k), hence inf over K(k) <= ... : we need rho(k) <= rho(k2) *for the smaller class k <= k2*  (rho(k) >= rho(k2))
for k in failed:
    ok = any(k2 in verified and k2[1] >= k[1] and k2[0] + k2[1] >= k[0] + k[1] and rho[k2] >= rho[k] for k2 in verified)
    print("  closure-justified" if ok else "  FAILED", k, rho[k])
    assert ok
print("directly verified states:", len(verified), " closure-justified:", len(failed))
for k in [(1, 2), (0, 3), (2, 2), (1, 3), (0, 4), (3, 2), (2, 3), (1, 4), (0, 5), (0, 6), (0, 10), (0, 50), (0, 151)]:
    if k in rho: print("rho_hat%s >= %.6e" % (k, rho[k]))
best = json.load(open(os.path.join(here, 'scheme_best.json')))
o = S.cert(best["Q"], best["k"], best["u"])
assert o["ok"]
print("scheme (Q=%d, k=%d, u=%s): gamma_Q=%.6f r_v=%.6f d=%.5f q=%d q_v=%d m=%d m_v=%d good/tet=%d Delta=%d" % (
    o["Q"], o["k"], o["u"], o["gamma_Q"], o["r_v"], o["d"], o["q"], o["qv"], o["m"], o["mv"], o["good"], o["Delta"]))
print("rho_hat(0,Q) used = %.6e ; b >= %.6e ; CERTIFIED density <= 1 - %.6e" % (o["rho_Q"], o["b_lb"], o["density_deficit_lb"]))
print("published (GEK): 1 - 2.6e-25 ; ratio of deficits = %.3e" % (o["density_deficit_lb"] / 2.6e-25))
