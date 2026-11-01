# L9 part D: random parents (c,h) -> children by the verifier's float ops; exact (integer) cover test.
# Shows (i) failures exist for small h (float semantics!), (ii) none for h >= threshold of the sufficient condition.
import numpy as np, math
INFL = 1e-11; lam = 1.0+INFL; u = 2.0**-53; epsp = lam-1.0
def I(x): return int(math.ldexp(x, 200))
rng = np.random.default_rng(11)
def trial(c, h):
    half = h*0.5; cl = c-half; cr = c+half; hc = half*lam
    ok = (I(cl)-I(hc) <= I(c)-I(h)) and (I(cr)+I(hc) >= I(c)+I(h)) and (I(cl)+I(hc) >= I(cr)-I(hc))
    return ok
print("h-range            trials  exact-cover failures   sufficient-cond holds for all?")
for lo, hi in ((1e-8, 1e-7), (1e-7, 1e-6), (1e-6, 1e-5), (1e-5, 1.5e-5), (1.5e-5, 3e-5), (3e-5, 1e-4), (1e-4, 1e-3), (1e-3, 0.7)):
    N = 200000; fails = 0; suff_all = True; fail_with_suff = 0
    hs = 10**rng.uniform(np.log10(lo), np.log10(hi), N); cs = rng.uniform(-0.7, 0.7, N)
    for c, h in zip(cs, hs):
        ok = trial(float(c), float(h)); s = (h*epsp >= u*(2*abs(c)+h*(1+lam)))
        if not ok: fails += 1
        if s and not ok: fail_with_suff += 1
    print(f"[{lo:.1e},{hi:.1e}]  {N}  {fails}   (cases where sufficient cond holds but cover FAILS: {fail_with_suff})")
