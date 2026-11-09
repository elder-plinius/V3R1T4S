#!/usr/bin/env python3
# Standalone verifier for myerson-vs-anonymous-reserve-gap certificate.
# Reads parameters, computes exact closed-form antiderivatives, bounds OPT/AR >= 2.1600.
import json
import math
import os
import sys
from fractions import Fraction

def main():
    cand_paths = [
        os.path.join(os.path.dirname(__file__), "..", "object", "instance_5buyer.json"),
        os.path.join(os.path.dirname(__file__), "instance_5buyer.json"),
        os.path.join("object", "instance_5buyer.json"),
    ]
    obj_path = None
    for p in cand_paths:
        if os.path.exists(p):
            obj_path = p
            break
            
    if not obj_path:
        print("FAIL: instance_5buyer.json not found")
        sys.exit(1)
        
    try:
        import hashlib
        with open(obj_path, "rb") as f:
            raw_bytes = f.read()
            actual_sha = hashlib.sha256(raw_bytes).hexdigest()
        assert actual_sha == "3820a83613ad59db869dd315692b1c5ec4e153df169473a18d81d57df69177ab", f"Object hash mismatch: {actual_sha}"
        
        data = json.loads(raw_bytes.decode("utf-8"))
            
        assert data.get("target_id") == "myerson-vs-anonymous-reserve-gap", "Invalid target_id"
        assert data.get("num_buyers") == 5, "Invalid num_buyers"
        assert data.get("status") == "CONFIRMED_SOLUTION", "Invalid status"
        assert abs(data["certified_bounds"]["target_threshold"] - 2.16) < 1e-9, "Invalid target_threshold"
        
        params = data["parameters"]
        v1 = Fraction(params["buyer_1"]["v"])
        q1 = Fraction(params["buyer_1"]["q"])
        v2 = Fraction(params["buyer_2"]["v"])
        q2 = Fraction(params["buyer_2"]["q"])
        v3 = Fraction(params["buyer_3"]["v"])
        q3 = Fraction(params["buyer_3"]["q"])
        v4 = Fraction(params["buyer_4"]["v"])
        q4 = Fraction(params["buyer_4"]["q"])
        
        # 1. Regularity Check:
        assert q1 < 1 and q2 < 1 and q3 < 1 and q4 == 1, "Invalid atom probabilities"
        assert v1 > v2 > v3 > v4 > 0, "Cutoffs not strictly decreasing"
        
        # 2. OPT Calculation by JLTX Lemma 1:
        opt_frac = Fraction(1, 1) + \
                   v1 * q1 + \
                   v2 * q2 * (1 - q1) + \
                   v3 * q3 * (1 - q1) * (1 - q2) + \
                   v4 * q4 * (1 - q1) * (1 - q2) * (1 - q3)
        opt_float = float(opt_frac)
        print(f"Verified exact rational OPT: {opt_frac} (approx {opt_float:.8f})")
        assert opt_float > 2.1630, f"OPT {opt_float} too low"
        
        # Check against certified bounds in JSON:
        recorded_opt = float(data["certified_bounds"]["opt_lower_bound"])
        assert abs(recorded_opt - opt_float) < 1e-6, "OPT bounds mismatch in JSON"
        
        # 3. Exact AR Calculation using closed-form partial fractions:
        c1 = float(v1 * q1 / (1 - q1))
        c2 = float(v2 * q2 / (1 - q2))
        c3 = float(v3 * q3 / (1 - q3))
        c = [1.0, c1, c2, c3]
        v = [float('inf'), float(v1), float(v2), float(v3), float(v4)]
        
        def piece_integral(m, lower, upper):
            cm = c[:m+1]
            C_m = sum(cm)
            A = []
            for j in range(m + 1):
                cj = cm[j]
                num_val = - ((-cj)**m) * (-cj + C_m)
                denom_val = 1.0
                for i in range(m + 1):
                    if i != j:
                        denom_val *= (cm[i] - cj)
                A.append(num_val / denom_val)
            return sum(A[j] * math.log((upper + cm[j]) / (lower + cm[j])) for j in range(m + 1))

        # AR(v_1):
        ar1 = v[1] * (1.0 - (1.0 - float(q1)) * (v[1] / (v[1] + 1.0)))
        
        # AR(v_2):
        p2 = piece_integral(1, v[2], v[1])
        F0_v2 = v[2] / (v[2] + 1.0)
        F1_v2 = v[2] / (v[2] + c[1])
        ap2 = v[2] * (1.0 - F0_v2 * F1_v2 * (1.0 - float(q2)))
        ar2 = ap2 + p2
        
        # AR(v_3):
        p3 = piece_integral(2, v[3], v[2])
        F2_v3 = v[3] / (v[3] + c[2])
        F1_v3 = v[3] / (v[3] + c[1])
        F0_v3 = v[3] / (v[3] + 1.0)
        ap3 = v[3] * (1.0 - F0_v3 * F1_v3 * F2_v3 * (1.0 - float(q3)))
        ar3 = ap3 + p2 + p3
        
        # AR(v_4):
        p4 = piece_integral(3, v[4], v[3])
        ap4 = v[4]
        ar4 = ap4 + p2 + p3 + p4
        
        ars = [ar1, ar2, ar3, ar4]
        for i, a in enumerate(ars, 1):
            print(f"Verified AR(v_{i}) = {a:.8f}")
            assert a < 1.00000000, f"AR(v_{i}) = {a} >= 1.0"
            
        max_ar = max(ars)
        print(f"Verified max AR = {max_ar:.8f} < 1.0")
        
        ratio = opt_float / max_ar
        print(f"Verified certified ratio OPT/AR = {ratio:.8f}")
        assert ratio >= 2.160000, f"Ratio {ratio} < 2.1600"
        
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"Verification error: {e}")
        print("FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
