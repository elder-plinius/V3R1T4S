"""Ablation of the three rigorous improvements (Q=40): which part of the gain comes from where.  Prints best certified deficit for
   (chain of previous run | chain with Lemma V2) x (old vertex count q_v | area vertex count), all with the multiplicity count (mu<=q)."""
import os, sys, json, importlib
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
res = {}
for rf in ('rho_cert.json', 'rho_cert2.json'):
    os.environ['RHO_FILE'] = rf
    import scheme2 as S
    importlib.reload(S)
    for av in (False, True):
        best = None
        for ui in range(100, 3200, 10):
            ustr = "%.5f" % (ui / 1e5); kc = int(0.31 / (ui / 1e5))
            for k in range(max(2, kc - 40), kc + 25):
                o = S.cert(40, k, ustr, use_area_vertex=av)
                if o.get("ok") and (best is None or o["density_deficit_lb"] > best["density_deficit_lb"]): best = o
        print("chain=%-15s area_vertex=%-5s -> deficit %.4e  (k=%d u=%s q=%d qv=%d good=%d)" % (rf, av, best["density_deficit_lb"], best["k"], best["u"], best["q"], best["qv"], best["good"]), flush=True)
print("previous run: 1.0215562e-15 (independent set /9, q_v from K2 count, chain rho_cert.json)")
