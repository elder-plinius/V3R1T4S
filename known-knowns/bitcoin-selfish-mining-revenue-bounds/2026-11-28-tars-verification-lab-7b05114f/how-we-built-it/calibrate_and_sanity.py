#!/usr/bin/env python3
"""Table 2 eps-OPT calibration and over-pay sanity, Table 1 builder."""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ssz_table1 as m

TABLE2 = {0.425: 0.56808, 0.45: 0.66891}
out = {"jobs": []}

def report(rec):
    out["jobs"].append(rec)
    print(json.dumps({k: rec[k] for k in rec if k != "hist"}, default=str), flush=True)

for alpha in (0.425, 0.45):
    t0 = time.time()
    rho, sol, tables, rates, hist = m.optimal_under_rev(95, alpha, ev_tol=1e-10)
    rec = {
        "kind": "under_opt_table1", "T": 95, "alpha": alpha, "rev": rates["rev"],
        "table2": TABLE2[alpha], "diff_table2": rates["rev"] - TABLE2[alpha],
        "within_one_last_digit": abs(rates["rev"] - TABLE2[alpha]) <= 1.5e-5,
        "gain": sol.gain, "pi_iters": sol.iters, "seconds": time.time() - t0,
    }
    report(rec)

t0 = time.time()
tables = m.build_action_tables(95, 0.45, 0.66, "over", gamma=0.0)
sol = m.policy_iteration_tables(tables, 95, 0.45, 0.66, "over", ev_tol=1e-10)
rec = {
    "kind": "over_sanity_table1", "T": 95, "alpha": 0.45, "rho": 0.66,
    "gain": sol.gain, "gain_positive": bool(sol.gain > 0),
    "pi_iters": sol.iters, "seconds": time.time() - t0,
}
report(rec)

ok_cal = all(j.get("within_one_last_digit") for j in out["jobs"] if j["kind"] == "under_opt_table1")
ok_san = all(j.get("gain_positive") for j in out["jobs"] if j["kind"] == "over_sanity_table1")
print("CALIBRATION:", "PASS" if ok_cal else "FAIL")
print("SANITY:", "PASS" if ok_san else "FAIL")
