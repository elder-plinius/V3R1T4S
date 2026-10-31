"""Certified chain rho_hat(c,w) with the sharper single-wedge excess E2 (Lemma V2, estab.py) in place of E (Lemma V).
Everything else is rig_dp.py unchanged (monkey-patched: rig_dp.E_up -> estab.E_up_combined, rig_dp.E_f -> estab.E_f_table).
Run: python code/rig2.py 150  > code/rig2.out   (writes code/rho_cert2.json)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rig_dp as R
import estab
R.E_up = estab.E_up_combined
R.E_f = estab.E_f_table

def main(QMAX):
    NMAX = 5
    order = sorted([(c, w) for w in range(2, 6) for c in range(0, 5) if c + w <= NMAX and (c, w) != (0, 2)], key=lambda x: (x[0] + x[1], x[1]))
    for (c, w) in order:
        Tf, T, t = R.solve_state(c, w, None)
        print("state", (c, w), "t=%.3f" % t, "float %.6e  CERTIFIED lower bound %.6e" % (Tf, T), flush=True)
        R.mono_close(R.rho, R.rho)
    for w in range(6, QMAX + 2):
        Tf, T, t = R.solve_state(0, w, None)
        R.rho[(0, w)] = min(T, R.rho[(0, w - 1)])
        if w <= 10 or w % 10 == 0: print("state", (0, w), "t=%.3f" % t, "float %.6e  CERTIFIED %.6e" % (Tf, R.rho[(0, w)]), flush=True)
    out = {"%d,%d" % k: v for k, v in R.rho.items()}
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rho_cert2.json"), "w"), indent=1, sort_keys=True)
    print("rho_cert2(0,5) =", R.rho[(0, 5)], " rho_cert2(0,%d) =" % (QMAX + 1), R.rho[(0, QMAX + 1)])

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 60)
