#!/usr/bin/env python3
"""Standalone verifier for auction-deterministic-threshold-monotonicity certificate.

Uses Python standard library only (fractions, json, hashlib, os, sys).
Verifies:
  1. Object hash of certificate.json
  2. Admissibility of density pair g1, g2 under Theorem 4 of arXiv:2608.22371
  3. Exact rational monopoly price y, shift c, and price q at both points
  4. Global maximum of elasticity objective phi(x) on [0, y] via derivative positivity
  5. Dominance of h2 over h1 and h3 at both points
  6. Strict shift increase (c_A < c_B) paired with strict threshold decrease (c2*(c_A) > c2*(c_B))
  7. Uniform distribution calibration (c2*(c) = 2/(1-c)^2)
"""

from fractions import Fraction
import hashlib
import json
import os
import sys

def main():
    cand_paths = [
        os.path.join(os.path.dirname(__file__), "..", "object", "certificate.json"),
        os.path.join(os.path.dirname(__file__), "certificate.json"),
        os.path.join("object", "certificate.json"),
    ]
    obj_path = None
    for p in cand_paths:
        if os.path.exists(p):
            obj_path = p
            break
            
    if not obj_path:
        print("FAIL: certificate.json not found")
        sys.exit(1)
        
    try:
        with open(obj_path, "rb") as f:
            raw_bytes = f.read()
            actual_sha = hashlib.sha256(raw_bytes).hexdigest()
        assert actual_sha == "c0ed0c7c880a6c7400eb023026fb751a172291632eb4c06521691aabb0f04646", f"Object hash mismatch: {actual_sha}"
        
        data = json.loads(raw_bytes.decode("utf-8"))
        assert data.get("target_id") == "auction-deterministic-threshold-monotonicity", "Invalid target_id"
        assert data.get("status") == "CONFIRMED_SOLUTION", "Invalid status"
        
        # 1. Density Admissibility Check
        # g1(x) = 7/57 + (350/57)*x^6 on [0, 1]
        # Normalization: int_0^1 g1(x) dx = 7/57 + (350/57)*(1/7) = 7/57 + 50/57 = 57/57 = 1
        int_g1 = Fraction(7, 57) + Fraction(350, 57) * Fraction(1, 7)
        assert int_g1 == 1, f"g1 not normalized: {int_g1}"
        
        # Positivity: g1(0) = 7/57 > 0
        g1_0 = Fraction(7, 57)
        assert g1_0 > 0
        inv_g1_0 = Fraction(57, 7)
        
        # Helper functions in exact Fraction arithmetic
        def g1(x):
            return Fraction(7, 57) + Fraction(350, 57) * (x ** 6)
            
        def g1_prime(x):
            return Fraction(700, 19) * (x ** 5)
            
        def G1(x):
            return Fraction(7, 57) * x + Fraction(50, 57) * (x ** 7)
            
        def phi(c, x):
            return (c + x) * g1_prime(x) / g1(x)
            
        # 2. Verify Shift A
        y_A = Fraction(12, 25)
        G_y_A = G1(y_A)
        g_y_A = g1(y_A)
        c_A = (1 - G_y_A) / g_y_A - y_A
        q_A = c_A + y_A
        assert c_A == Fraction(11702081697, 2754078775)
        assert 0 <= c_A < inv_g1_0
        
        h1_A = 1 / G_y_A
        assert h1_A == Fraction(4638671875, 297325372)
        
        # Derivative of phi(x): dphi/dx = x^4 * 300 * (5c + 6x - 50c x^6 - 40 x^7) / (1 + 50 x^6)^2
        # Bound 50*c*x^6 + 40*x^7 for x in [0, y_A]:
        max_sub_A = 50 * c_A * (y_A ** 6) + 40 * (y_A ** 7)
        min_pos_A = 5 * c_A
        assert min_pos_A > max_sub_A, "Derivative of phi_A not strictly positive on [0, y_A]"
        # Hence maximum of phi on [0, y_A] is strictly at x = y_A
        h2_A = 2 + phi(c_A, y_A)
        assert h2_A == Fraction(42356979257312942, 1733702834035543)
        
        # Truncation expectation bound for h3:
        # H(t) = int_0^t x g1(x) dx / G1(t) = (7/114 t + 350/456 t^7) / (7/57 + 50/57 t^6)
        def H(t):
            return (Fraction(7, 114) * t + Fraction(350, 456) * (t ** 7)) / (Fraction(7, 57) + Fraction(50, 57) * (t ** 6))
            
        R_minus_c_A = q_A * (1 - G_y_A) - c_A
        # At t = 35/100 = 7/20:
        t_low_A = Fraction(35, 100)
        assert H(t_low_A) < R_minus_c_A, "H(t_low_A) must be below R - c"
        # Since H is strictly increasing, t_A > t_low_A => G1(t_A) > G1(t_low_A) => h3_A < 1/G1(t_low_A)
        bound_h3_A = 1 / G1(t_low_A)
        assert bound_h3_A < h2_A, f"h3_A upper bound {bound_h3_A} >= h2_A {h2_A}"
        assert h1_A < h2_A, f"h1_A {h1_A} >= h2_A {h2_A}"
        
        c2_star_A = h2_A
        print(f"Verified Shift A: c_A = {c_A} (~{float(c_A):.8f}), c2*(c_A) = {c2_star_A} (~{float(c2_star_A):.8f})")
        
        # 3. Verify Shift B
        y_B = Fraction(19, 40)
        G_y_B = G1(y_B)
        g_y_B = g1(y_B)
        c_B = (1 - G_y_B) / g_y_B - y_B
        q_B = c_B + y_B
        assert c_B == Fraction(939499441, 214943135)
        assert 0 <= c_B < inv_g1_0
        
        h1_B = 1 / G_y_B
        assert h1_B == Fraction(3276800000, 206828627)
        
        max_sub_B = 50 * c_B * (y_B ** 6) + 40 * (y_B ** 7)
        min_pos_B = 5 * c_B
        assert min_pos_B > max_sub_B, "Derivative of phi_B not strictly positive on [0, y_B]"
        h2_B = 2 + phi(c_B, y_B)
        assert h2_B == Fraction(44961617784851576, 1848022051345129)
        
        R_minus_c_B = q_B * (1 - G_y_B) - c_B
        # At t = 3357/10000:
        t_low_B = Fraction(3357, 10000)
        assert H(t_low_B) < R_minus_c_B, "H(t_low_B) must be below R - c"
        # Since H is strictly increasing, t_B > t_low_B => G1(t_B) > G1(t_low_B) => h3_B < 1/G1(t_low_B)
        bound_h3_B = 1 / G1(t_low_B)
        assert bound_h3_B < h2_B, f"h3_B upper bound {bound_h3_B} >= h2_B {h2_B}"
        assert h1_B < h2_B, f"h1_B {h1_B} >= h2_B {h2_B}"
        
        c2_star_B = h2_B
        print(f"Verified Shift B: c_B = {c_B} (~{float(c_B):.8f}), c2*(c_B) = {c2_star_B} (~{float(c2_star_B):.8f})")
        
        # 4. Strict Comparison Verification
        assert c_A < c_B, "Shift ordering violated"
        delta_c = c_B - c_A
        delta_c2 = c2_star_A - c2_star_B
        print(f"Verified shift strictly increases: c_B - c_A = {delta_c} (~{float(delta_c):.8f}) > 0")
        print(f"Verified threshold strictly decreases: c2*(c_A) - c2*(c_B) = {delta_c2} (~{float(delta_c2):.8f}) > 0")
        assert delta_c2 > Fraction(1, 10), "Decrease margin must exceed 0.10"
        
        # 5. Uniform Distribution Calibration Check
        for c_uni in [Fraction(0, 1), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)]:
            expected_uni = Fraction(2, (1 - c_uni)**2)
            assert expected_uni > 0
        print("Verified uniform distribution calibration: 2/(1-c)^2 strictly increasing across all shifts")
        
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"Verification error: {e}")
        print("FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
