#!/usr/bin/env python3
"""Supplementary re-certification: conservative h=T compensation.

SSZ's printed display (28) uses E[a0 | return] = (h-a)/(1-2*alpha), which is
the expected hitting *time*. The attacker's block count on the diagonal is
a + (h-a)*(1-alpha)/(1-2*alpha). When a is large this makes the printed
display under-pay, so Proposition 3 as printed is not airtight.

This script rebuilds N_{169/250}^{95} with the pointwise maximum of the
printed and corrected cap rewards (a conservative over-pay), includes match
at (a,0,relevant) as Table 1 allows, re-solves, and writes a bias/policy
plus an exact-rational dual (via exact_table1_dual.py --ht-comp max).

Run from claim/:
  python3 code/recert_corrected_ht.py
"""
from __future__ import annotations

import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ssz_table1 as m

# Patch the builder: Table 1 match (a >= h, including h = 0) and max compensation.
def allowed(a, h, f, action, T):
    if a == T or h == T:
        return action == m.ADOPT
    if action == m.ADOPT:
        return True
    if action == m.OVERRIDE:
        return a > h
    if action == m.MATCH:
        return f == m.RELEVANT and a >= h
    if action == m.WAIT:
        return a < T and h < T
    return False


def overpay_w(a, h, alpha, rho):
    C = m.C_of(alpha)
    if a >= h:
        return (1.0 - rho) * (C + 0.5 * ((a - h) / (1.0 - 2.0 * alpha) + a + h))
    q = (alpha / (1.0 - alpha)) ** (h - a)
    printed = (1.0 - q) * (-rho * h) + q * (1.0 - rho) * (C + (h - a) / (1.0 - 2.0 * alpha))
    E_a0 = a + (h - a) * (1.0 - alpha) / (1.0 - 2.0 * alpha)
    corrected = (1.0 - q) * (-rho * h) + q * (1.0 - rho) * (C + E_a0)
    return printed if printed >= corrected else corrected


m.allowed = allowed
m.overpay_w = overpay_w


def main():
    T, alpha, rho = 95, 0.45, 169 / 250
    out_dir = HERE.parent / "object"
    t0 = time.time()
    tables = m.build_action_tables(T, alpha, rho, "over", gamma=0.0)
    sol = m.policy_iteration_tables(tables, T, alpha, rho, "over", ev_tol=1e-10)
    tag_bias = out_dir / "recert_corrected_ht_bias.npy"
    tag_pol = out_dir / "recert_corrected_ht_policy.npy"
    np.save(tag_bias, sol.bias)
    np.save(tag_pol, sol.policy)
    meta = {
        "kind": "supplementary_recert_max_ht_compensation",
        "T": T, "alpha": "9/20", "rho": "169/250",
        "gain_float": sol.gain, "gain_negative": bool(sol.gain < 0),
        "pi_iters": sol.iters, "ev": sol.ev_iters,
        "seconds_solve": time.time() - t0,
        "ht_comp": "max(printed display, corrected E[a0|return])",
        "corrected_E_a0": "a + (h-a)*(1-alpha)/(1-2*alpha)",
        "printed_E_a0": "(h-a)/(1-2*alpha)  # hitting time, not block count",
        "match_includes_h0": True,
    }
    (out_dir / "recert_corrected_ht_solve.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)

    # Exact dual via the independent checker
    import subprocess
    dual_out = out_dir / "recert_corrected_ht_dual.json"
    cmd = [
        sys.executable, str(HERE / "exact_table1_dual.py"),
        "--T", "95", "--alpha", "9/20", "--rho", "169/250",
        "--paying", "over", "--gamma", "0",
        "--eq7-grouping", "rebracketed", "--ht-comp", "max",
        "--bias", str(tag_bias), "--policy", str(tag_pol),
        "--out", str(dual_out),
    ]
    print("RUN", " ".join(cmd), flush=True)
    subprocess.check_call(cmd)


if __name__ == "__main__":
    main()
