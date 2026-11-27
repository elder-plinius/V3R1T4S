"""K5: for every rho level n: lambda_1 == 1 exactly, Lambda(n) = sum|lambda_d| == W(n)/V(n) exactly (rationals), and agreement with
the fixed-point tables (Vfx floor 2^64 dense float copy, Wfx ceil 2^40 dense) within 1e-12 relative. Usage: control_K5.py rhofx json"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lamfx
W = os.environ.get("BRUN_WORK", "work") + "/"
D = np.memmap(W + "Vfx_dense_1e8.bin", dtype=np.float64, mode="r"); Wd = np.memmap(W + "Wfx_dense_1e7.bin", dtype=np.float64, mode="r")
ok = True
for n in sorted(set(r[0] for r in json.load(open(sys.argv[2]))["rho_levels"])):
    r = lamfx.sigma_upper(n, sys.argv[1]); Lam = float(r["Lambda"]); tab = float(Wd[n]) / float(D[n])
    good = r["lam1"] == 1 and r["Lambda"] == r["W"] / r["V"] and abs(Lam - tab) / Lam < 1e-12
    ok &= good
    print("n=%d lambda_1==1:%s Lambda==W/V:%s Lambda=%.15g table W/V=%.15g rel=%.1e %s" % (n, r["lam1"] == 1, r["Lambda"] == r["W"] / r["V"], Lam, tab, abs(Lam - tab) / Lam, "ok" if good else "BAD"))
print("note: table W/V is an upper bound (W ceil, V floor), so table >= exact is expected")
print("PASS" if ok else "FAIL")
