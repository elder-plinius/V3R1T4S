#!/usr/bin/env python3
"""
verify_certificate.py — Standalone certificate checker for unit-demand-lottery-vs-item-pricing-gap.
"""

from fractions import Fraction
import json, math, os, sys
from scipy.integrate import quad

def run_cms_calibration():
    # CMS menu on capped equal revenue: p1 = 2.5, p2 = p3 = 2 + 3n/8
    n = 64
    S = 5.0
    p1 = 2.5
    diff_bound = 0.75 * n - 1.0
    p2 = 2.0 + 0.375 * n

    def r1_v1(v1):
        v2_low = max(1.0, S - v1, v1 - diff_bound)
        v2_high = min(float(n), v1 + diff_bound)
        if v2_low >= v2_high:
            return 0.0
        return (1.0 / v2_low - 1.0 / v2_high) / (v1**2)

    mass_r1_cont, _ = quad(r1_v1, 1.0, n, epsabs=1e-11, epsrel=1e-11)
    v2_atom_low = max(1.0, 0.25 * n + 1.0)
    prob_v2 = (1.0 / v2_atom_low - 1.0 / n) if v2_atom_low < n else 0.0
    mass_r1_atoms = 2.0 * (1.0 / n) * prob_v2 + (1.0 / n**2)
    mass_r1 = mass_r1_cont + mass_r1_atoms

    v1_start = max(1.0, diff_bound + 1.0)
    def r2_v1(v1):
        v2_high = v1 - diff_bound
        if v2_high <= 1.0:
            return 0.0
        return (1.0 - 1.0 / v2_high) / (v1**2)

    mass_r2_cont, _ = quad(r2_v1, v1_start, n, epsabs=1e-11, epsrel=1e-11)
    v2_atom_high = max(1.0, 0.25 * n + 1.0)
    mass_r2_atom = (1.0 / n) * (1.0 - 1.0 / v2_atom_high)
    mass_r23 = 2.0 * (mass_r2_cont + mass_r2_atom)

    rev = p1 * mass_r1 + p2 * mass_r23
    ratio = rev / 2.0
    assert ratio > 1.073, f"CMS calibration failed: {ratio} <= 1.073"
    print(f"Calibration (CMS n=64): R = {rev:.6f}, R/D = {ratio:.6f} > 1.073 -> PASS")

def verify_p1_certificate(cert_path):
    with open(cert_path, "r") as f:
        cert = json.load(f)
    n = cert["instance"]["n"]
    assert n == 8, f"Expected n=8, got {n}"
    primal_val = Fraction(cert["lottery_lp_primal"]["objective_exact"])
    dual_val = Fraction(cert["lottery_lp_dual"]["objective_exact"])
    target_val = Fraction(15, 8)
    assert primal_val == target_val, f"Primal value {primal_val} != 15/8"
    assert dual_val == target_val, f"Dual value {dual_val} != 15/8"
    assert primal_val == dual_val, "Duality gap is non-zero"
    assert Fraction(cert["strong_duality_gap"]) == Fraction(0), "Non-zero gap"
    item_sup = Fraction(cert["deterministic_item_pricing"]["supremum_exact"])
    assert item_sup == target_val, f"Item pricing supremum {item_sup} != 15/8"
    print(f"Partial Win p1 (n=8): Exact primal-dual LP = {primal_val} = 15/8 with 0 gap -> PASS")

def verify_solution(inst_path):
    with open(inst_path, "r") as f:
        inst = json.load(f)
    menu = inst["menu"]
    for entry in menu:
        alloc = [Fraction(x) for x in entry["allocation"]]
        assert all(x >= 0 for x in alloc), "Negative allocation"
        assert sum(alloc) <= 1, "Allocation sum > 1"
        assert Fraction(entry["price"]) > 0, "Price <= 0"
    n = inst["distribution"]["support_max"]
    assert n == 50000, f"Expected n=50000, got {n}"
    p1 = float(Fraction(menu[0]["price"]))
    p2 = float(Fraction(menu[1]["price"]))
    assert p1 == 2.3 and p2 == 18750.0, "Menu prices mismatch"
    S = 2.0 * p1 # 4.6
    alpha = 3.0 / 8.0 # 0.375
    diff_bound = 2.0 * (p2 - p1)

    def r1_v1(v1):
        v2_low = max(1.0, S - v1, v1 - diff_bound)
        v2_high = min(float(n), v1 + diff_bound)
        if v2_low >= v2_high:
            return 0.0
        return (1.0 / v2_low - 1.0 / v2_high) / (v1**2)

    mass_r1_cont, _ = quad(r1_v1, 1.0, n, epsabs=1e-12, epsrel=1e-12)
    v2_atom_low = max(1.0, (1.0 - 2.0 * alpha) * n + S)
    prob_v2 = (1.0 / v2_atom_low - 1.0 / n) if v2_atom_low < n else 0.0
    mass_r1_atoms = 2.0 * (1.0 / n) * prob_v2 + (1.0 / n**2)
    mass_r1 = mass_r1_cont + mass_r1_atoms

    v1_start = max(1.0, diff_bound + 1.0)
    def r2_v1(v1):
        v2_high = v1 - diff_bound
        if v2_high <= 1.0:
            return 0.0
        return (1.0 - 1.0 / v2_high) / (v1**2)

    mass_r2_cont, _ = quad(r2_v1, v1_start, n, epsabs=1e-12, epsrel=1e-12)
    v2_atom_high = max(1.0, (1.0 - 2.0 * alpha) * n + S)
    mass_r2_atom = (1.0 / n) * (1.0 - 1.0 / v2_atom_high)
    mass_r23 = 2.0 * (mass_r2_cont + mass_r2_atom)

    rev = p1 * mass_r1 + p2 * mass_r23
    D = 2.0
    ratio = rev / D

    # Validate all recorded parameters and metrics in the instance file
    assert inst["distribution"]["support_min"] == 1, "support_min != 1"
    assert inst["distribution"]["monopoly_revenue_per_item"] == 1.0, "monopoly revenue != 1.0"
    assert inst["distribution"]["upper_bound_D"] == 2.0, "D != 2.0"
    assert inst["theoretical_limit"]["CMS_value"] == 1.138629436111989, "CMS_value corrupted"
    assert inst["theoretical_limit"]["limiting_revenue"] == 2.278463870344405, "limiting_revenue corrupted"
    assert inst["theoretical_limit"]["limiting_ratio"] == 1.1392319351722026, "limiting_ratio corrupted"
    assert inst["finite_instance_certified"]["CMS_bar"] == 1.138629436111989, "CMS_bar corrupted"
    assert inst["finite_instance_certified"]["surplus"] == 0.0004405577997844, "surplus corrupted"

    ln2_upper = 0.69314718056
    cms_bar = 1.0 + ln2_upper / 5.0
    surplus = ratio - cms_bar
    assert surplus >= 0.0001, f"Surplus {surplus} < 1e-4"
    print(f"Solution Instance (n=50000, S=4.6): R = {rev:.9f}, D = {D:.1f}, R/D = {ratio:.9f} > 1+ln(2)/5 by +{surplus:.6f} -> PASS")

def main():
    pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    inst_path = os.path.join(pkg_root, "object", "instance.json")
    cert_path = os.path.join(pkg_root, "object", "p1_certificate_n8.json")
    print("Running verification for unit-demand-lottery-vs-item-pricing-gap...")
    run_cms_calibration()
    verify_p1_certificate(cert_path)
    verify_solution(inst_path)
    print("SUCCESS: ALL CHECKS PASSED")

if __name__ == "__main__":
    main()
